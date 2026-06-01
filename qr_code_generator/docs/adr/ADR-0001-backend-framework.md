# ADR-0001: Backend Framework

## Status

Accepted

## Decision

Use Python, FastAPI, and SQLite for the QR Code Generator MVP.

## Context

The service needs a small HTTP API, simple validation, redirects, and one persistent table.

## Consequences

FastAPI keeps the API explicit and easy to test. SQLite keeps local setup simple. A production deployment can later replace SQLite with Postgres without changing the route contract.
