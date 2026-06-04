"""
K리그 공식 API 통합 수집 스크립트
- K리그 공식 API만 사용
- 완료 경기 이벤트/라인업/선수통계 수집
- Ctrl+C 중단 후 재실행 시 이어서 수집

데이터 범위:
  - K리그 API는 모든 연도(1983~) 데이터 제공 가능
  - 현재: 최근 2020~2026년만 수집 (분석 효율성을 위해)
  - 필요시 --year 옵션으로 특정 연도만 수집 가능

사용법:
  python collect_all.py          # K1+K2 전체 (2020~2026)
  python collect_all.py --k1     # K League 1만
  python collect_all.py --k2     # K League 2만
  python collect_all.py --year 2024  # 특정 연도만
"""
import os, sys, sqlite3, time, json, argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)
os.chdir(_DIR)

# 로그: 파일 + stdout 동시 출력
_logfile = open(os.path.join(_DIR, "collect.log"), "w", encoding="utf-8", buffering=1)

def log(msg: str):
    _logfile.write(msg + "\n")
    _logfile.flush()
    try:
        print(msg, flush=True)
    except Exception:
        print(msg.encode("ascii", errors="replace").decode(), flush=True)


import storage
import kleague_client as kl

storage.init_db()

_KL_EVENT_MAP = {
    "골": "GOAL", "자책골": "GOAL",
    "경고": "CARD", "퇴장": "CARD", "경고퇴장": "CARD",
    "교체": "SUBST",
    "파울": "FOUL",
    "유효슈팅": "SHOT", "슈팅": "SHOT",
    "오프사이드": "OFFSIDE",
    "코너킥": "CORNER",
}
_KL_CARD_KR = {"경고": "경고", "퇴장": "퇴장", "경고퇴장": "경고누적 퇴장"}
_KL_GOAL_KR = {"골": "일반골", "자책골": "자살골"}

KL_DONE_FILE = os.path.join(_DIR, "kl_done.json")


def _kl_done_load() -> set:
    if os.path.exists(KL_DONE_FILE):
        with open(KL_DONE_FILE, encoding="utf-8") as f:
            return set(json.load(f).get("done", []))
    return set()


def _kl_done_save(done: set):
    with open(KL_DONE_FILE, "w", encoding="utf-8") as f:
        json.dump({"done": list(done)}, f)


def _parse_kl_events(events_data: dict, fixture_id: int) -> list[dict]:
    """matchInfo.do 응답 → events 테이블 포맷"""
    rows = []
    for half in ("firstHalf", "secondHalf"):
        for ev in events_data.get(half, []):
            ename = ev.get("eventName", "")
            etype = _KL_EVENT_MAP.get(ename)
            if not etype:
                continue  # 전반시작/후반시작 등 메타 이벤트 스킵
            team = ev.get("teamName", "")
            p1   = ev.get("playerName", "")
            p2   = ev.get("playerName2", "")
            minute = ev.get("num", 0)

            if etype == "GOAL":
                detail_kr = _KL_GOAL_KR.get(ename, "일반골")
                assist = p2
            elif etype == "CARD":
                detail_kr = _KL_CARD_KR.get(ename, ename)
                assist = ""
            elif etype == "SUBST":
                detail_kr = "교체"
                assist = p2   # 교체 아웃=p1, 인=p2
            else:
                detail_kr = ename
                assist = p2

            rows.append({
                "fixture_id": fixture_id,
                "minute": minute,
                "extra_time": None,
                "event_type": etype,
                "detail_kr": detail_kr,
                "team_name": team,
                "player_name": p1,
                "assist_name": assist,
                "raw_type": ename,
            })
    return rows


