"""
K리그 공식 홈페이지 (www.kleague.com) API 클라이언트

데이터:
  - 전체 시즌 경기 목록 (라운드별)
  - 경기 이벤트 (골/카드/교체/파울/슈팅)
  - 선수 기록 (라인업, 통계)

ID 규칙: fixture_id = year * 1_000_000 + meetSeq * 10_000 + gameId
  2025 K1 game 5  → 2025_1_0005 = 20251_0005
  2025 K2 game 12 → 2025_2_0012 = 20252_0012

리그 코드:
  KLEAGUE1 = 1 (meetSeq=1)
  KLEAGUE2 = 2 (meetSeq=2)
"""
import time
import requests

BASE     = "https://www.kleague.com"
DDF      = f"{BASE}/api/ddf/match"
DELAY    = 0.8

# DB league_id 매핑 (fixtures_full 테이블용)
LEAGUE_ID_K1 = 10001
LEAGUE_ID_K2 = 10002

_session = requests.Session()
_session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
})


def _init_session(year: int, meet_seq: int, game_id: int):
    """match.do 페이지 로드로 JSESSIONID + Referer 설정"""
    url = f"{BASE}/match.do"
    _session.get(url, params={
        "year": year, "leagueId": meet_seq,
        "gameId": game_id, "meetSeq": meet_seq,
    }, headers={"Accept": "text/html"}, timeout=15)
    _session.headers["Referer"] = (
        f"{BASE}/match.do?year={year}&leagueId={meet_seq}"
        f"&gameId={game_id}&meetSeq={meet_seq}"
    )


def _post(endpoint: str, params: dict) -> dict:
    time.sleep(DELAY)
    r = _session.post(f"{DDF}/{endpoint}", data=params, timeout=15)
    r.raise_for_status()
    return r.json()


def make_fixture_id(year: int, meet_seq: int, game_id: int) -> int:
    return year * 1_000_000 + meet_seq * 10_000 + game_id


def get_round_list(year: int, meet_seq: int, sample_game_id: int = 1) -> list[int]:
    """시즌 전체 라운드 번호 목록 반환"""
    _init_session(year, meet_seq, sample_game_id)
    d = _post("getRoundList.do", {
        "year": str(year), "meetSeq": str(meet_seq), "gameId": str(sample_game_id),
    })
    return d.get("data", {}).get("roundList", [])


def get_round_games(year: int, meet_seq: int, round_id: int,
                    sample_game_id: int = 1) -> list[dict]:
    """특정 라운드 경기 목록 반환"""
    d = _post("getRoundGameList.do", {
        "year": str(year), "meetSeq": str(meet_seq),
        "gameId": str(sample_game_id), "roundId": str(round_id),
    })
    games = d.get("data", {}).get("roundGameList", [])
    for g in games:
        g["year"] = year
        g["meetSeq"] = meet_seq
        g["fixture_id"] = make_fixture_id(year, meet_seq, g["gameId"])
        g["league_id"] = LEAGUE_ID_K1 if meet_seq == 1 else LEAGUE_ID_K2
    return games


def get_match_events(year: int, meet_seq: int, game_id: int,
                     home_team: str, away_team: str, round_id: int) -> dict:
    """경기 이벤트 반환 (골/카드/교체/파울/슈팅 등)"""
    params = {
        "year": str(year), "yearTst": str(year),
        "meetSeq": str(meet_seq),
        "gameId": str(game_id), "gameIdTst": str(game_id),
        "homeTeam": home_team, "awayTeam": away_team,
        "roundId": str(round_id),
    }
    d = _post("matchInfo.do", params)
    return d.get("data", {})


def get_match_player_records(year: int, meet_seq: int, game_id: int,
                              home_team: str, away_team: str, round_id: int) -> dict:
    """선수 기록/라인업 반환"""
    params = {
        "year": str(year), "yearTst": str(year),
        "meetSeq": str(meet_seq),
        "gameId": str(game_id), "gameIdTst": str(game_id),
        "homeTeam": home_team, "awayTeam": away_team,
        "roundId": str(round_id),
    }
    d = _post("getMatchRecordAllDetail.do", params)
    return d.get("data", {})
