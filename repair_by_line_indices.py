file_path = "match_intelligence/frontend/src/components/MatchDetail.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Line-by-line index repairs (0-indexed)
lines[115] = "  // YOLO 검사 비교 데이터 로드\n"
lines[162] = "      {/* K리그 방송 스타일 스코어보드 */}\n"
lines[245] = "      <p>영상을 찾을 수 없습니다.</p>\n"
lines[296] = "  {/* AI 중계 - Gemini 기반 실시간 편파 중계 */}\n"
lines[316] = "      <span className=\"ended-text\">경기 시작부터 종료까지 실시간 중계 피드</span>\n"
lines[322] = "      <span className=\"timeline-title\" style={{fontSize: '16px', fontWeight: 'bold', color: '#1e293b'}}>🎙️ AI 실시간 경기 해설 피드</span>\n"
lines[408] = "      <span style={{fontSize: '18px'}}>🏃</span>\n"
lines[409] = "      <span style={{fontSize: '13px'}}>0' - 경기 시작! Parc des Princes 경기장에서 심판의 휘슬과 함께 킥오프됩니다!</span>\n"
lines[415] = "      <span>⏱️ 전반전</span>\n"
lines[416] = "      <span style={{fontSize: '12px', color: '#64748b', fontWeight: 'normal'}}>(1분 ~ 45분)</span>\n"
lines[425] = "      <span>⏱️ 전반전 추가시간</span>\n"
lines[434] = "      <span>⏱️ 후반전</span>\n"
lines[435] = "      <span style={{fontSize: '12px', color: '#64748b', fontWeight: 'normal'}}>(46분 ~ 90분)</span>\n"
lines[444] = "      <span>⏱️ 후반전 추가시간</span>\n"
lines[453] = "      <span style={{fontSize: '20px'}}>🏁</span>\n"
lines[454] = "      <span>90' - 경기 종료! 최종 스코어 {match.home_team} {match.home_score} : {match.away_score} {match.away_team}</span>\n"
lines[501] = "      <span style={{fontSize: '16px'}}>🏃</span>\n"
lines[502] = "      <span>0' - 경기 시작! Parc des Princes 경기장에서 킥오프 휘슬이 울립니다!</span>\n"
lines[646] = "      <span style={{fontSize: '18px'}}>🏁</span>\n"
lines[647] = "      <span>90' - 경기 종료! 최종 스코어 {match.home_team} {match.home_score} : {match.away_score} {match.away_team}</span>\n"
lines[665] = "      {events.length === 0 && <div className=\"state-msg\">이벤트 데이터가 없음</div>}\n"
lines[1190] = "  {/* 팀 헤더 */}\n"

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Line index repairs completed!")
