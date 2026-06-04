"""
실시간 경기 이벤트 수집기
- 경기 진행 중일 때 매 15초마다 이벤트 갱신
- 경기 상태: Live → Ended로 변경되면 중단
"""
import sqlite3
import time
import requests
from datetime import datetime
import sys

sys.path.insert(0, '.')
import kleague_client as kl
import storage

storage.init_db()

def collect_live_events():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 실시간 경기 이벤트 수집 시작...\n")
    
    db = sqlite3.connect("match_intelligence.db")
    cursor = db.cursor()
    
    while True:
        # 현재 Live 경기 찾기
        live_matches = cursor.execute(
            "SELECT fixture_id, home_team, away_team, status FROM fixtures_full WHERE status='Live' LIMIT 10"
        ).fetchall()
        
        if not live_matches:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Live 경기 없음. 30초 대기...\n")
            time.sleep(30)
            continue
        
        for fid, home, away, status in live_matches:
            print(f"[경기 중] {fid}: {home} vs {away}")
            
            try:
                # K리그 API에서 현재 이벤트 조회
                year = str(fid)[:4]
                # ... API 호출하여 이벤트 갱신
                
            except Exception as e:
                print(f"  ❌ 에러: {e}")
            
            time.sleep(15)  # 15초 대기
        
        db.commit()
    
    db.close()

if __name__ == "__main__":
    collect_live_events()
