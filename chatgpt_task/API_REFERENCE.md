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
  "due_at": "2026-06-01T09:00:00+08:00",
  "priority": "high",
  "note": "Check failing CI before review."
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
    "created_at": "2026-06-01T...",
    "priority": "high",
    "note": "Check failing CI before review."
  }
}
```

## `GET /api/tasks/due`

Returns pending jobs whose due time is not in the future.

## `POST /api/tasks/process-due`

Moves due pending tasks through the local queue lifecycle and completes them.
This is an explicit local worker trigger, so the MVP does not require a background daemon.

### Response `200`

```json
{
  "queued": [
    {
      "id": 1,
      "content": "review PR #123",
      "status": "queued"
    }
  ],
  "executed": [
    {
      "id": 1,
      "content": "review PR #123",
      "status": "completed",
      "result": "Executed: review PR #123"
    }
  ]
}
```

## `PATCH /api/tasks/{id}`

Request:

```json
{
  "content": "review PR #123",
  "due_at": "2026-06-01T10:00:00+08:00",
  "priority": "medium",
  "note": "Updated schedule."
}
```

Returns the updated task.

## `DELETE /api/tasks/{id}`

Deletes a task.

Response:

```json
{
  "status": "deleted",
  "id": 1
}
```

## `POST /api/tasks/{id}/complete`

Marks a task completed.

## `POST /api/tasks/{id}/cancel`

Cancels a pending, queued, or running task.

### Response `200`

```json
{
  "job": {
    "id": 1,
    "status": "cancelled"
  }
}
```

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
    },
    "priority": {
      "type": "string",
      "enum": ["low", "medium", "high"],
      "default": "medium"
    },
    "note": {
      "type": "string"
    }
  },
  "required": ["content", "due_at"]
}
```

### Example Input

```json
{
  "content": "review PR #123",
  "due_at": "2026-06-01T09:00:00+08:00",
  "priority": "high",
  "note": "Check failing CI before review."
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
  "created_at": "2026-06-01T...",
  "priority": "high",
  "note": "Check failing CI before review."
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
      "created_at": "2026-06-01T...",
      "priority": "high",
      "note": "Check failing CI before review."
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

## Tool: `task.cancel`

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

## Tool: `task.process_due`

### Input Schema

```json
{
  "type": "object",
  "properties": {}
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
| `status` | string | `pending`, `queued`, `running`, `completed`, `failed`, or `cancelled` |
| `created_at` | string | UTC ISO datetime |
| `updated_at` | string | UTC ISO datetime |
| `priority` | string | `low`, `medium`, or `high` |
| `note` | string | Optional task context |
| `result` | string or null | Execution result for processed tasks |
