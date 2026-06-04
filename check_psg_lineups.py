import sqlite3
conn = sqlite3.connect('match_intelligence/match_intelligence.db')
cursor = conn.cursor()
cursor.execute("SELECT player_name, status, jersey_number, position, position_detail FROM lineups WHERE fixture_id = 1 AND team_name = 'PSG'")
for row in cursor.fetchall():
    print(row)
conn.close()
