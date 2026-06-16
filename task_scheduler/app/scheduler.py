import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DATABASE_PATH = Path(
    os.getenv("TASK_SCHEDULER_DATABASE_PATH", Path(__file__).resolve().parent.parent / "tasks.sqlite3")
)
BUCKET_FORMAT = "%Y%m%d%H%M"
ALLOWED_PRIORITIES = {"low", "medium", "high"}


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
    database_path.parent.mkdir(parents=True, exist_ok=True)
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
        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(jobs)").fetchall()
        }
        if "priority" not in columns:
            connection.execute("ALTER TABLE jobs ADD COLUMN priority TEXT NOT NULL DEFAULT 'medium'")
        if "note" not in columns:
            connection.execute("ALTER TABLE jobs ADD COLUMN note TEXT NOT NULL DEFAULT ''")
        if "updated_at" not in columns:
            connection.execute("ALTER TABLE jobs ADD COLUMN updated_at TEXT")
            connection.execute("UPDATE jobs SET updated_at = created_at WHERE updated_at IS NULL")
        if "result" not in columns:
            connection.execute("ALTER TABLE jobs ADD COLUMN result TEXT")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_jobs_due_bucket ON jobs(due_bucket, status)")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_priority(priority: str) -> str:
    normalized = priority.strip().lower()
    if normalized not in ALLOWED_PRIORITIES:
        raise ValueError("priority must be low, medium, or high")
    return normalized


def create_job(content: str, due_at: str, priority: str = "medium", note: str = "") -> dict[str, Any]:
    if not content.strip():
        raise ValueError("content is required")

    parsed_due_at = parse_iso_datetime(due_at)
    due_at_iso = parsed_due_at.isoformat()
    due_bucket = get_time_bucket(parsed_due_at)
    normalized_priority = validate_priority(priority)

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO jobs (content, due_at, due_bucket, status, created_at, updated_at, priority, note)
            VALUES (?, ?, ?, 'pending', ?, ?, ?, ?)
            """,
            (content.strip(), due_at_iso, due_bucket, utc_now_iso(), utc_now_iso(), normalized_priority, note.strip()),
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
        connection.execute(
            "UPDATE jobs SET status = 'completed', updated_at = ? WHERE id = ?",
            (utc_now_iso(), job_id),
        )
        row = connection.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    return dict(row) if row else None


def update_job(
    job_id: int,
    content: str,
    due_at: str,
    priority: str = "medium",
    note: str = "",
) -> dict[str, Any] | None:
    if not content.strip():
        raise ValueError("content is required")

    parsed_due_at = parse_iso_datetime(due_at)
    due_at_iso = parsed_due_at.isoformat()
    due_bucket = get_time_bucket(parsed_due_at)
    normalized_priority = validate_priority(priority)

    with get_connection() as connection:
        existing = connection.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        if existing is None:
            return None
        connection.execute(
            """
            UPDATE jobs
            SET content = ?, due_at = ?, due_bucket = ?, priority = ?, note = ?,
                status = 'pending', result = NULL, updated_at = ?
            WHERE id = ?
            """,
            (content.strip(), due_at_iso, due_bucket, normalized_priority, note.strip(), utc_now_iso(), job_id),
        )
        row = connection.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    return dict(row) if row else None


def delete_job(job_id: int) -> bool:
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    return cursor.rowcount > 0


def cancel_job(job_id: int) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        if row is None:
            return None
        if row["status"] in {"completed", "failed"}:
            raise ValueError(f"Cannot cancel job in '{row['status']}' state")
        connection.execute(
            "UPDATE jobs SET status = 'cancelled', updated_at = ? WHERE id = ?",
            (utc_now_iso(), job_id),
        )
        updated = connection.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    return dict(updated) if updated else None


def enqueue_due_jobs(now: str | datetime | None = None) -> list[dict[str, Any]]:
    due_jobs = find_due_jobs(now)
    queued: list[dict[str, Any]] = []
    with get_connection() as connection:
        for job in due_jobs:
            connection.execute(
                "UPDATE jobs SET status = 'queued', updated_at = ? WHERE id = ? AND status = 'pending'",
                (utc_now_iso(), job["id"]),
            )
            row = connection.execute("SELECT * FROM jobs WHERE id = ?", (job["id"],)).fetchone()
            if row:
                queued.append(dict(row))
    return queued


def execute_queued_jobs() -> list[dict[str, Any]]:
    executed: list[dict[str, Any]] = []
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM jobs WHERE status = 'queued' ORDER BY due_at ASC"
        ).fetchall()
        for row in rows:
            connection.execute(
                "UPDATE jobs SET status = 'running', updated_at = ? WHERE id = ?",
                (utc_now_iso(), row["id"]),
            )
            result = f"Executed: {row['content']}"
            connection.execute(
                "UPDATE jobs SET status = 'completed', result = ?, updated_at = ? WHERE id = ?",
                (result, utc_now_iso(), row["id"]),
            )
            updated = connection.execute("SELECT * FROM jobs WHERE id = ?", (row["id"],)).fetchone()
            if updated:
                executed.append(dict(updated))
    return executed


def process_due_jobs(now: str | datetime | None = None) -> dict[str, list[dict[str, Any]]]:
    queued = enqueue_due_jobs(now)
    executed = execute_queued_jobs()
    return {"queued": queued, "executed": executed}


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
