# Implementation Brief

## Objective

Build a local question-answering service over Markdown documents. The system should retrieve relevant sections, return a grounded extractive answer, and cite the sources used.

## MVP Scope

- Read Markdown documents from `docs/sample/`.
- Split documents by headings.
- Persist a section index to `.kb/index.json`.
- Rank relevant sections with local keyword scoring.
- Return an answer and source metadata.
- Provide a browser UI for indexing and question answering.

## API Surface

- `GET /health`
- `GET /metadata`
- `POST /index`
- `POST /chat`

## Retrieval Strategy

The implementation uses a Markdown knowledge base strategy:

1. Read local Markdown files.
2. Split documents into heading-based sections.
3. Score sections against the user question.
4. Return the strongest matching sections.
5. Extract answer text from the retrieved content.

## Key Design Decisions

1. Section-level retrieval is more precise than whole-file retrieval and more readable than arbitrary chunks.
2. JSON index storage is simple, inspectable, and adequate for small local knowledge bases.
3. No external generation prompt is required because this MVP uses extractive answering.
4. Citations include filename, heading, and retrieval score.
5. Weak retrieval returns an explicit cannot-confirm answer.

## Verification

```powershell
python -m pytest tests
```
