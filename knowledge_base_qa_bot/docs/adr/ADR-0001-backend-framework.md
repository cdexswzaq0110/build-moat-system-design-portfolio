# ADR-0001: Retrieval Architecture

## Status

Accepted

## Decision

Use Python, FastAPI, and local Markdown KB retrieval. Do not use paid APIs.

## Context

The project is a local knowledge base Q&A prototype designed to run without paid services.

## Consequences

The bot returns extractive, source-grounded answers. It will be less fluent than a generated answer, but it is deterministic, free to run locally, and easier to debug.