def _calc_match_parameters(fixture_id: int, evs: list, h_name: str, a_name: str) -> list:
    """경기 이벤트로부터 파라미터 계산"""
    params = []

    for team_name in [h_name, a_name]:
        team_evs = [e for e in evs if e["team_name"] == team_name]
        opp_evs = [e for e in evs if e["team_name"] != team_name]

        fouls = len([e for e in team_evs if e["event_type"] == "FOUL"])
        opp_fouls = len([e for e in opp_evs if e["event_type"] == "FOUL"])
        shots = len([e for e in team_evs if e["event_type"] == "SHOT"])
        corners = len([e for e in team_evs if e["event_type"] == "CORNER"])
        offsides = len([e for e in team_evs if e["event_type"] == "OFFSIDE"])

        press_intensity = min(100, (fouls / max(1, fouls + opp_fouls)) * 100) if (fouls + opp_fouls) > 0 else 50
        defensive_line = 50 + (offsides / max(1, shots + corners + offsides) * 30) if (shots + corners + offsides) > 0 else 50
        setpiece_focus = (corners / max(1, len(team_evs))) * 100 if len(team_evs) > 0 else 0
        offside_trap = min(100, (offsides / max(1, opp_fouls + offsides)) * 100) if (opp_fouls + offsides) > 0 else 0

        params.append({
            "fixture_id": fixture_id,
            "team_name": team_name,
            "possession": 50.0,
            "fouls": fouls,
            "shots": shots,
            "corners": corners,
            "press_intensity": round(press_intensity, 1),
            "defensive_line": round(defensive_line, 1),
            "setpiece_focus": round(setpiece_focus, 1),
            "offside_trap": round(offside_trap, 1),
        })

    return params


def _parse_kl_lineups(records: dict, fixture_id: int,
                      home_name: str, away_name: str) -> tuple[list, list]:
    """getMatchRecordAllDetail.do → (lineups, player_stats)"""
    lineups, pstats = [], []
    mapping = {"listH": home_name, "listA": away_name}

    for key, team_name in mapping.items():
        for p in records.get(key, []):
            pname = p.get("playerName", "")
            pos   = p.get("playerPos", "")
            backno = p.get("backNo", p.get("backno", p.get("uniformNo")))
            status = "Starting" if p.get("startYn") == "Y" else "Substitute"

            lineups.append({
                "fixture_id": fixture_id,
                "team_name": team_name,
                "formation": "",
                "player_name": pname,
                "jersey_number": backno,
                "status": status,
                "position": pos,
                "position_detail": "",
            })

            # 선수별 모든 통계 (K리그 공식 API의 모든 필드)
            stat_fields = {
                "goal": "Goals", "assist": "Assists", "playMinute": "Minutes",
                "yellowCard": "Yellow Cards", "redCard": "Red Cards", "shot": "Shots",
                "shotOnTarget": "Shots on Target", "foul": "Fouls", "foulSuffered": "Fouls Suffered",
                "intercept": "Interceptions", "tackle": "Tackles", "clearance": "Clearances",
                "offside": "Offsides", "dribble": "Dribbles", "dribbleSuccess": "Dribbles Successful",
                "pass": "Passes", "passAcc": "Passes Accurate", "airChalgWon": "Aerial Duels Won",
                "touchAtt": "Touches in Attack", "touchDef": "Touches in Defense",
                "lostBall": "Lost Balls", "ballRecoverie": "Ball Recoveries",
                "expectedGoal": "Expected Goals", "keyPass": "Key Passes",
            }

            # K리그 API의 모든 필드를 동적으로 저장 (stat_fields에 없는 것도)
            for field, value in p.items():
                if value is not None and field not in ["playerName", "playerPos", "backNo",
                                                        "teamName", "teamId", "playerId", "playerPosCode",
                                                        "nationality", "age", "backno", "uniformNo",
                                                        "playerImg", "startYn", "remark", "gubun",
                                                        "meetYear", "meetSeq", "gameId", "no"]:
                    stat_key = stat_fields.get(field, field)
                    pstats.append({
                        "fixture_id": fixture_id,
                        "team_name": team_name,
                        "player_name": pname,
                        "stat_key": stat_key,
                        "value": str(value),
                    })
    return lineups, pstats


