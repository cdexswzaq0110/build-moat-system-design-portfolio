# QR Code Generator

QR Code Generator is a local FastAPI application that creates a short redirect link and a QR Code for a destination URL. The browser interface is designed for a simple product workflow: enter a URL, generate the QR Code, preview it on the same page, and use the generated short URL for redirect testing.

## Features

- Create a short token for a destination URL.
- Generate a PNG QR Code for the stored destination.
- Redirect through `/r/{token}`.
- Support optional expiration timestamps.
- Update QR destinations without changing the token.
- Soft delete QR links while preserving metadata.
- Track redirect scans and return daily analytics.
- Check QR status before sharing.
- Provide a browser UI and HTTP API.
- Store link metadata in local SQLite.

## Run Locally

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8001
```

Open:

```text
http://127.0.0.1:8001
```

## API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/links` | Create a short link and QR Code URL |
| `POST` | `/api/qr/create` | Product API alias for QR creation |
| `GET` | `/api/qr/{token}` | Return link metadata |
| `PATCH` | `/api/qr/{token}` | Update destination or expiration |
| `DELETE` | `/api/qr/{token}` | Soft delete a link |
| `GET` | `/api/qr/{token}/analytics` | Return scan totals |
| `GET` | `/api/qr/{token}/check` | Return active/deleted/expired status |
| `GET` | `/qr/{token}.png` | Return QR Code PNG |
| `GET` | `/r/{token}` | Redirect to the destination URL |

See [API_REFERENCE.md](API_REFERENCE.md) for request and response details.

## Test

```powershell
python -m pytest tests
```

Expected result:

```text
5 passed
```

## Documentation

- [PRODUCT_REQUIREMENTS.md](PRODUCT_REQUIREMENTS.md)
- [IMPLEMENTATION_BRIEF.md](IMPLEMENTATION_BRIEF.md)
- [SPEC.md](SPEC.md)
- [API_REFERENCE.md](API_REFERENCE.md)
- [ACCEPTANCE_TESTS.md](ACCEPTANCE_TESTS.md)
- [ARCHITECTURE_NOTES.md](ARCHITECTURE_NOTES.md)
- [RUNBOOK.md](RUNBOOK.md)
