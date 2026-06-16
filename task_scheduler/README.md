# Task Scheduler

Task Scheduler is a local task scheduling prototype with a product-style SaaS dashboard. It provides a FastAPI browser interface and HTTP API for creating scheduled tasks, filtering task states, finding due tasks, editing schedules, deleting tasks, and marking tasks as complete. An MCP server is included as an optional integration path for MCP-compatible clients.

The primary demo does not require Node.js, `npx`, external service keys, or paid services.

## Features

- Create scheduled tasks with due timestamps.
- Assign low, medium, or high priority and optional task notes.
- Edit and delete scheduled tasks from the dashboard.
- List all, pending, completed, and due-now tasks.
- Complete pending tasks from the browser UI.
- Cancel pending, queued, or running tasks.
- Process due tasks through an explicit queued/running/completed lifecycle.
- Store tasks in local SQLite.
- Expose HTTP endpoints for automation.
- Optionally expose MCP tools: `task.create`, `task.list`, `task.get`, `task.complete`, `task.cancel`, and `task.process_due`.

## Product UI

The browser UI is structured as a SaaS web app dashboard instead of a landing page or debug screen:

- Left sidebar navigation for Dashboard, Today, Upcoming, Completed, and Developer links.
- Top action bar with global task search, Quick Add Task, workspace status, and avatar.
- Compact dashboard header focused on today's work instead of a marketing hero.
- Quick Add workflow with title, due time, priority, optional note, validation, loading, and toast states.
- Productized task workspace with search, filter tabs, sort controls, grouped task sections, quick actions, and status badges.
- Actionable Today Overview with next due task, overdue count, completion rate, small timeline, and suggested focus.
- Completed items are visually quieter; overdue items are clear without being visually harsh.
- Developer links are moved into a collapsed sidebar panel so they do not interrupt normal users.
- CSS variables define design tokens for colors, spacing, typography, radius, shadow, buttons, cards, badges, and form states.
- Responsive layout supports desktop app shell, tablet content stacking, and mobile single-column usage.

## Run Locally

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8003
```

Open:

```text
http://127.0.0.1:8003
```

Optional database path override:

```powershell
$env:TASK_SCHEDULER_DATABASE_PATH="C:\path\to\tasks.sqlite3"
python -m uvicorn app.main:app --reload --port 8003
```

## API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/api/tasks` | List tasks |
| `POST` | `/api/tasks` | Create a task |
| `GET` | `/api/tasks/due` | List due tasks |
| `POST` | `/api/tasks/process-due` | Queue and execute due tasks |
| `GET` | `/api/tasks/{id}` | Get one task |
| `PATCH` | `/api/tasks/{id}` | Update one task |
| `DELETE` | `/api/tasks/{id}` | Delete one task |
| `POST` | `/api/tasks/{id}/complete` | Complete one task |
| `POST` | `/api/tasks/{id}/cancel` | Cancel one task |
| `GET` | `/api/summary` | Return dashboard counts |

See [API_REFERENCE.md](API_REFERENCE.md) for request and response details.

## Screenshots

Add current screenshots here after running the app locally:

```text
docs/screenshots/task-scheduler-dashboard.png
docs/screenshots/task-scheduler-mobile.png
```

## Optional developer inspector

Use this path only when Node.js and `npx` are available:

```powershell
python -m pip install -r requirements-mcp.txt
npx @modelcontextprotocol/inspector python -m app.mcp_server
```

## Test

```powershell
python -m pytest tests
```

Expected result:

```text
10 passed
```

## Documentation

- [PRODUCT_REQUIREMENTS.md](PRODUCT_REQUIREMENTS.md)
- [IMPLEMENTATION_BRIEF.md](IMPLEMENTATION_BRIEF.md)
- [SPEC.md](SPEC.md)
- [API_REFERENCE.md](API_REFERENCE.md)
- [ACCEPTANCE_TESTS.md](ACCEPTANCE_TESTS.md)
- [ARCHITECTURE_NOTES.md](ARCHITECTURE_NOTES.md)
- [RUNBOOK.md](RUNBOOK.md)
