import sys

lines = open('match_intelligence/frontend/src/components/MatchDetail.jsx', 'r', encoding='utf-8', errors='ignore').readlines()
count = 0
for idx, line in enumerate(lines, 1):
    line_clean = line.strip()
    if '?' in line_clean:
        # Check if this '?' is a corrupted character
        # Corrupted characters are usually standalone '?' within Korean text.
        # We can detect it by checking if it's not ?. and not ?? and not ? : etc.
        # Let's check each '?' character index in the line
        is_corrupt = False
        for pos, char in enumerate(line_clean):
            if char == '?':
                # check surrounding characters
                is_safe = False
                # Optional chaining ?.
                if pos + 1 < len(line_clean) and line_clean[pos+1] == '.':
                    is_safe = True
                # Nullish coalescing ??
                if pos + 1 < len(line_clean) and line_clean[pos+1] == '?':
                    is_safe = True
                if pos - 1 >= 0 and line_clean[pos-1] == '?':
                    is_safe = True
                # Ternary ? :
                if pos + 1 < len(line_clean) and line_clean[pos+1] == ' ':
                    is_safe = True
                if pos - 1 >= 0 and line_clean[pos-1] == ' ':
                    is_safe = True
                # Quotes in JSON or string
                if pos + 1 < len(line_clean) and line_clean[pos+1] in ['"', "'", '`']:
                    is_safe = True
                if pos - 1 >= 0 and line_clean[pos-1] in ['"', "'", '`']:
                    is_safe = True
                # YouTube query params or URLs
                if "youtube" in line_clean.lower() or "youtu.be" in line_clean.lower():
                    is_safe = True
                
                if not is_safe:
                    is_corrupt = True
                    break
        
        if is_corrupt:
            print(f'{idx}: {line_clean}')
            count += 1

print(f'Total matches: {count}')
