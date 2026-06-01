from datetime import datetime, timezone

from app.mcp_server import TOOL_REGISTRY, route_tool_call
from app.scheduler import get_time_bucket, parse_iso_datetime


def test_get_time_bucket_uses_utc_minute() -> None:
    due_at = datetime(2026, 5, 31, 9, 7, 30, tzinfo=timezone.utc)

    assert get_time_bucket(due_at) == "202605310907"


def test_parse_iso_datetime_accepts_z_suffix() -> None:
    parsed = parse_iso_datetime("2026-05-31T09:00:00Z")

    assert parsed.tzinfo is not None
    assert parsed.hour == 9


def test_tool_registry_contains_expected_tools() -> None:
    assert set(TOOL_REGISTRY) == {"task.create", "task.list", "task.get", "task.complete"}


def test_route_tool_call_rejects_unknown_tool() -> None:
    try:
        route_tool_call("task.missing", {})
    except ValueError as error:
        assert "Unknown tool" in str(error)
    else:
        raise AssertionError("Expected ValueError")
