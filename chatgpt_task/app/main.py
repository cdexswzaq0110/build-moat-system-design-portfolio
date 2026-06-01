from datetime import datetime, timezone
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .scheduler import complete_job, create_job, find_due_jobs, get_job, initialize_database, list_jobs


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


initialize_database()
app = FastAPI(title="ChatGPT Task Scheduler", lifespan=lifespan)


class CreateTaskRequest(BaseModel):
    content: str = Field(..., min_length=1)
    due_at: str


class CompleteTaskResponse(BaseModel):
    job: dict


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/tasks")
def api_list_tasks(status: Optional[str] = None) -> dict:
    return {"jobs": list_jobs(status=status)}


@app.post("/api/tasks")
def api_create_task(request: CreateTaskRequest) -> dict:
    try:
        job = create_job(content=request.content, due_at=request.due_at)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"job": job}


@app.get("/api/tasks/due")
def api_due_tasks() -> dict:
    return {"jobs": find_due_jobs()}


@app.get("/api/tasks/{job_id}")
def api_get_task(job_id: int) -> dict:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="job not found")
    return {"job": job}


@app.post("/api/tasks/{job_id}/complete", response_model=CompleteTaskResponse)
def api_complete_task(job_id: int) -> CompleteTaskResponse:
    job = complete_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="job not found")
    return CompleteTaskResponse(job=job)


@app.get("/api/summary")
def api_summary() -> dict:
    jobs = list_jobs()
    now = datetime.now(timezone.utc)
    pending = [job for job in jobs if job["status"] == "pending"]
    completed = [job for job in jobs if job["status"] == "completed"]
    due = find_due_jobs(now)
    upcoming = [
        job
        for job in pending
        if datetime.fromisoformat(job["due_at"]) > now
    ]
    return {
        "total": len(jobs),
        "pending": len(pending),
        "completed": len(completed),
        "due": len(due),
        "upcoming": len(upcoming),
    }


