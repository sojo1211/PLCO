path = 'match_intelligence/frontend/src/components/MatchDetail.jsx'
try:
    lines = open(path, 'r', encoding='utf-8').readlines()
    lines[1697] = "              <span>{perspective === 'us' ? '상대 약점 × 우리 강점 매칭' : '우리 약점 × 상대 강점 도출'}</span>\n"
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Fixed line 1698 successfully!")
except Exception as e:
    print("Error:", e)
