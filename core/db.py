from contextlib import closing
import sqlite3
import os
from typing import Optional

DB_PATH = "agent_state.db"


def init_db() -> None:
    """Initializes the SQLite database and creates the settings table."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS settings (
                            key TEXT PRIMARY KEY,
                            value TEXT
                         )""")
            c.execute("""CREATE TABLE IF NOT EXISTS post_logs (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                            target_room TEXT,
                            payload TEXT,
                            status TEXT,
                            response TEXT
                         )""")
            conn.commit()



def get_db_connection():
    if not os.path.exists(DB_PATH):
        init_db()
    
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("SELECT 1 FROM settings LIMIT 1")
    except sqlite3.OperationalError:
        init_db()
    return conn

def log_post(target_room: str, payload: str, status: str, response: str) -> None:
    """Logs a post attempt to the database."""
    with closing(get_db_connection()) as conn:
        with conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO post_logs (target_room, payload, status, response) VALUES (?, ?, ?, ?)",
                (target_room, payload, status, response),
            )
            conn.commit()


def get_post_logs(limit: int = 10) -> list:
    """Retrieves the most recent post logs."""
    with closing(get_db_connection()) as conn:
        with conn:
            c = conn.cursor()
            c.execute(
                "SELECT timestamp, target_room, status, response, payload FROM post_logs ORDER BY timestamp DESC LIMIT ?",
                (limit,),
            )
            return c.fetchall()


def set_setting(key: str, value: str) -> None:
    """Stores a key-value pair in the database."""
    with closing(get_db_connection()) as conn:
        with conn:
            c = conn.cursor()
            c.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value)
            )
            conn.commit()


def get_setting(key: str) -> Optional[str]:
    """Retrieves a value for a given key from the database."""
    with closing(get_db_connection()) as conn:
        with conn:
            c = conn.cursor()
            c.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = c.fetchone()
            return row[0] if row else None


def get_dashboard_stats() -> dict:
    """Calculates true dashboard metrics from the database."""
    with closing(get_db_connection()) as conn:
        with conn:
            c = conn.cursor()

            # Total Executions
            c.execute("SELECT COUNT(*) FROM post_logs")
            total_executions = c.fetchone()[0]

            # 24h Stats
            c.execute(
                "SELECT COUNT(*) FROM post_logs WHERE timestamp >= datetime('now', '-1 day')"
            )
            total_24h = c.fetchone()[0]

            c.execute(
                "SELECT COUNT(*) FROM post_logs WHERE timestamp >= datetime('now', '-1 day') AND status = 'Success'"
            )
            success_24h = c.fetchone()[0]

            success_rate = 100
            if total_24h > 0:
                success_rate = int((success_24h / total_24h) * 100)

            # Last Active
            c.execute("SELECT timestamp FROM post_logs ORDER BY timestamp DESC LIMIT 1")
            last_active_row = c.fetchone()
            last_active = last_active_row[0] if last_active_row else None

            return {
                "total_executions": total_executions,
                "success_rate_24h": success_rate,
                "last_active": last_active,
            }
