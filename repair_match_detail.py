import re

file_path = "match_intelligence/frontend/src/components/MatchDetail.jsx"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# 1. Commented out GK position
old_gk = "// GK ?치 - ?? 골? ??  positions.push({ x: side === 'home' ? 3 : 97, y: 50, isGK: true })"
new_gk = "  positions.push({ x: side === 'home' ? 3 : 97, y: 50, isGK: true })"
content = content.replace(old_gk, new_gk)

# Let's also check if it is already commented out in a different encoding style:
content = re.sub(
    r"//\s*GK\s*\?치\s*-\s*\?\?\s*골\?\s*\?\?\s*positions\.push\(\{ x: side === 'home' \? 3 : 97, y: 50, isGK: true \}\)",
    "  positions.push({ x: side === 'home' ? 3 : 97, y: 50, isGK: true })",
    content
)

# 2. X multiplier to prevent team overlap
content = content.replace(
    "xPct = 10 + (lineIdx / (numLines - 1 || 1)) * 38",
    "xPct = 10 + (lineIdx / (numLines - 1 || 1)) * 35"
)
content = content.replace(
    "xPct = 90 - (lineIdx / (numLines - 1 || 1)) * 38",
    "xPct = 90 - (lineIdx / (numLines - 1 || 1)) * 35"
)

# 3. Case-insensitive team filtering in FormationPitch
content = content.replace(
    "homeLineup={lineups.filter(l => l.team_name === match.home_team)}",
    "homeLineup={lineups.filter(l => l.team_name?.trim().toLowerCase() === match.home_team?.trim().toLowerCase())}"
)
content = content.replace(
    "awayLineup={lineups.filter(l => l.team_name === match.away_team)}",
    "awayLineup={lineups.filter(l => l.team_name?.trim().toLowerCase() === match.away_team?.trim().toLowerCase())}"
)

# 4. Stat filtering
content = content.replace(
    "const homeStats = stats.filter(s => s.team_name === match.home_team)",
    "const homeStats = stats.filter(s => s.team_name?.trim().toLowerCase() === match.home_team?.trim().toLowerCase())"
)
content = content.replace(
    "const awayStats = stats.filter(s => s.team_name === match.away_team)",
    "const awayStats = stats.filter(s => s.team_name?.trim().toLowerCase() === match.away_team?.trim().toLowerCase())"
)

# 5. Goal events filtering
content = content.replace(
    "const homeGoals = events.filter(e => e.event_type === 'GOAL' && e.team_name === match.home_team && !e.detail_kr?.includes('자살골'))",
    "const homeGoals = events.filter(e => e.event_type === 'GOAL' && e.team_name?.trim().toLowerCase() === match.home_team?.trim().toLowerCase() && !e.detail_kr?.includes('자살골'))"
)
content = content.replace(
    "const awayGoals = events.filter(e => e.event_type === 'GOAL' && e.team_name === match.away_team && !e.detail_kr?.includes('자살골'))",
    "const awayGoals = events.filter(e => e.event_type === 'GOAL' && e.team_name?.trim().toLowerCase() === match.away_team?.trim().toLowerCase() && !e.detail_kr?.includes('자살골'))"
)

# 6. Early text corruptions
content = content.replace("// ?라미터 로드", "// 전술 파라미터 로드")
content = content.replace("중계 ?성 ?패", "중계 생성 실패")
content = content.replace("{/* ?정? */}", "{/* 원정팀 */}")
content = content.replace("{/* ?정? ?점 목록 */}", "{/* 원정팀 득점 목록 */}")
content = content.replace("{/* ?상 + 분석 분할 ?이?웃 */}", "{/* 영상 및 분석 분할 레이아웃 */}")
content = content.replace("{/* ?쪽: ?상 ?널 */}", "{/* 왼쪽: 영상 패널 */}")
content = content.replace('className="video-panel-title">? 경기 ?상', 'className="video-panel-title">🎬 경기 영상')
content = content.replace('placeholder="YouTube URL ?는 ?상 ID 붙여?기..."', 'placeholder="YouTube URL 또는 영상 ID 붙여넣기..."')
content = content.replace('className="video-load-btn" onClick={loadVideo}>?생', 'className="video-load-btn" onClick={loadVideo}>재생')
content = content.replace("{/* ?른? 분석 ?널 */}", "{/* 오른쪽 분석 패널 */}")
content = content.replace("{/* ?시?중계 링크 - ?이브일 ?만 ?시 */}", "{/* 실시간 중계 링크 - 라이브일 때만 표시 */}")
content = content.replace('className="live-badge">? LIVE', 'className="live-badge">🔴 LIVE')
content = content.replace('className="live-text">지?경기 ?- ?시?중계', 'className="live-text">진행 중인 경기 - 실시간 중계')
content = content.replace("{/* 경기 종료 ?태 ?시 */}", "{/* 경기 종료 상태 표시 */}")
content = content.replace('??경기 목록', '◀ 경기 목록')