@app.get("/", response_class=HTMLResponse)
def serve_home() -> HTMLResponse:
    return HTMLResponse(
        """
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Task Scheduler</title>
            <style>
                :root {
                    --bg: #f6f7f9;
                    --surface: #ffffff;
                    --surface-subtle: #f0f3f7;
                    --text: #172033;
                    --muted: #667085;
                    --border: #d8dee8;
                    --primary: #176b5c;
                    --primary-hover: #11564a;
                    --accent: #285da8;
                    --danger: #b42318;
                    --warning: #9a5b13;
                    --success: #067647;
                    --shadow: 0 18px 44px rgba(23, 32, 51, 0.09);
                    --radius: 8px;
                }

                * { box-sizing: border-box; }

                body {
                    margin: 0;
                    min-height: 100vh;
                    background: var(--bg);
                    color: var(--text);
                    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                    letter-spacing: 0;
                }

                a {
                    color: var(--accent);
                    text-decoration: none;
                    font-weight: 700;
                }

                .topbar {
                    height: 64px;
                    padding: 0 28px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    background: var(--surface);
                    border-bottom: 1px solid var(--border);
                }

                .brand {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    font-weight: 800;
                }

                .brand-mark {
                    width: 34px;
                    height: 34px;
                    border-radius: 8px;
                    display: grid;
                    place-items: center;
                    background: var(--text);
                    color: #ffffff;
                    font-size: 12px;
                }

                .top-actions {
                    display: flex;
                    align-items: center;
                    gap: 14px;
                    font-size: 14px;
                }

                .shell {
                    width: min(1240px, calc(100% - 40px));
                    margin: 0 auto;
                    padding: 28px 0;
                    display: grid;
                    grid-template-columns: 300px minmax(0, 1fr) 300px;
                    gap: 18px;
                    align-items: start;
                }

                .panel {
                    background: var(--surface);
                    border: 1px solid var(--border);
                    border-radius: var(--radius);
                    box-shadow: var(--shadow);
                    overflow: hidden;
                }

                .panel-header {
                    padding: 16px 18px;
                    border-bottom: 1px solid var(--border);
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    gap: 12px;
                }

                .panel-title {
                    margin: 0;
                    font-size: 14px;
                    font-weight: 800;
                }

                .panel-body {
                    padding: 18px;
                }

                .metric-grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 10px;
                }

                .metric {
                    padding: 12px;
                    border: 1px solid var(--border);
                    border-radius: var(--radius);
                    background: var(--surface-subtle);
                }

                .metric-label {
                    color: var(--muted);
                    font-size: 12px;
                    font-weight: 700;
                }

                .metric-value {
                    margin-top: 6px;
                    font-size: 24px;
                    line-height: 1;
                    font-weight: 850;
                }

                .form {
                    display: grid;
                    gap: 14px;
                }

                .field {
                    display: grid;
                    gap: 8px;
                }

                label {
                    font-size: 13px;
                    font-weight: 800;
                    color: #344054;
                }

                textarea,
                input,
                select {
                    width: 100%;
                    border: 1px solid var(--border);
                    border-radius: var(--radius);
                    padding: 11px 12px;
                    font: inherit;
                    color: var(--text);
                    background: #ffffff;
                }

                textarea {
                    min-height: 104px;
                    resize: vertical;
                    line-height: 1.5;
                }

                textarea:focus,
                input:focus,
                select:focus {
                    outline: 3px solid rgba(40, 93, 168, 0.16);
                    border-color: var(--accent);
                }

                button {
                    min-height: 40px;
                    border-radius: var(--radius);
                    border: 0;
                    padding: 0 14px;
                    font-size: 14px;
                    font-weight: 800;
                    cursor: pointer;
                }

                button:disabled {
                    opacity: 0.62;
                    cursor: not-allowed;
                }

                .button-primary {
                    color: #ffffff;
                    background: var(--primary);
                }

                .button-primary:hover {
                    background: var(--primary-hover);
                }

                .button-secondary {
                    color: var(--text);
                    background: #ffffff;
                    border: 1px solid var(--border);
                }

                .toolbar {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    gap: 12px;
                    flex-wrap: wrap;
                    padding: 14px 18px;
                    border-bottom: 1px solid var(--border);
                    background: #fbfcfe;
                }

                .segmented {
                    display: inline-flex;
                    padding: 3px;
                    border: 1px solid var(--border);
                    border-radius: var(--radius);
                    background: var(--surface-subtle);
                }

                .segment {
                    min-height: 32px;
                    background: transparent;
                    color: var(--muted);
                    padding: 0 12px;
                }

                .segment.is-active {
                    background: #ffffff;
                    color: var(--text);
                    box-shadow: 0 1px 3px rgba(23, 32, 51, 0.10);
                }

                .task-list {
                    display: grid;
                    gap: 10px;
                    padding: 18px;
                    min-height: 520px;
                    align-content: start;
                }

                .task-card {
                    border: 1px solid var(--border);
                    border-radius: var(--radius);
                    background: #ffffff;
                    padding: 14px;
                    display: grid;
                    grid-template-columns: minmax(0, 1fr) auto;
                    gap: 12px;
                    align-items: start;
                }

                .task-title {
                    margin: 0 0 8px;
                    font-weight: 800;
                    line-height: 1.45;
                    overflow-wrap: anywhere;
                }

                .task-meta {
                    display: flex;
                    gap: 8px;
                    flex-wrap: wrap;
                    color: var(--muted);
                    font-size: 12px;
                    line-height: 1.5;
                }

                .pill {
                    display: inline-flex;
                    align-items: center;
                    min-height: 24px;
                    border-radius: 999px;
                    padding: 0 9px;
                    font-size: 12px;
                    font-weight: 800;
                    background: #ecfdf3;
                    color: var(--success);
                }

                .pill.warning {
                    background: #fff7e8;
                    color: var(--warning);
                }

                .pill.muted {
                    background: var(--surface-subtle);
                    color: var(--muted);
                }

                .empty {
                    border: 1px dashed #b9c2d0;
                    border-radius: var(--radius);
                    padding: 24px;
                    color: var(--muted);
                    background: #fbfcfe;
                    line-height: 1.6;
                }

                .status {
                    min-height: 22px;
                    color: var(--muted);
                    font-size: 13px;
                    line-height: 1.5;
                }

                .status.error {
                    color: var(--danger);
                }

                .api-box {
                    display: grid;
                    gap: 10px;
                    font-size: 13px;
                    line-height: 1.5;
                }

                .code-line {
                    padding: 10px 12px;
                    border: 1px solid var(--border);
                    border-radius: var(--radius);
                    background: #101828;
                    color: #ffffff;
                    overflow-wrap: anywhere;
                    font-family: Consolas, monospace;
                    font-size: 12px;
                }

                @media (max-width: 1080px) {
                    .shell {
                        grid-template-columns: 1fr;
                    }

                    .task-list {
                        min-height: 260px;
                    }
                }

                @media (max-width: 640px) {
                    .topbar {
                        padding: 0 18px;
                    }

                    .top-actions {
                        display: none;
                    }

                    .shell {
                        width: min(100% - 24px, 1240px);
                        padding: 18px 0;
                    }

                    .task-card {
                        grid-template-columns: 1fr;
                    }
                }
            </style>
        </head>
        <body>
            <header class="topbar">
                <div class="brand">
                    <div class="brand-mark" aria-hidden="true">TS</div>
                    <span>Task Scheduler</span>
                </div>
                <nav class="top-actions" aria-label="Utilities">
                    <a href="/docs">API Docs</a>
                    <a href="/health">Health</a>
                </nav>
            </header>

            <main class="shell">
                <aside class="panel" aria-label="Create scheduled task">
                    <div class="panel-header">
                        <h2 class="panel-title">Create Task</h2>
                        <span class="pill">Local</span>
                    </div>
                    <div class="panel-body">
                        <form class="form" id="task-form">
                            <div class="field">
                                <label for="content">Task content</label>
                                <textarea id="content" required>review PR #123</textarea>
                            </div>
                            <div class="field">
                                <label for="due-at">Due time</label>
                                <input id="due-at" type="datetime-local" required>
                            </div>
                            <button class="button-primary" id="create-button" type="submit">Schedule Task</button>
                            <div class="status" id="form-status" role="status" aria-live="polite"></div>
                        </form>
                    </div>
                </aside>

                <section class="panel" aria-label="Scheduled tasks">
                    <div class="panel-header">
                        <h1 class="panel-title">Scheduled Work</h1>
                        <span class="pill warning" id="due-pill">0 due</span>
                    </div>
                    <div class="toolbar">
                        <div class="segmented" aria-label="Task filter">
                            <button class="segment is-active" type="button" data-filter="all">All</button>
                            <button class="segment" type="button" data-filter="pending">Pending</button>
                            <button class="segment" type="button" data-filter="completed">Completed</button>
                            <button class="segment" type="button" data-filter="due">Due now</button>
                        </div>
                        <button class="button-secondary" id="refresh-button" type="button">Refresh</button>
                    </div>
                    <div class="task-list" id="task-list"></div>
                </section>

                <aside class="panel" aria-label="Summary and API">
                    <div class="panel-header">
                        <h2 class="panel-title">Today Overview</h2>
                        <span class="pill" id="total-pill">0 total</span>
                    </div>
                    <div class="panel-body">
                        <div class="metric-grid">
                            <div class="metric">
                                <div class="metric-label">Pending</div>
                                <div class="metric-value" id="metric-pending">0</div>
                            </div>
                            <div class="metric">
                                <div class="metric-label">Due now</div>
                                <div class="metric-value" id="metric-due">0</div>
                            </div>
                            <div class="metric">
                                <div class="metric-label">Upcoming</div>
                                <div class="metric-value" id="metric-upcoming">0</div>
                            </div>
                            <div class="metric">
                                <div class="metric-label">Completed</div>
                                <div class="metric-value" id="metric-completed">0</div>
                            </div>
                        </div>
                    </div>
                    <div class="panel-header">
                        <h2 class="panel-title">No Node Required</h2>
                    </div>
                    <div class="panel-body api-box">
                        <div>This web UI replaces MCP Inspector for local verification.</div>
                        <div class="code-line">python -m uvicorn app.main:app --reload --port 8003</div>
                        <div class="code-line">GET /api/tasks</div>
                        <div class="code-line">POST /api/tasks</div>
                    </div>
                </aside>
            </main>

            <script>
                const form = document.getElementById("task-form");
                const contentInput = document.getElementById("content");
                const dueInput = document.getElementById("due-at");
                const createButton = document.getElementById("create-button");
                const formStatus = document.getElementById("form-status");
                const taskList = document.getElementById("task-list");
                const refreshButton = document.getElementById("refresh-button");
                const filterButtons = document.querySelectorAll("[data-filter]");
                const duePill = document.getElementById("due-pill");
                const totalPill = document.getElementById("total-pill");
                const metricPending = document.getElementById("metric-pending");
                const metricDue = document.getElementById("metric-due");
                const metricUpcoming = document.getElementById("metric-upcoming");
                const metricCompleted = document.getElementById("metric-completed");

                let currentFilter = "all";

                function defaultLocalDateTime() {
                    const date = new Date();
                    date.setHours(date.getHours() + 1, 0, 0, 0);
                    const offset = date.getTimezoneOffset();
                    const local = new Date(date.getTime() - offset * 60000);
                    return local.toISOString().slice(0, 16);
                }

                function toIsoFromLocal(value) {
                    return new Date(value).toISOString();
                }

                function formatDate(iso) {
                    return new Intl.DateTimeFormat("zh-TW", {
                        dateStyle: "medium",
                        timeStyle: "short"
                    }).format(new Date(iso));
                }

                function isDue(job) {
                    return job.status === "pending" && new Date(job.due_at) <= new Date();
                }

                function setStatus(message, isError = false) {
                    formStatus.textContent = message;
                    formStatus.classList.toggle("error", isError);
                }

                function setLoading(isLoading) {
                    createButton.disabled = isLoading;
                    refreshButton.disabled = isLoading;
                    createButton.textContent = isLoading ? "Scheduling..." : "Schedule Task";
                }

                async function fetchJson(url, options = {}) {
                    const response = await fetch(url, options);
                    const data = await response.json();
                    if (!response.ok) {
                        throw new Error(data.detail || "Request failed");
                    }
                    return data;
                }

                async function loadSummary() {
                    const summary = await fetchJson("/api/summary");
                    metricPending.textContent = summary.pending;
                    metricDue.textContent = summary.due;
                    metricUpcoming.textContent = summary.upcoming;
                    metricCompleted.textContent = summary.completed;
                    duePill.textContent = `${summary.due} due`;
                    totalPill.textContent = `${summary.total} total`;
                }

                function renderTasks(jobs) {
                    const filtered = jobs.filter((job) => {
                        if (currentFilter === "all") return true;
                        if (currentFilter === "due") return isDue(job);
                        return job.status === currentFilter;
                    });

                    taskList.innerHTML = "";
                    if (filtered.length === 0) {
                        const empty = document.createElement("div");
                        empty.className = "empty";
                        empty.textContent = "No tasks match this view. Create a task or switch filters.";
                        taskList.appendChild(empty);
                        return;
                    }

                    filtered.forEach((job) => {
                        const card = document.createElement("article");
                        card.className = "task-card";

                        const content = document.createElement("div");
                        const title = document.createElement("p");
                        title.className = "task-title";
                        title.textContent = job.content;
                        const meta = document.createElement("div");
                        meta.className = "task-meta";
                        meta.textContent = `Due ${formatDate(job.due_at)} · bucket ${job.due_bucket} · #${job.id}`;
                        content.appendChild(title);
                        content.appendChild(meta);

                        const actions = document.createElement("div");
                        const status = document.createElement("span");
                        status.className = job.status === "completed" ? "pill" : (isDue(job) ? "pill warning" : "pill muted");
                        status.textContent = job.status === "completed" ? "Completed" : (isDue(job) ? "Due now" : "Pending");
                        actions.appendChild(status);

                        if (job.status !== "completed") {
                            const complete = document.createElement("button");
                            complete.className = "button-secondary";
                            complete.type = "button";
                            complete.textContent = "Complete";
                            complete.style.marginTop = "10px";
                            complete.addEventListener("click", async () => {
                                await fetchJson(`/api/tasks/${job.id}/complete`, { method: "POST" });
                                await refresh();
                            });
                            actions.appendChild(complete);
                        }

                        card.appendChild(content);
                        card.appendChild(actions);
                        taskList.appendChild(card);
                    });
                }

                async function refresh() {
                    const data = await fetchJson("/api/tasks");
                    renderTasks(data.jobs);
                    await loadSummary();
                }

                form.addEventListener("submit", async (event) => {
                    event.preventDefault();
                    setLoading(true);
                    setStatus("");
                    try {
                        await fetchJson("/api/tasks", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({
                                content: contentInput.value.trim(),
                                due_at: toIsoFromLocal(dueInput.value)
                            })
                        });
                        setStatus("Task scheduled.");
                        contentInput.value = "";
                        dueInput.value = defaultLocalDateTime();
                        await refresh();
                    } catch (error) {
                        setStatus(error.message, true);
                    } finally {
                        setLoading(false);
                    }
                });

                refreshButton.addEventListener("click", refresh);

                filterButtons.forEach((button) => {
                    button.addEventListener("click", async () => {
                        filterButtons.forEach((item) => item.classList.remove("is-active"));
                        button.classList.add("is-active");
                        currentFilter = button.dataset.filter;
                        await refresh();
                    });
                });

                dueInput.value = defaultLocalDateTime();
                refresh().catch((error) => setStatus(error.message, true));
            </script>
        </body>
        </html>
        """
    )
