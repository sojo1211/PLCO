path = 'match_intelligence/frontend/src/components/MatchDetail.jsx'
try:
    lines = open(path, 'r', encoding='utf-8').readlines()
    
    # We must restore line 292 with JSX brackets
    lines[291] = "    { { commentary: 'AI 중계', timeline: '타임라인', lineups: '라인업', stats: '통계', parameters: '파라미터', yolo_val: 'YOLO 분석' }[tab] }\n"
    
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Successfully corrected line 292 to use JSX brackets!")
except Exception as e:
    print("Error:", e)
