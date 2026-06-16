from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .repository import initialize_database
from .routes import router


app = FastAPI(title="QR Code Generator")
app.include_router(router)
initialize_database()


@app.on_event("startup")
def startup() -> None:
    initialize_database()


@app.get("/", response_class=HTMLResponse)
def serve_home() -> HTMLResponse:
    return HTMLResponse(
        """
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>QR Code Generator</title>
            <style>
                :root {
                    --background: #f7f8fb;
                    --surface: #ffffff;
                    --surface-muted: #f1f4f8;
                    --text: #172033;
                    --muted: #667085;
                    --border: #d8dee8;
                    --primary: #176b5c;
                    --primary-hover: #11564a;
                    --accent: #2557a7;
                    --danger: #b42318;
                    --shadow: 0 16px 40px rgba(23, 32, 51, 0.10);
                    --radius: 8px;
                }

                * {
                    box-sizing: border-box;
                }

                body {
                    margin: 0;
                    min-height: 100vh;
                    background: var(--background);
                    color: var(--text);
                    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                    letter-spacing: 0;
                }

                a {
                    color: var(--accent);
                }

                .app-shell {
                    min-height: 100vh;
                    display: grid;
                    grid-template-rows: auto 1fr;
                }

                .topbar {
                    height: 64px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 0 32px;
                    background: var(--surface);
                    border-bottom: 1px solid var(--border);
                }

                .brand {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    font-weight: 700;
                }

                .brand-mark {
                    width: 34px;
                    height: 34px;
                    display: grid;
                    place-items: center;
                    border-radius: 8px;
                    background: var(--text);
                    color: #ffffff;
                    font-size: 14px;
                    line-height: 1;
                }

                .nav-link {
                    font-size: 14px;
                    font-weight: 600;
                    text-decoration: none;
                }

                .workspace {
                    width: min(1120px, calc(100% - 40px));
                    margin: 0 auto;
                    padding: 48px 0;
                    display: grid;
                    grid-template-columns: minmax(0, 1fr) 390px;
                    gap: 24px;
                    align-items: start;
                }

                .hero-copy {
                    margin-bottom: 22px;
                }

                h1 {
                    margin: 0 0 10px;
                    font-size: 40px;
                    line-height: 1.08;
                    letter-spacing: 0;
                }

                .lede {
                    margin: 0;
                    max-width: 680px;
                    color: var(--muted);
                    font-size: 16px;
                    line-height: 1.6;
                }

                .panel {
                    background: var(--surface);
                    border: 1px solid var(--border);
                    border-radius: var(--radius);
                    box-shadow: var(--shadow);
                }

                .form-panel {
                    padding: 24px;
                }

                .field {
                    display: grid;
                    gap: 8px;
                    margin-bottom: 16px;
                }

                label {
                    font-size: 13px;
                    font-weight: 700;
                    color: #344054;
                }

                input {
                    width: 100%;
                    min-height: 48px;
                    border: 1px solid var(--border);
                    border-radius: var(--radius);
                    padding: 12px 14px;
                    font-size: 15px;
                    color: var(--text);
                    background: #ffffff;
                }

                input:focus {
                    outline: 3px solid rgba(37, 87, 167, 0.18);
                    border-color: var(--accent);
                }

                .actions {
                    display: flex;
                    gap: 10px;
                    flex-wrap: wrap;
                    align-items: center;
                }

                button {
                    min-height: 44px;
                    border: 0;
                    border-radius: var(--radius);
                    padding: 0 16px;
                    font-size: 14px;
                    font-weight: 700;
                    cursor: pointer;
                }

                .button-primary {
                    background: var(--primary);
                    color: #ffffff;
                }

                .button-primary:hover {
                    background: var(--primary-hover);
                }

                .button-secondary {
                    background: var(--surface-muted);
                    color: var(--text);
                    border: 1px solid var(--border);
                }

                button:disabled {
                    cursor: not-allowed;
                    opacity: 0.65;
                }

                .status {
                    min-height: 22px;
                    margin-top: 14px;
                    color: var(--muted);
                    font-size: 14px;
                }

                .status.error {
                    color: var(--danger);
                }

                .preview-panel {
                    overflow: hidden;
                }

                .preview-header {
                    padding: 18px 20px;
                    border-bottom: 1px solid var(--border);
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    gap: 12px;
                }

                .preview-title {
                    margin: 0;
                    font-size: 15px;
                    font-weight: 800;
                }

                .preview-state {
                    color: var(--muted);
                    font-size: 13px;
                }

                .qr-frame {
                    padding: 24px;
                    display: grid;
                    place-items: center;
                    background: #fbfcfe;
                    min-height: 340px;
                }

                .empty-preview {
                    width: 220px;
                    aspect-ratio: 1;
                    border: 1px dashed #b9c2d0;
                    border-radius: var(--radius);
                    display: grid;
                    place-items: center;
                    color: var(--muted);
                    font-weight: 700;
                    background: #ffffff;
                }

                .qr-image {
                    width: min(260px, 100%);
                    aspect-ratio: 1;
                    object-fit: contain;
                    border: 1px solid var(--border);
                    border-radius: var(--radius);
                    background: #ffffff;
                    padding: 12px;
                }

                .result-details {
                    display: none;
                    border-top: 1px solid var(--border);
                    padding: 18px 20px 20px;
                    gap: 12px;
                }

                .result-details.is-visible {
                    display: grid;
                }

                .detail-row {
                    display: grid;
                    gap: 6px;
                }

                .detail-label {
                    color: var(--muted);
                    font-size: 12px;
                    font-weight: 700;
                    text-transform: uppercase;
                }

                .detail-value {
                    overflow-wrap: anywhere;
                    font-size: 14px;
                    line-height: 1.5;
                }

                @media (max-width: 860px) {
                    .topbar {
                        padding: 0 20px;
                    }

                    .workspace {
                        grid-template-columns: 1fr;
                        padding: 32px 0;
                    }

                    h1 {
                        font-size: 32px;
                    }
                }
            </style>
        </head>
        <body>
            <div class="app-shell">
                <header class="topbar">
                    <div class="brand" aria-label="QR Code Generator">
                        <div class="brand-mark" aria-hidden="true">QR</div>
                        <span>QR Code Generator</span>
                    </div>
                    <a class="nav-link" href="/docs">API Docs</a>
                </header>

                <main class="workspace">
                    <section>
                        <div class="hero-copy">
                            <h1>Generate a trackable QR destination.</h1>
                            <p class="lede">Create a short redirect link and QR code in one flow. The result appears instantly in this workspace.</p>
                        </div>

                        <form class="panel form-panel" id="qr-form">
                            <div class="field">
                                <label for="url-input">Destination URL</label>
                                <input
                                    id="url-input"
                                    name="url"
                                    type="url"
                                    value="https://github.com/cdexswzaq0110"
                                    placeholder="https://github.com/cdexswzaq0110"
                                    autocomplete="url"
                                    required
                                >
                            </div>

                            <div class="field">
                                <label for="expires-input">Expiration ISO datetime</label>
                                <input
                                    id="expires-input"
                                    name="expires_at"
                                    type="text"
                                    placeholder="Optional"
                                    autocomplete="off"
                                >
                            </div>

                            <div class="actions">
                                <button class="button-primary" id="generate-button" type="submit">Generate QR Code</button>
                                <button class="button-secondary" id="reset-button" type="button">Reset</button>
                            </div>
                            <div class="status" id="status" role="status" aria-live="polite"></div>
                        </form>
                    </section>

                    <aside class="panel preview-panel" aria-label="QR code result">
                        <div class="preview-header">
                            <p class="preview-title">Preview</p>
                            <span class="preview-state" id="preview-state">Ready</span>
                        </div>
                        <div class="qr-frame" id="qr-frame">
                            <div class="empty-preview" id="empty-preview">QR</div>
                        </div>
                        <div class="result-details" id="result-details">
                            <div class="detail-row">
                                <span class="detail-label">Short URL</span>
                                <a class="detail-value" id="short-url" href="#"></a>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Destination</span>
                                <a class="detail-value" id="target-url" href="#"></a>
                            </div>
                            <div class="detail-row">
                                <span class="detail-label">Token</span>
                                <span class="detail-value" id="token-value"></span>
                            </div>
                        </div>
                    </aside>
                </main>
            </div>

            <script>
                const form = document.getElementById("qr-form");
                const urlInput = document.getElementById("url-input");
                const expiresInput = document.getElementById("expires-input");
                const button = document.getElementById("generate-button");
                const resetButton = document.getElementById("reset-button");
                const status = document.getElementById("status");
                const previewState = document.getElementById("preview-state");
                const qrFrame = document.getElementById("qr-frame");
                const resultDetails = document.getElementById("result-details");
                const shortUrl = document.getElementById("short-url");
                const targetUrl = document.getElementById("target-url");
                const tokenValue = document.getElementById("token-value");

                function setStatus(message, isError = false) {
                    status.textContent = message;
                    status.classList.toggle("error", isError);
                }

                function setLoading(isLoading) {
                    button.disabled = isLoading;
                    button.textContent = isLoading ? "Generating..." : "Generate QR Code";
                    previewState.textContent = isLoading ? "Working" : "Ready";
                }

                function clearResult() {
                    qrFrame.innerHTML = '<div class="empty-preview" id="empty-preview">QR</div>';
                    resultDetails.classList.remove("is-visible");
                    shortUrl.removeAttribute("href");
                    shortUrl.textContent = "";
                    targetUrl.removeAttribute("href");
                    targetUrl.textContent = "";
                    tokenValue.textContent = "";
                    setStatus("");
                    previewState.textContent = "Ready";
                }

                function renderResult(data) {
                    const qrAbsoluteUrl = `${window.location.origin}${data.qr_url}`;
                    const shortAbsoluteUrl = `${window.location.origin}${data.short_url}`;

                    const image = document.createElement("img");
                    image.className = "qr-image";
                    image.src = `${qrAbsoluteUrl}?v=${encodeURIComponent(data.token)}`;
                    image.alt = `QR code for ${data.url}`;

                    qrFrame.innerHTML = "";
                    qrFrame.appendChild(image);

                    shortUrl.href = shortAbsoluteUrl;
                    shortUrl.textContent = shortAbsoluteUrl;
                    targetUrl.href = data.url;
                    targetUrl.textContent = data.url;
                    tokenValue.textContent = data.token;
                    resultDetails.classList.add("is-visible");
                    previewState.textContent = "Generated";
                    setStatus("QR code generated.");
                }

                form.addEventListener("submit", async (event) => {
                    event.preventDefault();
                    setLoading(true);
                    setStatus("");

                    const payload = {
                        url: urlInput.value.trim(),
                        expires_at: expiresInput.value.trim() || null
                    };

                    try {
                        const response = await fetch("/links", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify(payload)
                        });

                        const data = await response.json();
                        if (!response.ok) {
                            throw new Error(data.detail || "Could not generate QR code");
                        }

                        renderResult(data);
                    } catch (error) {
                        previewState.textContent = "Error";
                        setStatus(error.message, true);
                    } finally {
                        setLoading(false);
                    }
                });

                resetButton.addEventListener("click", () => {
                    urlInput.value = "https://github.com/cdexswzaq0110";
                    expiresInput.value = "";
                    clearResult();
                    urlInput.focus();
                });
            </script>
        </body>
        </html>
        """
    )
