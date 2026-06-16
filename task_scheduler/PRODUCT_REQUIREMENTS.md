# Task Scheduler PRD

## Problem

Independent builders need a focused way to create, schedule, track, and complete time-based tasks without setting up a full project-management system.

## Target User

- Independent developer managing focused work.
- Student planning project deadlines.
- Freelancer tracking client tasks and due times.
- Developer who wants an optional local automation API.

## Goals

1. Expose a polished browser dashboard and HTTP API.
2. Persist tasks locally with SQLite.
3. Support due-time bucket scanning logic.
4. Support create, list, get, update, complete, cancel, and process-due workflows.
5. Run without paid services or external accounts.

## Non-Goals

- Natural-language due-date parsing.
- Real notifications.
- Recurring tasks.
- Queue/worker implementation.
- Hosted deployment.
- Node.js requirement for the main demo.

## MVP User Stories

### Story 0: Use Without npx

As a user, I want a browser dashboard so that I can create, review, and complete scheduled tasks quickly.

Acceptance:

- Running `python -m uvicorn app.main:app --reload --port 8003` starts the product UI.
- The UI can create, list, filter, and complete tasks.
- The UI shows due-now and summary counts.

### Story 1: Create Task

As an automation client, I want to call `task.create` so that I can store a scheduled task.

Acceptance:

- Input includes `content` and `due_at`.
- Output includes `id`, `content`, `due_at`, `due_bucket`, and `status`.
- Status starts as `pending`.

### Story 2: List Tasks

As an automation client, I want to call `task.list` so that I can inspect stored tasks.

Acceptance:

- Tool returns all jobs by default.
- Optional `status` filter returns matching jobs.

### Story 3: Get Task

As an automation client, I want to call `task.get` so that I can inspect a specific task.

Acceptance:

- Existing id returns the task.
- Missing id returns a clear error.

### Story 4: Complete Task

As an automation client, I want to call `task.complete` so that I can mark work finished.

Acceptance:

- Existing task status becomes `completed`.
- Missing task returns a clear error.

## Success Metrics

- Browser UI can create and complete a task.
- HTTP API smoke tests pass.
- Optional automation interface can load when Node.js is available.
- Task tools are listed when the optional automation interface is used.
- Core tests pass.
- No paid service key is required.

## Risks

- Global Python dependency conflicts can happen if this project shares one environment with FastAPI projects.
- No worker loop means due tasks are discoverable but not automatically executed.

## Future Improvements

- Watcher process.
- Durable queue.
- Worker execution.
- Recurring schedules.
- Automation resources and prompts.