# Emojis in events
content = content.replace("e.detail_kr?.includes('?드') || e.detail_kr?.includes('?장')", "e.detail_kr?.includes('레드') || e.detail_kr?.includes('퇴장')")
content = content.replace("emoji = isRed ? '?' : '?';", "emoji = isRed ? '🟥' : '🟨';")
content = content.replace("emoji = '?';\ncolor = '#3b82f6';", "emoji = '🎯';\ncolor = '#3b82f6';")
content = content.replace("emoji = '?';\ncolor = '#8b5cf6';", "emoji = '🚩';\ncolor = '#8b5cf6';")
content = content.replace("emoji = '?';\ncolor = '#10b981';", "emoji = '🔄';\ncolor = '#10b981';")

# 7. Timeline text corruptions
content = content.replace("<span style={{fontSize: '18px'}}>?</span>\n<span style={{fontSize: '13px'}}>0' - 경기 ?작!", "<span style={{fontSize: '18px'}}>🏃</span>\n<span style={{fontSize: '13px'}}>0' - 경기 시작!")
content = content.replace("Parc des Princes 경기?에???판???슬??께 ?오?됩?다!", "Parc des Princes 경기장에서 심판의 휘슬과 함께 킥오프됩니다!")
content = content.replace("<span>?️ </span>\n<span style={{fontSize: '12px', color: '#64748b', fontWeight: 'normal'}}>(1?~ 45?", "<span>⏱️ 전반전</span>\n<span style={{fontSize: '12px', color: '#64748b', fontWeight: 'normal'}}>(1분 ~ 45분")
content = content.replace("?점 ??별???벤?? ?었?니??", "이 기간에는 특별한 이벤트가 없었습니다.")
content = content.replace("⏱️ ?반??추??간", "⏱️ 전반전 추가시간")
content = content.replace("<span>?️ </span>\n<span style={{fontSize: '12px', color: '#64748b', fontWeight: 'normal'}}>(46?~ 90?", "<span>⏱️ 후반전</span>\n<span style={{fontSize: '12px', color: '#64748b', fontWeight: 'normal'}}>(46분 ~ 90분")
content = content.replace("⏱️ ?반??추??간", "⏱️ 후반전 추가시간")
content = content.replace("<span style={{fontSize: '20px'}}>?</span>\n<span>90' - 경기 ?? 최종 ?코??", "<span style={{fontSize: '20px'}}>🏁</span>\n<span>90' - 경기 종료! 최종 스코어 ")
content = content.replace("? `AS 모나?AS_Monaco)가 ?리 ?제르맹(PSG)?????${match.away_score} ? ${match.home_score}??리?거두?경기가 종료?었?니??`", "? `AS 모나코(AS_Monaco)가 파리 생제르맹(PSG)을 상대로 ${match.away_score} 대 ${match.home_score}로 승리를 거두며 경기가 종료되었습니다.`")
content = content.replace("? `?리 ?제르맹(PSG)??AS 모나?AS_Monaco)????${match.home_score} ? ${match.away_score}??리?거두?경기가 종료?었?니??`", "? `파리 생제르맹(PSG)이 AS 모나코(AS_Monaco)를 상대로 ${match.home_score} 대 ${match.away_score}로 승리를 거두며 경기가 종료되었습니다.`")
content = content.replace(": `??? 치열???전 ?에 ${match.home_score} ? ${match.away_score} 무승부?경기가 종료?었?니??`}", ": `양 팀 치열한 접전 끝에 ${match.home_score} 대 ${match.away_score} 무승부로 경기가 종료되었습니다.`}")
content = content.replace("<p>경기 ?벤?? ?습?다</p>", "<p>경기 이벤트가 없습니다.</p>")
content = content.replace("{/* 중앙 ?로??*/}", "{/* 중앙 세로선 */}")
content = content.replace("{/* 경기 ?작 ?오??중앙 카드 */}", "{/* 경기 시작 킥오프 중앙 카드 */}")
content = content.replace("<span style={{fontSize: '16px'}}>?</span>\n<span>0' - 경기 ?작! Parc des Princes 경기?에???오???슬???립?다!</span>", "<span style={{fontSize: '16px'}}>🏃</span>\n<span>0' - 경기 시작! Parc des Princes 경기장에서 킥오프 휘슬이 울립니다!</span>")
content = content.replace("// ??(PSG)? ?쪽(isLeft = true), ?정?(Monaco)? ?른?isLeft = false)", "// 홈(PSG)은 왼쪽(isLeft = true), 원정(Monaco)은 오른쪽(isLeft = false)")
content = content.replace("{/* ?쪽 콘텐?공간 (??) */}", "{/* 홈팀 콘텐츠 공간 (왼쪽) */}")
content = content.replace("{/* 중앙 ?건 ?간/?이?배? */}", "{/* 중앙 사건 시간/아이콘 배치 */}")
content = content.replace("{/* ?른?콘텐?공간 (?정?) */}", "{/* 원정팀 콘텐츠 공간 (오른쪽) */}")
content = content.replace("{/* 경기 종료 ?최종 결과 중앙 카드 */}", "{/* 경기 종료 최종 결과 중앙 카드 */}")
content = content.replace("<span style={{fontSize: '18px'}}>?</span>\n<span>90' - 경기 종료! 최종 ?코??", "<span style={{fontSize: '18px'}}>🏁</span>\n<span>90' - 경기 종료! 최종 스코어 ")
content = content.replace("{/* ?벤??*/}", "{/* 이벤트 카드 */}")
content = content.replace('e.events.length === 0 && <div className="state-msg">?벤???이???음</div>', 'events.length === 0 && <div className="state-msg">이벤트 데이터가 없음</div>')
content = content.replace("?시?트:", "도움:")
content = content.replace("{/* ?수 ?인??- K리그 공식 ????*/}", "{/* 선수 라인업 - K리그 공식 스타일 */}")
content = content.replace('<div className="state-msg">?수 ?이???음</div>', '<div className="state-msg">선수 데이터가 없음</div>')
content = content.replace("?발 {starting.length}", "선발 {starting.length}")
content = content.replace('<div className="lineup-section-label">?발 </div>', '<div className="lineup-section-label">선발</div>')
content = content.replace('교체 ?수 ({subs.length}?', '교체 선수 ({subs.length}명)')

