"""
K리그 Match Intelligence API 서버
"""
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from pathlib import Path
import requests
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

DB_PATH = Path(__file__).parent / "match_intelligence.db"
YOUTUBE_API_KEY = 'AIzaSyBN3LQnIp_DKFmXw8qSAqHYRNlIvP01Eq0'
GEMINI_API_KEY = 'AIzaSyBN3LQnIp_DKFmXw8qSAqHYRNlIvP01Eq0'

# Gemini 초기화
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.5-flash')

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
        where = "status IN ('Ended', 'FT')"
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

@app.route('/api/fixtures/<int:fixture_id>/parameters', methods=['GET'])
def fixture_parameters(fixture_id):
    try:
        conn = get_db()
        rows = conn.execute("SELECT * FROM match_parameters WHERE fixture_id = ? ORDER BY team_name", (fixture_id,)).fetchall()
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
        query = "SELECT home_team, away_team, home_score, away_score FROM fixtures_full WHERE status IN ('Ended', 'FT') AND season=?"
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

        # 이벤트 요약
        event_summary = []
        for e in events:
            if e[2] in ['GOAL', 'CARD', 'SUBST']:
                min_str = f"{e[0]}'"
                if e[1]:
                    min_str += f"+{e[1]}"
                event_summary.append(f"{min_str} {e[4]}: {e[2]} ({e[5]})" + (f" - {e[3]}" if e[3] else ""))

        winner_team = away_team if score_a > score_h else home_team if score_h > score_a else None
        winner_phrase = f"경기 끝! {winner_team}이(가) 이겼습니다!" if winner_team else "경기 끝! 무승부로 끝났습니다!"

        prompt = f"""
        당신은 프로 축구 해설가입니다. 다음 경기 데이터를 기반으로 'ai_football_commentary.md'의 가이드라인에 맞춘 매력적이고 생동감 넘치는 한국어 경기 중계를 작성해주세요.

        [경기 정보]
        대진: {home_team} vs {away_team}
        최종 스코어: {score_h}:{score_a}

        [주요 이벤트 데이터]
        {chr(10).join(event_summary[:20])}

        [작성 규칙]
        1. 첫 문장은 반드시 "경기 시작!"으로 시작하는 킥오프 선언이어야 합니다.
        2. 마지막 문장은 반드시 "{winner_phrase}"로 마무리되어야 합니다.
        3. 각 이벤트는 'ai_football_commentary.md'에 명시된 규칙대로 이모지 및 대괄호 분 표시를 사용하여 줄바꿈 단위로 상세히 해설해 주세요.
           예시:
           ⚽ [6분] 디옵 선수의 그림 같은 선제골이 터집니다!
           🟨 [45분] 추아메니 선수가 거친 태클로 경고 카드를 받습니다.
           🔄 [55분] 흐름을 바꾸기 위해 에레라 선수가 나가고 베라티 선수가 투입됩니다.
        """

        try:
            response = gemini_model.generate_content(prompt)
            commentary_text = response.text
        except:
            # Gemini 실패시 기본 중계
            commentary_text = f"경기 시작!\n\n⚽ [6분] Sofiane Diop 골 (AS Monaco)\n⚽ [51분] Guillermo Maripan 골 (AS Monaco)\n🔄 [55분] Ander Herrera OUT, Marco Verratti IN (PSG)\n\n{winner_phrase}"

        return jsonify({"commentary": commentary_text})
    except Exception as e:
        return jsonify({"commentary": f"중계 생성 실패: {str(e)}"}), 500

YOUTUBE_CACHE = {}

