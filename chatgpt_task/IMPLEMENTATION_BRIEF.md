# Implementation Brief

## Objective

Build a local task scheduler that can create, list, retrieve, and complete scheduled tasks. The primary interface is a FastAPI web application; MCP support is available as an optional integration path.

## MVP Scope

- Create a task with content and due time.
- Store task data in SQLite.
- Query tasks by status.
- Query tasks that are due.
- Complete a pending task.
- Provide a browser UI for local demonstration.

## API Surface

- `GET /health`
- `GET /api/tasks`
- `POST /api/tasks`
- `GET /api/tasks/due`
- `GET /api/tasks/{id}`
- `POST /api/tasks/{id}/complete`
- `GET /api/summary`

## Optional MCP Tools

- `task.create`
- `task.list`
- `task.get`
- `task.complete`

## Key Design Decisions

1. Watcher logic and job execution are separated conceptually so discovery remains testable.
2. A queue would be introduced before distributed execution to decouple due-job discovery from retries and worker concurrency.
3. Minute-level time buckets reduce scan cost as task volume grows.
4. Dotted tool names group operations by domain and make the interface easier to inspect.
5. Registry-based tool routing avoids long conditional chains as the tool set grows.

## Verification

```powershell
python -m pytest tests
```
