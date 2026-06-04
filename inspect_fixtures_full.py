import sqlite3

try:
    conn = sqlite3.connect('match_intelligence/match_intelligence.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fixtures_full")
    rows = cursor.fetchall()
    print("Fixtures count:", len(rows))
    for r in rows:
        print(r)
    conn.close()
except Exception as e:
    print("Error:", e)
