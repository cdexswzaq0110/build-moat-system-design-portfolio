# ChatGPT Task Scheduler MCP Server PRD

## Problem

LLM clients need a structured way to create and manage scheduled tasks through MCP tools instead of relying on free-form text.

## Target User

- Workshop participant learning MCP.
- Developer testing MCP Inspector.
- Agent builder exploring tool naming and registry routing.

## Goals

1. Expose a local browser UI and HTTP API that work without `npx`.
2. Keep the MCP stdio server available as an optional interface.
3. Provide four task tools.
3. Persist tasks locally with SQLite.
4. Support due-time bucket scanning logic.
5. Run without paid APIs.

## Non-Goals

- Natural language parsing through paid LLM APIs.
- Real notifications.
- Recurring tasks.
- Queue/worker implementation.
- Hosted deployment.
- Node.js requirement for the main demo.

## MVP User Stories

### Story 0: Use Without npx

As a learner whose machine cannot run `npx`, I want a browser UI so that I can still verify and demo the scheduler.

Acceptance:

- Running `python -m uvicorn app.main:app --reload --port 8003` starts the product UI.
- The UI can create, list, filter, and complete tasks.
- The UI shows due-now and summary counts.

### Story 1: Create Task

As an MCP client, I want to call `task.create` so that I can store a scheduled task.

Acceptance:

- Input includes `content` and `due_at`.
- Output includes `id`, `content`, `due_at`, `due_bucket`, and `status`.
- Status starts as `pending`.

### Story 2: List Tasks

As an MCP client, I want to call `task.list` so that I can inspect stored tasks.

Acceptance:

- Tool returns all jobs by default.
- Optional `status` filter returns matching jobs.

### Story 3: Get Task

As an MCP client, I want to call `task.get` so that I can inspect a specific task.

Acceptance:

- Existing id returns the task.
- Missing id returns a clear error.

### Story 4: Complete Task

As an MCP client, I want to call `task.complete` so that I can mark work finished.

Acceptance:

- Existing task status becomes `completed`.
- Missing task returns a clear error.

## Success Metrics

- Browser UI can create and complete a task.
- HTTP API smoke tests pass.
- Optional MCP Inspector can load the server when Node.js is available.
- Four MCP tools are listed when optional MCP is used.
- Core tests pass.
- No paid API key is required.

## Risks

- Global Python dependency conflicts can happen if this project shares one environment with FastAPI projects.
- No worker loop means due tasks are discoverable but not automatically executed.

## Future Improvements

- Watcher process.
- Durable queue.
- Worker execution.
- Recurring schedules.
- MCP resources and prompts.
