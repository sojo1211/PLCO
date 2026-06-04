# K리그 공식 API만 사용
# (365Scores, API-Football 제외)
CURRENT_YEAR = 2026

POLL_INTERVAL_SECONDS = 15

# 모든 요청에 공통으로 붙는 파라미터
_365_PARAMS = {
    "appTypeId": "5",
    "langId": "1",
    "timezoneName": "Asia/Seoul",
    "userCountryId": "116",
    "sportId": "1",
}

# ===== K리그 데이터 수집 규칙 (자동 적용) =====

# 데이터 소스
DATA_SOURCE = "KLEAGUE_OFFICIAL_ONLY"  # K리그 공식 API만 사용

# 수집 필터
COLLECTION_RULES = {
    "collect_ended_games_only": True,      # 완료된 경기만 수집
    "skip_scheduled_games": True,          # 미진행 경기 건너뛰기
    "skip_live_games": True,               # 진행 중 경기 건너뛰기
    "use_kleague_all_fields": True,        # K리그 모든 필드 저장
}

# 저장 규칙
STORAGE_RULES = {
    "store_all_player_stats": True,        # 선수 모든 통계 저장
    "store_event_details": True,           # 경기 이벤트 상세 저장
    "store_lineups": True,                 # 라인업 저장
}
