path = 'match_intelligence/frontend/src/components/MatchDetail.jsx'
try:
    lines = open(path, 'r', encoding='utf-8', errors='ignore').readlines()
    for idx, line in enumerate(lines, 1):
        if '?' in line:
            # Print only if it looks like a UI text string or a comment
            trimmed = line.strip()
            # Ignore lines that are mostly code
            if any(x in trimmed for x in ["const", "function", "import", "console.log", "useEffect", "axios.get"]):
                continue
            print(f"{idx}: {trimmed}")
except Exception as e:
    print("Error:", e)
