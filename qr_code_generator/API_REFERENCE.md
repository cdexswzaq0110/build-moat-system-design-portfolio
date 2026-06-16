# QR Code Generator API Contract

## Base URL

```text
http://127.0.0.1:8001
```

## `GET /`

Returns the browser UI.

### Response

- `200 text/html`

## `GET /health`

### Response `200`

```json
{
  "status": "ok"
}
```

## `POST /links`

### Request

```json
{
  "url": "https://github.com/cdexswzaq0110",
  "expires_at": null
}
```

### Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `url` | string | yes | Must be public `http` or `https` URL |
| `expires_at` | string or null | no | ISO datetime |

### Response `200`

```json
{
  "token": "Ab12Cd34",
  "url": "https://github.com/cdexswzaq0110",
  "short_url": "/r/Ab12Cd34",
  "qr_url": "/qr/Ab12Cd34.png"
}
```

### Response `400`

```json
{
  "detail": "Only http and https URLs are allowed"
}
```

## `GET /qr/{token}.png`

### Path Parameters

| Parameter | Type | Required |
|---|---|---|
| `token` | string | yes |

### Responses

| Status | Content Type | Meaning |
|---|---|---|
| `200` | `image/png` | Active QR code |
| `404` | `application/json` | Token not found |
| `410` | `application/json` | Token expired |

## `GET /r/{token}`

### Responses

| Status | Meaning |
|---|---|
| `307` | Redirects to target URL |
| `404` | Token not found |
| `410` | Token expired |

Redirect requests also record a scan event for analytics.

## `POST /api/qr/create`

Product API alias for `POST /links`.

### Request

```json
{
  "url": "https://github.com/cdexswzaq0110",
  "expires_at": null
}
```

### Response `200`

```json
{
  "token": "Ab12Cd34",
  "url": "https://github.com/cdexswzaq0110",
  "short_url": "/r/Ab12Cd34",
  "qr_url": "/qr/Ab12Cd34.png"
}
```

## `GET /api/qr/{token}`

Returns link metadata.

### Response `200`

```json
{
  "token": "Ab12Cd34",
  "url": "https://github.com/cdexswzaq0110",
  "created_at": "2026-06-16T10:00:00+00:00",
  "updated_at": "2026-06-16T10:00:00+00:00",
  "expires_at": null,
  "is_deleted": false
}
```

## `PATCH /api/qr/{token}`

Updates destination URL and/or expiration.

### Request

```json
{
  "url": "https://example.com/updated",
  "expires_at": null
}
```

### Response `200`

Returns the updated link metadata.

## `DELETE /api/qr/{token}`

Soft deletes a QR link.

### Response `200`

```json
{
  "status": "deleted",
  "token": "Ab12Cd34"
}
```

## `GET /api/qr/{token}/image`

Product API alias for `GET /qr/{token}.png`.

## `GET /api/qr/{token}/analytics`

Returns scan totals.

### Response `200`

```json
{
  "token": "Ab12Cd34",
  "total_scans": 3,
  "scans_by_day": [
    {
      "date": "2026-06-16",
      "count": 3
    }
  ]
}
```

## `GET /api/qr/{token}/check`

Returns redirectability status.

### Response `200`

```json
{
  "token": "Ab12Cd34",
  "status": "active",
  "redirectable": true
}
```

## Curl Verification

```powershell
curl http://127.0.0.1:8001/health
curl -X POST http://127.0.0.1:8001/links -H "Content-Type: application/json" -d "{\"url\":\"https://github.com/cdexswzaq0110\"}"
curl http://127.0.0.1:8001/api/qr/{token}/analytics
```
