path = 'match_intelligence/frontend/src/components/MatchDetail.jsx'
try:
    lines = open(path, 'r', encoding='utf-8').read().splitlines()
    stack = []
    # Trace from line 228 to 242 (0-indexed 227 to 241)
    for line_idx in range(227, 242):
        line = lines[line_idx]
        print(f"Line {line_idx+1}: {line.strip()}")
        for char_idx, char in enumerate(line):
            if char == '{':
                stack.append((line_idx+1, char_idx, '{'))
                print(f"  Push: '{char}' from line {line_idx+1}, stack size: {len(stack)}")
            elif char == '}':
                if stack:
                    popped = stack.pop()
                    print(f"  Pop: '{char}' matches '{popped[2]}' from line {popped[0]}, stack size: {len(stack)}")
                else:
                    print(f"  Error: Extra closing brace '}}' at line {line_idx+1}, char {char_idx}")
except Exception as e:
    print("Error:", e)
