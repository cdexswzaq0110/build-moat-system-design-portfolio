# ChatGPT Task Scheduler Design Questions

## Context

This project uses the Challenge Track because the scaffold files and original `PROMPT.md` were missing. The MVP was rebuilt from the README and the user's exercise description.

## 1. Watcher vs Cron: why separate them?

### Decision

Keep watcher logic separate from cron-like scheduling.

### Why

Cron answers "when should the system wake up?" Watcher answers "which app-owned jobs are due?" These are different responsibilities. If they are mixed, infrastructure timing and application state become tangled.

### Alternatives

- Use only cron: simple, but cron cannot easily understand app-level retry state, job ownership, or custom filtering.
- Use only a long-running loop: easy in local dev, but less reliable without process supervision.

### Trade-off

Separating watcher and cron adds one conceptual boundary, but it keeps the data flow testable.

### Production Direction

Use cron or a scheduler to trigger the watcher every minute. The watcher scans due jobs and enqueues work.

## 2. Why put a queue between Watcher and Worker?

### Decision

The MVP does not implement a queue, but the design expects one between due-job discovery and execution.

### Why

Watcher should find due jobs. Worker should execute them. A queue lets workers retry, scale, and fail independently from the watcher.

### Alternatives

- Watcher directly executes jobs: simplest, but one slow job blocks scanning.
- Worker scans the DB itself: duplicates watcher logic and increases database load.

### Trade-off

A queue adds infrastructure. For MVP, it is documented but not implemented.

### Production Direction

Use Redis, SQS, or another durable queue. Store idempotency keys so duplicate deliveries do not execute the same task twice.

## 3. Time bucket partitioning: what happens without it?

### Decision

Store a minute-level `due_bucket` next to the exact `due_at`.

### Why

Without a bucket/index strategy, the watcher risks scanning all pending jobs every time. As job count grows, that becomes a full table scan problem.

### Alternatives

- Index only `due_at`: acceptable for many systems, but buckets make the partitioning concept explicit for this exercise.
- Partition by day/hour: fewer partitions, but less precise scans.

### Trade-off

The bucket duplicates information from `due_at`. That duplication is intentional because it supports simpler scanning and indexing.

### Production Direction

Keep both `due_at` and bucket fields. Add composite indexes by `(status, due_bucket)` and possibly shard/partition by bucket for large scale.

## 4. `task.create` vs `createTask`: does naming matter to LLMs?

### Decision

Use dotted tool names such as `task.create`, `task.list`, `task.get`, and `task.complete`.

### Why

Dotted names group tools by domain. LLMs and humans can see that all task operations belong together. This reduces ambiguity when many tools exist.

### Alternatives

- `createTask`: familiar camelCase, but less visually grouped.
- `create_task`: Pythonic, but still weaker as a tool namespace.
- Natural language names: readable, but harder to route consistently.

### Trade-off

Dotted names are slightly less common in normal Python APIs, but they work well as MCP tool identifiers.

### Production Direction

Keep `{domain}.{verb}` naming for all MCP tools, for example `calendar.create`, `calendar.list`, `notification.send`.

## 5. Registry vs if-else: what happens at tool 20?

### Decision

Use `TOOL_REGISTRY` mapping tool names to handlers.

### Why

With if-else routing, adding tools grows branching logic and increases accidental fallthrough or inconsistent validation. A registry keeps routing data-driven.

### Alternatives

- if-else chain: fine for two tools, poor for twenty.
- Decorator-based registration: elegant, but extra abstraction for MVP.
- Class-based command objects: powerful, but too heavy here.

### Trade-off

The registry requires handlers to share a common calling convention. That is acceptable because MCP tool calls all receive a name and arguments.

### Production Direction

Add per-tool schema, permissions, observability labels, and structured error mapping to the registry.

## 6. What if `npx` is unavailable?

### Decision

Make MCP Inspector optional and provide a FastAPI browser UI plus HTTP API as the primary local demo path.

### Why

The learning goal is scheduler design, not debugging Node.js availability. If `npx` fails, the user still needs a reliable way to create tasks, inspect due jobs, and verify the data model.

### Alternatives

- Require Node.js: faithful to MCP Inspector, but blocks users with broken npm/npx setups.
- Use only CLI scripts: reliable, but weak product experience.
- Build a browser UI: slightly more code, but easiest to demo and inspect.

### Trade-off

The web UI is not MCP itself. It verifies the same scheduler core and data model, while MCP remains available for clients that can run it.

### Production Direction

Keep multiple interfaces over the same domain layer: web UI, HTTP API, MCP tools, and watcher/worker processes.

## 7. What should the product UI emphasize?

### Decision

Use a three-panel task workspace: create task, scheduled work list, and summary/API status.

### Why

Professional task products such as Todoist, Asana, and Microsoft To Do emphasize fast capture, due-date visibility, list filtering, and completion flow. This prototype adopts those patterns without adding unnecessary project-management complexity.

### Alternatives

- Chat-only interface: natural, but weak for scanning multiple tasks.
- Calendar-only interface: useful for scheduling, but too heavy for MVP.
- Table-only interface: efficient, but less polished for a product demo.

### Trade-off

The MVP does not implement drag-and-drop calendar scheduling. It focuses on capture, due status, filtering, and completion.

### Production Direction

Add calendar view, reminders, recurrence, labels, priorities, and natural-language due-date parsing.
