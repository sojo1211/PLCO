lines = open('match_intelligence/frontend/src/components/MatchDetail.jsx', 'r', encoding='utf-8', errors='ignore').readlines()
print("Total lines:", len(lines))
# print lines 1400 to 1450 and lines 2800 to 2831
print("--- Lines 1425 to 1445 ---")
for idx in range(1425, min(1445, len(lines))):
    print(f"{idx+1}: {lines[idx].strip()}")

print("--- Lines 2800 to end ---")
for idx in range(2800, len(lines)):
    print(f"{idx+1}: {lines[idx].strip()}")
