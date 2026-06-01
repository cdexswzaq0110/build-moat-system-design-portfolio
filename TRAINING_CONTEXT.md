# Training Context

This repository was implemented from the following Build Moat live-session training brief. The text is preserved to show the original assignment context and the design questions that guided the implementation.

## Prototype Template: QR Code Generator

Read `README.md` first and choose one track.

### Track Options

#### Challenge Track

- Build the architecture from scratch.
- Read `PROMPT.md` as the specification.
- Decide the file structure and implementation approach.
- Any language or framework is acceptable. Python + FastAPI is recommended.
- Best for practicing complete system design thinking.

#### Guided Track

- Use the provided `scaffold/` directory.
- File structure, routes, database, and schemas are already configured.
- Complete the three core functions marked as TODO.
- Python + FastAPI + SQLite.
- Best for understanding the overall architecture before implementing core logic.

Both tracks use the same curl-based API verification tests from the final section of `PROMPT.md`.

### Coding Agent Usage

Using Claude Code, Codex, or another coding agent is allowed, especially for the Challenge Track. The important part of the live session is the system design reasoning and tradeoff discussion.

### Live Session Preparation

`PROMPT.md` includes five Design Questions. The answers should be written before the live session for discussion.

## ChatGPT Task Scheduler MCP Server

Read `README.md` to choose a track, then read `PROMPT.md` for the requirements and Design Questions.

### Track Options

#### Challenge Track

- Build from scratch.
- Decide the architecture, file structure, and implementation approach.
- Python + the official MCP SDK is recommended, but any language with an MCP SDK is acceptable.
- Use `PROMPT.md` as the specification.

#### Guided Track

Complete four TODOs:

- `scheduler.py`: `get_time_bucket()`
- `scheduler.py`: `find_due_jobs()`
- `mcp_server.py`: `TOOL_REGISTRY`
- `mcp_server.py`: `route_tool_call()`

The goal is to focus on time bucket partitioning and registry-pattern routing.

### Verification

Primary intended verification in the original brief:

```powershell
npx @modelcontextprotocol/inspector python -m app.mcp_server
```

The implementation in this repository also provides a FastAPI web UI because `npx` may be unavailable in local environments.

### Design Questions

1. Watcher vs Cron: why should they be separate?
2. Why place a queue between Watcher and Worker?
3. Time bucket partitioning: what happens without partitioning?
4. `task.create` vs `createTask`: does naming matter for tool selection?
5. Registry vs if-else: what happens when the system grows to 20 tools?

## Knowledge Base Q&A Bot

The theme is answering questions from a knowledge base.

The original exercise includes two retrieval directions:

### Markdown KB

Inspired by Andrej Karpathy's LLM Wiki pattern:

- Markdown files
- Explicit index
- Agent-readable knowledge base

Reference: <https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>

### Vector RAG

Traditional retrieval-augmented generation:

- Markdown chunks
- Embeddings
- FAISS vector search
- Retrieved context
- LLM answer

This repository uses the no-paid-API Markdown KB path.

### Design Focus

The exercise is not only about returning an answer. The key tradeoffs are:

1. Should the retrieval unit be file, section, or chunk?
2. How should the index be stored?
3. What context should be passed into an answer step?
4. How should the answer cite sources?
5. How should weak retrieval results be handled?
6. When is Markdown KB better than Vector RAG?
7. When is Vector RAG better than Markdown KB?

## Vibe Engineering Sprint Mapping

| Station | Skill | Output |
|---|---|---|
| 1 | `/spec-it` | PRD, API, BDD |
| 2 | `/adr` | ADR-0001 backend framework decision |
| 3 | `/plan-sprint` | `sprint-1.md` |
| 4 | `/tdd-cycle` | code plus passing tests |
| 5 | `/verify` | five-dimension verification |
| 6 | `/sync-it` | code and documentation alignment |
| 7 | `/commit-msg` | Conventional Commit message |
| 8 | deployment | local demo URL |
| 9 | `/retro` | 4Ls retrospective |
| cross | `/explain-code` | architecture-level explanation |
| cross | `/check-key` | API key leak check |

## Repository Adaptations

- The public README is written as a portfolio entry.
- The original training context is preserved in this file.
- Runtime artifacts are excluded from Git.
- The task scheduler uses a FastAPI web UI as the primary demo path because `npx` is not reliable in the target environment.
- The knowledge base project avoids paid APIs and uses local Markdown retrieval.
