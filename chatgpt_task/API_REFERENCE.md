# ChatGPT Task Scheduler API And MCP Contract

## HTTP Base URL

```text
http://127.0.0.1:8003
```

## Browser UI

### `GET /`

Returns the local product UI.

## `GET /health`

Response:

```json
{
  "status": "ok"
}
```

## `GET /api/tasks`

Optional query:

```text
?status=pending
```

Response:

```json
{
  "jobs": []
}
```

## `POST /api/tasks`

Request:

```json
{
  "content": "review PR #123",
  "due_at": "2026-06-01T09:00:00+08:00"
}
```

Response:

```json
{
  "job": {
    "id": 1,
    "content": "review PR #123",
    "due_at": "2026-06-01T01:00:00+00:00",
    "due_bucket": "202606010100",
    "status": "pending",
    "created_at": "2026-06-01T..."
  }
}
```

## `GET /api/tasks/due`

Returns pending jobs whose due time is not in the future.

## `POST /api/tasks/{id}/complete`

Marks a task completed.

## `GET /api/summary`

Response:

```json
{
  "total": 1,
  "pending": 1,
  "completed": 0,
  "due": 0,
  "upcoming": 1
}
```

## Transport

Optional MCP stdio server.

Run:

```powershell
npx @modelcontextprotocol/inspector python -m app.mcp_server
```

## Tool: `task.create`

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "content": {
      "type": "string"
    },
    "due_at": {
      "type": "string",
      "description": "ISO datetime"
    }
  },
  "required": ["content", "due_at"]
}
```

### Example Input

```json
{
  "content": "review PR #123",
  "due_at": "2026-06-01T09:00:00+08:00"
}
```

### Example Output

```json
{
  "id": 1,
  "content": "review PR #123",
  "due_at": "2026-06-01T01:00:00+00:00",
  "due_bucket": "202606010100",
  "status": "pending",
  "created_at": "2026-06-01T..."
}
```

## Tool: `task.list`

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string"
    }
  }
}
```

### Example Input

```json
{
  "status": "pending"
}
```

### Example Output

```json
{
  "jobs": [
    {
      "id": 1,
      "content": "review PR #123",
      "due_at": "2026-06-01T01:00:00+00:00",
      "due_bucket": "202606010100",
      "status": "pending",
      "created_at": "2026-06-01T..."
    }
  ]
}
```

## Tool: `task.get`

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer"
    }
  },
  "required": ["id"]
}
```

## Tool: `task.complete`

### Input Schema

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer"
    }
  },
  "required": ["id"]
}
```

## Error Behavior

| Case | Behavior |
|---|---|
| Unknown tool | Raises `Unknown tool: {name}` |
| Missing job | Raises `job not found` |
| Empty content | Raises `content is required` |

## Data Contract

| Field | Type | Notes |
|---|---|---|
| `id` | integer | SQLite primary key |
| `content` | string | Task body |
| `due_at` | string | UTC ISO datetime |
| `due_bucket` | string | `YYYYMMDDHHMM` |
| `status` | string | `pending` or `completed` |
| `created_at` | string | UTC ISO datetime |
