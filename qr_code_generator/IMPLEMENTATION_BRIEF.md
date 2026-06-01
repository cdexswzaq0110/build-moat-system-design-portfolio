# Implementation Brief

## Objective

Build a local service that creates short redirect links and QR Code PNG images for public HTTP(S) URLs.

## MVP Scope

- Accept a destination URL.
- Validate and normalize the URL.
- Store a generated public token and destination URL.
- Return a short redirect URL and QR Code URL.
- Redirect valid tokens to the stored destination.
- Return `410 Gone` when an expired link is requested.

## API Surface

- `GET /health`
- `POST /links`
- `GET /qr/{token}.png`
- `GET /r/{token}`

## Key Design Decisions

1. Tokens use random URL-safe characters to avoid exposing database sequence information.
2. URL validation only permits `http` and `https`.
3. Local SQLite is sufficient for the MVP data volume and keeps the demo self-contained.
4. Expiration is stored as optional metadata and enforced at read time.
5. The MVP uses direct database lookup; caching can be added later without changing the public API.

## Verification

```powershell
python -m pytest tests
```