# Vertical Timeline cards styling
content = content.replace("e.detail_kr?.includes('?드')", "e.detail_kr?.includes('레드')")
content = content.replace("icon = isRed ? '?' : '?';", "icon = isRed ? '🟥' : '🟨';")
content = content.replace("icon = '?';\n} else if (e.event_type === 'CORNER') {", "icon = '🎯';\n} else if (e.event_type === 'CORNER') {")
content = content.replace("icon = '?';\n} else if (e.event_type === 'SUBST') {", "icon = '🚩';\n} else if (e.event_type === 'SUBST') {")
content = content.replace("icon = '?';\n}", "icon = '🔄';\n}")

# 8. Stats / Parameters corruptions
content = content.replace("{/* ?계 */}", "{/* 팀 통계 */}")
content = content.replace("{/* ?라미터 */}", "{/* 전술 파라미터 */}")
content = content.replace("?울: {p.fouls || 0}", "파울: {p.fouls || 0}")
content = content.replace("?팅: {p.shots || 0}", "슈팅: {p.shots || 0}")
content = content.replace("진행 ?", "진행 중")
content = content.replace("?메?션 & ?술 분석", "포메이션 & 전술 분석")
content = content.replace("K리그 ?이??기반 ?동 분류", "AI 전술 분석 및 포메이션 매핑")
content = content.replace("// ?비 ?인 (tier 1)", "// 수비 라인 (tier 1)")
content = content.replace("// 중앙 미드?더 (tier 3)", "// 중앙 미드필더 (tier 3)")
content = content.replace("// ?트?이?(tier 5)", "// 스트라이커 (tier 5)")

# 9. Lineups legends
content = content.replace("{/* ?치 + 교체 */}", "{/* 피치 + 교체목록 */}")
content = content.replace("{/* ?치 마킹 */}", "{/* 피치 마킹 */}")
content = content.replace("{/* 범? */}", "{/* 범례 */}")
content = content.replace("???점", "⚽ 득점")
content = content.replace("?장", "퇴장")
content = content.replace('<span className="fp-ev subout" style={{fontSize:10}}>??교체?웃</span>', '<span className="fp-ev subout" style={{fontSize:10, marginRight: 4}}>🔄</span> 교체 아웃')
content = content.replace('<span className="fp-ev subin" style={{fontSize:10}}></span>', '')

