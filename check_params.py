import sqlite3
conn = sqlite3.connect('match_intelligence/match_intelligence.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM match_parameters WHERE fixture_id = 1")
print(cursor.fetchall())
conn.close()
