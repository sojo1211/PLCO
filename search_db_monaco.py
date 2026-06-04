import sqlite3

dbs = ['kleague.db', 'match_intelligence/match_intelligence.db']
for db in dbs:
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [x[0] for x in cursor.fetchall()]
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table})")
            cols = [x[1] for x in cursor.fetchall()]
            for col in cols:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} LIKE '%모나코%' OR {col} LIKE '%Monaco%'")
                    cnt = cursor.fetchone()[0]
                    if cnt > 0:
                        print(f"Found match in DB '{db}', Table '{table}', Column '{col}': {cnt} rows")
                        cursor.execute(f"SELECT DISTINCT {col} FROM {table} WHERE {col} LIKE '%모나코%' OR {col} LIKE '%Monaco%'")
                        print("  Distinct values:", cursor.fetchall())
                except Exception as col_err:
                    pass
        conn.close()
    except Exception as e:
        print("Error reading db:", db, e)
