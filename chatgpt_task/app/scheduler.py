import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DATABASE_PATH = Path(__file__).resolve().parent.parent / "tasks.sqlite3"
BUCKET_FORMAT = "%Y%m%d%H%M"


def parse_iso_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def get_time_bucket(due_at: str | datetime) -> str:
    parsed = due_at if isinstance(due_at, datetime) else parse_iso_datetime(due_at)
    return parsed.astimezone(timezone.utc).strftime(BUCKET_FORMAT)


def get_connection(database_path: Path = DATABASE_PATH) -> sqlite3.Connection:
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(database_path: Path = DATABASE_PATH) -> None:
    with get_connection(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                due_at TEXT NOT NULL,
                due_bucket TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL
            )
            """
        )
        connection.execute("CREATE INDEX IF NOT EXISTS idx_jobs_due_bucket ON jobs(due_bucket, status)")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_job(content: str, due_at: str) -> dict[str, Any]:
    if not content.strip():
        raise ValueError("content is required")

    parsed_due_at = parse_iso_datetime(due_at)
    due_at_iso = parsed_due_at.isoformat()
    due_bucket = get_time_bucket(parsed_due_at)

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO jobs (content, due_at, due_bucket, status, created_at)
            VALUES (?, ?, ?, 'pending', ?)
            """,
            (content.strip(), due_at_iso, due_bucket, utc_now_iso()),
        )
        row = connection.execute("SELECT * FROM jobs WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return dict(row)


def list_jobs(status: str | None = None) -> list[dict[str, Any]]:
    query = "SELECT * FROM jobs"
    parameters: tuple[Any, ...] = ()
    if status:
        query += " WHERE status = ?"
        parameters = (status,)
    query += " ORDER BY due_at ASC"

    with get_connection() as connection:
        rows = connection.execute(query, parameters).fetchall()
    return [dict(row) for row in rows]


def get_job(job_id: int) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    return dict(row) if row else None


def complete_job(job_id: int) -> dict[str, Any] | None:
    with get_connection() as connection:
        connection.execute("UPDATE jobs SET status = 'completed' WHERE id = ?", (job_id,))
        row = connection.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    return dict(row) if row else None


def find_due_jobs(now: str | datetime | None = None) -> list[dict[str, Any]]:
    current = now or datetime.now(timezone.utc)
    current_datetime = current if isinstance(current, datetime) else parse_iso_datetime(current)
    current_bucket = get_time_bucket(current_datetime)

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM jobs
            WHERE status = 'pending'
              AND due_bucket <= ?
              AND due_at <= ?
            ORDER BY due_at ASC
            """,
            (current_bucket, current_datetime.isoformat()),
        ).fetchall()
    return [dict(row) for row in rows]
