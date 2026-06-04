"""
K리그 Match Intelligence API 서버
"""
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from pathlib import Path
import requests

app = Flask(__name__)
CORS(app)

DB_PATH = Path(__file__).parent / "match_intelligence.db"
YOUTUBE_API_KEY = 'AIzaSyDWvUxIoZko9r8ElBRONO5ICGEHTCd_h8k'

TEAM_LOGOS = {
    "서울": "https://www.kleague.com/assets/images/emblem/emblem_K09.png",
    "수원": "https://www.kleague.com/assets/images/emblem/emblem_K02.png",
    "인천": "https://www.kleague.com/assets/images/emblem/emblem_K18.png",
    "대구": "https://www.kleague.com/assets/images/emblem/emblem_K17.png",
    "대전": "https://www.kleague.com/assets/images/emblem/emblem_K10.png",
    "광주": "https://www.kleague.com/assets/images/emblem/emblem_K22.png",
    "전북": "https://www.kleague.com/assets/images/emblem/emblem_K05.png",
    "전남": "https://www.kleague.com/assets/images/emblem/emblem_K07.png",
    "포항": "https://www.kleague.com/assets/images/emblem/emblem_K03.png",
    "울산": "https://www.kleague.com/assets/images/emblem/emblem_K01.png",
    "제주": "https://www.kleague.com/assets/images/emblem/emblem_K04.png",
    "부산": "https://www.kleague.com/assets/images/emblem/emblem_K06.png",
    "파주": "https://www.kleague.com/assets/images/emblem/emblem_K40.png",
    "수원FC": "https://www.kleague.com/assets/images/emblem/emblem_K29.png",
    "충남아산": "https://www.kleague.com/assets/images/emblem/emblem_K34.png",
    "대구FC": "https://www.kleague.com/assets/images/emblem/emblem_K17.png",
    "안양": "https://www.kleague.com/assets/images/emblem/emblem_K27.png",
    "성남": "https://www.kleague.com/assets/images/emblem/emblem_K08.png",
    "용인": "https://www.kleague.com/assets/images/emblem/emblem_K42.png",
    "김포": "https://www.kleague.com/assets/images/emblem/emblem_K36.png",
    "김해": "https://www.kleague.com/assets/images/emblem/emblem_K41.png",
    "천안": "https://www.kleague.com/assets/images/emblem/emblem_K38.png",
    "화성": "https://www.kleague.com/assets/images/emblem/emblem_K39.png",
    "서울E": "https://www.kleague.com/assets/images/emblem/emblem_K31.png",
    "강원": "https://www.kleague.com/assets/images/emblem/emblem_K21.png",
    "강원FC": "https://www.kleague.com/assets/images/emblem/emblem_K21.png",
    "부천": "https://www.kleague.com/assets/images/emblem/emblem_K26.png",
    "경남": "https://www.kleague.com/assets/images/emblem/emblem_K20.png",
    "김천": "https://www.kleague.com/assets/images/emblem/emblem_K35.png",
    "청주": "https://www.kleague.com/assets/images/emblem/emblem_K37.png",
    "충북청주": "https://www.kleague.com/assets/images/emblem/emblem_K37.png",
    "안산": "https://www.kleague.com/assets/images/emblem/emblem_K32.png",
    "이천": "https://www.kleague.com/assets/images/emblem/emblem_K25.png",
    "여수": "https://www.kleague.com/assets/images/emblem/emblem_K26.png",
    "시흥": "https://www.kleague.com/assets/images/emblem/emblem_K24.png",
}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/health', methods=['GET'])
def health():
    try:
        conn = get_db()
        count = conn.execute("SELECT COUNT(*) FROM fixtures_full").fetchone()[0]
        conn.close()
        return jsonify({"status": "ok", "fixtures": count})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/fixtures', methods=['GET'])
def fixtures():
    try:
        year = request.args.get('year', type=int)
        league = request.args.get('league', type=int)
        limit = request.args.get('limit', default=50, type=int)

        conn = get_db()
        where = "status='Ended' AND (home_score > 0 OR away_score > 0)"
        if year:
            where += f" AND season={year}"
        if league:
            where += f" AND league_id={league}"

        rows = conn.execute(f"SELECT * FROM fixtures_full WHERE {where} ORDER BY date DESC LIMIT {limit}").fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fixtures/<int:fixture_id>/events', methods=['GET'])
def fixture_events(fixture_id):
    try:
        conn = get_db()
        rows = conn.execute("SELECT * FROM events WHERE fixture_id = ? ORDER BY minute, extra_time", (fixture_id,)).fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fixtures/<int:fixture_id>/lineups', methods=['GET'])
def fixture_lineups(fixture_id):
    try:
        conn = get_db()
        rows = conn.execute("SELECT * FROM lineups WHERE fixture_id = ? ORDER BY team_name, status DESC, jersey_number", (fixture_id,)).fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fixtures/<int:fixture_id>/player_stats', methods=['GET'])
