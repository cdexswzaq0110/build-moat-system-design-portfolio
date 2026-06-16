# System Design Portfolio

This repository contains three local-first system design prototypes:

- QR Code Generator
- Knowledge Base Q&A Bot
- Task Scheduler

The projects demonstrate API design, local persistence, retrieval design, task scheduling, validation, testing, and product-oriented browser interfaces.

## Projects

| Project | Description | Local URL |
|---|---|---|
| `qr_code_generator` | Creates short redirect links and QR Code images for public URLs. | `http://127.0.0.1:8001` |
| `knowledge_base_qa_bot` | Answers questions from a local Markdown knowledge base with source citations. | `http://127.0.0.1:8002` |
| `task_scheduler` | Provides a local task scheduler with web UI, HTTP API, and optional automation tools. | `http://127.0.0.1:8003` |

## Repository Structure

```text
.
|-- qr_code_generator/
|-- knowledge_base_qa_bot/
|-- task_scheduler/
|-- PROJECT_INDEX.md
`-- DELIVERY_REPORT.md
```

Each project follows the same documentation layout:

```text
README.md
IMPLEMENTATION_BRIEF.md
PRODUCT_REQUIREMENTS.md
SPEC.md
API_REFERENCE.md
ACCEPTANCE_TESTS.md
ARCHITECTURE_NOTES.md
RUNBOOK.md
docs/
tests/
app/
```

## Local-First Runtime

All projects run locally and do not require paid service access. The Knowledge Base Q&A Bot uses local Markdown retrieval and extractive answering. The Task Scheduler includes an optional developer automation interface, but the main demo path is the FastAPI web application.

## Quick Start

### QR Code Generator

```powershell
cd qr_code_generator
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8001
```

### Knowledge Base Q&A Bot

```powershell
cd knowledge_base_qa_bot
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8002
```

### Task Scheduler

```powershell
cd task_scheduler
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8003
```

## Verification

Run tests inside each project:

```powershell
python -m pytest tests
```

See [PROJECT_INDEX.md](PROJECT_INDEX.md) for the documentation index and [DELIVERY_REPORT.md](DELIVERY_REPORT.md) for the delivery summary.
