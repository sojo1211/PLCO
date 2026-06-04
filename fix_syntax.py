import re

path = 'match_intelligence/frontend/src/components/MatchDetail.jsx'
try:
    content = open(path, 'rb').read()
    text = content.decode('utf-8', errors='replace')
    lines = text.splitlines()
    
    # 1. Fix line 5 emojis (index 4)
    lines[4] = "  GOAL: '⚽', CARD: '🟨', SUBST: '🔄', VAR: '📺',"
    print("Fixed line 5 emojis.")
    
    # 2. Fix lines 165-166 (index 164 and 165)
    lines[164] = "        const homeGoals = events.filter(e => e.event_type === 'GOAL' && e.team_name === match.home_team && !e.detail_kr?.includes('자살골'))"
    lines[165] = "        const awayGoals = events.filter(e => e.event_type === 'GOAL' && e.team_name === match.away_team && !e.detail_kr?.includes('자살골'))"
    print("Fixed lines 165 and 166 (자살골).")
    
    # 3. Fix corrupted closing tags
    # This pattern matches any corrupted closing tag like ??/div>, ?/span>, 못했?니??/p> and replaces it with </tag>
    pattern = re.compile(r'[^a-zA-Z0-9<>{}="\'\s\r\n\t]+/([a-zA-Z0-9]+)>')
    
    modified_count = 0
    for idx, line in enumerate(lines):
        if idx in [4, 164, 165]:
            continue
        new_line, count = pattern.subn(r'</\1>', line)
        if count > 0:
            lines[idx] = new_line
            modified_count += count
            
    print(f"Fixed {modified_count} corrupted closing tags.")
    
    # Write back as UTF-8
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print("Successfully wrote fixed MatchDetail.jsx to disk!")
    
except Exception as e:
    print("Error:", e)
