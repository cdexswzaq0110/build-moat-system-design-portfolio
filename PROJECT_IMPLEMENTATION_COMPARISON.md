# Project Implementation Comparison

This document compares the current `build-moat-live-sessions-main` implementation with the reference project in `build-moat-live-sessions-main_A`.

## Summary

The reference project has higher engineering granularity. It is organized as workshop scaffolds and answer keys with clearer file boundaries such as `routes.py`, `schemas.py`, `database.py`, `models.py`, and dedicated frontend folders. The current project was more MVP-oriented: each app worked, but API contracts and route wiring were often kept directly in `main.py`.

This pass adopts the low-risk granularity improvements from the reference project without changing the existing primary APIs or replacing the current local-first runtime. Where the reference project had clearly higher product/API detail, this project now includes matching lightweight capabilities.

## High-Level Differences

| Area | Current project before this pass | Reference project A | Decision |
|---|---|---|---|
| API structure | Routes and schemas often lived in `main.py` | `routes.py` and `schemas.py` are separate | Adopted |
| Persistence abstraction | SQLite helper modules or direct functions | SQLAlchemy `database.py` + `models.py` | Deferred |
| Frontend | Inline FastAPI HTML for local demo/product UI | QR uses React/Vite; KB uses static HTML | Deferred |
| QR features | Create short link, QR PNG, redirect, expiration | Update, soft delete, cache, scan analytics | Adopted with SQLite helpers |
| Task scheduler | Local dashboard, CRUD-ish API, due bucket | MCP-first watcher/worker/queue model | Partially adopted with cancel/process-due flow |
| KB retrieval | Local keyword retrieval in one `retrieval.py` | Separate `indexer.py`, `routes.py`, `schemas.py`, BM25 metadata | Adopted local indexer/BM25-style ranking |

## Adopted Changes

### QR Code Generator

Reference A separates API contracts and routes:

```text
app/
  main.py
  routes.py
  schemas.py
```

Current project now follows the same API boundary:

```text
qr_code_generator/app/
  main.py       # FastAPI setup, startup, browser UI
  routes.py     # /health, /links, /api/qr/*, /qr/{token}.png, /r/{token}
  schemas.py    # create, update, info, status, analytics contracts
  repository.py # SQLite links, soft delete, scan events, analytics
```

Feature-level parity adopted from reference A:

- `POST /api/qr/create` as a product API alias.
- `GET /api/qr/{token}` for link metadata.
- `PATCH /api/qr/{token}` for updating destination URL or expiration.
- `DELETE /api/qr/{token}` for soft delete.
- `GET /api/qr/{token}/analytics` for total scans and scans by day.
- `GET /api/qr/{token}/check` for status checks.
- Redirect scan tracking through `scan_events`.

### Knowledge Base Q&A Bot

Reference A separates HTTP contracts from retrieval logic. Current project now has:

```text
knowledge_base_qa_bot/app/
  main.py       # FastAPI setup and browser UI
  routes.py     # /health, /metadata, /documents, /index, /chat
  schemas.py    # chat, source, index, document contracts
  indexer.py    # Markdown parsing, persisted index, BM25-style ranking
  retrieval.py  # compatibility facade plus answer extraction
```

Feature-level parity adopted from reference A:

- Dedicated indexer module instead of keeping all retrieval code in one file.
- Heading path metadata for better source context.
- Persisted `.kb/index.json` payload with sections and stats.
- `GET /documents` for indexed document/section inspection.
- Source snippets and `learning_focus` in chat responses.
- BM25-style local scoring with stopword filtering and heading boosts.

### ChatGPT Task Scheduler

Reference A separates MCP/API concepts and routing from app bootstrap. Current project now has:

```text
chatgpt_task/app/
  main.py       # FastAPI setup, lifespan, browser UI
  routes.py     # HTTP API routes
  schemas.py    # Pydantic request/response models
  scheduler.py  # persistence and scheduling domain logic
  mcp_server.py # optional MCP interface
  ui.py         # product dashboard HTML/CSS/JS
```

Feature-level parity adopted from reference A:

- Added task lifecycle fields: `updated_at` and `result`.
- Added `cancelled`, `queued`, and `running` lifecycle support in domain logic.
- Added `POST /api/tasks/process-due` to enqueue and execute due pending work.
- Added `POST /api/tasks/{id}/cancel`.
- Added MCP tools `task.cancel` and `task.process_due`.
- Kept existing `GET /api/tasks` and `POST /api/tasks` contracts intact.

## Still Deferred

These reference-project ideas are useful, but intentionally not moved in this pass:

- SQLAlchemy migration for all apps: higher blast radius than needed for the current MVP.
- React/Vite frontend for QR: current local FastAPI UI works and avoids Node dependency.
- Long-running background watcher process for task scheduling: useful production direction, but it changes runtime/deployment behavior.
- KB optional Groq/LangChain generation: current project explicitly avoids paid/external LLM requirements.

## Why This Scope

The goal was to raise implementation granularity where the reference project is clearly stronger while preserving:

- Existing API paths.
- Existing browser UIs.
- Existing tests.
- Local-first, no-paid-service behavior.
- Low setup cost.

The next safe phase would be production hardening: real migrations, auth, frontend screenshot capture, deployment packaging, and optional background workers.
