# ChatGPT Task Scheduler MCP Server Specification

## Track

Challenge Track.

The original `PROMPT.md` was missing from the repository, so this MVP specification was rebuilt from `README.md` and the user-provided exercise description.

## Goal

Create a local task scheduler that exposes:

- A FastAPI browser UI and HTTP API for machines where `npx` is unavailable.
- An optional MCP stdio server for MCP-compatible clients.

## Non-Goals

- No paid API usage.
- No LLM-based natural language parsing.
- No recurring jobs.
- No distributed workers.
- No external queue in this MVP.
- No Node.js requirement for the main local demo.

## Browser UI

### `GET /`

Serves a production-style task scheduler workspace.

Behavior:

- Create a task with content and due time.
- View all, pending, completed, and due-now tasks.
- Complete pending tasks.
- Show summary metrics for pending, due, upcoming, and completed tasks.

## HTTP API

### `GET /health`

Returns `{ "status": "ok" }`.

### `GET /api/tasks`

Lists tasks. Optional query: `status=pending` or `status=completed`.

### `POST /api/tasks`

Creates a task.

### `GET /api/tasks/due`

Lists pending tasks whose due time is not in the future.

### `GET /api/tasks/{id}`

Gets one task.

### `POST /api/tasks/{id}/complete`

Marks one task as completed.

### `GET /api/summary`

Returns task counts for the UI.

## Tools

### `task.create`

Creates a scheduled task.

Input:

```json
{
  "content": "review PR #123",
  "due_at": "2026-06-01T09:00:00+08:00"
}
```

Output:

```json
{
  "id": 1,
  "content": "review PR #123",
  "due_at": "2026-06-01T01:00:00+00:00",
  "due_bucket": "202606010100",
  "status": "pending",
  "created_at": "2026-05-31T..."
}
```

### `task.list`

Lists scheduled tasks.

Input:

```json
{
  "status": "pending"
}
```

`status` is optional.

### `task.get`

Gets one task by id.

Input:

```json
{
  "id": 1
}
```

### `task.complete`

Marks one task completed.

Input:

```json
{
  "id": 1
}
```

## Data Model

SQLite table: `jobs`

| Column | Type | Meaning |
|---|---|---|
| `id` | INTEGER PRIMARY KEY | Internal task id |
| `content` | TEXT | Task content |
| `due_at` | TEXT | UTC ISO due time |
| `due_bucket` | TEXT | Minute-level bucket for scans |
| `status` | TEXT | `pending` or `completed` |
| `created_at` | TEXT | UTC ISO creation time |

## Design Decisions

- Use minute-level time buckets with format `YYYYMMDDHHMM`.
- Store due time as UTC ISO string.
- Keep scheduler data logic in `app/scheduler.py`.
- Use `TOOL_REGISTRY` in `app/mcp_server.py` instead of long if-else routing.

## Acceptance Criteria

- Browser UI runs without Node.js or `npx`.
- User can create and complete tasks from the browser.
- User can filter all/pending/completed/due-now tasks.
- MCP server lists four tools.
- `task.create` stores a pending task.
- `task.list` returns stored tasks.
- `task.get` returns one task or a clear error.
- `task.complete` changes status to `completed`.
- `find_due_jobs()` returns pending jobs whose due time is not in the future.
