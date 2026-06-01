# Knowledge Base Q&A Bot API Contract

## Base URL

```text
http://127.0.0.1:8002
```

## `GET /health`

### Response `200`

```json
{
  "status": "ok"
}
```

## `GET /`

Returns the browser product UI.

### Response

- `200 text/html`

## `GET /metadata`

Returns local KB status.

### Response `200`

```json
{
  "documents": ["product.md"],
  "indexed_sections": 4,
  "index_exists": true
}
```

## `POST /index`

Builds a local Markdown section index.

### Request

No body.

### Response `200`

```json
{
  "status": "indexed",
  "count": 4
}
```

### Side Effect

Creates:

```text
.kb/index.json
```

## `POST /chat`

### Request

```json
{
  "question": "Does this require paid APIs?"
}
```

### Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `question` | string | yes | Must be non-empty |

### Response `200`

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

### Empty Index Response

```json
{
  "answer": "Knowledge base is empty. Run /index first.",
  "sources": []
}
```

### Weak Retrieval Response

```json
{
  "answer": "I cannot confirm the answer from the knowledge base.",
  "sources": []
}
```

## Source Object

| Field | Type | Meaning |
|---|---|---|
| `source` | string | Markdown filename |
| `heading` | string | Matched section heading |
| `score` | number | Local keyword relevance score |

## Curl Verification

```powershell
curl http://127.0.0.1:8002/health
curl -X POST http://127.0.0.1:8002/index
curl -X POST http://127.0.0.1:8002/chat -H "Content-Type: application/json" -d "{\"question\":\"Does this require paid APIs?\"}"
```
