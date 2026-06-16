# Project Documentation Index

This file is the documentation index for the repository. It links the product, API, architecture, operation, and verification documents for each prototype.

## Project Documents

| Project | Implementation Brief | Product Requirements | API Reference | Acceptance Tests | Architecture Notes | Runbook |
|---|---|---|---|---|---|---|
| QR Code Generator | `qr_code_generator/IMPLEMENTATION_BRIEF.md` | `qr_code_generator/PRODUCT_REQUIREMENTS.md` | `qr_code_generator/API_REFERENCE.md` | `qr_code_generator/ACCEPTANCE_TESTS.md` | `qr_code_generator/ARCHITECTURE_NOTES.md` | `qr_code_generator/RUNBOOK.md` |
| Task Scheduler | `task_scheduler/IMPLEMENTATION_BRIEF.md` | `task_scheduler/PRODUCT_REQUIREMENTS.md` | `task_scheduler/API_REFERENCE.md` | `task_scheduler/ACCEPTANCE_TESTS.md` | `task_scheduler/ARCHITECTURE_NOTES.md` | `task_scheduler/RUNBOOK.md` |
| Knowledge Base Q&A Bot | `knowledge_base_qa_bot/IMPLEMENTATION_BRIEF.md` | `knowledge_base_qa_bot/PRODUCT_REQUIREMENTS.md` | `knowledge_base_qa_bot/API_REFERENCE.md` | `knowledge_base_qa_bot/ACCEPTANCE_TESTS.md` | `knowledge_base_qa_bot/ARCHITECTURE_NOTES.md` | `knowledge_base_qa_bot/RUNBOOK.md` |

## Implementation Policy

- All projects run locally.
- No project requires paid API access.
- SQLite runtime files and generated indexes are excluded from version control.
- Each project includes a focused test suite under `tests/`.

## Local Demo Commands

### QR Code Generator

```powershell
cd qr_code_generator
python -m uvicorn app.main:app --reload --port 8001
```

### Knowledge Base Q&A Bot

```powershell
cd knowledge_base_qa_bot
python -m uvicorn app.main:app --reload --port 8002
```

### Task Scheduler

```powershell
cd task_scheduler
python -m uvicorn app.main:app --reload --port 8003
```

## Verification Commands

```powershell
cd qr_code_generator
python -m pytest tests
```

```powershell
cd knowledge_base_qa_bot
python -m pytest tests
```

```powershell
cd task_scheduler
python -m pytest tests
```
