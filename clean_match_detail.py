file_path = "match_intelligence/frontend/src/components/MatchDetail.jsx"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

def find_matching_brace(text, start_pos):
    brace_start = text.find("{", start_pos)
    if brace_start == -1:
        return -1
    count = 1
    for idx in range(brace_start + 1, len(text)):
        if text[idx] == "{":
            count += 1
        elif text[idx] == "}":
            count -= 1
            if count == 0:
                if idx + 1 < len(text) and text[idx+1] == ";":
                    return idx + 2
                return idx + 1
    return -1

# 1. EVENT_ICON
old_event_icon = """const EVENT_ICON = {
  GOAL: '??, CARD: '?', SUBST: '?', VAR: '?',
}"""
new_event_icon = """const EVENT_ICON = {
  GOAL: '⚽', CARD: '🟨', SUBST: '🔄', VAR: '🖥️',
}"""
content = content.replace(old_event_icon, new_event_icon)
if "const EVENT_ICON = {" in content and "GOAL: '" in content and "VAR:" in content:
    start_event = content.find("const EVENT_ICON = {")
    end_event = content.find("}", start_event) + 1
    content = content[:start_event] + new_event_icon + content[end_event:]

# 2. getEventDescription function
old_get_event_desc_start = "function getEventDescription(event) {"
end_get_event_desc_marker = "function getYoutubeId(url) {"
start_idx = content.find(old_get_event_desc_start)
end_idx = content.find(end_get_event_desc_marker)
new_get_event_desc = """function getEventDescription(event) {
  const { event_type, detail_kr, player_name, team_name, assist_name } = event

  switch(event_type) {
    case 'GOAL':
      if (detail_kr?.includes('자살')) {
        return `앗!! 이게 무슨 일인가요! ${team_name}의 ${player_name} 선수의 뼈아픈 자살골이 기록되고 맙니다. 경기장 분위기가 급격하게 얼어붙습니다.`;
      }
      return `골!!! 골망을 흔듭니다! 들어갔습니다! ${team_name}의 ${player_name}! 환상적인 결정력을 보여주네요!${assist_name ? ` 날카로운 패스를 찔러준 ${assist_name} 선수의 어시스트도 명품이었습니다!` : ''}`;

    case 'CARD':
      const isRed = detail_kr?.includes('퇴장') || detail_kr?.includes('레드')
      if (isRed) {
        return `레드카드 발동!!!! 심판이 지체 없이 퇴장을 명령합니다. ${team_name}의 ${player_name} 선수가 퇴장하면서 경기 구도가 요동치기 시작합니다!`;
      }
      return `경고 누적을 주의해야 합니다! 주심이 ${team_name}의 ${player_name} 선수에게 옐로카드를 부여합니다. 거친 태클이었습니다.`;

    case 'SUBST':
      if (detail_kr && detail_kr.includes('OUT') && detail_kr.includes('IN')) {
        return `감독이 전술에 중대한 변화를 줍니다! ${team_name}에서 ${detail_kr}를 진행합니다. 그라운드에 새로운 활력을 공급합니다.`;
      }
      if (player_name && assist_name) {
        return `교체 아웃/인! ${team_name}의 ${player_name} 선수가 아웃되고, ${assist_name} 선수가 그라운드로 뛰어 들어갑니다.`;
      }
      return `교체 카드 투입! ${team_name}팀이 선수 교체(${player_name || '선수'})를 단행하며 새로운 흐름을 꾀합니다.`;

    case 'SHOT':
      return `과감하게 때려봅니다! ${team_name}의 ${player_name}! 아주 날카로운 슈팅이었으나 골키퍼 정면 혹은 아슬아슬하게 골문을 비껴갑니다.`;

    case 'CORNER':
      return `코너킥 세트피스 기회를 맞이합니다, ${team_name}! 공중볼 경합 상황에서 어떤 선수가 득점 기회를 만들어낼 수 있을지 기대됩니다.`;

    default:
      return `박진감 넘치는 경기 진행 중: ${team_name} - ${detail_kr || event_type}`;
  }
}

"""
if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_get_event_desc + content[end_idx:]

# 3. Text/Badge fixes in timeline & layouts
content = content.replace("// YOLO 검?비교 ?이??로드", "// YOLO 검사 비교 데이터 로드")
content = content.replace("{/* K리그 방송 ?????코?보??*/}", "{/* K리그 방송 스타일 스코어보드 */}")
content = content.replace("<p>?상??찾? </p>", "<p>영상을 찾을 수 없습니다.</p>")
content = content.replace("{/* AI 중계 - Gemini ?성 ?연?러??중계 */}", "{/* AI 중계 - Gemini 기반 실시간 편파 중계 */}")
content = content.replace("경기 ?작부??종료까? ?시?중계?드", "경기 시작부터 종료까지 실시간 중계 피드")
content = content.replace("??AI ?시?경기 ?설 ?드", "🎙️ AI 실시간 경기 해설 피드")
content = content.replace("events.filter(e => ['GOAL', 'CARD', 'SHOT', 'CORNER', 'SUBST'].includes(e.event_type)).length}??벤??", "events.filter(e => ['GOAL', 'CARD', 'SHOT', 'CORNER', 'SUBST'].includes(e.event_type)).length}개 이벤트")
content = content.replace("<div style={{fontSize: '48px', marginBottom: '12px'}}>??/div>", "<div style={{fontSize: '48px', marginBottom: '12px'}}>📅</div>")
content = content.replace("<p>경기 ?벤?? ?습?다</p>", "<p>경기 이벤트가 없습니다</p>")

# 4. Video Placeholder fixes
content = content.replace('<div className="video-placeholder-icon">??/div>', '<div className="video-placeholder-icon">📺</div>')
content = content.replace('<p>?상??찾? 못했?니??/p>', '<p>영상을 찾을 수 없습니다.</p>')
btn_start = content.find('<button className="yt-search-btn large" onClick={searchYoutube}>')
if btn_start != -1:
    btn_end = content.find('</button>', btn_start) + 9
    old_btn_block = content[btn_start:btn_end]
    new_btn_block = """<button className="yt-search-btn large" onClick={searchYoutube}>
                🔍 YouTube에서 직접 검색
              </button>"""
    content = content.replace(old_btn_block, new_btn_block)

