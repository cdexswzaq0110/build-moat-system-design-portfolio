# Verification

## Results

- Unit tests: `python -m pytest tests` -> 4 passed
- Compile check: `python -m compileall app tests` -> passed
- API smoke test: FastAPI `GET /health` -> `200 {"status": "ok"}`
- Key scan: no secret key pattern matches

## Risk

The MVP depends on the free local `qrcode` package for PNG generation.
