# Build Moat System Design Portfolio

This repository contains three local-first system design prototypes:

- QR Code Generator
- Knowledge Base Q&A Bot
- ChatGPT Task Scheduler

The projects demonstrate API design, local persistence, retrieval design, task scheduling, validation, testing, and product-oriented browser interfaces.

This portfolio was developed after my training in the Build Moat system design live sessions. The original training repository is [bohr109/build-moat-live-sessions](https://github.com/bohr109/build-moat-live-sessions), and the program website is [Build Moat](https://www.buildmoat.org/).

## Projects

| Project | Description | Local URL |
|---|---|---|
| `qr_code_generator` | Creates short redirect links and QR Code images for public URLs. | `http://127.0.0.1:8001` |
| `knowledge_base_qa_bot` | Answers questions from a local Markdown knowledge base with source citations. | `http://127.0.0.1:8002` |
| `chatgpt_task` | Provides a local task scheduler with web UI, HTTP API, and optional MCP tools. | `http://127.0.0.1:8003` |

## Repository Structure

```text
.
|-- qr_code_generator/
|-- knowledge_base_qa_bot/
|-- chatgpt_task/
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

## No Paid API Requirement

All projects run locally and do not require paid API access. The Knowledge Base Q&A Bot uses local Markdown retrieval and extractive answering. The MCP Inspector path in `chatgpt_task` is optional and is not required for the main demo.

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

### ChatGPT Task Scheduler

```powershell
cd chatgpt_task
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8003
```

## Verification

Run tests inside each project:

```powershell
python -m pytest tests
```

See [PROJECT_INDEX.md](PROJECT_INDEX.md) for the documentation index and [DELIVERY_REPORT.md](DELIVERY_REPORT.md) for the delivery summary.

The original live-session assignment context is preserved in [TRAINING_CONTEXT.md](TRAINING_CONTEXT.md).
