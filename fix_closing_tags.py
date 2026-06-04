import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = 'match_intelligence/frontend/src/components/MatchDetail.jsx'
try:
    content = open(path, 'rb').read()
    text = content.decode('utf-8', errors='replace')
    lines = text.splitlines()
    
    modified_count = 0
    # Pattern to match corrupted closing tags: anything like ??/div, ?/span, /p, ??/button
    pattern = re.compile(r'[^a-zA-Z0-9<>{}="\'\s\r\n\t]+/(div|span|p|button|h4|strong|h2|h3)\b')
    
    for idx, line in enumerate(lines):
        match = pattern.search(line)
        if match:
            tag = match.group(1)
            span = match.span()
            old_str = line[span[0]:span[1]]
            new_str = f"</{tag}>"
            new_line = line[:span[0]] + new_str + line[span[1]:]
            print(f"Line {idx+1}: {old_str!r} -> {new_str!r}")
            lines[idx] = new_line
            modified_count += 1
            
    if modified_count > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f"Successfully fixed {modified_count} corrupted closing tags!")
    else:
        print("No corrupted closing tags matched the pattern.")
except Exception as e:
    print("Error:", e)
