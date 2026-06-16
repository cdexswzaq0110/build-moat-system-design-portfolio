import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


DATABASE_PATH = Path(__file__).resolve().parent.parent / "qr_links.sqlite3"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_connection(database_path: Path = DATABASE_PATH) -> sqlite3.Connection:
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(database_path: Path = DATABASE_PATH) -> None:
    with get_connection(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS links (
                token TEXT PRIMARY KEY,
                target_url TEXT NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT
            )
            """
        )
        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(links)").fetchall()
        }
        if "updated_at" not in columns:
            connection.execute("ALTER TABLE links ADD COLUMN updated_at TEXT")
            connection.execute("UPDATE links SET updated_at = created_at WHERE updated_at IS NULL")
        if "is_deleted" not in columns:
            connection.execute("ALTER TABLE links ADD COLUMN is_deleted INTEGER NOT NULL DEFAULT 0")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS scan_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token TEXT NOT NULL,
                scanned_at TEXT NOT NULL,
                user_agent TEXT,
                ip_address TEXT
            )
            """
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_scan_events_token_scanned_at ON scan_events(token, scanned_at)"
        )


def create_link(token: str, target_url: str, expires_at: Optional[str] = None) -> dict:
    now = utc_now_iso()
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO links (token, target_url, created_at, updated_at, expires_at, is_deleted)
            VALUES (?, ?, ?, ?, ?, 0)
            """,
            (token, target_url, now, now, expires_at),
        )
        row = connection.execute("SELECT * FROM links WHERE token = ?", (token,)).fetchone()
    return dict(row)


def find_link(token: str) -> Optional[dict]:
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM links WHERE token = ?", (token,)).fetchone()
    return dict(row) if row else None


def update_link(token: str, target_url: Optional[str] = None, expires_at: Optional[str] = None) -> Optional[dict]:
    existing = find_link(token)
    if existing is None or existing.get("is_deleted"):
        return None

    next_url = target_url if target_url is not None else existing["target_url"]
    next_expires_at = expires_at if expires_at is not None else existing.get("expires_at")
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE links
            SET target_url = ?, expires_at = ?, updated_at = ?
            WHERE token = ?
            """,
            (next_url, next_expires_at, utc_now_iso(), token),
        )
        row = connection.execute("SELECT * FROM links WHERE token = ?", (token,)).fetchone()
    return dict(row) if row else None


def soft_delete_link(token: str) -> bool:
    existing = find_link(token)
    if existing is None or existing.get("is_deleted"):
        return False
    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE links SET is_deleted = 1, updated_at = ? WHERE token = ?",
            (utc_now_iso(), token),
        )
    return cursor.rowcount > 0


def record_scan(token: str, user_agent: Optional[str] = None, ip_address: Optional[str] = None) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO scan_events (token, scanned_at, user_agent, ip_address)
            VALUES (?, ?, ?, ?)
            """,
            (token, utc_now_iso(), user_agent, ip_address),
        )


def get_scan_analytics(token: str) -> dict:
    with get_connection() as connection:
        total = connection.execute(
            "SELECT COUNT(*) AS total FROM scan_events WHERE token = ?",
            (token,),
        ).fetchone()["total"]
        rows = connection.execute(
            """
            SELECT substr(scanned_at, 1, 10) AS date, COUNT(*) AS count
            FROM scan_events
            WHERE token = ?
            GROUP BY substr(scanned_at, 1, 10)
            ORDER BY date ASC
            """,
            (token,),
        ).fetchall()
    return {
        "token": token,
        "total_scans": total,
        "scans_by_day": [dict(row) for row in rows],
    }


def is_expired(link: dict) -> bool:
    if not link.get("expires_at"):
        return False
    expires_at = datetime.fromisoformat(link["expires_at"])
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    return expires_at <= datetime.now(timezone.utc)