# 5. Timeline Cards
content = content.replace("<span>?️ ?반??/span>", "<span>⏱️ 전반전</span>")
content = content.replace("<span style={{fontSize: '12px', color: '#64748b', fontWeight: 'normal'}}>(1?~ 45?", "<span style={{fontSize: '12px', color: '#64748b', fontWeight: 'normal'}}>(1분 ~ 45분)")
content = content.replace("?점 ??별???벤?? ?었?니??", "이 기간에는 특별한 이벤트가 없었습니다.")
content = content.replace("⏱️ ?반??추??간", "⏱️ 전반전 추가시간")
content = content.replace("<span>?️ ?반??/span>", "<span>⏱️ 후반전</span>")
content = content.replace("<span style={{fontSize: '12px', color: '#64748b', fontWeight: 'normal'}}>(46?~ 90?", "<span style={{fontSize: '12px', color: '#64748b', fontWeight: 'normal'}}>(46분 ~ 90분)")
content = content.replace("⏱️ ?반??추??간", "⏱️ 후반전 추가시간")
content = content.replace("<span style={{fontSize: '20px'}}>?</span>", "<span style={{fontSize: '20px'}}>🏁</span>")
content = content.replace("90' - 경기 ?? 최종 ?코??", "90' - 경기 종료! 최종 스코어 ")
content = content.replace("AS 모나?AS_Monaco)가 ?리 ?제르맹(PSG)?????", "AS 모나코(AS_Monaco)가 파리 생제르맹(PSG)을 상대로 ")
content = content.replace("??리?거두?경기가 종료?었?니??", "로 승리를 거두며 경기가 종료되었습니다.")
content = content.replace("?리 ?제르맹(PSG)??AS 모나?AS_Monaco)????", "파리 생제르맹(PSG)이 AS 모나코(AS_Monaco)를 상대로 ")
content = content.replace("??? 치열???전 ?에 ${match.home_score} ? ${match.away_score} 무승부?경기가 종료?었?니??", "양 팀 치열한 접전 끝에 ${match.home_score} 대 ${match.away_score} 무승부로 경기가 종료되었습니다.")
content = content.replace("<span style={{fontSize: '16px'}}>?</span>\n<span>0' - 경기 ?작! Parc des Princes 경기?에???오???슬???립?다!</span>", "<span style={{fontSize: '16px'}}>🏃</span>\n<span>0' - 경기 시작! Parc des Princes 경기장에서 킥오프 휘슬이 울립니다!</span>")
content = content.replace("<span style={{fontSize: '16px'}}>?</span>\n      <span>0' - 경기 ?작! Parc des Princes 경기?에???오???슬???립?다!</span>", "<span style={{fontSize: '16px'}}>🏃</span>\n      <span>0' - 경기 시작! Parc des Princes 경기장에서 킥오프 휘슬이 울립니다!</span>")
content = content.replace("// ??(PSG)? ?쪽(isLeft = true), ?정?(Monaco)? ?른?isLeft = false)", "// 홈(PSG)은 왼쪽(isLeft = true), 원정(Monaco)은 오른쪽(isLeft = false)")
content = content.replace("{/* ?쪽 콘텐?공간 (??) */}", "{/* 홈팀 콘텐츠 공간 (왼쪽) */}")
content = content.replace("{/* 중앙 ?건 ?간/?이?배? */}", "{/* 중앙 사건 시간/아이콘 배치 */}")
content = content.replace("{/* ?른?콘텐?공간 (?정?) */}", "{/* 원정팀 콘텐츠 공간 (오른쪽) */}")
content = content.replace("{/* 경기 종료 ?최종 결과 중앙 카드 */}", "{/* 경기 종료 최종 결과 중앙 카드 */}")
content = content.replace("<span style={{fontSize: '18px'}}>?</span>\n<span>90' - 경기 종료! 최종 ?코??", "<span style={{fontSize: '18px'}}>🏁</span>\n<span>90' - 경기 종료! 최종 스코어 ")
content = content.replace("<span style={{fontSize: '18px'}}>?</span>\n  <span>90' - 경기 종료! 최종 ?코??", "<span style={{fontSize: '18px'}}>🏁</span>\n  <span>90' - 경기 종료! 최종 스코어 ")
content = content.replace("?벤???이???음", "이벤트 데이터가 없음")
content = content.replace("?시?트:", "도움:")
content = content.replace("{/* ?수 ?인??- K리그 공식 ????*/}", "{/* 선수 라인업 - K리그 공식 스타일 */}")
content = content.replace("?수 ?이???음", "선수 데이터가 없음")
content = content.replace("?발 {starting.length}?", "선발 {starting.length}명")
content = content.replace("?발 ?인??", "선발 라인업")
content = content.replace("교체 ?수 ({subs.length}?", "교체 선수 ({subs.length}명)")

# 6. Team stats tab
content = content.replace("{/* ?계 */}", "{/* 팀 통계 */}")
content = content.replace("<span>??</span>", "<span>항목</span>")

# 7. Parameters tab
content = content.replace("{/* ?라미터 */}", "{/* 전술 파라미터 */}")
content = content.replace("?박 강도:", "압박 강도:")
content = content.replace("?비 ?인:", "수비 라인:")
content = content.replace("?트?스:", "세트피스:")
content = content.replace("?프?이??", "오프사이드:")
content = content.replace("?라미터 ?이???음", "파라미터 데이터가 없음")

# 8. Yolo validation tab
content = content.replace("? YOLO 추적 vs 1??이???파?코?? 일치??검?", "🖥️ YOLO 추적 vs 1차 데이터(소파스코어) 일치도 검증")
content = content.replace("YOLO 비디??분석 ?이?라?에??추출???술 ?보? 공식 1??계 ?이??SofaScore)??공식 ?이?? 매칭?여 ?확?? 검증합?다.", "YOLO 비디오 분석 파이프라인에서 추출한 전술 정보와 공식 1차계 데이터(SofaScore)의 공식 데이터를 매칭하여 정확도를 검증합니다.")
content = content.replace("'? ?유??(%)'", "'공 점유율(%)'")
content = content.replace("'?스 ?공?(%)'", "'패스 성공률(%)'")
content = content.replace("일치?? {accuracy.toFixed(1)}%", "일치도 {accuracy.toFixed(1)}%")
content = content.replace("{/* 진행 중*/}", "{/* 진행 중 */}")
content = content.replace("{/* ?? ?이??비교 */}", "{/* 데이터 비교 */}")
content = content.replace("공식 1??이??", "공식 1차 데이터: ")
content = content.replace("YOLO 추출 ?이??", "YOLO 추출 데이터: ")
content = content.replace("검??이?? 존재?? ?습?다.", "검증 데이터가 존재하지 않습니다.")

