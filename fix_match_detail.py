path = 'match_intelligence/frontend/src/components/MatchDetail.jsx'
try:
    content = open(path, 'rb').read()
    text = content.decode('utf-8', errors='replace')
    lines = text.splitlines()
    
    # Line 165 (index 164) and Line 166 (index 165)
    lines[164] = "        const homeGoals = events.filter(e => e.event_type === 'GOAL' && e.team_name === match.home_team && !e.detail_kr?.includes('자살골'))"
    lines[165] = "        const awayGoals = events.filter(e => e.event_type === 'GOAL' && e.team_name === match.away_team && !e.detail_kr?.includes('자살골'))"
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print("Fixed lines 165 and 166 successfully!")
except Exception as e:
    print("Error:", e)
