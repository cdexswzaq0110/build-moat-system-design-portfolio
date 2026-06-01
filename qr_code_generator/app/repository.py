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


def create_link(token: str, target_url: str, expires_at: Optional[str] = None) -> dict:
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO links (token, target_url, created_at, expires_at) VALUES (?, ?, ?, ?)",
            (token, target_url, utc_now_iso(), expires_at),
        )
        row = connection.execute("SELECT * FROM links WHERE token = ?", (token,)).fetchone()
    return dict(row)


def find_link(token: str) -> Optional[dict]:
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM links WHERE token = ?", (token,)).fetchone()
    return dict(row) if row else None


def is_expired(link: dict) -> bool:
    if not link.get("expires_at"):
        return False
    expires_at = datetime.fromisoformat(link["expires_at"])
    return expires_at <= datetime.now(timezone.utc)