# 9. Formations & Tactic Analysis section
content = content.replace("{/* ?? ?메?션 & ?술 ?션 ?? */}", "{/* 하단 포메이션 & 전술 섹션 배치 */}")
content = content.replace("?메?션 & ?술 분석", "포메이션 & 전술 분석")
content = content.replace("K리그 ?이??기반 ?동 분류", "AI 전술 분석 및 포메이션 매핑")
content = content.replace("getPositionTier(posDetail, posCode) {", "getPositionTier(posDetail, posCode) {")
content = content.replace("// ?비 ?인 (tier 1)", "// 수비 라인 (tier 1)")
content = content.replace("?비??미드필더 / ?백 (tier 2)", "수비형 미드필더 / 윙백 (tier 2)")
content = content.replace("공격??미드필더 / ?어 (tier 4)", "공격형 미드필더 / 윙어 (tier 4)")
content = content.replace("좌우(Left/Right) ?렬??", "좌우(Left/Right) 정렬 순서")
content = content.replace("일치 ?로??서 결정", "피치 가로 배치 결정")
content = content.replace("?메?션 ?인??요 ?원: [4, 2, 3, 1] ??  // ?인 ?덱??0=?비, 1=DM, 2=AM, 마??ST", "포메이션 라인별 소요 인원: [4, 2, 3, 1] 등  // 라인 인덱스는 0=수비, 1=DM, 2=AM, 마지막=ST")
content = content.replace("?수?을 tier 기??로 ?렬", "선수들을 tier 기준으로 정렬")
content = content.replace("?인???수 배정 (tier ?서??채워?기)", "라인별로 선수 배정 (tier 순으로 채워넣기)")
content = content.replace("Left ??Center ??Right ?서??정??", "Left -> Center -> Right 순서로 정렬")
content = content.replace("// ??38%??: ?????기 반코??50%)?만 머물?록 ?한", "  // 가로 35%: 선수들이 자기 반코트(50%) 안에서만 머물도록 제한")
content = content.replace("// ?? GK(3%) ??DEF(10%) ??... ??FW(48%)", "  // 홈팀: GK(3%) -> DEF(10%) -> ... -> FW(45%)")
content = content.replace("// ?웨?? GK(97%) ??DEF(90%) ??... ??FW(52%)", "  // 원정팀: GK(97%) -> DEF(90%) -> ... -> FW(55%)")

# 10. getHorizLayout coordinate spacing and Goalkeeper activation
content = content.replace("// GK ?치 - ?? 골? ??  positions.push({ x: side === 'home' ? 3 : 97, y: 50, isGK: true })", "  positions.push({ x: side === 'home' ? 3 : 97, y: 50, isGK: true })")
content = content.replace("xPct = 10 + (lineIdx / (numLines - 1 || 1)) * 38", "xPct = 10 + (lineIdx / (numLines - 1 || 1)) * 35")
content = content.replace("xPct = 90 - (lineIdx / (numLines - 1 || 1)) * 38", "xPct = 90 - (lineIdx / (numLines - 1 || 1)) * 35")

# 11. YoloTacticalReport heading
content = content.replace("YOLO ? ???ε", "YOLO 검사 비교 데이터 로드")
content = content.replace("??PSG (?리 공격 기?)", "우리 관점 (PSG 공격 시)")
content = content.replace("??Monaco (?? 공격 기?)", "상대 관점 (Monaco 공격 시)")
content = content.replace("{/* ?각??그래???역 */}", "{/* 전술 일치도 분석 영역 */}")
content = content.replace("?치", "일치")
content = content.replace("{/* ?? ?시?HUD ?분석 ?로?스 ??지 ?션 추? ?? */}", "{/* 실시간 전술 HUD 분석 프로세스 이미지 섹션 */}")
content = content.replace("YOLOv11 분석 ?시?HUD ??이??보정 ?로?스", "YOLOv11 분석 실시간 HUD 및 원근 보정 프로세스")
content = content.replace("{/* 1. HUD ??트???지 그리??*/}", "{/* 1. HUD 및 히트맵 이미지 그리드 */} ")
content = content.replace("{/* ?시??술 HUD 카드 */}", "{/* 실시간 전술 HUD 카드 */} ")
content = content.replace("?시?객체 ?래??HUD ??보??", "실시간 객체 트래킹 HUD 및 전술 시각화")
content = content.replace("YOLOv11 모델???레?당 22명의 ?수 ?치, ?판, 그리?볼의 바운??박스????고 ?용 HUD 가?드 ?인(?비??깊이 ??박 반경)??캔버???버?이?출력??모습?니??", "YOLOv11 모델로 프레임당 22명의 선수 위치, 심판, 그리고 축구공의 바운딩 박스를 검출하고, 전용 HUD 가이드 라인(수비선 깊이 및 압박 반경)을 캔버스 오버레이로 출력한 결과입니다.")
content = content.replace("{/* 2D ?영 ?트?카드 */}", "{/* 2D 투영 히트맵 카드 */} ")
content = content.replace("?모그래???면 ?영 ?트?", "호모그래피 평면 투영 히트맵")
content = content.replace("카메???? ?의 ?근??차??모그래???렬(Homography Matrix) 보정???해 2차원 ?뷰(Top-down) ?치 좌표계로 ?사 ?영?여 ???한 밀???트?분석 ?료?니??", "카메라 뷰의 원근 왜곡을 호모그래피 행렬(Homography Matrix) 보정을 통해 2차원 탑다운(Top-down) 피치 좌표계로 투사 투영하여 시각화한 밀도 히트맵 분석 자료입니다.")
content = content.replace("{/* 2. 3?계 ?이??보정 ?제 ?로?스 갤러?*/}", "{/* 2. 3단계 데이터 정제 프로세스 갤러리 */} ")
content = content.replace("?️ 3?계 ?이??보정 ?좌표 ?제 ?로?스 (Data Refinement Pipeline)", "🛠️ 3단계 데이터 보정 실좌표 정제 프로세스 (Data Refinement Pipeline)")
content = content.replace("{/* 1?계 */}", "{/* 1단계 */} ")
content = content.replace("비디???의 ?곡??카메???크??? 좌표?x, y)???천 ?집???것???태?니?? ????이즈? 많습?다.", "비디오 프레임 내 왜곡된 카메라 스크린상의 2D 좌표(x, y)를 원천 수집한 상태로, 원근 왜곡 and 노이즈가 많습니다.")
content = content.replace("{/* 2?계 */}", "{/* 2단계 */} ")
content = content.replace("?모그래???영 보정", "호모그래피 평면 투영 보정")
content = content.replace("?근 변???렬(Homography) ??산???해 ?선 구도??????2D 105m×68m 공식 축구??좌표 ?면?로 캘리브레?션???계?니??", "원근 변환 행렬(Homography Matrix) 역산 연산을 통해 경기장 라인 구도를 감지하고, 실제 105m × 68m 공식 축구장 좌표 평면으로 캘리브레이션을 진행한 단계입니다.")
content = content.replace("{/* 3?계 */}", "{/* 3단계 */} ")
content = content.replace("?이??터?& ?제", "이동 평균 필터링 & 노이즈 정제")
content = content.replace("?동 ?균 ?터(Moving Average)? ?상??거 ?고리즘??추? ?용???비?인 ?차? ?탐지?차단??최종 ?술 분석 ?이?셋?니??", "이동 평균 필터(Moving Average)와 이상치 제거 알고리즘을 적용하여, 수비 라인 오차나 튀는 노이즈 좌표를 탐지/차단한 최종 정밀 전술 분석 데이터셋입니다.")
content = content.replace("{/* 교체 ?택 ?롭?운 */}", "{/* 교체 선택 드롭다운 */} ")
content = content.replace("교체 ?택 (?제 경기 교체 목록)", "교체 선택 (실제 경기 교체 목록)")
content = content.replace("교체 ?행", "교체 진행")
content = content.replace("?웃:", "아웃:")
content = content.replace("?입:", "투입:")
content = content.replace("4? ?심 ?술 분석 결과", "4대 핵심 전술 분석 결과")
content = content.replace("? 분석 결과:", "💡 분석 결과:")
content = content.replace("PSG ?협 ?비율:", "PSG 위협 대비율:")
content = content.replace("Monaco ?도:", "Monaco 역습 속도:")
content = content.replace("{/* 과제 3. ?트?스 불안 구역 & ?련 ?릴 추천 */}", "{/* 과제 3. 세트피스 불안 구역 & 훈련 드릴 추천 */} ")
content = content.replace("?트?스 취약 구역 & ?련 추천", "세트피스 취약 구역 & 훈련 추천")
content = content.replace("{/* 골? 박스 ?역 취약 구역 ?시 */}", "{/* 골대 박스 영역 취약 구역 표시 */} ")
content = content.replace("?험 Zone", "위험 Zone")
content = content.replace("추천 ?련 ?릴", "추천 훈련 드릴")

