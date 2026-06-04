"""
K리그 공식 API 응답 → DB 포맷 파싱
이벤트 / 라인업 / 경기 정보
"""

# ─────────────────────────────────────────
# K리그 공식 API 파서
# ─────────────────────────────────────────

_KL_EVENT_MAP = {
    "골": "GOAL",
    "자책골": "GOAL",
    "경고": "CARD",
    "퇴장": "CARD",
    "경고퇴장": "CARD",
    "교체": "SUBST",
    "파울": "FOUL",
    "유효슈팅": "SHOT",
    "슈팅": "SHOT",
    "오프사이드": "OFFSIDE",
    "코너킥": "CORNER",
}

_KL_CARD_KR = {
    "경고": "경고",
    "퇴장": "퇴장",
    "경고퇴장": "경고누적 퇴장",
}

_KL_GOAL_KR = {
    "골": "일반골",
    "자책골": "자살골",
}

_KL_STAT_FIELDS = {
    "goal": "Goals",
    "assist": "Assists",
    "playMinute": "Minutes",
    "yellowCard": "Yellow Cards",
    "redCard": "Red Cards",
    "shot": "Shots",
    "shotOnTarget": "Shots on Target",
    "foul": "Fouls",
    "foulSuffered": "Fouls Suffered",
    "intercept": "Interceptions",
    "tackle": "Tackles",
    "clearance": "Clearances",
    "offside": "Offsides",
    "dribble": "Dribbles",
    "dribbleSuccess": "Dribbles Successful",
    "pass": "Passes",
    "passAcc": "Passes Accurate",
    "airChalgWon": "Aerial Duels Won",
    "touchAtt": "Touches in Attack",
    "touchDef": "Touches in Defense",
    "lostBall": "Lost Balls",
    "ballRecoverie": "Ball Recoveries",
    "expectedGoal": "Expected Goals",
    "keyPass": "Key Passes",
}


def parse_kl_events(events_data: dict, fixture_id: int) -> list[dict]:
    """K리그 API matchInfo.do → events 테이블 포맷"""
    rows = []
    for half in ("firstHalf", "secondHalf"):
        for ev in events_data.get(half, []):
            ename = ev.get("eventName", "")
            etype = _KL_EVENT_MAP.get(ename)
            if not etype:
                continue

            team = ev.get("teamName", "")
            p1 = ev.get("playerName", "")
            p2 = ev.get("playerName2", "")
            minute = ev.get("num", 0)

            if etype == "GOAL":
                detail_kr = _KL_GOAL_KR.get(ename, "일반골")
                assist = p2
            elif etype == "CARD":
                detail_kr = _KL_CARD_KR.get(ename, ename)
                assist = ""
            elif etype == "SUBST":
                detail_kr = "교체"
                assist = p2
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


def parse_kl_lineups(records: dict, fixture_id: int,
                     home_name: str, away_name: str) -> tuple[list, list]:
    """K리그 API getMatchRecordAllDetail.do → (lineups, player_stats)"""
    lineups, pstats = [], []
    mapping = {"listH": home_name, "listA": away_name}

    for key, team_name in mapping.items():
        for p in records.get(key, []):
            pname = p.get("playerName", "")
            pos = p.get("playerPos", "")
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

            for field, value in p.items():
                if value is not None and field not in [
                    "playerName", "playerPos", "backNo", "teamName", "teamId",
                    "playerId", "playerPosCode", "nationality", "age",
                    "backno", "uniformNo", "playerImg", "startYn", "remark",
                    "gubun", "meetYear", "meetSeq", "gameId", "no"
                ]:
                    stat_key = _KL_STAT_FIELDS.get(field, field)
                    pstats.append({
                        "fixture_id": fixture_id,
                        "team_name": team_name,
                        "player_name": pname,
                        "stat_key": stat_key,
                        "value": str(value),
                    })

    return lineups, pstats
