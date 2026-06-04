file_path = "match_intelligence/frontend/src/components/MatchDetail.jsx"
content = open(file_path, "r", encoding="utf-8", errors="ignore").read()

lines = content.splitlines()
import re

for idx, line in enumerate(lines, 1):
    # Strip comments
    clean_line = re.sub(r'//.*', '', line)
    # Check for unclosed single quotes
    s_quotes = clean_line.count("'")
    if s_quotes % 2 != 0:
        # Check if it has a template literal backtick or comment block or regex
        if "/*" not in clean_line and "*/" not in clean_line and "`" not in clean_line:
            print(f"Unclosed single quote on line {idx}: {line.strip()}")

    d_quotes = clean_line.count('"')
    if d_quotes % 2 != 0:
        if "/*" not in clean_line and "*/" not in clean_line and "`" not in clean_line:
            print(f"Unclosed double quote on line {idx}: {line.strip()}")
