file_path = "match_intelligence/frontend/src/components/MatchDetail.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Line-by-line index repairs (0-indexed)
lines[867] = "                    <strong>압박 강도:</strong> {p.press_intensity?.toFixed(0) || '-'}%\n"
lines[870] = "                    <strong>수비 라인:</strong> {p.defensive_line?.toFixed(0) || '-'}%\n"
lines[873] = "                    <strong>세트피스:</strong> {p.setpiece_focus?.toFixed(0) || '-'}%\n"
lines[876] = "                    <strong>오프사이드:</strong> {p.offside_trap?.toFixed(0) || '-'}%\n"
lines[896] = "      <div className=\"state-msg\">파라미터 데이터가 없음</div>\n"
lines[905] = "    🖥️ YOLO 추적 vs 1차 데이터(소파스코어) 일치도 검증\n"
lines[907] = "    YOLO 비디오 분석 파이프라인에서 추출한 전술 정보와 공식 1차계 데이터(SofaScore)의 공식 데이터를 매칭하여 정확도를 검증합니다.\n"
lines[913] = "          const labelMap = { 'possession': '공 점유율(%)', 'pass_accuracy': '패스 성공률(%)' }\n"
lines[921] = "              <span style={{ color: '#00D9A3', fontWeight: 'bold', fontSize: '14px' }}>일치도 {accuracy.toFixed(1)}%</span>\n"
lines[929] = "          {/* 데이터 비교 */}\n"
lines[931] = "              <div>공식 1차 데이터: <strong style={{ color: '#fff' }}>{v.sofascore_value}%</strong></div>\n"
lines[933] = "              <div>YOLO 추출 데이터: <strong style={{ color: '#00D9A3' }}>{v.yolo_value}%</strong></div>\n"
lines[941] = "            검증 데이터가 존재하지 않습니다.\n"
lines[949] = "{/* 하단 포메이션 & 전술 섹션 배치 */}\n"
lines[1041] = "  // 나머지 선수가 있으면 추가 (완전 일치)\n"

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("More line index repairs completed!")
