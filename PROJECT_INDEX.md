# Project Documentation Index

This file is the documentation index for the repository. It links the product, API, architecture, operation, and verification documents for each prototype.

## Project Documents

| Project | Implementation Brief | Product Requirements | API Reference | Acceptance Tests | Architecture Notes | Runbook |
|---|---|---|---|---|---|---|
| QR Code Generator | `qr_code_generator/IMPLEMENTATION_BRIEF.md` | `qr_code_generator/PRODUCT_REQUIREMENTS.md` | `qr_code_generator/API_REFERENCE.md` | `qr_code_generator/ACCEPTANCE_TESTS.md` | `qr_code_generator/ARCHITECTURE_NOTES.md` | `qr_code_generator/RUNBOOK.md` |
| ChatGPT Task Scheduler | `chatgpt_task/IMPLEMENTATION_BRIEF.md` | `chatgpt_task/PRODUCT_REQUIREMENTS.md` | `chatgpt_task/API_REFERENCE.md` | `chatgpt_task/ACCEPTANCE_TESTS.md` | `chatgpt_task/ARCHITECTURE_NOTES.md` | `chatgpt_task/RUNBOOK.md` |
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

### ChatGPT Task Scheduler

```powershell
cd chatgpt_task
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
cd chatgpt_task
python -m pytest tests
```
