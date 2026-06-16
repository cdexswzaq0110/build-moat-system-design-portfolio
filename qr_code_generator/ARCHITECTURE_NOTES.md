# QR Code Generator Design Questions

## 1. How should short tokens be generated?

### Decision

Use random URL-safe alphanumeric tokens with a default length of 8.

### Why

The token is public. A sequential integer token would leak creation order and make enumeration easy. A random token avoids exposing database sequence information and is simple enough for the MVP.

### Alternatives

- Sequential IDs: simpler, but easy to guess.
- Hash of URL: deterministic, but two users creating the same URL would collide by design.
- UUID: safe, but too long for a short link product.

### Trade-off

Random tokens can collide. The MVP retries token creation up to five times. For production, use a database uniqueness constraint plus better retry handling and collision metrics.

### Production Direction

Use a configurable token length, collision monitoring, and possibly a reserved-word blocklist.

## 2. What URL validation is needed?

### Decision

Allow only `http` and `https`, remove URL fragments, require a host, and block localhost/private IP/link-local targets.

### Why

The service stores and redirects user-provided URLs. Without validation, the app can become a tool for unsafe internal redirects or SSRF-style misuse.

### Alternatives

- Accept everything: fastest, but unsafe.
- Domain allowlist only: safer, but too restrictive for a general QR tool.
- Full threat-intelligence URL scanning: stronger, but outside this free local MVP.

### Trade-off

This MVP blocks obvious local/private targets but does not classify phishing or malware domains.

### Production Direction

Add rate limiting, abuse reporting, optional domain allowlists, and async safety scanning.

## 3. Why use SQLite?

### Decision

Use SQLite for local MVP persistence.

### Why

The data model is one table and the project runs locally. SQLite keeps setup low-friction and makes the prototype easy to demo.

### Alternatives

- In-memory dictionary: simpler, but loses data on restart.
- Postgres: production-ready, but unnecessary setup cost for MVP.

### Trade-off

SQLite is not ideal for high write concurrency. That is acceptable for a local-first MVP.

### Production Direction

Move to Postgres when multiple app instances or higher write volume are needed.

## 4. How should expired links behave?

### Decision

Return `410 Gone` for expired links and `404 Not Found` for unknown links.

### Why

The two states mean different things. Unknown means the token never existed. Expired means the token existed but is no longer usable.

### Alternatives

- Always return `404`: hides state but loses useful product semantics.
- Redirect to an expiration page: better UX, but requires more UI work.

### Trade-off

Returning `410` reveals that a token once existed. For public short links, that is usually acceptable.

### Production Direction

Add a branded expired-link page and configurable privacy behavior.

## 5. Why add a browser UI instead of only Swagger?

### Decision

Add a production-style `GET /` UI that creates links and renders the QR code on the same page.

### Why

Swagger is an API testing tool, not a product experience. The user wanted the QR code to appear directly after clicking a button.

### Alternatives

- Keep only Swagger: acceptable for API tests, poor for end users.
- Build a separate frontend app: more flexible, but too much overhead for MVP.

### Trade-off

Inline HTML/CSS/JS in FastAPI is less scalable than a separate frontend, but it keeps this prototype easy to run.

### Production Direction

Move UI into a dedicated frontend when auth, analytics, teams, or advanced QR customization are added.
