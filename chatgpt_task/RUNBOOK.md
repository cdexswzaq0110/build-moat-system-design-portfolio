# ChatGPT Task Scheduler Runbook

## Environment

- OS used during implementation: Windows
- Python verified: 3.12.10
- Node.js is not required for the main local demo
- Paid APIs: none

The main verification path is the local FastAPI web app. MCP Inspector is optional because `npx` may be unavailable on some machines.

## Install

### Windows / PowerShell

```powershell
cd chatgpt_task
python -m pip install -r requirements.txt
```

### WSL / Linux

```bash
cd chatgpt_task
python3 -m pip install -r requirements.txt
```

## Run Web Application

### Windows / PowerShell

```powershell
cd chatgpt_task
python -m uvicorn app.main:app --reload --port 8003
```

Open:

```text
http://127.0.0.1:8003
```

### WSL / Linux

```bash
cd chatgpt_task
python3 -m uvicorn app.main:app --reload --port 8003
```

Open:

```text
http://127.0.0.1:8003
```

The browser UI can create tasks, show pending/completed/due-now views, and complete tasks without Node.js.

## Optional MCP Inspector

Use this only if Node.js and `npx` work on your machine:

```powershell
cd chatgpt_task
python -m pip install -r requirements-mcp.txt
npx @modelcontextprotocol/inspector python -m app.mcp_server
```

The MCP server exposes:

- `task.create`
- `task.list`
- `task.get`
- `task.complete`

## Manual Tool Payloads

Create:

```json
{
  "content": "review PR #123",
  "due_at": "2026-06-01T09:00:00+08:00"
}
```

List:

```json
{
  "status": "pending"
}
```

Get:

```json
{
  "id": 1
}
```

Complete:

```json
{
  "id": 1
}
```

## Test

### Windows / PowerShell

```powershell
cd chatgpt_task
python -m pytest tests
```

### WSL / Linux

```bash
cd chatgpt_task
python3 -m pytest tests
```

## Runtime Files

The app creates `tasks.sqlite3` when task storage is initialized.

## Troubleshooting

- If `npx` is unavailable, use the web app at `http://127.0.0.1:8003`.
- If port `8003` is busy, change `--port 8003` to another port.
- If MCP Inspector fails, first verify the web app and tests; MCP is optional.
- If dependency conflicts appear, recreate a project-local virtual environment.
