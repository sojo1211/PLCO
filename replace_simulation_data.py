file_path = "match_intelligence/frontend/src/components/MatchDetail.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Define the clean SIMULATION_DATA dictionary text
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
    setpieceComment: '킨의 피지컬과 헤더 제공권 확보(제공권 78%) 덕분에 코너킥 수비 시 공중볼 처리 위험 Zone이 크게 축소됩니다.',
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
    setpieceComment: '음바페와 모이세 킨 투톱의 전방 장악력과 세트피스 제공권 강화로 헤더 실점 리스크는 낮아집니다.',
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
    counterComment: '전방 압박 감소로 PSG의 패스 성공률과 조율 빈도는 늘어나나, 5-4-1 수비 블록 형성으로 박스 침투를 제한합니다.',
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
    posComment: '골로빈의 창의적인 드리블과 전진 패스 전개 능력으로 중원 패스 빌드업 주도 면적이 넓어집니다.',
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
    matchCommentThem: 'PSG의 중원 압박과 골로빈의 개인 능력 활용이 충돌하며 상호 위협 노출률이 69%를 기록합니다.'
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
    setpieceComment: '발로투레의 강력한 맨마킹으로 경기 막판 코너킥 및 크로스 실점 리스크를 최소화합니다.',
    matchRateUs: 18,
    matchCommentUs: '공격을 자제하고 지키는 전술이므로 역습 연계 및 슈팅 기회 창출 일치도는 18%에 불과합니다.',
    matchRateThem: 32,
    matchCommentThem: 'PSG의 좌측 측면 돌파 시도가 완전히 제어되며 상대 강점 노출률이 32%로 제어됩니다.'
  }
};"""

# Locate and replace SIMULATION_DATA in content
# We will use regex or find to replace from 'const SIMULATION_DATA = {' to '};' that is immediately followed by a blank line or 'function YoloTacticalReport'
start_idx = content.find("const SIMULATION_DATA = {")
end_marker = "};\n\nfunction YoloTacticalReport"
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + clean_simulation_data + content[end_idx + 2:]
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("SIMULATION_DATA replaced successfully!")
else:
    # If the end marker was slightly different, let's try finding the next occurrence of YoloTacticalReport
    end_idx_2 = content.find("function YoloTacticalReport")
    # find the }; just before it
    sub_content = content[:end_idx_2]
    last_brace = sub_content.rfind("};")
    if start_idx != -1 and last_brace != -1:
        new_content = content[:start_idx] + clean_simulation_data + content[last_brace + 2:]
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("SIMULATION_DATA replaced successfully via fallback!")
    else:
        print("Error: Could not find SIMULATION_DATA boundaries.")
