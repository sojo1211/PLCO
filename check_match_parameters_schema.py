import sqlite3
conn = sqlite3.connect('match_intelligence/match_intelligence.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(match_parameters)")
for col in cursor.fetchall():
    print(col)
conn.close()
