# ADR-0001: MCP Server Framework

## Status

Accepted

## Decision

Use Python, SQLite, and the official MCP SDK.

## Context

The prototype is a local stdio MCP server with simple durable state and no paid API dependency.

## Consequences

The server can run in developer inspector and compatible local clients. SQLite keeps setup local and deterministic.