# actual substitutes DB data
content = content.replace("미드?더", "미드필더")
content = content.replace("?레?메?커", "플레이메이커")
content = content.replace("?비??MF", "수비형 MF")
content = content.replace("공격??MF", "공격형 MF")
content = content.replace("?프?백", "레프트백")
content = content.replace("공격???어", "공격형 윙어")

# YOLO tactical reports
content = content.replace("areaText: '+14.2% ?장',", "areaText: '+14.2% 확장',")
content = content.replace("counterIndexText: 'Monaco 89% (매우 ?험)',", "counterIndexText: 'Monaco 89% (매우 위험)',")
content = content.replace("areaText: '+9.8% ?장 (공격 집중)',", "areaText: '+9.8% 확장 (공격 집중)',")
content = content.replace("counterIndexText: 'Monaco 95% (최고 ?험)',", "counterIndexText: 'Monaco 95% (최고 위험)',")
content = content.replace("areaText: '+11.5% ?장',", "areaText: '+11.5% 확장',")
content = content.replace("counterIndexText: 'Monaco 78% (?험)',", "counterIndexText: 'Monaco 78% (위험)',")
content = content.replace("areaText: '+15.2% ?장',", "areaText: '+15.2% 확장',")
content = content.replace("counterIndexText: 'Monaco 92% (매우 ?험)',", "counterIndexText: 'Monaco 92% (매우 위험)',")
content = content.replace("areaText: '+7.5% ?장 (?백 보호 ?화)',", "areaText: '+7.5% 확장 (포백 보호 강화)',")
content = content.replace("areaText: '+2.1% (?비 ?정 ?환)',", "areaText: '+2.1% (수비 안정 전환)',")
content = content.replace("counterIndexText: 'PSG 48% (?정)',", "counterIndexText: 'PSG 48% (안정)',")
content = content.replace("counterIndexText: 'PSG 67% (?험)',", "counterIndexText: 'PSG 67% (위험)',")
content = content.replace("areaText: '-8.2% (좌측 공격 ?기)',", "areaText: '-8.2% (좌측 공격 대기)',")

content = content.replace("{/* 교체 ?택 ?롭?운 */}", "{/* 교체 선택 드롭다운 */}")
content = content.replace("교체 ?택 (?제 경기 교체 목록)", "교체 선택 (실제 경기 교체 목록)")
content = content.replace("교체 ?행", "교체 진행")
content = content.replace("?웃:", "아웃:")
content = content.replace("?입:", "투입:")
content = content.replace("4? ?심 ?술 분석 결과", "4대 핵심 전술 분석 결과")
content = content.replace("? 분석 결과:", "💡 분석 결과:")
content = content.replace("PSG ?협 ?비율:", "PSG 위협 대비율:")
content = content.replace("Monaco ?도:", "Monaco 역습 속도:")
content = content.replace("{/* 과제 3. ?트?스 불안 구역 & ?련 ?릴 추천 */}", "{/* 과제 3. 세트피스 불안 구역 & 훈련 드릴 추천 */}")
content = content.replace("?트?스 취약 구역 & ?련 추천", "세트피스 취약 구역 & 훈련 추천")
content = content.replace("{/* 골? 박스 ?역 취약 구역 ?시 */}", "{/* 골대 박스 영역 취약 구역 표시 */}")
content = content.replace("?험 Zone", "위험 Zone")
content = content.replace("추천 ?련 ?릴", "추천 훈련 드릴")

