path = 'match_intelligence/frontend/src/components/MatchDetail.jsx'
try:
    lines = open(path, 'r', encoding='utf-8').readlines()
    block = lines[1098:1248] # line 1099 to 1248
    
    stack = []
    for idx, line in enumerate(block, 1099):
        # Ignore comments
        line_clean = line
        if '//' in line_clean:
            line_clean = line_clean.split('//')[0]
            
        for char_idx, char in enumerate(line_clean):
            if char == '{':
                stack.append((idx, char_idx, '{'))
            elif char == '}':
                if stack:
                    stack.pop()
                else:
                    print(f"Extra closing brace '}}' at line {idx}, char {char_idx}")
                    
    if stack:
        print("Unclosed braces remaining in stack:")
        for idx, char_idx, char in stack:
            print(f"  Opened '{char}' at line {idx}, char {char_idx}: {lines[idx-1].strip()}")
    else:
        print("Braces are balanced inside the block itself!")
except Exception as e:
    print("Error:", e)
