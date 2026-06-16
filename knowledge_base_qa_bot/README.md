# Knowledge Base Q&A Bot

Knowledge Base Q&A Bot is a local retrieval prototype for answering questions from Markdown documents. It builds a section-level index from local Markdown files, ranks relevant sections with keyword retrieval, returns an extractive answer, and cites the matched sources.

This implementation is intentionally local-first. It does not require OpenAI API keys, paid embedding APIs, FAISS, or external LLM calls.

## Features

- Index Markdown files under `docs/sample/`.
- Split documents into heading-based sections.
- Rank relevant sections with local BM25-style scoring.
- Preserve heading paths for stronger source context.
- Return grounded answers with section citations, source previews, and learning focus.
- Inspect indexed documents through `/documents`.
- Provide a browser UI for indexing, asking questions, and reviewing sources.
- Persist the generated index under `.kb/index.json`.

## Run Locally

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8002
```

Open:

```text
http://127.0.0.1:8002
```

Click `Rebuild Index` before asking questions.

## API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/metadata` | Return document and index status |
| `GET` | `/documents` | Return indexed documents and sections |
| `POST` | `/index` | Build the local Markdown index |
| `POST` | `/chat` | Answer a question from indexed sources |

See [API_REFERENCE.md](API_REFERENCE.md) for request and response details.

## Test

```powershell
python -m pytest tests
```

Expected result:

```text
7 passed
```

## Documentation

- [PRODUCT_REQUIREMENTS.md](PRODUCT_REQUIREMENTS.md)
- [IMPLEMENTATION_BRIEF.md](IMPLEMENTATION_BRIEF.md)
- [SPEC.md](SPEC.md)
- [API_REFERENCE.md](API_REFERENCE.md)
- [ACCEPTANCE_TESTS.md](ACCEPTANCE_TESTS.md)
- [ARCHITECTURE_NOTES.md](ARCHITECTURE_NOTES.md)
- [RUNBOOK.md](RUNBOOK.md)
