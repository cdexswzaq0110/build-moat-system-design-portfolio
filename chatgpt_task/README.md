# ChatGPT Task Scheduler

ChatGPT Task Scheduler is a local task scheduling prototype. It provides a FastAPI browser interface and HTTP API for creating scheduled tasks, filtering task states, finding due tasks, and marking tasks as complete. An MCP server is included as an optional integration path for MCP-compatible clients.

The primary demo does not require Node.js, `npx`, OpenAI API keys, or paid services.

## Features

- Create scheduled tasks with due timestamps.
- List all, pending, completed, and due-now tasks.
- Complete pending tasks from the browser UI.
- Store tasks in local SQLite.
- Expose HTTP endpoints for automation.
- Optionally expose MCP tools: `task.create`, `task.list`, `task.get`, and `task.complete`.

## Run Locally

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8003
```

Open:

```text
http://127.0.0.1:8003
```

## API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/api/tasks` | List tasks |
| `POST` | `/api/tasks` | Create a task |
| `GET` | `/api/tasks/due` | List due tasks |
| `GET` | `/api/tasks/{id}` | Get one task |
| `POST` | `/api/tasks/{id}/complete` | Complete one task |
| `GET` | `/api/summary` | Return dashboard counts |

See [API_REFERENCE.md](API_REFERENCE.md) for request and response details.

## Optional MCP Inspector

Use this path only when Node.js and `npx` are available:

```powershell
python -m pip install -r requirements-mcp.txt
npx @modelcontextprotocol/inspector python -m app.mcp_server
```

## Test

```powershell
python -m pytest tests
```

## Documentation

- [PRODUCT_REQUIREMENTS.md](PRODUCT_REQUIREMENTS.md)
- [IMPLEMENTATION_BRIEF.md](IMPLEMENTATION_BRIEF.md)
- [SPEC.md](SPEC.md)
- [API_REFERENCE.md](API_REFERENCE.md)
- [ACCEPTANCE_TESTS.md](ACCEPTANCE_TESTS.md)
- [ARCHITECTURE_NOTES.md](ARCHITECTURE_NOTES.md)
- [RUNBOOK.md](RUNBOOK.md)