def collect_kleague_official(year: int, meet_seq: int):
    """K리그 공식 홈페이지로 연도/리그 전체 경기 수집"""
    league_name = f"K리그{'1' if meet_seq == 1 else '2'} {year}"
    log(f"\n=== K리그 공식 {league_name} 수집 ===")

    done = _kl_done_load()

    # 1단계: 라운드 목록
    log("  라운드 목록 조회 중...")
    rounds = kl.get_round_list(year, meet_seq)
    log(f"  총 {len(rounds)}라운드")

    # 2단계: 라운드별 경기 목록
    all_games = []
    for rnd in rounds:
        games = kl.get_round_games(year, meet_seq, rnd)
        all_games.extend(games)

    # 점수가 있는 경기만 (0-0 제외)
    ended = [g for g in all_games if (g.get("homeGoal") or 0) > 0 or (g.get("awayGoal") or 0) > 0]
    log(f"  전체 경기: {len(all_games)} / 점수 있는 경기: {len(ended)}")

    # fixtures_full 저장 (점수 있는 경기만)
    for g in ended:
        storage.upsert_fixture_full({
            "fixture_id": g["fixture_id"],
            "league_id":  g["league_id"],
            "season":     year,
            "date":       g.get("gameDate", "").replace("/", "-"),
            "status":     "Ended" if g.get("homeGoal") is not None else "Scheduled",
            "elapsed":    90,
            "home_team":  g.get("homeTeamName", ""),
            "home_logo":  "",
            "away_team":  g.get("awayTeamName", ""),
            "away_logo":  "",
            "home_score": g.get("homeGoal") or 0,
            "away_score": g.get("awayGoal") or 0,
        })

    # 3단계: 경기별 상세 수집 (병렬 처리)
    todo = [g for g in ended if g["fixture_id"] not in done]
    log(f"  신규 수집: {len(todo)}경기 (기완료: {len(done & {g['fixture_id'] for g in ended})})")

    def collect_match(g):
        fid      = g["fixture_id"]
        gid      = g["gameId"]
        home     = g.get("homeTeam", "")
        away     = g.get("awayTeam", "")
        h_name   = g.get("homeTeamName", "")
        a_name   = g.get("awayTeamName", "")
        rnd      = g.get("roundId", 0)
        hs, as_  = g.get("homeGoal", 0), g.get("awayGoal", 0)

        try:
            ev_data = kl.get_match_events(year, meet_seq, gid, home, away, rnd)
            evs = _parse_kl_events(ev_data, fid)
            for ev in evs:
                storage.insert_event(ev)

            rec_data = kl.get_match_player_records(year, meet_seq, gid, home, away, rnd)
            lus, pss = _parse_kl_lineups(rec_data, fid, h_name, a_name)
            for m in lus:
                storage.upsert_lineup(m)
            for ps in pss:
                storage.upsert_player_stat(ps)

            return (True, fid, h_name, hs, a_name, as_, len(evs), len(lus))
        except Exception as e:
            return (False, fid, str(e))

    success = 0
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(collect_match, g): (i+1, g) for i, g in enumerate(todo)}

        for future in as_completed(futures):
            i, g = futures[future]
            try:
                result = future.result()
                if result[0]:
                    _, fid, h_name, hs, a_name, as_, ev_cnt, lu_cnt = result
                    done.add(fid)
                    success += 1
                    log(f"  [{i}/{len(todo)}] {g.get('gameDate')}  {h_name} {hs}-{as_} {a_name}  ev={ev_cnt} lu={lu_cnt}")

                    if success % 10 == 0:
                        _kl_done_save(done)
                else:
                    _, fid, err = result
                    log(f"  [{i}/{len(todo)}] fixture_id={fid} ERR: {err}")
            except Exception as e:
                log(f"  [{i}/{len(todo)}] ERR: {e}")

    _kl_done_save(done)

    conn = sqlite3.connect("match_intelligence.db")
    ev  = conn.execute("SELECT COUNT(DISTINCT fixture_id) FROM events").fetchone()[0]
    lu  = conn.execute("SELECT COUNT(DISTINCT fixture_id) FROM lineups").fetchone()[0]
    conn.close()
    log(f"  완료: {success}경기  DB: events={ev} lineups={lu}")


# ─── 메인 ──────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--k1",       action="store_true", help="K리그1만 수집")
    p.add_argument("--k2",       action="store_true", help="K리그2만 수집")
    p.add_argument("--year",     type=int, default=None, help="연도 (기본: 2025~2026)")
    args = p.parse_args()

    years = [args.year] if args.year else list(range(2025, 2027))

    for yr in years:
        if not args.k2:
            collect_kleague_official(yr, 1)  # K리그1
        if not args.k1:
            collect_kleague_official(yr, 2)  # K리그2


if __name__ == "__main__":
    main()
