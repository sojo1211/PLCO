path = 'match_intelligence/frontend/src/components/MatchDetail.jsx'
try:
    content = open(path, 'r', encoding='utf-8').read()
    # Replace \ufffd with empty string
    clean_text = content.replace('\ufffd', '')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(clean_text)
    print("Successfully removed all replacement characters!")
except Exception as e:
    print("Error:", e)
