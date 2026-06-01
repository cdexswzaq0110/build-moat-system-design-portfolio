# ADR-0001: Retrieval Architecture

## Status

Accepted

## Decision

Use Python, FastAPI, and local Markdown KB retrieval. Do not use paid APIs.

## Context

The exercise asks for a knowledge base Q&A prototype. The user explicitly disallowed APIs that cost extra money.

## Consequences

The bot returns extractive, source-grounded answers. It will be less fluent than an LLM answer, but it is deterministic, free to run locally, and easier to debug.
