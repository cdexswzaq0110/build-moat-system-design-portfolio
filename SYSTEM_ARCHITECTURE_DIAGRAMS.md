# 三個專案的系統設計架構圖

> Accuracy note: 以下不是宣稱來自任何大廠內部文件，而是依照常見系統設計實務整理：清楚邊界、資料所有權、狀態流、可靠性、安全性、可觀測性與可擴展性。

## 1. QR Code Generator

### 核心設計重點

- 問題本質：把一個外部 URL 轉成可分享的短網址與 QR Code。
- 核心資料：`links(token, target_url, created_at, expires_at)`。
- 核心原則：公開 token 不能可預測；Redirect 前必須驗證 token 與過期狀態；使用者輸入 URL 不能直接信任。
- MVP 邊界：FastAPI + SQLite + 即時產生 PNG；不做帳號、分析、網域管理、風險掃描。

```mermaid
flowchart TD
    U["使用者 / Browser UI"]
    API["FastAPI API Boundary"]
    Create["POST /links\n建立短連結"]
    Validate["URL Validator\n- 只允許 http/https\n- 必須有 host\n- 移除 fragment\n- 阻擋 localhost/private IP"]
    Token["Token Generator\nsecrets + A-Z/a-z/0-9\n預設長度 8\n最多重試 5 次"]
    DB[("SQLite\nlinks table\nPK: token")]
    Result["回傳\nshort_url: /r/{token}\nqr_url: /qr/{token}.png"]

    QR["GET /qr/{token}.png\n產生 QR PNG"]
    Redirect["GET /r/{token}\n短網址跳轉"]
    Lookup["find_link(token)"]
    Expiry{"是否過期?"}
    NotFound["404 Not Found\n未知 token"]
    Gone["410 Gone\n已過期 token"]
    PNG["qrcode.make(target_url)\nPNG Response"]
    Target["307 Redirect\ntarget_url"]

    Security["安全核心思考\n不要讓服務變成\n內網探測 / 開放跳轉濫用工具"]
    Scale["未來生產級擴展\nPostgres / Redis cache\nrate limit / abuse scan\nanalytics / custom domain\ncollision metrics"]

    U --> API
    API --> Create
    Create --> Validate
    Validate --> Token
    Token --> DB
    DB --> Result
    Result --> U

    U --> QR
    U --> Redirect
    QR --> Lookup
    Redirect --> Lookup
    Lookup --> DB
    DB -->|不存在| NotFound
    DB -->|存在| Expiry
    Expiry -->|是| Gone
    Expiry -->|否, QR path| PNG
    Expiry -->|否, redirect path| Target

    Validate -. protects .-> Security
    Token -. protects .-> Security
    DB -. evolves to .-> Scale
```

### 工作流

```text
輸入 URL
→ 驗證 URL 安全性
→ 產生不可預測 token
→ 寫入 SQLite
→ 回傳短網址與 QR 圖片網址
→ 使用者掃 QR 或打開短網址
→ 系統查 token
→ 不存在回 404，過期回 410，正常則回 PNG 或 307 redirect
```

## 2. Knowledge Base Q&A Bot

### 核心設計重點

- 問題本質：只根據本機 Markdown 知識庫回答問題，不憑空猜。
- 核心資料：`docs/sample/*.md` 與 `.kb/index.json`。
- 核心原則：先檢索，再回答；答案必須有來源；找不到證據就拒答。
- MVP 邊界：關鍵字檢索與抽取式答案；不使用付費 API、不使用外部生成服務、不使用向量資料庫。

```mermaid
flowchart TD
    U["使用者 / Browser UI"]
    API["FastAPI API Boundary"]

    Meta["GET /metadata\n文件數 / section 數 / index 狀態"]
    IndexAPI["POST /index\n重建索引"]
    Docs["docs/sample/*.md\n本機 Markdown"]
    Split["split_markdown_sections()\n依 heading 切 section"]
    IndexFile[(".kb/index.json\n可讀、可除錯的 section index")]

    Chat["POST /chat\nquestion"]
    Load["load_index()"]
    Tokenize["tokenize_meaningful()\n小寫化 / 移除 stopwords"]
    Rank["rank_sections()\nterm frequency + IDF-like score\nscore >= 2.0\nlimit 3"]
    HasEvidence{"有足夠 section?"}
    Extract["extract_answer()\n從命中 section 抽句子"]
    Sources["sources\nsource + heading + score"]
    Answer["Grounded Answer\n答案 + 引用來源"]
    Refuse["拒答\nI cannot confirm the answer\nfrom the knowledge base."]

    Principle["核心思考\nGroundedness > 流暢度\n可追溯來源 > 看似聰明"]
    Future["未來生產級擴展\nline-level citation\nSQLite/Postgres/Search Engine\nlocal embeddings / hybrid search\neval set / reranker / feedback"]

    U --> API
    API --> Meta
    API --> IndexAPI
    API --> Chat

    Meta --> Docs
    Meta --> IndexFile

    IndexAPI --> Docs
    Docs --> Split
    Split --> IndexFile

    Chat --> Load
    Load --> IndexFile
    Load --> Tokenize
    Tokenize --> Rank
    Rank --> HasEvidence
    HasEvidence -->|否| Refuse
    HasEvidence -->|是| Extract
    Extract --> Answer
    Rank --> Sources
    Sources --> Answer

    Rank -. enforces .-> Principle
    Refuse -. enforces .-> Principle
    IndexFile -. evolves to .-> Future
```

