# QR Code Generator Specification

## Track

Challenge Track.

The original `PROMPT.md` was missing from the repository, so this MVP specification was rebuilt from `README.md` and the user-provided exercise description.

## Goal

Create a local FastAPI service that accepts a public URL, stores it with a short token, returns a QR code image endpoint, and redirects visitors through the token.

## Non-Goals

- No paid API usage.
- No analytics dashboard.
- No rate limiting in this MVP.

## API

### `GET /`

Serves the production-style browser UI.

Behavior:

- Shows a destination URL input.
- Defaults to `https://github.com/cdexswzaq0110`.
- Calls `POST /links` from the page.
- Renders the generated QR code image in the same page.
- Shows the short redirect URL, destination URL, and token.

### `GET /health`

Checks service liveness.

Response:

```json
{
  "status": "ok"
}
```

### `POST /links`

Creates a short link and QR endpoint.

Request:

```json
{
  "url": "https://example.com",
  "expires_at": null
}
```

Response:

```json
{
  "token": "Ab12Cd34",
  "url": "https://example.com",
  "short_url": "/r/Ab12Cd34",
  "qr_url": "/qr/Ab12Cd34.png"
}
```

Validation:

- `url` is required.
- Only `http` and `https` are allowed.
- URL fragments are removed.
- `localhost`, private IPs, loopback IPs, and link-local IPs are blocked.
- `expires_at`, when provided, must be ISO datetime.

### `GET /qr/{token}.png`

Returns a PNG QR code image for the stored target URL.

Responses:

- `200 image/png`: QR code exists and is active.
- `404`: token not found.
- `410`: token expired.

### `GET /r/{token}`

Redirects to the stored target URL.

Responses:

- `307`: active redirect.
- `404`: token not found.
- `410`: token expired.

## Data Model

SQLite table: `links`

| Column | Type | Meaning |
|---|---|---|
| `token` | TEXT PRIMARY KEY | Public short token |
| `target_url` | TEXT | Normalized destination URL |
| `created_at` | TEXT | UTC ISO creation time |
| `expires_at` | TEXT nullable | Optional UTC/ISO expiration |

## Design Decisions

- Use random alphanumeric tokens to avoid leaking sequence information.
- Keep URL validation in `app/url_validator.py`.
- Keep persistence in `app/repository.py`.
- Use direct DB lookup for MVP; cache can be added later without changing the API.

## Acceptance Criteria

- Creating a valid link returns token, redirect path, and QR path.
- Invalid/private URLs return `400`.
- Unknown token returns `404`.
- Expired token returns `410`.
- QR endpoint returns `image/png`.
- Browser UI can generate and display a QR code without manually opening `/qr/{token}.png`.
