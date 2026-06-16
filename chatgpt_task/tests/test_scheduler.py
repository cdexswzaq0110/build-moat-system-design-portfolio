from datetime import datetime, timezone

from app.mcp_server import TOOL_REGISTRY, route_tool_call
from app.scheduler import create_job, get_time_bucket, initialize_database, parse_iso_datetime, process_due_jobs


def test_get_time_bucket_uses_utc_minute() -> None:
    due_at = datetime(2026, 5, 31, 9, 7, 30, tzinfo=timezone.utc)

    assert get_time_bucket(due_at) == "202605310907"


def test_parse_iso_datetime_accepts_z_suffix() -> None:
    parsed = parse_iso_datetime("2026-05-31T09:00:00Z")

    assert parsed.tzinfo is not None
    assert parsed.hour == 9


def test_tool_registry_contains_expected_tools() -> None:
    assert set(TOOL_REGISTRY) == {
        "task.create",
        "task.list",
        "task.get",
        "task.complete",
        "task.cancel",
        "task.process_due",
    }


def test_route_tool_call_rejects_unknown_tool() -> None:
    try:
        route_tool_call("task.missing", {})
    except ValueError as error:
        assert "Unknown tool" in str(error)
    else:
        raise AssertionError("Expected ValueError")


def test_process_due_jobs_executes_due_task() -> None:
    initialize_database()
    job = create_job("run due task", "2026-05-31T09:00:00Z")

    result = process_due_jobs("2026-05-31T09:01:00Z")

    executed_ids = {item["id"] for item in result["executed"]}
    assert job["id"] in executed_ids
