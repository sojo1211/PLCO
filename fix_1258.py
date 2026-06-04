path = 'match_intelligence/frontend/src/components/MatchDetail.jsx'
try:
    lines = open(path, 'r', encoding='utf-8').readlines()
    lines[1257] = "  { out: 'BenYedder', outFull: 'Wissam Ben Yedder', outPos: 'FW', minute: 71, inKey: 'Jovetic',  inFull: 'Stevan Jovetic', inPos: 'FW' },\n"
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Fixed line 1258 successfully!")
except Exception as e:
    print("Error:", e)