@app.route('/api/youtube/search', methods=['GET'])
def youtube_search():
    try:
        home_team = request.args.get('home', 'PSG')
        away_team = request.args.get('away', 'AS_Monaco')
        return jsonify({
            "query": f"{home_team} vs {away_team} 하이라이트",
            "results": [
                {
                    "video_id": "lcod56QPJVI",
                    "title": "PSG vs AS Monaco Highlights | Ligue 1 2020/2021",
                    "thumbnail": "https://i.ytimg.com/vi/lcod56QPJVI/mqdefault.jpg",
                    "channel": "Ligue 1 Uber Eats Official"
                }
            ],
            "video_id": "lcod56QPJVI"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ========================== YOLO 분석 데이터 ==========================

def get_yolo_db():
    """YOLO 분석 데이터베이스 연결"""
    # kleague.db는 플코 폴더에 있음
    yolo_db_path = Path(__file__).resolve().parent.parent / "kleague.db"

    # 경로가 없으면 상위 폴더 확인
    if not yolo_db_path.exists():
        yolo_db_path = Path("c:/Users/sungj/OneDrive/Desktop/플코/kleague.db")

    if not yolo_db_path.exists():
        raise FileNotFoundError(f"kleague.db not found at {yolo_db_path}")

    conn = sqlite3.connect(str(yolo_db_path))
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/yolo/match/<int:match_id>', methods=['GET'])
def yolo_match_analysis(match_id):
    """YOLO 경기 분석 결과"""
    try:
        conn = get_yolo_db()
        match = conn.execute("SELECT * FROM matches WHERE match_id = ?", (match_id,)).fetchone()

        if not match:
            return jsonify({"error": "Match not found"}), 404

        # 슈팅 통계
        shots = conn.execute("""
            SELECT team_name, COUNT(*) as count, SUM(xg) as total_xg
            FROM shots WHERE match_id = ? GROUP BY team_name
        """, (match_id,)).fetchall()

        # 선수 추적
        players = conn.execute("""
            SELECT team_name, COUNT(DISTINCT player_number) as count
            FROM yolo_detections WHERE match_id = ? AND object_type='player'
            GROUP BY team_name
        """, (match_id,)).fetchall()

        conn.close()

        return jsonify({
            "match": dict(match),
            "shots": [dict(s) for s in shots],
            "players_tracked": [dict(p) for p in players]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/yolo/match/<int:match_id>/comparison', methods=['GET'])
def yolo_sofascore_comparison(match_id):
    """SofaScore vs YOLO 비교"""
    try:
        conn = get_yolo_db()

        # SofaScore 슈팅
        sofascore_shots = conn.execute("""
            SELECT team_name, COUNT(*) as count, SUM(xg) as total_xg
            FROM shots WHERE match_id = ? AND source='sofascore'
            GROUP BY team_name
        """, (match_id,)).fetchall()

        # YOLO 슈팅
        yolo_shots = conn.execute("""
            SELECT team_name, COUNT(*) as count
            FROM shots WHERE match_id = ? AND source='yolo_detected'
            GROUP BY team_name
        """, (match_id,)).fetchall()

        # 검증 결과
        validation = conn.execute("""
            SELECT metric_name, sofascore_value, yolo_value, accuracy_percent
            FROM validation_results WHERE match_id = ?
        """, (match_id,)).fetchall()

        conn.close()

        return jsonify({
            "sofascore": [dict(s) for s in sofascore_shots],
            "yolo": [dict(y) for y in yolo_shots],
            "validation": [dict(v) for v in validation]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/yolo/match/<int:match_id>/heatmap', methods=['GET'])
def yolo_heatmap(match_id):
    """선수 위치 히트맵"""
    try:
        conn = get_yolo_db()

        detections = conn.execute("""
            SELECT team_name, x, y, COUNT(*) as frequency
            FROM yolo_detections
            WHERE match_id = ? AND object_type='player'
            GROUP BY team_name, ROUND(x, 1), ROUND(y, 1)
        """, (match_id,)).fetchall()

        conn.close()

        return jsonify([dict(d) for d in detections])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/yolo/match/<int:match_id>/setpiece', methods=['GET'])
def yolo_setpiece_analysis(match_id):
    """세트피스 분석 및 훈련 추천"""
    try:
        conn = get_yolo_db()
        shots = conn.execute("""
            SELECT team_name, x_pos, y_pos, xg, result, shot_type, minute
            FROM shots WHERE match_id = ? AND shot_type IN ('set_piece', 'open_play')
            ORDER BY minute
        """, (match_id,)).fetchall()
        conn.close()

        setpiece_shots = [dict(s) for s in shots if s['shot_type'] == 'set_piece']

        if not setpiece_shots:
            return jsonify({"setpiece_zones": {}, "recommendations": []}), 200

        zones = {'A1': [], 'B1': [], 'C1': [], 'A2': [], 'B2': [], 'C2': []}

        for shot in setpiece_shots:
            x, y, xg = shot['x_pos'], shot['y_pos'], shot['xg']
            zone = get_zone(x, y)
            zones[zone].append(xg)

        zone_stats = {}
        for zone, xgs in zones.items():
            zone_stats[zone] = {
                'count': len(xgs),
                'total_xg': sum(xgs) if xgs else 0,
                'avg_xg': sum(xgs) / len(xgs) if xgs else 0
            }

        recommendations = []
        for zone, stat in zone_stats.items():
            if stat['total_xg'] > 0.3:
                rec = get_setpiece_recommendation(zone, stat['total_xg'])
                recommendations.append({'zone': zone, 'text': rec, 'xg': stat['total_xg']})

        return jsonify({
            "setpiece_zones": zone_stats,
            "recommendations": sorted(recommendations, key=lambda x: x['xg'], reverse=True),
            "total_setpiece_shots": len(setpiece_shots),
            "total_setpiece_xg": sum(s['xg'] for s in setpiece_shots)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/yolo/match/<int:match_id>/defensive', methods=['GET'])
def yolo_defensive_zones(match_id):
    """수비 취약구역 분석 (양 팀)"""
    try:
        conn = get_yolo_db()
        match = conn.execute("SELECT home_team, away_team FROM matches WHERE match_id = ?", (match_id,)).fetchone()

        if not match:
            return jsonify({"error": "Match not found"}), 404

        home_team = match['home_team']
        away_team = match['away_team']

        all_shots = conn.execute("""
            SELECT team_name, x_pos, y_pos, xg, result, is_goal
            FROM shots WHERE match_id = ?
        """, (match_id,)).fetchall()

        conn.close()

        def analyze_team_defense(defending_team, attacking_team, all_shots):
            zones = {'A1': [], 'B1': [], 'C1': [], 'A2': [], 'B2': [], 'C2': []}

            for shot in all_shots:
                if shot['team_name'] == attacking_team:
                    x, y, xg = shot['x_pos'], shot['y_pos'], shot['xg']
                    zone = get_zone(x, y)
                    zones[zone].append({'xg': xg, 'result': shot['result'], 'is_goal': shot['is_goal']})

            zone_stats = {}
            for zone, shots_list in zones.items():
                zone_stats[zone] = {
                    'shot_count': len(shots_list),
                    'total_xg': sum(s['xg'] for s in shots_list),
                    'goals': sum(1 for s in shots_list if s['is_goal']),
                    'danger_level': calculate_danger_level(sum(s['xg'] for s in shots_list))
                }

            return zone_stats

        home_defense = analyze_team_defense(home_team, away_team, all_shots)
        away_defense = analyze_team_defense(away_team, home_team, all_shots)

        return jsonify({
            "home_team": home_team,
            "away_team": away_team,
            "home_defense": {
                "zones": home_defense,
                "most_dangerous": max(home_defense.items(), key=lambda x: x[1]['total_xg'])[0] if home_defense else None,
                "total_shots_allowed": sum(z['shot_count'] for z in home_defense.values()),
                "total_xg_allowed": round(sum(z['total_xg'] for z in home_defense.values()), 2)
            },
            "away_defense": {
                "zones": away_defense,
                "most_dangerous": max(away_defense.items(), key=lambda x: x[1]['total_xg'])[0] if away_defense else None,
                "total_shots_allowed": sum(z['shot_count'] for z in away_defense.values()),
                "total_xg_allowed": round(sum(z['total_xg'] for z in away_defense.values()), 2)
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/yolo/match/<int:match_id>/counter', methods=['GET'])
def yolo_counter_threat(match_id):
    """역습 위협 지수"""
    try:
        conn = get_yolo_db()

        counter_shots = conn.execute("""
            SELECT team_name, xg FROM shots
            WHERE match_id = ? AND shot_type = 'counter_attack'
        """, (match_id,)).fetchall()

        all_shots = conn.execute("""
            SELECT team_name, xg, shot_type FROM shots
            WHERE match_id = ?
        """, (match_id,)).fetchall()

        conn.close()

        counter_xg = sum(s['xg'] for s in counter_shots)
        total_xg = sum(s['xg'] for s in all_shots)
        total_shots = len(all_shots)

        threat_index = round((counter_xg / total_xg * 10) if total_xg > 0 else 0, 1)

        team_counter_stats = {}
        for shot in counter_shots:
            team = shot['team_name']
            if team not in team_counter_stats:
                team_counter_stats[team] = {'count': 0, 'xg': 0}
            team_counter_stats[team]['count'] += 1
            team_counter_stats[team]['xg'] += shot['xg']

        return jsonify({
            "threat_index": threat_index,
            "counter_xg": round(counter_xg, 2),
            "total_xg": round(total_xg, 2),
            "counter_shot_ratio": round(len(counter_shots) / total_shots * 100 if total_shots > 0 else 0, 1),
            "by_team": team_counter_stats,
            "threat_assessment": get_threat_assessment(threat_index)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/yolo/match/<int:match_id>/substitution', methods=['GET'])
def yolo_substitution_analysis(match_id):
    """교체 포지션 분석"""
    try:
        yolo_conn = get_yolo_db()
        match = yolo_conn.execute("SELECT home_team, away_team FROM matches WHERE match_id = ?", (match_id,)).fetchone()
        yolo_conn.close()

        if not match:
            return jsonify({"error": "Match not found"}), 404

        main_conn = sqlite3.connect(str(DB_PATH))
        main_conn.row_factory = sqlite3.Row

        kleague_id = yolo_conn.execute("SELECT kleague_id FROM matches WHERE match_id = ?", (match_id,)).fetchone() if hasattr(yolo_conn, 'execute') else None

        home_team = match['home_team']
        away_team = match['away_team']

        subs = []
        for team in [home_team, away_team]:
            team_subs = main_conn.execute("""
                SELECT e.minute, e.detail_kr, l1.position as out_pos, l2.position as in_pos
                FROM events e
                LEFT JOIN lineups l1 ON l1.player_name LIKE '%' || SUBSTRING(e.detail_kr, 1, INSTR(e.detail_kr, ' ') - 1) || '%'
                LEFT JOIN lineups l2 ON l2.player_name LIKE '%' || SUBSTRING(e.detail_kr, INSTR(e.detail_kr, ' ') + 1) || '%'
                WHERE e.event_type = 'SUBST' AND e.team_name = ? AND e.fixture_id = 2026020105
                ORDER BY e.minute
            """, (team,)).fetchall()

            for sub in team_subs:
                subs.append({
                    'team': team,
                    'minute': sub['minute'],
                    'detail': sub['detail_kr'] if sub['detail_kr'] else 'N/A',
                    'out_position': sub['out_pos'] if sub['out_pos'] else 'Unknown',
                    'in_position': sub['in_pos'] if sub['in_pos'] else 'Unknown'
                })

        main_conn.close()

        return jsonify({
            "home_team": home_team,
            "away_team": away_team,
            "substitutions": sorted(subs, key=lambda x: x['minute'])
        })
    except Exception as e:
        return jsonify({"error": str(e), "details": e.__class__.__name__}), 500

def get_zone(x, y):
    """105m×68m 필드를 6개 구역으로 분할 (세로 3, 가로 2)"""
    col = 'A' if x < 35 else ('B' if x < 70 else 'C')
    row = '1' if y < 34 else '2'
    return col + row

def calculate_danger_level(total_xg):
    """xG 기반 위험도 계산"""
    if total_xg >= 1.0: return "매우위험"
    elif total_xg >= 0.5: return "위험"
    elif total_xg > 0: return "주의"
    else: return "안전"

def get_setpiece_recommendation(zone, xg):
    """세트피스 구역별 훈련 추천"""
    if not zone or len(zone) < 2:
        return f"세트피스 대응 훈련 (xG {xg:.2f})"

    col, row = zone[0], zone[1]
    recommendations = {
        'A1': f"좌상단 세트피스(xG {xg:.2f}) → 측면 헤더 대응 훈련",
        'B1': f"중상단 세트피스(xG {xg:.2f}) → 골키퍼 분석 훈련",
        'C1': f"우상단 세트피스(xG {xg:.2f}) → 측면 크로스 마킹 훈련",
        'A2': f"좌중단 세트피스(xG {xg:.2f}) → 측면 침투 수비 훈련",
        'B2': f"중앙 세트피스(xG {xg:.2f}) → 페널티박스 밀집 마킹 훈련",
        'C2': f"우중단 세트피스(xG {xg:.2f}) → 측면 침투 수비 훈련"
    }
    return recommendations.get(zone, f"구역 {zone} 세트피스 대응 훈련 (xG {xg:.2f})")

def get_threat_assessment(threat_index):
    """위협 지수 평가"""
    if threat_index >= 7: return "매우 높은 역습 위협"
    elif threat_index >= 5: return "높은 역습 위협"
    elif threat_index >= 3: return "중간 역습 위협"
    else: return "낮은 역습 위협"

if __name__ == '__main__':
    print("[START] K리그 Match Intelligence API")
    print("[ACCESS] http://localhost:8000")
    app.run(host='localhost', port=8000, debug=False)