# 12. Pitch team headers and legends
content = content.replace("{/* ? ?더 */}", "{/* 팀 헤더 */} ")
content = content.replace("?치 + 교체", "피치 + 교체목록")
content = content.replace("?치 마킹", "피치 마킹")
content = content.replace("{/* 범? */}", "{/* 범례 */} ")
content = content.replace("???점", "⚽ 득점")
content = content.replace("?장", "퇴장")
content = content.replace('<span className="fp-ev subout" style={{fontSize:10}}>??교체?웃</span>', '<span className="fp-ev subout" style={{fontSize:10, marginRight: 4}}>🔄</span> 교체 아웃')
content = content.replace('<span className="fp-ev subin" style={{fontSize:10}}>??교체??/span>', '')
content = content.replace("??교체?웃", "교체 아웃")
content = content.replace("??교체??", "교체 투입")
content = content.replace("?? (??계열, ?쪽?오른쪽 공격)", "홈팀 (파란계열, 왼쪽→오른쪽 공격)")
content = content.replace("?웨?? (빨간계열, ?른쪽→?쪽 공격)", "원정팀 (빨간계열, 오른쪽→왼쪽 공격)")

# 13. Case-insensitive team filtering in FormationPitch
content = content.replace("homeLineup={lineups.filter(l => l.team_name === match.home_team)}", "homeLineup={lineups.filter(l => l.team_name?.trim().toLowerCase() === match.home_team?.trim().toLowerCase())}")
content = content.replace("awayLineup={lineups.filter(l => l.team_name === match.away_team)}", "awayLineup={lineups.filter(l => l.team_name?.trim().toLowerCase() === match.away_team?.trim().toLowerCase())}")
content = content.replace("const homeStats = stats.filter(s => s.team_name === match.home_team)", "const homeStats = stats.filter(s => s.team_name?.trim().toLowerCase() === match.home_team?.trim().toLowerCase())")
content = content.replace("const awayStats = stats.filter(s => s.team_name === match.away_team)", "const awayStats = stats.filter(s => s.team_name?.trim().toLowerCase() === match.away_team?.trim().toLowerCase())")
content = content.replace("const homeGoals = events.filter(e => e.event_type === 'GOAL' && e.team_name === match.home_team && !e.detail_kr?.includes('자살골'))", "const homeGoals = events.filter(e => e.event_type === 'GOAL' && e.team_name?.trim().toLowerCase() === match.home_team?.trim().toLowerCase() && !e.detail_kr?.includes('자살골'))")
content = content.replace("const awayGoals = events.filter(e => e.event_type === 'GOAL' && e.team_name === match.away_team && !e.detail_kr?.includes('자살골'))", "const awayGoals = events.filter(e => e.event_type === 'GOAL' && e.team_name?.trim().toLowerCase() === match.away_team?.trim().toLowerCase() && !e.detail_kr?.includes('자살골'))")

# 14. tactical type colors
content = content.replace("const tacColor = { '고압박형':'#ef4444','?유?형':'#3b82f6','카운?형':'#f59e0b','?블록??:'#8b5cf6' }", "const tacColor = { '고압박형':'#ef4444','점유형':'#3b82f6','카운터형':'#f59e0b','텐백블록형':'#8b5cf6' }")
content = content.replace("return p.press_intensity > 65 ? '고압박형' : p.defensive_line > 55 ? '?유?형' : p.press_intensity < 40 ? '?블록?? : '카운?형'", "return p.press_intensity > 65 ? '고압박형' : p.defensive_line > 55 ? '점유형' : p.press_intensity < 40 ? '텐백블록형' : '카운터형'")

# 15. Substitutes arrays
clean_psg_subs = """const PSG_SUBS = [
  { out: 'Herrera',  outFull: 'Ander Herrera',   outPos: '미드필더',      minute: 55, inKey: 'Verratti',  inFull: 'Marco Verratti',   inPos: '플레이메이커' },
  { out: 'Gueye',   outFull: 'Idrissa Gueye',    outPos: '수비형 MF',     minute: 71, inKey: 'Rafinha',   inFull: 'Rafinha',          inPos: '공격형 MF' },
  { out: 'Kurzawa', outFull: 'Layvin Kurzawa',   outPos: '레프트백',      minute: 71, inKey: 'Draxler',  inFull: 'Julian Draxler',   inPos: '공격형 윙어' },
  { out: 'Paredes', outFull: 'Leandro Paredes',  outPos: '수비형 MF',     minute: 71, inKey: 'Danilo',   inFull: 'Danilo Pereira',   inPos: '수비형 MF' },
]"""
clean_monaco_subs = """const MONACO_SUBS = [
  { out: 'BenYedder', outFull: 'Wissam Ben Yedder', outPos: '스트라이커',   minute: 71, inKey: 'Jovetic',  inFull: 'Stevan Jovetic',       inPos: '포워드' },
  { out: 'Aguilar',   outFull: 'Ruben Aguilar',     outPos: '라이트백',     minute: 80, inKey: 'Sidibe',   inFull: 'Sidibe',               inPos: '수비수' },
  { out: 'Diop',      outFull: 'Sofiane Diop',      outPos: '공격형 MF',   minute: 80, inKey: 'Golovin',  inFull: 'Aleksandr Golovin',    inPos: '미드필더' },
  { out: 'Henrique',  outFull: 'Caio Henrique',     outPos: '레프트백',     minute: 90, inKey: 'Ballo',    inFull: 'Fode Ballo-Toure',     inPos: '수비수' },
]"""