content = content.replace("??PSG (?리 공격 기?)", "우리 관점 (PSG 공격 시)")
content = content.replace("??Monaco (?? 공격 기?)", "상대 관점 (Monaco 공격 시)")
content = content.replace("{/* ?각??그래???역 */}", "{/* 전술 일치도 분석 영역 */}")
content = content.replace("?치", "일치")
content = content.replace("{/* ?? ?시?HUD ?분석 ?로?스 ??지 ?션 추? ?? */}", "{/* 실시간 전술 HUD 분석 프로세스 이미지 섹션 */}")
content = content.replace("YOLOv11 분석 ?시?HUD ??이??보정 ?로?스", "YOLOv11 분석 실시간 HUD 및 원근 보정 프로세스")
content = content.replace("{/* 1. HUD ??트???지 그리??*/}", "{/* 1. HUD 및 히트맵 이미지 그리드 */}")
content = content.replace("{/* ?시??술 HUD 카드 */}", "{/* 실시간 전술 HUD 카드 */}")
content = content.replace("?시?객체 ?래??HUD ??보??", "실시간 객체 트래킹 HUD 및 전술 시각화")
content = content.replace("YOLOv11 모델???레?당 22명의 ?수 ?치, ?판, 그리?볼의 바운??박스????고 ?용 HUD 가?드 ?인(?비??깊이 ??박 반경)??캔버???버?이?출력??모습?니??", "YOLOv11 모델로 프레임당 22명의 선수 위치, 심판, 그리고 축구공의 바운딩 박스를 검출하고, 전용 HUD 가이드 라인(수비선 깊이 및 압박 반경)을 캔버스 오버레이로 출력한 결과입니다.")
content = content.replace("{/* 2D ?영 ?트?카드 */}", "{/* 2D 투영 히트맵 카드 */}")
content = content.replace("?모그래???면 ?영 ?트?", "호모그래피 평면 투영 히트맵")
content = content.replace("카메???? ?의 ?근??차??모그래???렬(Homography Matrix) 보정???해 2차원 ?뷰(Top-down) ?치 좌표계로 ?사 ?영?여 ???한 밀???트?분석 ?료?니??", "카메라 뷰의 원근 왜곡을 호모그래피 행렬(Homography Matrix) 보정을 통해 2차원 탑다운(Top-down) 피치 좌표계로 투사 투영하여 시각화한 밀도 히트맵 분석 자료입니다.")
content = content.replace("{/* 2. 3?계 ?이??보정 ?제 ?로?스 갤러?*/}", "{/* 2. 3단계 데이터 정제 프로세스 갤러리 */}")
content = content.replace("?️ 3?계 ?이??보정 ?좌표 ?제 ?로?스 (Data Refinement Pipeline)", "🛠️ 3단계 데이터 보정 실좌표 정제 프로세스 (Data Refinement Pipeline)")
content = content.replace("{/* 1?계 */}", "{/* 1단계 */}")
content = content.replace("비디???의 ?곡??카메???크??? 좌표?x, y)???천 ?집???것???태?니?? ????이즈? 많습?다.", "비디오 프레임 내 왜곡된 카메라 스크린상의 2D 좌표(x, y)를 원천 수집한 상태로, 원근 왜곡 and 노이즈가 많습니다.")
content = content.replace("{/* 2?계 */}", "{/* 2단계 */}")
content = content.replace("?모그래???영 보정", "호모그래피 평면 투영 보정")
content = content.replace("?근 변???렬(Homography) ??산???해 ?선 구도??????2D 105m×68m 공식 축구??좌표 ?면?로 캘리브레?션???계?니??", "원근 변환 행렬(Homography Matrix) 역산 연산을 통해 경기장 라인 구도를 감지하고, 실제 105m × 68m 공식 축구장 좌표 평면으로 캘리브레이션을 진행한 단계입니다.")
content = content.replace("{/* 3?계 */}", "{/* 3단계 */}")
content = content.replace("?이??터?& ?제", "이동 평균 필터링 & 노이즈 정제")
content = content.replace("?동 ?균 ?터(Moving Average)? ?상??거 ?고리즘??추? ?용???비?인 ?차? ?탐지?차단??최종 ?술 분석 ?이?셋?니??", "이동 평균 필터(Moving Average)와 이상치 제거 알고리즘을 추가 적용하여, 수비 라인 오차나 튀는 노이즈 좌표를 탐지/차단한 최종 정밀 전술 분석 데이터셋입니다.")

