# QR Code Generator PRD

## Problem

Users need a fast way to turn a public URL into a QR code and short redirect link without manually calling multiple API endpoints.

## Target User

- Developer testing a QR code prototype.
- Small creator or operator who wants a QR code pointing to a website.
- Developer validating API behavior through curl or Swagger.

## Goals

1. Generate a short token for a public URL.
2. Generate a QR code image for that URL.
3. Redirect visitors through the short token.
4. Provide a browser UI where the QR appears immediately.
5. Run locally without paid APIs.

## Non-Goals

- User accounts.
- Analytics dashboard.
- Custom QR styling.
- Bulk QR generation.
- Paid URL safety APIs.

## MVP User Stories

### Story 1: Generate From Browser

As a user, I want to enter my GitHub URL and click one button so I can see the QR code immediately.

Acceptance:

- The homepage defaults to `https://github.com/cdexswzaq0110`.
- Clicking `Generate QR Code` calls `POST /links`.
- The QR image appears on the same page.
- The short URL and token are visible.

### Story 2: Generate From API

As a developer, I want to call `POST /links` so I can integrate QR generation into another tool.

Acceptance:

- Valid public URL returns token, short URL, and QR URL.
- Invalid URL returns `400`.

### Story 3: Redirect

As a QR scanner, I want the short URL to redirect to the original destination.

Acceptance:

- Existing active token returns `307`.
- Unknown token returns `404`.
- Expired token returns `410`.

## Success Metrics

- User can generate QR code from homepage in one click after server starts.
- Core tests pass.
- No paid API key is required.

## Risks

- URL validation is basic and does not detect phishing.
- SQLite is local and not suitable for multi-instance production deployments.

## Future Improvements

- QR style customization.
- Download button.
- Rate limiting.
- Click analytics.
- Branded expired-link page.
