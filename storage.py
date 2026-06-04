import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "match_intelligence.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS events (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                fixture_id   INTEGER,
                minute       INTEGER,
                extra_time   INTEGER,
                event_type   TEXT,
                detail_kr    TEXT,
                team_name    TEXT,
                player_name  TEXT,
                assist_name  TEXT,
                raw_type     TEXT,
                created_at   TEXT DEFAULT (datetime('now')),
                UNIQUE(fixture_id, minute, extra_time, event_type, player_name)
            );

            CREATE TABLE IF NOT EXISTS lineups (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                fixture_id     INTEGER,
                team_name      TEXT,
                formation      TEXT,
                player_name    TEXT,
                jersey_number  INTEGER,
                status         TEXT,
                position       TEXT,
                position_detail TEXT,
                created_at     TEXT DEFAULT (datetime('now')),
                UNIQUE(fixture_id, team_name, player_name)
            );

            CREATE TABLE IF NOT EXISTS player_stats (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                fixture_id  INTEGER,
                team_name   TEXT,
                player_name TEXT,
                stat_key    TEXT,
                value       TEXT,
                updated_at  TEXT DEFAULT (datetime('now')),
                UNIQUE(fixture_id, team_name, player_name, stat_key)
            );

            CREATE TABLE IF NOT EXISTS fixtures_full (
                fixture_id   INTEGER PRIMARY KEY,
                league_id    INTEGER,
                season       INTEGER,
                date         TEXT,
                status       TEXT,
                elapsed      INTEGER,
                home_team    TEXT,
                home_logo    TEXT,
                away_team    TEXT,
                away_logo    TEXT,
                home_score   INTEGER,
                away_score   INTEGER,
                updated_at   TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS match_parameters (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                fixture_id      INTEGER,
                team_name       TEXT,
                possession      REAL,
                fouls           INTEGER,
                shots           INTEGER,
                corners         INTEGER,
                press_intensity REAL,
                defensive_line  REAL,
                setpiece_focus  REAL,
                offside_trap    REAL,
                updated_at      TEXT DEFAULT (datetime('now')),
                UNIQUE(fixture_id, team_name)
            );
        """)


def insert_event(e: dict):
    with get_conn() as conn:
        conn.execute("""
            INSERT OR IGNORE INTO events
                (fixture_id, minute, extra_time, event_type, detail_kr, team_name, player_name, assist_name, raw_type)
            VALUES
                (:fixture_id, :minute, :extra_time, :event_type, :detail_kr, :team_name, :player_name, :assist_name, :raw_type)
        """, e)


def upsert_fixture_full(f: dict):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO fixtures_full
                (fixture_id, league_id, season, date, status, elapsed,
                 home_team, home_logo, away_team, away_logo, home_score, away_score)
            VALUES
                (:fixture_id, :league_id, :season, :date, :status, :elapsed,
                 :home_team, :home_logo, :away_team, :away_logo, :home_score, :away_score)
            ON CONFLICT(fixture_id) DO UPDATE SET
                status=excluded.status,
                home_score=excluded.home_score,
                away_score=excluded.away_score,
                updated_at=datetime('now')
        """, f)


def upsert_lineup(m: dict):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO lineups
                (fixture_id, team_name, formation, player_name, jersey_number,
                 status, position, position_detail)
            VALUES
                (:fixture_id, :team_name, :formation, :player_name, :jersey_number,
                 :status, :position, :position_detail)
            ON CONFLICT(fixture_id, team_name, player_name) DO UPDATE SET
                formation=excluded.formation,
                jersey_number=excluded.jersey_number,
                status=excluded.status,
                position=excluded.position,
                position_detail=excluded.position_detail
        """, m)


def upsert_player_stat(s: dict):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO player_stats (fixture_id, team_name, player_name, stat_key, value)
            VALUES (:fixture_id, :team_name, :player_name, :stat_key, :value)
            ON CONFLICT(fixture_id, team_name, player_name, stat_key) DO UPDATE SET
                value=excluded.value,
                updated_at=datetime('now')
        """, s)


def upsert_match_parameters(p: dict):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO match_parameters
                (fixture_id, team_name, possession, fouls, shots, corners,
                 press_intensity, defensive_line, setpiece_focus, offside_trap)
            VALUES
                (:fixture_id, :team_name, :possession, :fouls, :shots, :corners,
                 :press_intensity, :defensive_line, :setpiece_focus, :offside_trap)
            ON CONFLICT(fixture_id, team_name) DO UPDATE SET
                possession=excluded.possession,
                fouls=excluded.fouls,
                shots=excluded.shots,
                corners=excluded.corners,
                press_intensity=excluded.press_intensity,
                defensive_line=excluded.defensive_line,
                setpiece_focus=excluded.setpiece_focus,
                offside_trap=excluded.offside_trap,
                updated_at=datetime('now')
        """, p)


def get_fixtures_by_league(league_id: int, season: int) -> list[dict]:
    with get_conn() as conn:
        try:
            rows = conn.execute(
                "SELECT * FROM fixtures_full WHERE league_id=? AND season=?",
                (league_id, season)
            ).fetchall()
            return [dict(r) for r in rows]
        except Exception:
            return []


def get_fixture_lineups(fixture_id: int) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM lineups WHERE fixture_id=? ORDER BY team_name, status DESC, jersey_number",
            (fixture_id,)
        ).fetchall()
    return [dict(r) for r in rows]
