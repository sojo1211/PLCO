import sqlite3

for db_name in ['kleague.db', 'match_intelligence/frontend/match_intelligence.db', 'match_intelligence/match_intelligence.db']:
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        print(f"--- DB: {db_name} ---")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [x[0] for x in cursor.fetchall()]
        print("  Tables:", tables)
        
        for table in tables:
            if 'lineup' in table or 'match' in table or 'tactic' in table:
                cursor.execute(f"PRAGMA table_info({table})")
                cols = [x[1] for x in cursor.fetchall()]
                print(f"  Table '{table}' columns: {cols}")
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                print(f"    Count: {cursor.fetchone()[0]}")
                cursor.execute(f"SELECT * FROM {table} LIMIT 1")
                print(f"    Sample row: {cursor.fetchone()}")
        conn.close()
    except Exception as e:
        print(f"  Error reading {db_name}: {e}")
