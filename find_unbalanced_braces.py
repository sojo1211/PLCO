import re

path = 'match_intelligence/frontend/src/components/MatchDetail.jsx'
try:
    content = open(path, 'r', encoding='utf-8').read()
    # Strip comments to avoid false matches in comments
    # Replace multiline comments /* ... */ with spaces of same length to keep line numbers
    def repl_multiline(m):
        return m.group(0).count('\n') * '\n'
    content_no_comments = re.sub(r'/\*.*?\*/', repl_multiline, content, flags=re.DOTALL)
    
    # Strip single line comments
    lines = content_no_comments.splitlines()
    for idx, line in enumerate(lines):
        if '//' in line:
            lines[idx] = line.split('//')[0]
            
    stack = []
    for line_idx, line in enumerate(lines, 1):
        for char_idx, char in enumerate(line):
            if char == '{':
                stack.append((line_idx, char_idx, '{'))
            elif char == '}':
                if stack:
                    stack.pop()
                else:
                    print(f"Line {line_idx}: Extra closing brace '}}' at character {char_idx}")
                    
    print(f"\nScanning finished. Stack size: {len(stack)}")
    if stack:
        print("Unclosed braces:")
        for line_idx, char_idx, char in stack:
            raw_line = open(path, 'r', encoding='utf-8').read().splitlines()[line_idx-1]
            print(f"  Line {line_idx}, Char {char_idx}: {raw_line.strip()}")
            
except Exception as e:
    print("Error:", e)
