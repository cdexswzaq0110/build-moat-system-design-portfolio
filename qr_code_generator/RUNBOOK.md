# QR Code Generator Runbook

## Environment

- OS used during implementation: Windows
- Python verified: 3.12.10
- Paid APIs: none

## Install

### Windows / PowerShell

```powershell
cd qr_code_generator
python -m pip install -r requirements.txt
```

### WSL / Linux

```bash
cd qr_code_generator
python3 -m pip install -r requirements.txt
```

## Run

### Windows / PowerShell

```powershell
cd qr_code_generator
python -m uvicorn app.main:app --reload --port 8001
```

Demo URL:

```text
http://127.0.0.1:8001
```

Open this URL in the browser. The page defaults to:

```text
https://github.com/cdexswzaq0110
```

Click `Generate QR Code`. The QR code appears in the right-side preview panel.

### WSL / Linux

```bash
cd qr_code_generator
python3 -m uvicorn app.main:app --reload --port 8001
```

## Verify

### Windows / PowerShell

```powershell
curl http://127.0.0.1:8001/health
curl -X POST http://127.0.0.1:8001/links -H "Content-Type: application/json" -d "{\"url\":\"https://example.com\"}"
```

Browser UI verification:

1. Open `http://127.0.0.1:8001`.
2. Keep the default URL or enter another public URL.
3. Click `Generate QR Code`.
4. Confirm the QR preview appears on the same page.
5. Click the displayed short URL to verify redirect.

Use the returned token:

```powershell
curl -I http://127.0.0.1:8001/r/YOUR_TOKEN
curl -I http://127.0.0.1:8001/qr/YOUR_TOKEN.png
```

### WSL / Linux

```bash
curl http://127.0.0.1:8001/health
curl -X POST http://127.0.0.1:8001/links \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

## Test

### Windows / PowerShell

```powershell
cd qr_code_generator
python -m pytest tests
```

### WSL / Linux

```bash
cd qr_code_generator
python3 -m pytest tests
```

## Runtime Files

The app creates `qr_links.sqlite3` when it starts.

## Troubleshooting

- If `uvicorn` is missing, run the install command again.
- If port `8001` is busy, change `--port 8001` to another port.