# Replace PSG_SUBS
psg_start = content.find("const PSG_SUBS = [")
psg_end = content.find("]", psg_start) + 1
if psg_start != -1 and psg_end != -1:
    content = content[:psg_start] + clean_psg_subs + content[psg_end:]

# Replace MONACO_SUBS
monaco_start = content.find("const MONACO_SUBS = [")
monaco_end = content.find("]", monaco_start) + 1
if monaco_start != -1 and monaco_end != -1:
    content = content[:monaco_start] + clean_monaco_subs + content[monaco_end:]

# 16. PitchPlayer component override
pitch_player_start = content.find("function PitchPlayer({ player, pos, color }) {")
pitch_player_end_marker = "function SubList({ players, side }) {"
pitch_player_end = content.find(pitch_player_end_marker)
new_pitch_player = """function PitchPlayer({ player, pos, color }) {
  const isGK = pos.isGK || player?.position === 'GK'
  const name = player?.player_name?.split(' ').slice(-1)[0] || '?'
  const num  = player?.jersey_number ?? '?'
  const ev   = getPlayerEv(player?.player_name)
  const isRed = ev.cards?.some(c => c.detail_kr?.includes('레드') || c.detail_kr?.includes('퇴장'))
  return (
    <div className="fp-player" style={{ left:`${pos.x}%`, top:`${pos.y}%` }}>
      <div className="fp-jersey-wrapper" style={{ position: 'relative' }}>
        <div className="fp-jersey" style={{ background: isGK ? '#ec4899' : color }}>
          {num}
        </div>
        {ev.goals?.length > 0 && (
          <span className="fp-badge goal" style={{ position: 'absolute', top: -5, right: -5, fontSize: 10 }}>⚽</span>
        )}
        {ev.cards?.length > 0 && (
          <span className="fp-badge card" style={{
            position: 'absolute',
            top: -5,
            left: -5,
            width: 7,
            height: 10,
            background: isRed ? '#ef4444' : '#f59e0b',
            borderRadius: 1,
            boxShadow: '0 1px 2px rgba(0,0,0,0.3)'
          }} />
        )}
        {(ev.subOut || ev.subIn) && (
          <span className="fp-badge sub" style={{
            position: 'absolute',
            bottom: -5,
            right: -5,
            background: ev.subOut ? '#f97316' : '#22c55e',
            color: '#fff',
            fontSize: '7.5px',
            fontWeight: 'bold',
            padding: '1px 3px',
            borderRadius: '4px',
            boxShadow: '0 1px 2px rgba(0,0,0,0.3)',
            lineHeight: 1
          }}>
            {ev.subOut ? `↓${ev.subOut.minute}'` : `↑${ev.subIn.minute}'`}
          </span>
        )}
      </div>
      <div className="fp-pname">{name}</div>
    </div>
  )
}

"""
if pitch_player_start != -1 and pitch_player_end != -1:
    content = content[:pitch_player_start] + new_pitch_player + content[pitch_player_end:]

# 17. SubList event symbols cleanup
content = content.replace("className=\"fp-ev goal\">??/span>", "className=\"fp-ev goal\">⚽</span>")
content = content.replace("className=\"fp-ev subin\">??ev.subIn.minute}'</span>", "className=\"fp-ev subin\">🔄 {ev.subIn.minute}'</span>")
content = content.replace("className=\"fp-ev subout\">??ev.subOut.minute}'</span>", "className=\"fp-ev subout\">🔄 {ev.subOut.minute}'</span>")

