path = 'match_intelligence/frontend/src/components/MatchDetail.jsx'
try:
    lines = open(path, 'r', encoding='utf-8').readlines()
    
    # getTacType 함수 영역 재설정 (1115 ~ 1121번째 라인)
    lines[1115] = "function getTacType(team) {\n"
    lines[1116] = "  const tac = teamTactics[team]\n"
    lines[1117] = "  const p = parameters?.find(x => x.team_name === team)\n"
    lines[1118] = "  if (tac?.tactical_type) return tac.tactical_type\n"
    lines[1119] = "  if (!p) return null\n"
    lines[1120] = "  return p.press_intensity > 65 ? '압박' : p.defensive_line > 55 ? '역습' : p.press_intensity < 40 ? '침투' : '지연'\n"
    lines[1121] = "}\n"
    
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Successfully restored flat getTacType function structure!")
except Exception as e:
    print("Error:", e)
