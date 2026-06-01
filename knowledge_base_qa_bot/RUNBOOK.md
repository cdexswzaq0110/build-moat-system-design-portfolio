# Knowledge Base Q&A Bot Runbook

## Environment

- OS used during implementation: Windows
- Python verified: 3.12.10
- Paid APIs: none

## Install

### Windows / PowerShell

```powershell
cd knowledge_base_qa_bot
python -m pip install -r requirements.txt
```

### WSL / Linux

```bash
cd knowledge_base_qa_bot
python3 -m pip install -r requirements.txt
```

## Run

### Windows / PowerShell

```powershell
cd knowledge_base_qa_bot
python -m uvicorn app.main:app --reload --port 8002
```

Demo URL:

```text
http://127.0.0.1:8002
```

Open this URL in the browser. The product UI has three working areas:

- Left: knowledge base status and `Rebuild Index`
- Center: question and answer workspace
- Right: retrieved sources and sample questions

### WSL / Linux

```bash
cd knowledge_base_qa_bot
python3 -m uvicorn app.main:app --reload --port 8002
```

## Verify

### Windows / PowerShell

```powershell
curl http://127.0.0.1:8002/health
curl -X POST http://127.0.0.1:8002/index
curl -X POST http://127.0.0.1:8002/chat -H "Content-Type: application/json" -d "{\"question\":\"Does this require paid APIs?\"}"
```

Browser UI verification:

1. Open `http://127.0.0.1:8002`.
2. Click `Rebuild Index`.
3. Confirm the indexed section count updates.
4. Ask `Does this require paid APIs?`.
5. Confirm the answer appears in the center workspace.
6. Confirm the source panel shows at least one source.

### WSL / Linux

```bash
curl http://127.0.0.1:8002/health
curl -X POST http://127.0.0.1:8002/index
curl -X POST http://127.0.0.1:8002/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"Does this require paid APIs?"}'
```

## Test

### Windows / PowerShell

```powershell
cd knowledge_base_qa_bot
python -m pytest tests
```

### WSL / Linux

```bash
cd knowledge_base_qa_bot
python3 -m pytest tests
```

## Runtime Files

The app creates `.kb/index.json` after `POST /index`.

## Add Knowledge

Add or edit Markdown files here:

```text
knowledge_base_qa_bot/docs/sample/
```

Then call:

```powershell
curl -X POST http://127.0.0.1:8002/index
```

## Troubleshooting

- If answers are empty, run `/index` first.
- If a synonym does not match, add the exact term to the Markdown KB or improve retrieval in a later iteration.
- If port `8002` is busy, change `--port 8002` to another port.
