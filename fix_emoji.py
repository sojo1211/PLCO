import sys

path = 'match_intelligence/frontend/src/components/MatchDetail.jsx'
try:
    content = open(path, 'rb').read()
    # Decode using replace to preserve content and avoid crash
    text = content.decode('utf-8', errors='replace')
    lines = text.splitlines()
    
    # Replace line 5 (index 4) with correct string
    lines[4] = "  GOAL: '⚽', CARD: '🟨', SUBST: '🔄', VAR: '📺',"
    
    # Write back as UTF-8
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print("Successfully replaced line 5 with clean emojis and quotes!")
except Exception as e:
    print("Error:", e)
