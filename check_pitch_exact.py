path = 'match_intelligence/frontend/src/components/MatchDetail.jsx'
try:
    code = open(path, 'r', encoding='utf-8').read()
    lines = code.splitlines()
    
    # We want to tokenize from line 1099 (index 1098) to line 1248 (index 1247)
    # To do this accurately, we should tokenize the whole file and keep track of brace matching
    stack = []
    in_string = None # ' or " or `
    in_comment = None # // or /*
    in_jsx_text = False
    
    i = 0
    n = len(code)
    line_no = 1
    col_no = 0
    
    # We will record open braces and match them
    while i < n:
        char = code[i]
        
        # Newline handling
        if char == '\n':
            line_no += 1
            col_no = 0
            if in_comment == '//':
                in_comment = None
            i += 1
            continue
        
        col_no += 1
        
        # Comment handling
        if in_comment:
            if in_comment == '/*' and code[i:i+2] == '*/':
                in_comment = None
                i += 2
                col_no += 1
            else:
                i += 1
            continue
            
        if code[i:i+2] == '//':
            in_comment = '//'
            i += 2
            col_no += 1
            continue
        elif code[i:i+2] == '/*':
            in_comment = '/*'
            i += 2
            col_no += 1
            continue
            
        # String handling
        if in_string:
            if char == '\\':
                # Skip escaped character
                i += 2
                col_no += 1
                continue
            if char == in_string:
                in_string = None
            i += 1
            continue
            
        if char in ["'", '"', '`']:
            in_string = char
            i += 1
            continue
            
        # Brace matching
        if char == '{':
            stack.append((line_no, col_no))
            # print(f"Push: line {line_no}, col {col_no}, depth {len(stack)}")
        elif char == '}':
            if stack:
                popped = stack.pop()
                # print(f"Pop: line {line_no}, col {col_no} matches line {popped[0]}, col {popped[1]}, depth {len(stack)}")
            else:
                print(f"Error: Extra closing brace '}}' at line {line_no}, col {col_no}")
                
        i += 1
        
    print(f"\nFinal stack size: {len(stack)}")
    if stack:
        print("Unclosed braces:")
        for l, c in stack:
            print(f"  Line {l}, Col {c}: {lines[l-1].strip()}")
            
except Exception as e:
    print("Error:", e)