def fixture_player_stats(fixture_id):
    try:
        conn = get_db()
        rows = conn.execute("SELECT * FROM player_stats WHERE fixture_id = ? ORDER BY team_name, player_name", (fixture_id,)).fetchall()
        conn.close()
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/standings', methods=['GET'])
def standings():
    try:
        year = request.args.get('year', type=int, default=2026)
        league = request.args.get('league', type=int)

        conn = get_db()
        query = "SELECT home_team, away_team, home_score, away_score FROM fixtures_full WHERE status='Ended' AND season=? AND (home_score > 0 OR away_score > 0)"
        params = [year]
        if league:
            query += " AND league_id=?"
            params.append(league)

        rows = conn.execute(query, params).fetchall()

        teams = {}
        for home, away, h_score, a_score in rows:
            for team in [home, away]:
                if team not in teams:
                    teams[team] = {"W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0}
            teams[home]["GF"] += h_score
            teams[home]["GA"] += a_score
            teams[away]["GF"] += a_score
            teams[away]["GA"] += h_score
            if h_score > a_score:
                teams[home]["W"] += 1
                teams[away]["L"] += 1
            elif h_score < a_score:
                teams[away]["W"] += 1
                teams[home]["L"] += 1
            else:
                teams[home]["D"] += 1
                teams[away]["D"] += 1

        standings_list = []
        for team, stats in teams.items():
            pts = stats["W"] * 3 + stats["D"]
            standings_list.append({
                "team": team,
                "played": stats["W"] + stats["D"] + stats["L"],
                "wins": stats["W"],
                "draws": stats["D"],
                "losses": stats["L"],
                "gf": stats["GF"],
                "ga": stats["GA"],
                "gd": stats["GF"] - stats["GA"],
                "pts": pts,
                "logo": TEAM_LOGOS.get(team, "")
            })

        standings_list.sort(key=lambda x: (-x["pts"], -x["gd"]))
        conn.close()
        return jsonify(standings_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/matches/<fixture_id>/commentary', methods=['GET'])
def commentary(fixture_id):
    try:
        fixture_id = int(fixture_id)
        home_team = request.args.get('home', '')
        away_team = request.args.get('away', '')

        conn = get_db()
        fixture = conn.execute("SELECT home_score, away_score, date, home_team, away_team FROM fixtures_full WHERE fixture_id = ?", (fixture_id,)).fetchone()

        if not fixture:
            return jsonify({"commentary": "경기 데이터 없음"})

        events = conn.execute("SELECT minute, extra_time, event_type, player_name, team_name, detail_kr FROM events WHERE fixture_id = ? ORDER BY minute, extra_time", (fixture_id,)).fetchall()
        conn.close()

        home_team = fixture[3]
        away_team = fixture[4]
        score_h = fixture[0]
        score_a = fixture[1]

        event_lines = []
        for e in events:
            min_str = f"{e[0]}'"
            if e[1]:
                min_str += f"+{e[1]}"
            event_lines.append(f"{min_str} {e[4]} - {e[2]}: {e[3]}")

        commentary_text = f"[{home_team} vs {away_team} {score_h}:{score_a} 경기 종료]\n\n{home_team}이(가) {score_h}:{score_a}로 경기를 완주했습니다."

        if event_lines:
            goals = [e for e in event_lines if 'GOAL' in e]
            if goals:
                commentary_text += f"\n\n[득점 장면]\n" + "\n".join(goals[:5])

        return jsonify({"commentary": commentary_text})
    except Exception as e:
        return jsonify({"commentary": f"중계 생성 실패: {str(e)}"}), 500

@app.route('/api/youtube/search', methods=['GET'])
def youtube_search():
    try:
        home_team = request.args.get('home', '')
        away_team = request.args.get('away', '')
        date = request.args.get('date', '')

        query = f"{home_team} vs {away_team} K리그"

        try:
            official_channels = [
                "UCjj7-qRkpzBpOcBhbD5RQtA",
                "UC0WYCQY1kbHk8n0xvxqfyEw",
                "UCPrJIoKp_fPa7pUA3Q5C8zQ",
            ]

            results = []
            video_id = None

            for channel_id in official_channels:
                url = "https://www.googleapis.com/youtube/v3/search"
                params = {
                    "part": "snippet",
                    "q": query,
                    "channelId": channel_id,
                    "type": "video",
                    "maxResults": 5,
                    "order": "date",
                    "key": YOUTUBE_API_KEY,
                }

                try:
                    response = requests.get(url, params=params, timeout=5)
                    data = response.json()

                    if "items" in data:
                        for item in data["items"]:
                            vid = item["id"]["videoId"]
                            title = item["snippet"]["title"]
                            thumb = item["snippet"]["thumbnails"]["medium"]["url"]
                            channel = item["snippet"]["channelTitle"]

                            results.append({
                                "video_id": vid,
                                "title": title,
                                "thumbnail": thumb,
                                "channel": channel
                            })

                            if not video_id:
                                video_id = vid

                    if video_id:
                        break
                except:
                    pass

            if not video_id:
                url = "https://www.googleapis.com/youtube/v3/search"
                params = {
                    "part": "snippet",
                    "q": f"{query} 경기 하이라이트",
                    "type": "video",
                    "maxResults": 10,
                    "order": "relevance",
                    "key": YOUTUBE_API_KEY,
                }

                try:
                    response = requests.get(url, params=params, timeout=5)
                    data = response.json()

                    if "items" in data:
                        for item in data["items"]:
                            vid = item["id"]["videoId"]
                            title = item["snippet"]["title"]
                            thumb = item["snippet"]["thumbnails"]["medium"]["url"]
                            channel = item["snippet"]["channelTitle"]

                            results.append({
                                "video_id": vid,
                                "title": title,
                                "thumbnail": thumb,
                                "channel": channel
                            })

                            if not video_id:
                                video_id = vid
                except:
                    pass

            return jsonify({
                "query": query,
                "results": results,
                "video_id": video_id
            })
        except:
            return jsonify({
                "query": query,
                "results": [],
                "video_id": None
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("[START] K리그 Match Intelligence API")
    print("[ACCESS] http://localhost:5003")
    app.run(host='localhost', port=5003, debug=False)