# 18. SIMULATION_DATA replacement
clean_simulation_data = """const SIMULATION_DATA = {
  'Herrera_Verratti': {
    areaText: '+14.2% 확장',
    areaPercent: 84,
    posComment: '베라티 투입 즉시 모나코의 하이프레스 압박 라인이 뒤로 12m 밀려났으며, PSG 중원 패스 루트가 전면적으로 복구되었습니다.',
    counterIndexText: 'Monaco 72% (보통)',
    counterPercent: 72,
    counterSpeedText: '5.5m/s',
    counterComment: '베라티의 영리한 위치 선정과 패스 차단으로 모나코의 다이렉트 롱볼 역습 개시 속도가 초당 5.5m로 떨어졌습니다.',
    setpieceHeight: 20,
    setpieceDrill: 'Zone Defense Block Drill A',
    setpieceComment: '평균 키가 줄어들었으나 영리한 대인 방어 전환으로 박스 내 공중볼 마크 성공률이 55%로 상승했습니다.',
    matchRateUs: 73,
    matchCommentUs: '베라티의 좌우 패스 전개 방향(우리 강점)과 상대 수비 약점(모나코 좌측 배후)의 교차 시너지가 73% 일치합니다.',
    matchRateThem: 62,
    matchCommentThem: '베라티 투입으로 수비 차단 지점이 증가하여 모나코의 우측 공격 루트(상대 강점)와 PSG 좌측 배후 노출(우리 약점) 매칭율을 62%로 떨어뜨렸습니다.'
  },
  'Herrera_Rafinha': {
    areaText: '+18.5% 확장 (전진 빌드업)',
    areaPercent: 92,
    posComment: '라피냐의 전진 드리블과 우측 하프스페이스 공략으로 PSG의 다이렉트 전방 공격 빌드업 면적이 극대화되었습니다.',
    counterIndexText: 'Monaco 89% (매우 위험)',
    counterPercent: 89,
    counterSpeedText: '6.8m/s',
    counterComment: '라피냐의 공격 전진 성향으로 인해 볼 소유권 상실 시 수비 복귀 속도가 지연되며 모나코의 역습 공간 배후 면적이 89% 노출됩니다.',
    setpieceHeight: 32,
    setpieceDrill: 'Defensive Transition Drill B',
    setpieceComment: '라피냐의 공중볼 경합 약점으로 인해 상대 코너킥 및 세트피스 상황에서의 실점 위험도가 High(높음)로 상승합니다.',
    matchRateUs: 89,
    matchCommentUs: '상대 우측 하프스페이스 균열 구역(상대 약점)과 라피냐의 적극적인 전진 경로(우리 강점)가 89% 매치되어 화력을 뿜어냅니다.',
    matchRateThem: 84,
    matchCommentThem: '라피냐의 높은 공격 전진선으로 인해 발생한 우측 배후(우리 약점)와 모나코의 빠른 역습 침투 전개(상대 강점)가 84% 오버랩되어 득점 위협이 발생합니다.'
  },
  'Herrera_MoiseKean': {
    areaText: '+9.8% 확장 (공격 집중)',
    areaPercent: 65,
    posComment: '미드필더를 빼고 공격수를 투입하여 박스 내 영향력을 키웠으나, 중원에서 볼을 점유하는 면적은 크게 감소했습니다.',
    counterIndexText: 'Monaco 95% (최고 위험)',
    counterPercent: 95,
    counterSpeedText: '7.4m/s',
    counterComment: '중원 밸런스가 붕괴되며 모나코의 역습 시 배후 공간이 완전히 노출되어 실점 위협도가 95%로 최고조에 달합니다.',
    setpieceHeight: 10,
    setpieceDrill: 'Man-to-Man Marker System C',
    setpieceComment: '킨의 피지컬 and 헤더 제공권 확보(제공권 78%) 덕분에 코너킥 수비 시 공중볼 처리 위험 Zone이 크게 축소됩니다.',
    matchRateUs: 54,
    matchCommentUs: '박스 안으로의 다이렉트 롱볼 매칭은 양호하지만, 하프스페이스 연계 약점을 찌르는 강점 매칭은 54%로 감소합니다.',
    matchRateThem: 91,
    matchCommentThem: '중원 숫자가 1명 줄어들면서 모나코의 다이렉트 패스 전개(상대 강점)와 PSG 수비 1차 저지선 붕괴(우리 약점) 매칭이 91%로 다가옵니다.'
  },
  'Paredes_Verratti': {
    areaText: '+11.5% 확장',
    areaPercent: 78,
    posComment: '수비형 미드필더 파레데스가 빠지고 조율 능력의 베라티가 투입되면서 빌드업 주도 영역이 모나코 진영으로 전진했습니다.',
    counterIndexText: 'Monaco 78% (위험)',
    counterPercent: 78,
    counterSpeedText: '5.8m/s',
    counterComment: '중원 수비 1차 저지선이 약화되어 모나코의 볼 탈취 후 역습 전개 속도가 초당 5.8m로 상승했습니다.',
    setpieceHeight: 22,
    setpieceDrill: 'Zone Defense Block Drill A',
    setpieceComment: '세트피스 공중볼 대인 방어율이 48%로 준수한 수준으로 유지되는 것으로 나타납니다.',
    matchRateUs: 68,
    matchCommentUs: '베라티의 전진 패스 전개 각도가 다양해졌으나, 전방 투입 패스의 직접적인 침투 루트 일치도는 68%입니다.',
    matchRateThem: 68,
    matchCommentThem: '베라티의 수비 범위 내에서 모나코의 다이렉트 패스 경로와 PSG의 수비 균열 구역(우리 약점) 매칭률이 68%로 소폭 상승했습니다.'
  },
  'Paredes_Rafinha': {
    areaText: '+15.2% 확장',
    areaPercent: 88,
    posComment: '파레데스가 맡았던 빌드업의 중심을 라피냐가 이어받으며, 전방 침투 패스 위주로 중원 전술이 변화했습니다.',
    counterIndexText: 'Monaco 92% (매우 위험)',
    counterPercent: 92,
    counterSpeedText: '7.1m/s',
    counterComment: '중원 수비 블록 붕괴와 라피냐의 전진 성향으로 인해 볼 소유권을 빼앗긴 후 3.5초 만에 하프라인이 돌파당합니다.',
    setpieceHeight: 35,
    setpieceDrill: 'Set-piece Zone Defense C',
    setpieceComment: '박스 안에서의 세트피스 평균 방어 성공률이 28%로 최하위에 근접하며 실점 불안 요소가 극대화됩니다.',
    matchRateUs: 82,
    matchCommentUs: '모나코 수비 조직의 좌측 하프스페이스 균열 구역(상대 약점)과 라피냐의 적극적인 침투가 어우러져 공격 에너지가 82%에 육박합니다.',
    matchRateThem: 88,
    matchCommentThem: '원래 포백 보호 역할(파레데스) 부재 및 라피냐의 오버랩으로 인해, 모나코의 전방 침투(상대 강점)와 수비 뒷공간 노출(우리 약점)이 88% 고강도로 매칭됩니다.'
  },
  'Paredes_MoiseKean': {
    areaText: '+7.5% 확장 (포백 보호 약화)',
    areaPercent: 58,
    posComment: '파레데스 대신 공격수가 투입되며 4-2-4에 가까운 극단적인 공격 전술로 변모했으나 중원 지배력은 크게 약화됩니다.',
    counterIndexText: 'Monaco 98% (최상 위험)',
    counterPercent: 98,
    counterSpeedText: '8.2m/s',
    counterComment: '포백을 보호해주는 수비형 미드필더가 전무하여 모나코의 롱볼 역습이 이어지는 즉시 슈팅 기회를 내주게 됩니다.',
    setpieceHeight: 8,
    setpieceDrill: 'Man-to-Man Marker System C',
    setpieceComment: '음바페와 모이세 킨 투톱의 전방 장악력 and 세트피스 제공권 강화로 헤더 실점 리스크는 낮아집니다.',
    matchRateUs: 48,
    matchCommentUs: '상대 약점 구역으로 직접 연결되는 롱볼 매칭은 48%에 불과하며, 대부분 직선적인 크로스에 의존하게 됩니다.',
    matchRateThem: 96,
    matchCommentThem: '수비형 미드필더 부재로 인해 모나코의 세컨볼 획득 및 2차 공격 전개(상대 강점)가 PSG 중앙 수비 뒷공간(우리 약점)과 96% 일치하여 극도로 취약해집니다.'
  },
  'BenYedder_Jovetic': {
    areaText: '+2.1% (수비 안정 전환)',
    areaPercent: 45,
    posComment: '벤 예데르가 아웃되면서 최전방 압박 강도가 감소했고, 조베티치 투입으로 수비 안정성을 꾀하는 코바치 감독의 선택입니다.',
    counterIndexText: 'PSG 55% (보통)',
    counterPercent: 55,
    counterSpeedText: '4.8m/s',
    counterComment: '전방 압박 감소로 PSG의 패스 성공률 and 조율 빈도는 늘어나나, 5-4-1 수비 블록 형성으로 박스 침투를 제한합니다.',
    setpieceHeight: 18,
    setpieceDrill: 'Compact Block Defensive Drill',
    setpieceComment: '조베티치의 뛰어난 공중볼 경합 능력으로 세트피스 수비 시 제공권 공백이 대폭 감소합니다.',
    matchRateUs: 38,
    matchCommentUs: '수비 전술 전환 시 상대 공격을 효율적으로 차단하는 매칭률이 38% 수준을 기록합니다.',
    matchRateThem: 61,
    matchCommentThem: 'PSG의 측면 돌파(상대 강점)와 모나코의 수비 측면 공백(우리 약점)이 61% 매칭됩니다.'
  },
  'Aguilar_Sidibe': {
    areaText: '-5.3% (우측 수비 보강)',
    areaPercent: 38,
    posComment: '아길라르의 적극적인 공격 오버랩이 줄어드는 대신 시디베의 안정적인 수비 밸런스로 우측 수비 라인을 단단히 굳힙니다.',
    counterIndexText: 'PSG 48% (안정)',
    counterPercent: 48,
    counterSpeedText: '4.2m/s',
    counterComment: '수비 블록의 깊이가 확보되어 PSG의 다이렉트 침투 속도가 초당 4.2m로 제어됩니다.',
    setpieceHeight: 12,
    setpieceDrill: 'Zone Defense Block Drill A',
    setpieceComment: '시디베의 탄탄한 피지컬 덕분에 우측 코너킥 및 크로스 수비 성공률이 72%로 상승합니다.',
    matchRateUs: 32,
    matchCommentUs: '수비 안정에 집중하며 역습 전환 시 공격 효율성은 32% 수준에 그칩니다.',
    matchRateThem: 45,
    matchCommentThem: 'PSG의 좌측 측면 공격(음바페)과 모나코의 우측 수비 강화가 맞붙으며 돌파 허용률이 45%로 낮아집니다.'
  },
  'Diop_Golovin': {
    areaText: '+8.7% (중원 창의성 강화)',
    areaPercent: 62,
    posComment: '골로빈의 창의적인 드리블 and 전진 패스 전개 능력으로 중원 패스 빌드업 주도 면적이 넓어집니다.',
    counterIndexText: 'PSG 67% (위험)',
    counterPercent: 67,
    counterSpeedText: '5.9m/s',
    counterComment: '골로빈의 높은 공격 참여로 인해 수비 복귀 시 공간 노출 위험이 생겨 PSG의 역습 위협도가 상승합니다.',
    setpieceHeight: 25,
    setpieceDrill: 'Set-piece Zone Defense B',
    setpieceComment: '골로빈의 날카로운 킥 능력으로 세트피스 상황 시 PSG 수비진에 큰 긴장감을 제공합니다.',
    matchRateUs: 71,
    matchCommentUs: '골로빈의 하프스페이스 침투 전개가 PSG 수비진의 약점 구역과 71% 매칭되어 위협적인 찬스를 만듭니다.',
    matchRateThem: 69,
    matchCommentThem: 'PSG의 중원 압박 및 골로빈의 개인 능력 활용이 충돌하며 상호 위협 노출률이 69%를 기록합니다.'
  },
  'Henrique_Ballo': {
    areaText: '-8.2% (좌측 측면 수비 집중)',
    areaPercent: 28,
    posComment: '90분에 발로투레를 투입하여 수비를 강화하고, 3-0 리드 상황에서 좌측 오버랩 공격 가담을 자제하며 걸어 잠급니다.',
    counterIndexText: 'PSG 35% (최소 위험)',
    counterPercent: 35,
    counterSpeedText: '3.5m/s',
    counterComment: '5백 수비 블록이 촘촘하게 유지되어 PSG의 마지막 총공세 침투 위협을 35% 이하로 최소화합니다.',
    setpieceHeight: 8,
    setpieceDrill: 'Man-to-Man Lock Drill',
    setpieceComment: '발로투레의 강력한 맨마킹으로 경기 막판 코너킥 and 크로스 실점 리스크를 최소화합니다.',
    matchRateUs: 18,
    matchCommentUs: '공격을 자제하고 지키는 전술이므로 역습 연계 및 슈팅 기회 창출 일치도는 18%에 불과합니다.',
    matchRateThem: 32,
    matchCommentThem: 'PSG의 좌측 측면 돌파 시도가 완전히 제어되며 상대 강점 노출률이 32%로 제어됩니다.'
  }
};"""

