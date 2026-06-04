import sqlite3

try:
    conn = sqlite3.connect('match_intelligence/match_intelligence.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, detail_kr, team_name, event_type FROM events WHERE fixture_id = 1")
    rows = cursor.fetchall()
    print("--- Events Detail_KR ---")
    for r in rows:
        val = r[1]
        if val:
            # Let's see if we can convert it
            try:
                # SQLite usually returns python strings. If they are already decoded incorrectly,
                # we can encode them back to bytes using raw_unicode_escape or utf-8 and decode as cp949/euc-kr.
                b = val.encode('utf-8')
                print(f"ID {r[0]} ({r[3]}): {val}")
                try:
                    # Let's try different decodings
                    print("  as CP949:", val.encode('latin1').decode('cp949'))
                except Exception:
                    pass
                try:
                    print("  as UTF-8:", val.encode('latin1').decode('utf-8'))
                except Exception:
                    pass
            except Exception as e:
                print(f"ID {r[0]} error: {e}")
    conn.close()
except Exception as e:
    print("Error:", e)