# 10. Commentary generator text repairs
content = content.replace("if (detail_kr?.includes('?살')) {", "if (detail_kr?.includes('자살')) {")
content = content.replace("??!! ?게 무슨 ?인가?? ${team_name}??${player_name} ?수??뼈아???살골이 기록?고 맙니?? 경기??분위기? 급격?게 ?어붙습?다.", "앗!! 이게 무슨 일인가요! {team_name}의 {player_name} 선수의 뼈아픈 자살골이 기록되고 맙니다. 경기장 분위기가 급격하게 얼어붙습니다.")
content = content.replace("?!!! 골망???듭?다! ?어갔습?다! ${team_name}??${player_name}! ?상?인 ?결정?을 보여주네??${assist_name ? ` ?카로운 ????찔러준 ${assist_name} ?수???시?트??명품?었?니??` : ''}", "골!!! 골망을 흔듭니다! 들어갔습니다! {team_name}의 {player_name}! 환상적인 결정력을 보여주네요!{assist_name ? ` 날카로운 패스를 찔러준 ${assist_name} 선수의 어시스트도 명품이었습니다!` : ''}")
content = content.replace("const isRed = detail_kr?.includes('퇴장') || detail_kr?.includes('?드')", "const isRed = detail_kr?.includes('퇴장') || detail_kr?.includes('레드')")
content = content.replace("?드카드 발동!!!! ?판??지??이 퇴장??명령?니?? ${team_name}??${player_name} ?수가 퇴장?하면서 경기???도가 ?동치기 ?작?니??", "레드카드 발동!!!! 심판이 지체 없이 퇴장을 명령합니다. {team_name}의 {player_name} 선수가 퇴장하면서 경기 구도가 요동치기 시작합니다!")
content = content.replace("경고 ?적??주의?야 ?니?? 주심??${team_name}??${player_name} ?수?게 ?로?카?? 부?합?다. 거친 ?클?었?요.", "경고 누적을 주의해야 합니다! 주심이 {team_name}의 {player_name} 선수에게 옐로카드를 부여합니다. 거친 태클이었습니다.")
content = content.replace("감독???술??중???변?? 줍니?? ${team_name}?서 ${detail_kr}??진행?니?? 그라?드???로???력??공급?니??", "감독이 전술에 중대한 변화를 줍니다! {team_name}에서 {detail_kr}를 진행합니다. 그라운드에 새로운 활력을 공급합니다.")
content = content.replace("교체 ?웃/?? ${team_name}??${player_name} ?수가 ?웃?고, ${assist_name} ?수가 그라?드??어 ?어갑니??", "교체 아웃/인! {team_name}의 {player_name} 선수가 아웃되고, {assist_name} 선수가 그라운드로 뛰어 들어갑니다.")
content = content.replace("교체 카드 ?입! ${team_name}??가) ?수 교체(${player_name || '?수'})??행?며 ?로???름??꾀?니??", "교체 카드 투입! {team_name}팀이 선수 교체({player_name || '선수'})를 단행하며 새로운 흐름을 꾀합니다.")
content = content.replace("과감?게 ?려봅니?? ${team_name}??${player_name}! ?주 ?카로운 ?팅?었?나 골키???면 ?? ?슬?슬?게 골문??비껴갑니??", "과감하게 때려봅니다! {team_name}의 {player_name}! 아주 날카로운 슈팅이었으나 골키퍼 정면 혹은 아슬아슬하게 골문을 비껴갑니다.")
content = content.replace("코너???트?스 기회?맞이?니?? ${team_name}! 공중?경합 ?황?서 ??퇴장??가??수?이 ?방?로 ???동?니??", "코너킥 세트피스 기회를 맞이합니다, {team_name}! 공중볼 경합 상황에서 어떤 선수가 득점 기회를 만들어낼 수 있을지 기대됩니다.")
content = content.replace("박진?일치??경기 진행 중 ${team_name} - ${detail_kr || event_type}", "박진감 넘치는 경기 진행 중: {team_name} - {detail_kr || event_type}")

# Miscellaneous fixes
content = content.replace("YOLO ? ???ε", "YOLO 검사 비교 데이터 로드")
content = content.replace("{/* K  ????????*/}", "{/* K리그 방송 스타일 스코어보드 */}")
content = content.replace("<p>???ã? </p>", "<p>영상을 찾을 수 없습니다.</p>")
content = content.replace("? YouTube?서 직접 검??", "🔍 YouTube에서 직접 검색")
content = content.replace("{/* AI ߰ - Gemini ? ????߰ */}", "{/* AI 중계 - Gemini 기반 실시간 편파 중계 */}")
content = content.replace('<span className="ended-badge">??경기 종료</span>', '<span className="ended-badge">🏁 경기 종료</span>')
content = content.replace("경기 ?작부??종료까? ?시?중계?드", "경기 시작부터 종료까지 실시간 중계 피드")
content = content.replace("??AI ?시?경기 ?설 ?드", "🎙️ AI 실시간 경기 해설 피드")
content = content.replace("{events.filter(e => ['GOAL', 'CARD', 'SHOT', 'CORNER', 'SUBST'].includes(e.event_type)).length}??벤??", "{events.filter(e => ['GOAL', 'CARD', 'SHOT', 'CORNER', 'SUBST'].includes(e.event_type)).length}개 이벤트")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Second repair completed successfully!")
