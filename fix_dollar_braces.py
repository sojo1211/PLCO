file_path = "match_intelligence/frontend/src/components/MatchDetail.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Let's replace the commentary lines explicitly by index to avoid any matching issues!
# Line 14:
lines[13] = "      return `앗!! 이게 무슨 일인가요! ${team_name}의 ${player_name} 선수의 뼈아픈 자살골이 기록되고 맙니다. 경기장 분위기가 급격하게 얼어붙습니다.`;\n"

# Line 16:
lines[15] = "      return `골!!! 골망을 흔듭니다! 들어갔습니다! ${team_name}의 ${player_name}! 환상적인 결정력을 보여주네요!${assist_name ? ` 날카로운 패스를 찔러준 ${assist_name} 선수의 어시스트도 명품이었습니다!` : ''}`;\n"

# Line 21:
lines[20] = "      return `레드카드 발동!!!! 심판이 지체 없이 퇴장을 명령합니다. ${team_name}의 ${player_name} 선수가 퇴장하면서 경기 구도가 요동치기 시작합니다!`;\n"

# Line 23:
lines[22] = "      return `경고 누적을 주의해야 합니다! 주심이 ${team_name}의 ${player_name} 선수에게 옐로카드를 부여합니다. 거친 태클이었습니다.`;\n"

# Line 27:
lines[26] = "      return `감독이 전술에 중대한 변화를 줍니다! ${team_name}에서 ${detail_kr}를 진행합니다. 그라운드에 새로운 활력을 공급합니다.`;\n"

# Line 30:
lines[29] = "      return `교체 아웃/인! ${team_name}의 ${player_name} 선수가 아웃되고, ${assist_name} 선수가 그라운드로 뛰어 들어갑니다.`;\n"

# Line 32:
lines[31] = "      return `교체 카드 투입! ${team_name}팀이 선수 교체(${player_name || '선수'})를 단행하며 새로운 흐름을 꾀합니다.`;\n"

# Line 35:
lines[34] = "      return `과감하게 때려봅니다! ${team_name}의 ${player_name}! 아주 날카로운 슈팅이었으나 골키퍼 정면 혹은 아슬아슬하게 골문을 비껴갑니다.`;\n"

# Line 38:
lines[37] = "      return `코너킥 세트피스 기회를 맞이합니다, ${team_name}! 공중볼 경합 상황에서 어떤 선수가 득점 기회를 만들어낼 수 있을지 기대됩니다.`;\n"

# Line 41:
lines[40] = "      return `박진감 넘치는 경기 진행 중: ${team_name} - ${detail_kr || event_type}`;\n"

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Template literals fixed successfully!")
