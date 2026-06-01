from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .retrieval import DOCS_DIR, INDEX_PATH, build_index, extract_answer, load_index, rank_sections


app = FastAPI(title="Knowledge Base Q&A Bot")


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)


class Source(BaseModel):
    source: str
    heading: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def serve_home() -> HTMLResponse:
    return HTMLResponse(
        """
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Knowledge Base Q&A Bot</title>
            <style>
                :root {
                    --bg: #f6f7f9;
                    --surface: #ffffff;
                    --surface-subtle: #f0f3f7;
                    --text: #172033;
                    --muted: #667085;
                    --border: #d9e0ea;
                    --primary: #176b5c;
                    --primary-hover: #11564a;
                    --accent: #285da8;
                    --warning: #9a5b13;
                    --danger: #b42318;
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
                    gap: 12px;
                    font-size: 14px;
                    font-weight: 700;
                }

                .shell {
                    width: min(1220px, calc(100% - 40px));
                    margin: 0 auto;
                    padding: 28px 0;
                    display: grid;
                    grid-template-columns: 280px minmax(0, 1fr) 320px;
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
                    justify-content: space-between;
                    gap: 12px;
                    align-items: center;
                }

                .panel-title {
                    margin: 0;
                    font-size: 14px;
                    font-weight: 800;
                }

                .panel-body {
                    padding: 18px;
                }

                .status-row {
                    display: flex;
                    justify-content: space-between;
                    gap: 14px;
                    padding: 12px 0;
                    border-bottom: 1px solid var(--border);
                    font-size: 14px;
                }

                .status-row:last-child {
                    border-bottom: 0;
                }

                .status-label {
                    color: var(--muted);
                }

                .status-value {
                    font-weight: 800;
                    text-align: right;
                }

                .badge {
                    display: inline-flex;
                    align-items: center;
                    min-height: 24px;
                    border-radius: 999px;
                    padding: 0 10px;
                    font-size: 12px;
                    font-weight: 800;
                    background: #ecfdf3;
                    color: var(--success);
                }

                .badge.warning {
                    background: #fff7e8;
                    color: var(--warning);
                }

                .docs-list {
                    margin: 14px 0 0;
                    padding: 0;
                    list-style: none;
                    display: grid;
                    gap: 8px;
                }

                .doc-item {
                    padding: 10px 12px;
                    border: 1px solid var(--border);
                    border-radius: var(--radius);
                    background: var(--surface-subtle);
                    font-size: 13px;
                    font-weight: 700;
                    overflow-wrap: anywhere;
                }

                .workspace {
                    min-height: 680px;
                    display: grid;
                    grid-template-rows: auto 1fr auto;
                }

                .answer-feed {
                    padding: 18px;
                    display: grid;
                    gap: 14px;
                    align-content: start;
                    min-height: 430px;
                    max-height: 560px;
                    overflow-y: auto;
                }

                .message {
                    max-width: 82%;
                    padding: 14px 16px;
                    border-radius: var(--radius);
                    line-height: 1.55;
                    font-size: 15px;
                    border: 1px solid var(--border);
                    white-space: pre-wrap;
                }

                .message.user {
                    justify-self: end;
                    background: #eaf1fb;
                }

                .message.assistant {
                    justify-self: start;
                    background: #ffffff;
                }

                .message.empty {
                    max-width: 100%;
                    width: 100%;
                    background: #fbfcfe;
                    color: var(--muted);
                }

                .composer {
                    border-top: 1px solid var(--border);
                    padding: 16px;
                    background: #fbfcfe;
                    display: grid;
                    gap: 10px;
                }

                .textarea-wrap {
                    display: grid;
                    gap: 8px;
                }

                label {
                    font-size: 13px;
                    font-weight: 800;
                    color: #344054;
                }

                textarea {
                    width: 100%;
                    min-height: 104px;
                    resize: vertical;
                    border: 1px solid var(--border);
                    border-radius: var(--radius);
                    padding: 12px 14px;
                    font: inherit;
                    line-height: 1.5;
                    color: var(--text);
                    background: #ffffff;
                }

                textarea:focus {
                    outline: 3px solid rgba(40, 93, 168, 0.16);
                    border-color: var(--accent);
                }

                .composer-actions {
                    display: flex;
                    justify-content: space-between;
                    gap: 10px;
                    align-items: center;
                    flex-wrap: wrap;
                }

                .button-row {
                    display: flex;
                    gap: 10px;
                    flex-wrap: wrap;
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
                    opacity: 0.6;
                    cursor: not-allowed;
                }

                .button-primary {
                    color: #ffffff;
                    background: var(--primary);
                }

                .button-primary:hover {
                    background: var(--primary-hover);
                }

                .button-secondary,
                .sample-button {
                    color: var(--text);
                    background: #ffffff;
                    border: 1px solid var(--border);
                }

                .inline-status {
                    min-height: 22px;
                    color: var(--muted);
                    font-size: 13px;
                }

                .inline-status.error {
                    color: var(--danger);
                }

                .source-list,
                .sample-list {
                    display: grid;
                    gap: 10px;
                }

                .source-card {
                    padding: 12px;
                    border: 1px solid var(--border);
                    border-radius: var(--radius);
                    background: #fbfcfe;
                }

                .source-heading {
                    margin: 0 0 6px;
                    font-size: 13px;
                    font-weight: 800;
                    overflow-wrap: anywhere;
                }

                .source-meta {
                    color: var(--muted);
                    font-size: 12px;
                    line-height: 1.5;
                }

                .sample-button {
                    width: 100%;
                    min-height: 0;
                    text-align: left;
                    padding: 10px 12px;
                    font-weight: 700;
                    line-height: 1.35;
                }

                @media (max-width: 1060px) {
                    .shell {
                        grid-template-columns: 1fr;
                    }

                    .workspace {
                        min-height: 0;
                    }

                    .answer-feed {
                        max-height: none;
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
                        width: min(100% - 24px, 1220px);
                        padding: 18px 0;
                    }

                    .message {
                        max-width: 100%;
                    }
                }
            </style>
        </head>
        <body>
            <header class="topbar">
                <div class="brand">
                    <div class="brand-mark" aria-hidden="true">KB</div>
                    <span>Knowledge Base Q&A</span>
                </div>
                <nav class="top-actions" aria-label="Utilities">
                    <a href="/docs">API Docs</a>
                    <a href="/health">Health</a>
                </nav>
            </header>

            <main class="shell">
                <aside class="panel" aria-label="Knowledge base status">
                    <div class="panel-header">
                        <h2 class="panel-title">Knowledge Base</h2>
                        <span class="badge warning" id="index-badge">Checking</span>
                    </div>
                    <div class="panel-body">
                        <div class="status-row">
                            <span class="status-label">Documents</span>
                            <span class="status-value" id="docs-count">0</span>
                        </div>
                        <div class="status-row">
                            <span class="status-label">Indexed sections</span>
                            <span class="status-value" id="sections-count">0</span>
                        </div>
                        <div class="status-row">
                            <span class="status-label">Answer mode</span>
                            <span class="status-value">Local</span>
                        </div>
                        <ul class="docs-list" id="docs-list"></ul>
                        <div style="margin-top: 16px;">
                            <button class="button-primary" id="index-button" type="button">Rebuild Index</button>
                        </div>
                    </div>
                </aside>

                <section class="panel workspace" aria-label="Question and answer workspace">
                    <div class="panel-header">
                        <h1 class="panel-title">Ask the knowledge base</h1>
                        <span class="badge" id="mode-badge">No paid API</span>
                    </div>
                    <div class="answer-feed" id="answer-feed">
                        <div class="message empty">Ask a question after the index is ready. Answers are extracted from local Markdown sources.</div>
                    </div>
                    <form class="composer" id="chat-form">
                        <div class="textarea-wrap">
                            <label for="question-input">Question</label>
                            <textarea id="question-input" required>Does this require paid APIs?</textarea>
                        </div>
                        <div class="composer-actions">
                            <div class="inline-status" id="status" role="status" aria-live="polite"></div>
                            <div class="button-row">
                                <button class="button-secondary" id="clear-button" type="button">Clear</button>
                                <button class="button-primary" id="ask-button" type="submit">Ask</button>
                            </div>
                        </div>
                    </form>
                </section>

                <aside class="panel" aria-label="Retrieved sources">
                    <div class="panel-header">
                        <h2 class="panel-title">Sources</h2>
                        <span class="badge warning" id="source-count">0</span>
                    </div>
                    <div class="panel-body">
                        <div class="source-list" id="source-list">
                            <div class="source-card">
                                <p class="source-heading">No sources yet</p>
                                <div class="source-meta">Sources appear after a grounded answer.</div>
                            </div>
                        </div>
                    </div>
                    <div class="panel-header">
                        <h2 class="panel-title">Sample Questions</h2>
                    </div>
                    <div class="panel-body">
                        <div class="sample-list">
                            <button class="sample-button" type="button" data-question="Does this require paid APIs?">Does this require paid APIs?</button>
                            <button class="sample-button" type="button" data-question="How does Markdown KB retrieval work?">How does Markdown KB retrieval work?</button>
                            <button class="sample-button" type="button" data-question="How are answers cited?">How are answers cited?</button>
                        </div>
                    </div>
                </aside>
            </main>

            <script>
                const indexBadge = document.getElementById("index-badge");
                const docsCount = document.getElementById("docs-count");
                const sectionsCount = document.getElementById("sections-count");
                const docsList = document.getElementById("docs-list");
                const indexButton = document.getElementById("index-button");
                const chatForm = document.getElementById("chat-form");
                const questionInput = document.getElementById("question-input");
                const answerFeed = document.getElementById("answer-feed");
                const statusText = document.getElementById("status");
                const askButton = document.getElementById("ask-button");
                const clearButton = document.getElementById("clear-button");
                const sourceList = document.getElementById("source-list");
                const sourceCount = document.getElementById("source-count");

                function setStatus(message, isError = false) {
                    statusText.textContent = message;
                    statusText.classList.toggle("error", isError);
                }

                function setWorking(isWorking) {
                    askButton.disabled = isWorking;
                    indexButton.disabled = isWorking;
                    askButton.textContent = isWorking ? "Searching..." : "Ask";
                }

                function renderMetadata(metadata) {
                    docsCount.textContent = metadata.documents.length;
                    sectionsCount.textContent = metadata.indexed_sections;
                    indexBadge.textContent = metadata.index_exists ? "Indexed" : "Not indexed";
                    indexBadge.classList.toggle("warning", !metadata.index_exists);
                    docsList.innerHTML = "";

                    if (metadata.documents.length === 0) {
                        const item = document.createElement("li");
                        item.className = "doc-item";
                        item.textContent = "No Markdown files found";
                        docsList.appendChild(item);
                        return;
                    }

                    metadata.documents.forEach((doc) => {
                        const item = document.createElement("li");
                        item.className = "doc-item";
                        item.textContent = doc;
                        docsList.appendChild(item);
                    });
                }

                async function refreshMetadata() {
                    const response = await fetch("/metadata");
                    const metadata = await response.json();
                    renderMetadata(metadata);
                }

                function addMessage(text, kind) {
                    const message = document.createElement("div");
                    message.className = `message ${kind}`;
                    message.textContent = text;
                    const empty = answerFeed.querySelector(".empty");
                    if (empty) {
                        empty.remove();
                    }
                    answerFeed.appendChild(message);
                    answerFeed.scrollTop = answerFeed.scrollHeight;
                }

                function renderSources(sources) {
                    sourceList.innerHTML = "";
                    sourceCount.textContent = sources.length;
                    sourceCount.classList.toggle("warning", sources.length === 0);

                    if (sources.length === 0) {
                        const empty = document.createElement("div");
                        empty.className = "source-card";
                        empty.innerHTML = '<p class="source-heading">No matching source</p><div class="source-meta">The answer was not grounded in an indexed section.</div>';
                        sourceList.appendChild(empty);
                        return;
                    }

                    sources.forEach((source) => {
                        const card = document.createElement("div");
                        card.className = "source-card";
                        const heading = document.createElement("p");
                        heading.className = "source-heading";
                        heading.textContent = source.heading;
                        const filename = document.createElement("div");
                        filename.className = "source-meta";
                        filename.textContent = source.source;
                        const score = document.createElement("div");
                        score.className = "source-meta";
                        score.textContent = `Score ${source.score}`;
                        card.appendChild(heading);
                        card.appendChild(filename);
                        card.appendChild(score);
                        sourceList.appendChild(card);
                    });
                }

                indexButton.addEventListener("click", async () => {
                    setWorking(true);
                    setStatus("Indexing local Markdown files...");
                    try {
                        const response = await fetch("/index", { method: "POST" });
                        const data = await response.json();
                        if (!response.ok) {
                            throw new Error(data.detail || "Indexing failed");
                        }
                        setStatus(`Indexed ${data.count} sections.`);
                        await refreshMetadata();
                    } catch (error) {
                        setStatus(error.message, true);
                    } finally {
                        setWorking(false);
                    }
                });

                chatForm.addEventListener("submit", async (event) => {
                    event.preventDefault();
                    const question = questionInput.value.trim();
                    if (!question) {
                        setStatus("Question is required.", true);
                        return;
                    }

                    addMessage(question, "user");
                    setWorking(true);
                    setStatus("Searching indexed sections...");

                    try {
                        const response = await fetch("/chat", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ question })
                        });
                        const data = await response.json();
                        if (!response.ok) {
                            throw new Error(data.detail || "Question failed");
                        }
                        addMessage(data.answer, "assistant");
                        renderSources(data.sources);
                        setStatus(data.sources.length ? "Grounded answer returned." : "No grounded source found.");
                    } catch (error) {
                        setStatus(error.message, true);
                    } finally {
                        setWorking(false);
                    }
                });

                clearButton.addEventListener("click", () => {
                    answerFeed.innerHTML = '<div class="message empty">Ask a question after the index is ready. Answers are extracted from local Markdown sources.</div>';
                    renderSources([]);
                    setStatus("");
                    questionInput.focus();
                });

                document.querySelectorAll("[data-question]").forEach((button) => {
                    button.addEventListener("click", () => {
                        questionInput.value = button.dataset.question;
                        questionInput.focus();
                    });
                });

                refreshMetadata().catch(() => {
                    setStatus("Could not load metadata.", true);
                });
            </script>
        </body>
        </html>
        """
    )


@app.get("/metadata")
def metadata() -> dict:
    documents = [path.name for path in sorted(DOCS_DIR.glob("*.md"))] if DOCS_DIR.exists() else []
    sections = load_index()
    return {
        "documents": documents,
        "indexed_sections": len(sections),
        "index_exists": INDEX_PATH.exists(),
    }


@app.post("/index")
def index_documents() -> dict:
    sections = build_index()
    return {"status": "indexed", "count": len(sections)}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    sections = load_index()
    if not sections:
        return ChatResponse(answer="Knowledge base is empty. Run /index first.", sources=[])

    ranked_sections = rank_sections(request.question, sections)
    if not ranked_sections:
        return ChatResponse(answer="I cannot confirm the answer from the knowledge base.", sources=[])

    answer = extract_answer(request.question, ranked_sections)
    sources = [
        Source(source=section["source"], heading=section["heading"], score=section["score"])
        for section in ranked_sections
    ]
    return ChatResponse(answer=answer, sources=sources)