start_sim = content.find("const SIMULATION_DATA = {")
if start_sim != -1:
    end_sim = find_matching_brace(content, start_sim)
    if end_sim != -1:
        content = content[:start_sim] + clean_simulation_data + content[end_sim:]

# Target the unclosed strings specifically
content = content.replace(
    "const homeGoals = events.filter(e => e.event_type === 'GOAL' && e.team_name === match.home_team && !e.detail_kr?.includes('?살?))",
    "const homeGoals = events.filter(e => e.event_type === 'GOAL' && e.team_name?.trim().toLowerCase() === match.home_team?.trim().toLowerCase() && !e.detail_kr?.includes('자살골'))"
)
content = content.replace(
    "const awayGoals = events.filter(e => e.event_type === 'GOAL' && e.team_name === match.away_team && !e.detail_kr?.includes('?살?))",
    "const awayGoals = events.filter(e => e.event_type === 'GOAL' && e.team_name?.trim().toLowerCase() === match.away_team?.trim().toLowerCase() && !e.detail_kr?.includes('자살골'))"
)

# Line-by-line processing
lines = content.splitlines(keepends=True)
for idx, line in enumerate(lines):
    # 1. Tab labels line
    if 'commentary:' in line and 'timeline:' in line:
        lines[idx] = "                {{ commentary: 'AI 중계', timeline: '타임라인', lineups: '선수단', stats: '스탯', parameters: '전술 설정', yolo_val: 'YOLO 검증' }[tab]}\n"
    
    # 2. KLeague button
    if 'kleague' in line and 'window.open' in line:
        lines[idx] = "                    <button className=\"broadcast-btn kleague\" onClick={() => window.open('https://www.kleague.com', '_blank')}>K리그 공식 홈페이지</button>\n"

    # 2.1 Naver button
    if 'naver' in line and 'window.open' in line:
        lines[idx] = "                    <button className=\"broadcast-btn naver\" onClick={() => window.open('https://sports.naver.com/football/schedule', '_blank')}>네이버 스포츠</button>\n"

    # 2.2 Commentary empty events div close tag error fix
    if "fontSize: '48px'" in line and "??/div>" in line:
        lines[idx] = line.replace("??/div>", "📅</div>")

    # 3. Emojis and icons in event timeline (vertical side-by-side)
    if "let icon = '??;" in line:
        lines[idx] = "              let icon = '🏃';\n"
    if "icon = '??;" in line:
        lines[idx] = "              icon = '⚽';\n"
    if "icon = isRed ? '?' : '?';" in line:
        lines[idx] = "              icon = isRed ? '🟥' : '🟨';\n"
    if "icon = '?';" in line:
        prev_line = lines[idx-1] if idx > 0 else ""
        if '#0284c7' in prev_line:
            lines[idx] = "              icon = '🎯';\n"
        elif '#7c3aed' in prev_line:
            lines[idx] = "              icon = '🚩';\n"
        elif '#16a34a' in prev_line:
            lines[idx] = "              icon = '🔄';\n"

    # 3.1 Emojis and icons in renderTimelineCard (horizontal chronological card deck)
    if "let emoji = '??;" in line:
        lines[idx] = "  let emoji = '🏃';\n"
    if "emoji = '??;" in line:
        lines[idx] = "  emoji = '⚽';\n"
    if "emoji = isRed ? '?' : '?';" in line:
        lines[idx] = "  emoji = isRed ? '🟥' : '🟨';\n"
    if "emoji = '?';" in line:
        next_line = lines[idx+1] if idx + 1 < len(lines) else ""
        if '#3b82f6' in next_line:
            lines[idx] = "  emoji = '🎯';\n"
        elif '#8b5cf6' in next_line:
            lines[idx] = "  emoji = '🚩';\n"
        elif '#10b981' in next_line:
            lines[idx] = "  emoji = '🔄';\n"

    # 4. event-icon fallback
    if "EVENT_ICON[e.event_type] || '??}" in line:
        lines[idx] = "                <div className=\"event-icon\">{EVENT_ICON[e.event_type] || '⚽'}</div>\n"

    # 5. Position Map in lineups tab
    if "const posMap = { 'GK':" in line:
        lines[idx] = "                const posMap = { 'GK': '골키퍼', 'DF': '수비수', 'MF': '미드필더', 'FW': '공격수' }\n"

    # 6. Corrupted tag replacements
    if "?/span>" in line:
        if "{min}' ?/span>" in line:
            lines[idx] = line.replace("{min}' ?/span>", "{min}'</span>")
        elif "marginRight: '8px'}}>??/span>" in line:
            lines[idx] = line.replace("marginRight: '8px'}}>??/span>", "marginRight: '8px'}}>🛡️</span>")
        elif "color: '#00D9A3' }}>??/span>" in line:
            lines[idx] = line.replace("color: '#00D9A3' }}>??/span>", "color: '#00D9A3' }}>➜</span>")
        elif "color: '#64748b' }}>??/span>" in line:
            lines[idx] = line.replace("color: '#64748b' }}>??/span>", "color: '#64748b' }}>➜</span>")
        elif "침투 ?협 지??/span>" in line:
            lines[idx] = line.replace("?차단 ?점 ?방 ?? 침투 ?협 지??/span>", "수비 차단 시점 전방 침투 위협 지수</span>")
        elif "YOLOv11" in line and "<span>??/span>" in line:
            lines[idx] = line.replace("<span>??/span>", "<span>⚙️</span>")
    
    if "starting.length}명/span>" in line:
        lines[idx] = line.replace("starting.length}명/span>", "starting.length}명</span>")
        
    if "선발 라인업/div>" in line:
        lines[idx] = line.replace("선발 라인업/div>", "선발 라인업</div>")

    # 7. getPositionTier comment wrapper fix
    if "getPositionTier" in line and "//" in line:
        lines[idx] = "function getPositionTier(posDetail, posCode) {\n"

    # 8. Set-piece and tactical match tab text fixes (lines 1625-1740)
    if "? 1??이???결" in line:
        lines[idx] = line.replace("? 1??이???결", "🛡️ 1차 데이터 연결")
    if "SofaScore ?팅?" in line:
        lines[idx] = line.replace("SofaScore ?팅? 코너???하지??xG 분포 ??<strong>집계???이??모델?/strong>만으??트?스 불안 구역???교?게 ?출???며, 보완???한 맞춤???련 ?로그램??처방?니??", "SofaScore 슈팅과 코너킥 위치, xG 분포 등 <strong>집계 데이터 모델</strong>만으로 세트피스 불안 구역을 정교하게 검출하며, 보완을 위한 맞춤형 훈련 프로그램을 처방합니다.")
    if "?? ?비 조직" in line:
        lines[idx] = line.replace("?? ?비 조직?????용 공간(?점 구역)??리 ???최다 ?시?트/?스 개시 방향(강점 구역)??<strong>?트??이??교차 ?버??/strong>???해 ?점 ?률 극????인?? ?각?했?니??", "상대 수비 조직의 노출 공간(약점 구역)과 우리 전술의 최다 어시스트/패스 개시 방향(강점 구역)의 <strong>택티컬 매칭 교차 오버랩</strong>을 통해 득점 확률을 극대화하는 요인을 시각화했습니다.")
    if "perspective === 'us' ?" in line and "?? 강점 ?출?" in line:
        lines[idx] = line.replace("'?? ?점 × ?리 강점 매칭? : '?리 ?점 × ?? 강점 ?출?", "'상대 약점 × 우리 강점 매칭' : '우리 약점 × 상대 강점 노출'")

    # 9. Additional strong tag missing "<" fixes
    if "모델?/strong>" in line:
        lines[idx] = line.replace("모델?/strong>", "모델</strong>")
    if "교차 ?버??/strong>" in line:
        lines[idx] = line.replace("교차 ?버??/strong>", "교차 오버랩</strong>")

content = "".join(lines)

# Additional team filtering fixes
content = content.replace("homeLineup={lineups.filter(l => l.team_name === match.home_team)}", "homeLineup={lineups.filter(l => l.team_name?.trim().toLowerCase() === match.home_team?.trim().toLowerCase())}")
content = content.replace("awayLineup={lineups.filter(l => l.team_name === match.away_team)}", "awayLineup={lineups.filter(l => l.team_name?.trim().toLowerCase() === match.away_team?.trim().toLowerCase())}")
content = content.replace("const homeStats = stats.filter(s => s.team_name === match.home_team)", "const homeStats = stats.filter(s => s.team_name?.trim().toLowerCase() === match.home_team?.trim().toLowerCase())")
content = content.replace("const awayStats = stats.filter(s => s.team_name === match.away_team)", "const awayStats = stats.filter(s => s.team_name?.trim().toLowerCase() === match.away_team?.trim().toLowerCase())")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Full clean-up with syntax fixes completed successfully!")
