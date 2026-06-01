# Knowledge Base Q&A Bot Specification

## Track

Challenge Track with Markdown KB retrieval.

The original `PROMPT.md` was missing from the repository, so this MVP specification was rebuilt from `README.md` and the user-provided exercise description.

## Goal

Create a local FastAPI service that indexes Markdown documents and answers questions with source-grounded extractive answers.

## Non-Goals

- No paid API usage.
- No OpenAI API.
- No hosted embedding API.
- No FAISS/vector route in this MVP.
- No streaming UI.

## API

### `GET /`

Serves the browser product UI.

Behavior:

- Shows knowledge base document and index status.
- Can rebuild the local Markdown index.
- Lets the user ask a question.
- Displays the answer in a central workspace.
- Displays retrieved sources in a dedicated source panel.
- Uses only local retrieval and extractive answers.

### `GET /metadata`

Returns local knowledge base status for the browser UI.

Response:

```json
{
  "documents": ["product.md"],
  "indexed_sections": 4,
  "index_exists": true
}
```

### `GET /health`

Checks service liveness.

Response:

```json
{
  "status": "ok"
}
```

### `POST /index`

Reads Markdown files from `docs/sample/*.md`, splits them by headings, and writes `.kb/index.json`.

Response:

```json
{
  "status": "indexed",
  "count": 4
}
```

### `POST /chat`

Answers a question from the indexed knowledge base.

Request:

```json
{
  "question": "Does this require paid APIs?"
}
```

Response:

```json
{
  "answer": "The Moat prototype is designed for local learning sessions and does not require paid APIs.",
  "sources": [
    {
      "source": "product.md",
      "heading": "Pricing",
      "score": 7.6652
    }
  ]
}
```

## Retrieval Flow

```text
docs/sample/*.md
  -> split by Markdown headings
  -> persist .kb/index.json
  -> tokenize question and sections
  -> local keyword scoring
  -> extract matching sentences
  -> return answer + sources
```

## Data Model

Persisted JSON section object:

| Field | Meaning |
|---|---|
| `id` | Stable source plus heading id |
| `source` | Markdown filename |
| `heading` | Markdown heading text |
| `content` | Raw section content |

Runtime ranked source object:

| Field | Meaning |
|---|---|
| `source` | Markdown filename |
| `heading` | Matched section heading |
| `score` | Local keyword relevance score |

## Design Decisions

- Use section-level retrieval because it is more precise than whole files and easier to inspect than arbitrary chunks.
- Use JSON index because the MVP knowledge base is small and should be agent-readable.
- Use extractive answers to satisfy the no-paid-API constraint.
- Return explicit fallback when retrieval has no match.

## Acceptance Criteria

- `/index` creates an index from Markdown files.
- `/chat` answers only from indexed content.
- `/chat` includes source metadata.
- Weak/no retrieval returns `I cannot confirm the answer from the knowledge base.`
- No paid API key is required.
- Browser UI can index, ask, and inspect sources without using Swagger.
