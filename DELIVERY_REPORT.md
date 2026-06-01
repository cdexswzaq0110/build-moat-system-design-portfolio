# Delivery Report

## Scope

This repository contains three local-first system design prototypes:

- QR Code Generator
- Knowledge Base Q&A Bot
- ChatGPT Task Scheduler

The implementation emphasizes clear API contracts, simple local operations, testable architecture, and product-oriented browser interfaces.

## Delivery Summary

| Area | Output |
|---|---|
| Product definition | `PRODUCT_REQUIREMENTS.md` in each project |
| API contract | `API_REFERENCE.md` in each project |
| Acceptance criteria | `ACCEPTANCE_TESTS.md` in each project |
| Architecture | `SPEC.md`, `ARCHITECTURE_NOTES.md`, and ADR files |
| Implementation | `app/` source code |
| Verification | `tests/` and `docs/verification.md` |
| Operation | `RUNBOOK.md` in each project |

## Technical Constraints

- Python and FastAPI are used for the executable prototypes.
- SQLite is used for local persistence where persistence is required.
- The knowledge base implementation uses local Markdown retrieval.
- Paid APIs are not used.
- MCP Inspector support in `chatgpt_task` is optional; the primary demo path is the FastAPI web application.

## Local Demo URLs

| Project | URL |
|---|---|
| QR Code Generator | `http://127.0.0.1:8001` |
| Knowledge Base Q&A Bot | `http://127.0.0.1:8002` |
| ChatGPT Task Scheduler | `http://127.0.0.1:8003` |

## Verification Summary

Run the test suite inside each project:

```powershell
python -m pytest tests
```

Runtime files such as SQLite databases, generated retrieval indexes, Python bytecode, and local environment files are intentionally excluded from version control.
