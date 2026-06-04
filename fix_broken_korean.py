
# MatchDetail.jsx 깨진 한글(?) 일괄 수정 스크립트
file_path = "match_intelligence/frontend/src/components/MatchDetail.jsx"

with open(file_path, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# --- 수정 매핑 (깨진 텍스트 → 올바른 한글) ---
fixes = [
    # 주석 및 UI 텍스트
    ("// YouTube ?동 검??\n    setVideoLoading(true)", "// YouTube 자동 검색\n    setVideoLoading(true)"),
    ("// ?인??로드", "// 라인업 로드"),
    ("// ?라미터 로드", "// 파라미터 로드"),
    ("// AI 중계 ???택 ???동 ?성", "// AI 중계 탭 선택 시 자동 생성"),
    ("중계 ?성 ?패", "중계 생성 실패"),
    ("alert('?효??YouTube URL ?는 ?상 ID??력?주?요')", "alert('유효한 YouTube URL 또는 영상 ID를 입력해주세요')"),
    # 버튼 텍스트
    ("??경기 목록", "← 경기 목록"),
    ("YouTube 검???", "YouTube 검색 →"),
    ("경기 ?상 검???...", "경기 영상 검색 중..."),
    ("YouTube URL ?는 ?상 ID 붙여?기...", "YouTube URL 또는 영상 ID 붙여넣기..."),
    (">?생<", ">재생<"),
    # 패널 제목 주석
    ("{/* ?상 + 분석 분할 ?이?웃 */}", "{/* 영상 + 분석 분할 레이아웃 */}"),
    ("{/* ?쪽: ?상 ?널 */}", "{/* 왼쪽: 영상 패널 */}"),
    ("{/* ?른? 분석 ?널 */}", "{/* 오른쪽: 분석 패널 */}"),
    ("? 경기 ?상", "▶ 경기 영상"),
    # 스코어보드 주석
    ("{/* ?? ?점 목록 */}", "{/* 홈팀 득점 목록 */}"),
    ("{/* ?? */}", "{/* 팀명 */}"),
    ("{/* ?코??*/}", "{/* 스코어 */}"),
    ("{/* ?정? */}", "{/* 원정팀 */}"),
    ("{/* ?정? ?점 목록 */}", "{/* 원정팀 득점 목록 */}"),
    # 방송바 텍스트
    ("? LIVE", "🔴 LIVE"),
    ("지?경기 ?- ?시?중계", "지금 경기 중 - 실시간 중계"),
    ("??경기 종료", "✅ 경기 종료"),
    # 경기 시작/종료 카드
    # line 410
    ('><span style={{fontSize: \'18px\'}}>?</span>', '><span style={{fontSize: \'18px\'}}>🏃</span>'),
    ('><span style={{fontSize: \'16px\'}}>?</span>', '><span style={{fontSize: \'16px\'}}>🏃</span>'),
    ("0' - 경기 ?작! Parc des Princes 경기?에???판???슬??께 ?오?됩?다!", "0' - 경기 시작! Parc des Princes 경기장에서 심판의 휘슬과 함께 킥오프됩니다!"),
    ("0' - 경기 ?작! Parc des Princes 경기?에???오???슬???립?다!", "0' - 경기 시작! Parc des Princes 경기장에서 킥오프 휘슬이 울립니다!"),
    # 경기 결과 텍스트 (대 표기)
    ("${match.away_score} ? ${match.home_score}로 승리", "${match.away_score} 대 ${match.home_score}로 승리"),
    ("${match.home_score} ? ${match.away_score}로 승리", "${match.home_score} 대 ${match.away_score}로 승리"),
    # 타임라인 섹션 주석
    ("{/* ?반??*/}", "{/* 전반전 */}"),
    ("{/* ?반??추??간 */}", "{/* 전·후반 추가시간 */}"),
    ("{/* ??라??*/}", "{/* 타임라인 */}"),
    # 타임라인 헤더 섹션 텍스트
    ("<span>⏱️ 전반전</span>", "<span>⏱️ 전반전</span>"),  # already ok, skip
    ("?️ ?반??추??간", "⏱️ 전반 추가시간"),
    # 경기 시작 블록 주석
    ("{/* 경기 ?작 ?오??*/}", "{/* 경기 시작 킥오프 */}"),
    ("{/* 경기 ?작 ?오??중앙 카드 */}", "{/* 경기 시작 킥오프 중앙 카드 */}"),
    ("{/* 중앙 ?로??*/}", "{/* 중앙 세로선 */}"),
    ("{/* ?시?중계 링크 - ?이브일 ?만 ?시 */}", "{/* 실시간 중계 링크 - 라이브일 때만 표시 */}"),
    ("{/* 경기 종료 ?태 ?시 */}", "{/* 경기 종료 상태 표시 */}"),
    # 라인업 주석
    ("{/* ?수 ?이???음 */}", "{/* 선수 데이터가 없음 */}"),
    # 파라미터 탭 내 배지 텍스트 (라인 883, 886)
    ("?울: {p.fouls", "파울: {p.fouls"),
    ("?팅: {p.shots", "슈팅: {p.shots"),
    # YOLO 검증 섹션 주석
    ("{/* YOLO 검???*/}", "{/* YOLO 검증 탭 */}"),
    # 레드카드 체크
    ("e.detail_kr?.includes('?드') || e.detail_kr?.includes('퇴장')", "e.detail_kr?.includes('레드') || e.detail_kr?.includes('퇴장')"),
    ("e.detail_kr?.includes('?드')", "e.detail_kr?.includes('레드')"),
    # SubList 레드카드 체크
    ("c.detail_kr?.includes('?드')", "c.detail_kr?.includes('레드')"),
    # 검색 결과 패널 주석
    ("{/* 검??결과 ?네??목록 */}", "{/* 검색 결과 썸네일 목록 */}"),
    # 후반전 레이블 (이미 ⏱️ 전반전으로 잘못 표기됨 → 후반전으로)
    # 라인 436은 ⏱️ 전반전으로 되어있어 후반전이어야 함 — 이건 별도 처리
]

for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        print(f"✅ 수정: {old[:50]!r}")
    else:
        print(f"⚠️  미발견: {old[:50]!r}")

# 후반전 레이블 특수 처리: "(46분 ~ 90분)" 직전 "⏱️ 전반전" → "⏱️ 후반전"
content = content.replace(
    "<span>⏱️ 전반전</span>\n                          <span style={{fontSize: '12px', color: '#64748b', fontWeight: 'normal'}}>(46분 ~ 90분)</span>",
    "<span>⏱️ 후반전</span>\n                          <span style={{fontSize: '12px', color: '#64748b', fontWeight: 'normal'}}>(46분 ~ 90분)</span>"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("\n✅ MatchDetail.jsx 깨진 한글 수정 완료!")