### 工作流

```text
Rebuild Index
→ 讀取 Markdown
→ 依標題切成可引用 section
→ 寫入 .kb/index.json

Ask Question
→ 載入 index
→ 將問題 tokenize
→ 對 section 計分排序
→ 分數不足就拒答
→ 分數足夠就抽取答案句子
→ 回傳答案與 source / heading / score
```

## 3. Task Scheduler

### 核心設計重點

- 問題本質：管理「何時該做」的工作，而不是直接執行所有工作。
- 核心資料：`jobs(id, content, due_at, due_bucket, status, created_at)`。
- 核心原則：排程時間、任務狀態、到期掃描要分開；查 due job 不能每次全表掃描。
- MVP 邊界：FastAPI + SQLite + Web UI；MCP 是可選入口；Queue / Worker 是設計方向但目前未實作。

```mermaid
flowchart TD
    U["使用者 / Browser UI"]
    HTTP["HTTP API"]
    MCP["Optional MCP Server\ntask.create / task.list\ntask.get / task.complete"]
    API["FastAPI API Boundary"]

    Create["POST /api/tasks\ncreate_job(content, due_at)"]
    Parse["parse_iso_datetime()\n統一轉 UTC"]
    Bucket["get_time_bucket()\nminute bucket: YYYYMMDDHHMM"]
    DB[("SQLite jobs table\nid / content / due_at\ndue_bucket / status / created_at\nindex: due_bucket + status")]

    List["GET /api/tasks\n依狀態列出"]
    Due["GET /api/tasks/due\nfind_due_jobs(now)"]
    Summary["GET /api/summary\npending / due / upcoming / completed"]
    Complete["POST /api/tasks/{id}/complete\nstatus -> completed"]
    State{"Job State Machine"}
    Pending["pending"]
    Completed["completed"]

    FutureCron["未來 Cron / Scheduler\n每分鐘喚醒"]
    Watcher["Watcher\n掃描 due_bucket <= now_bucket\n且 due_at <= now"]
    Queue["Durable Queue\nRedis / SQS\nretry / backpressure"]
    Worker["Worker\n執行任務\nidempotency key"]

    Principle["核心思考\nCron 決定何時醒來\nWatcher 決定哪些 job 到期\nWorker 決定如何執行"]
    Scale["未來生產級擴展\npartition by time bucket\nretry policy / dead letter queue\nobservability / permissions\nmulti-interface over same domain"]

    U --> HTTP
    HTTP --> API
    MCP --> API

    API --> Create
    Create --> Parse
    Parse --> Bucket
    Bucket --> DB
    DB --> List
    DB --> Due
    DB --> Summary
    DB --> Complete

    Create --> Pending
    Complete --> Completed
    Pending --> State
    Completed --> State

    FutureCron -. production direction .-> Watcher
    Watcher -. scans .-> DB
    Watcher -. enqueue .-> Queue
    Queue -. consume .-> Worker

    Due -. MVP equivalent of watcher scan .-> Watcher
    Bucket -. avoids full scan .-> Principle
    Watcher -. separation of concerns .-> Principle
    Queue -. evolves to .-> Scale
```

### 工作流

```text
建立任務
→ 驗證 content 與 due_at
→ due_at 統一轉 UTC
→ 建立 minute-level due_bucket
→ 寫入 jobs，狀態為 pending

查詢到期任務
→ 取得 now
→ 轉成 current_bucket
→ 查 status = pending 且 due_bucket <= current_bucket 且 due_at <= now
→ 回傳 due jobs

完成任務
→ 用 job id 查詢
→ status 改為 completed
→ summary 重新計算 pending / completed / due / upcoming
```

