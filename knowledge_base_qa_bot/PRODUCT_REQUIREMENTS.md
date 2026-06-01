# Knowledge Base Q&A Bot PRD

## Problem

Users need a way to ask questions against a small Markdown knowledge base and receive grounded answers with sources, without using paid APIs.

## Target User

- Workshop participant learning retrieval trade-offs.
- Developer comparing Markdown KB and RAG designs.
- Knowledge owner who wants transparent, inspectable retrieval.

## Goals

1. Index Markdown documents.
2. Retrieve relevant sections by local keyword scoring.
3. Return extractive answers from the retrieved context.
4. Cite source filename and heading.
5. Run locally without paid APIs.
6. Provide a product-quality browser UI for indexing, asking, and source inspection.

## Non-Goals

- Paid LLM generation.
- Hosted embeddings.
- FAISS vector search in this MVP.
- Multi-user auth.
- Multi-turn browser chat history.

## MVP User Stories

### Story 1: Build Index

As a user, I want to call `/index` so that the service reads Markdown docs and creates a searchable index.

Acceptance:

- Reads `docs/sample/*.md`.
- Splits content by Markdown headings.
- Writes `.kb/index.json`.
- Returns indexed section count.

### Story 2: Ask Question

As a user, I want to call `/chat` with a question so that I get an answer grounded in the KB.

Acceptance:

- Uses only indexed content.
- Returns answer text.
- Returns source metadata.
- Does not require API keys.

### Story 3: Weak Result Handling

As a user, I want the system to say when it cannot confirm the answer so that I do not receive fake confidence.

Acceptance:

- No matching section returns a refusal message.
- The system does not fabricate unsupported details.

### Story 4: Browser Workspace

As a user, I want a polished browser workspace so that I can demo indexing, asking, and source inspection without Swagger.

Acceptance:

- The UI shows whether the index exists.
- The UI lists Markdown documents.
- The UI can trigger `/index`.
- The UI can submit `/chat`.
- The UI shows retrieved sources separately from the answer.

## Success Metrics

- `/index` succeeds on sample docs.
- `/chat` returns a cited answer for a known question.
- Core tests pass.
- No paid API key is required.

## Risks

- Keyword search can miss paraphrases.
- Extractive answers are less polished than LLM-generated answers.
- Long sections may return broad context.

## Future Improvements

- Local embedding model.
- Hybrid keyword + vector retrieval.
- Line-level citations.
- Rich source previews.
- Streaming answer display if local generation is added.
