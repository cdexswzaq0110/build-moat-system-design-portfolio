# Knowledge Base Q&A Bot Design Questions

## Context

This project uses the Challenge Track with Markdown KB retrieval because the scaffold files and original `PROMPT.md` were missing. The user also explicitly required no paid APIs, so OpenAI generation and hosted embeddings are out of scope.

## 1. Retrieval unit: file, section, or chunk?

### Decision

Use Markdown heading sections as the retrieval unit.

### Why

A file can be too broad. A chunk can be hard for humans to inspect if it cuts across meaning. A Markdown section usually has a title and a coherent topic, which makes it good for both retrieval and citation.

### Alternatives

- File-level retrieval: simple, but returns too much unrelated text.
- Fixed-size chunks: common in vector RAG, but less aligned with human-written document structure.
- Paragraph-level retrieval: precise, but can lose context.

### Trade-off

Section retrieval depends on well-structured Markdown. Poor headings produce poor retrieval units.

### Production Direction

Support section retrieval first, then optionally split very long sections into smaller chunks while preserving heading metadata.

## 2. How should the index be stored?

### Decision

Persist `.kb/index.json`.

### Why

The index must be inspectable for workshop debugging. JSON makes the index readable by humans and coding agents without a database browser.

### Alternatives

- SQLite: better query support, but less transparent for learning.
- In-memory only: simplest, but disappears on restart.
- FAISS: useful for vector search, but unnecessary for local keyword MVP.

### Trade-off

JSON is not ideal for large knowledge bases. That is acceptable for this exercise.

### Production Direction

Move to SQLite, Postgres, or a search engine when corpus size grows.

## 3. What context should be sent to the answerer?

### Decision

No LLM prompt is used in the MVP. The system returns extractive answers from retrieved sections.

### Why

The user disallowed paid APIs. Using a paid LLM to turn context into prose would violate that constraint.

### Alternatives

- OpenAI chat completion: fluent, but paid and disallowed.
- Local LLM: possible, but setup-heavy and environment-dependent.
- Pure extractive answer: less fluent, but deterministic and free.

### Trade-off

Extractive answers may sound less natural and may include Markdown heading text.

### Production Direction

If a local model is available, add optional local generation. Keep citations and retrieval grounding mandatory.

## 4. How should answers cite sources?

### Decision

Return source filename, heading, and score for each retrieved section.

### Why

The user needs to inspect whether the answer came from the knowledge base. Filename alone is not enough when a file has many sections.

### Alternatives

- No citation: easier, but untrustworthy.
- Filename only: better than nothing, but vague.
- Exact line ranges: excellent, but requires more parsing and line tracking.

### Trade-off

Heading-level citation is clear enough for MVP but not as precise as line-level citation.

### Production Direction

Store line numbers and stable anchor IDs in `.kb/index.json`.

## 5. How should weak retrieval be handled?

### Decision

Return `I cannot confirm the answer from the knowledge base.` when no section matches.

### Why

The system should not invent answers. A weak retrieval result is not permission to guess.

### Alternatives

- Always answer from top result: dangerous when retrieval is wrong.
- Ask a follow-up question: useful in chat UI, but extra workflow for API MVP.
- Search the web: outside the local KB scope.

### Trade-off

The system may refuse to answer when a human could infer something from nearby text.

### Production Direction

Add thresholds, retrieval diagnostics, and query rewriting. Keep refusal behavior when evidence is weak.

## 6. Markdown KB vs Vector RAG: which fits this MVP?

### Decision

Use Markdown KB.

### Why

Markdown KB is local, inspectable, and free. Vector RAG would need embeddings. The original exercise mentioned OpenAI embeddings, but the user later prohibited paid APIs.

### Alternatives

- Vector RAG with OpenAI embeddings: not allowed.
- Vector RAG with local embeddings: possible, but requires extra model dependencies.
- Hybrid search: good production direction, too much for MVP.

### Trade-off

Keyword retrieval misses synonyms that embeddings may catch.

### Production Direction

Add optional local embeddings and compare Markdown KB vs local vector retrieval with a fixed evaluation set.

## 7. What should the product UI emphasize?

### Decision

Use a three-panel workspace: knowledge base status, question/answer workspace, and retrieved sources.

### Why

Professional knowledge-base products make evidence visible. The user should know whether the KB is indexed, what documents exist, and which source sections supported an answer.

### Alternatives

- Chat-only UI: familiar, but hides retrieval quality.
- Swagger-only UI: good for developers, not a product experience.
- Dashboard-only UI: operationally useful, but weak for question answering.

### Trade-off

Three panels take more screen space. On mobile, they collapse into one column.

### Production Direction

Add source previews, line-level citations, feedback controls, and conversation history.
