import sqlite3

def getPositionTier(posDetail, posCode):
    d = (posDetail or '').lower()
    c = (posCode or '').upper()
    if c == 'GK' or 'goalkeeper' in d: return 0
    if 'center back' in d or 'left back' in d or 'right back' in d: return 1
    if 'defensive mid' in d or 'wingback' in d: return 2
    if 'central mid' in d: return 3
    if 'attacking mid' in d or 'winger' in d: return 4
    if 'striker' in d or 'forward' in d or 'center forward' in d: return 5
    if c == 'DF': return 1
    if c == 'MF': return 3
    if c == 'FW': return 5
    return 3

def getLateralOrder(posDetail):
    d = (posDetail or '').lower()
    if 'left' in d: return 1
    if 'center' in d or 'central' in d or 'striker' in d: return 2
    if 'right' in d: return 3
    return 2

def sortStartersToFormation(starters, formationStr):
    formation = [int(n) for n in formationStr.split('-')]
    sorted_starters = sorted(starters, key=lambda p: (
        getPositionTier(p['position_detail'], p['position']),
        getLateralOrder(p['position_detail'])
    ))
    
    gk = next((p for p in sorted_starters if getPositionTier(p['position_detail'], p['position']) == 0), None)
    outfield = [p for p in sorted_starters if getPositionTier(p['position_detail'], p['position']) != 0]
    
    result = [gk] if gk else []
    player_idx = 0
    for count in formation:
        line_players = outfield[player_idx:player_idx + count]
        line_players = sorted(line_players, key=lambda p: getLateralOrder(p['position_detail']))
        result.extend(line_players)
        player_idx += count
        
    while player_idx < len(outfield):
        result.append(outfield[player_idx])
        player_idx += 1
        
    return result

conn = sqlite3.connect('match_intelligence/match_intelligence.db')
cursor = conn.cursor()

# Fetch PSG starters
cursor.execute("SELECT player_name, jersey_number, position, position_detail, formation FROM lineups WHERE fixture_id = 1 AND team_name = 'PSG' AND status = 'Starting'")
psg_rows = cursor.fetchall()
psg_players = [{'player_name': r[0], 'jersey_number': r[1], 'position': r[2], 'position_detail': r[3]} for r in psg_rows]
print("PSG Database Players Count:", len(psg_players))

psg_sorted = sortStartersToFormation(psg_players, '4-3-3')
print("PSG Sorted Starters (first 11):")
for idx, p in enumerate(psg_sorted):
    print(f"  {idx}: {p['player_name']} ({p['position']}, {p['position_detail']})")

# Fetch Monaco starters
cursor.execute("SELECT player_name, jersey_number, position, position_detail, formation FROM lineups WHERE fixture_id = 1 AND team_name = 'AS_Monaco' AND status = 'Starting'")
monaco_rows = cursor.fetchall()
monaco_players = [{'player_name': r[0], 'jersey_number': r[1], 'position': r[2], 'position_detail': r[3]} for r in monaco_rows]
print("Monaco Database Players Count:", len(monaco_players))

monaco_sorted = sortStartersToFormation(monaco_players, '3-4-2-1')
print("Monaco Sorted Starters (first 11):")
for idx, p in enumerate(monaco_sorted):
    print(f"  {idx}: {p['player_name']} ({p['position']}, {p['position_detail']})")

conn.close()
