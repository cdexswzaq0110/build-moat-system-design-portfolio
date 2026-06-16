HOME_HTML = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Task Scheduler</title>
    <style>
        :root {
            --color-bg: #f7f8fb;
            --color-surface: #ffffff;
            --color-surface-muted: #f2f4f8;
            --color-sidebar: #0f172a;
            --color-border: #d9dee8;
            --color-border-strong: #b8c1d1;
            --color-text: #111827;
            --color-text-muted: #667085;
            --color-primary: #4f46e5;
            --color-primary-soft: #eef2ff;
            --color-success: #067647;
            --color-success-soft: #ecfdf3;
            --color-warning: #b54708;
            --color-warning-soft: #fffaeb;
            --color-danger: #b42318;
            --color-danger-soft: #fef3f2;
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.05);
            --shadow-md: 0 16px 36px rgba(15, 23, 42, 0.08);
            --space-1: 4px;
            --space-2: 8px;
            --space-3: 12px;
            --space-4: 16px;
            --space-5: 20px;
            --space-6: 24px;
            --font-sans: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        * { box-sizing: border-box; }

        body {
            margin: 0;
            min-height: 100vh;
            background: var(--color-bg);
            color: var(--color-text);
            font-family: var(--font-sans);
            letter-spacing: 0;
        }

        a { color: inherit; text-decoration: none; }
        button, input, textarea, select { font: inherit; }
        button { border: 0; cursor: pointer; }
        button:disabled { cursor: not-allowed; opacity: 0.55; }
        :focus-visible { outline: 3px solid rgba(79, 70, 229, 0.24); outline-offset: 2px; }

        .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }

        .app-shell {
            min-height: 100vh;
            display: grid;
            grid-template-columns: 248px minmax(0, 1fr);
        }

        .sidebar {
            position: sticky;
            top: 0;
            height: 100vh;
            display: flex;
            flex-direction: column;
            gap: var(--space-5);
            padding: var(--space-5);
            background: var(--color-sidebar);
            color: #dbe4f0;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: var(--space-3);
            color: #ffffff;
            font-weight: 820;
        }

        .brand-mark {
            display: grid;
            place-items: center;
            width: 36px;
            height: 36px;
            border-radius: 11px;
            background: linear-gradient(135deg, #6366f1, #22c55e);
            font-size: 13px;
            font-weight: 900;
        }

        .side-section-label {
            margin: var(--space-2) 0 0;
            color: #8da2bd;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .side-nav {
            display: grid;
            gap: var(--space-1);
        }

        .side-link {
            min-height: 38px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: var(--space-3);
            border-radius: var(--radius-md);
            padding: 0 11px;
            color: #cbd5e1;
            font-size: 14px;
            font-weight: 720;
        }

        .side-link:hover,
        .side-link.is-active {
            background: rgba(255, 255, 255, 0.09);
            color: #ffffff;
        }

        .side-count {
            color: #93a4ba;
            font-size: 12px;
        }

        .developer-panel {
            margin-top: auto;
            border-top: 1px solid rgba(255, 255, 255, 0.10);
            padding-top: var(--space-4);
        }

        .developer-panel summary {
            cursor: pointer;
            color: #cbd5e1;
            font-size: 13px;
            font-weight: 760;
        }

        .developer-links {
            display: grid;
            gap: var(--space-2);
            margin-top: var(--space-3);
        }

        .developer-links a {
            color: #93c5fd;
            font-size: 13px;
            font-weight: 700;
        }

        .main {
            min-width: 0;
            display: grid;
            grid-template-rows: auto 1fr;
        }

        .topbar {
            position: sticky;
            top: 0;
            z-index: 5;
            min-height: 68px;
            display: grid;
            grid-template-columns: minmax(220px, 460px) auto;
            gap: var(--space-4);
            align-items: center;
            padding: 0 var(--space-6);
            background: rgba(247, 248, 251, 0.86);
            border-bottom: 1px solid var(--color-border);
            backdrop-filter: blur(14px);
        }

        .search-wrap {
            position: relative;
        }

        .search-wrap input {
            width: 100%;
            min-height: 42px;
            border: 1px solid var(--color-border);
            border-radius: 999px;
            padding: 0 14px 0 40px;
            background: var(--color-surface);
            color: var(--color-text);
        }

        .search-prefix {
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--color-text-muted);
            font-size: 13px;
            font-weight: 900;
        }

        .top-actions {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: var(--space-3);
        }

        .workspace-chip {
            display: inline-flex;
            align-items: center;
            gap: var(--space-2);
            min-height: 38px;
            border: 1px solid var(--color-border);
            border-radius: 999px;
            padding: 0 12px;
            background: var(--color-surface);
            color: var(--color-text-muted);
            font-size: 13px;
            font-weight: 750;
        }

        .live-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #22c55e;
            box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.14);
        }

        .avatar {
            display: grid;
            place-items: center;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: #111827;
            color: #ffffff;
            font-size: 13px;
            font-weight: 900;
        }

        .page {
            display: grid;
            gap: var(--space-5);
            padding: var(--space-6);
        }

        .page-header {
            display: flex;
            justify-content: space-between;
            gap: var(--space-4);
            align-items: flex-start;
        }

        .page-kicker {
            color: var(--color-text-muted);
            font-size: 13px;
            font-weight: 760;
        }

        h1 {
            margin: 4px 0 0;
            font-size: 28px;
            line-height: 1.15;
            letter-spacing: -0.01em;
        }

        .page-subtitle {
            margin: var(--space-2) 0 0;
            color: var(--color-text-muted);
            line-height: 1.5;
        }

        .header-meta {
            display: flex;
            align-items: center;
            gap: var(--space-3);
            flex-wrap: wrap;
            justify-content: flex-end;
        }

        .date-pill {
            min-height: 40px;
            display: inline-flex;
            align-items: center;
            border: 1px solid var(--color-border);
            border-radius: 999px;
            padding: 0 13px;
            background: var(--color-surface);
            color: var(--color-text-muted);
            font-size: 13px;
            font-weight: 760;
        }

        .button {
            min-height: 40px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: var(--space-2);
            border-radius: var(--radius-md);
            padding: 0 14px;
            font-size: 13px;
            font-weight: 820;
        }

        .button-primary {
            background: var(--color-primary);
            color: #ffffff;
            box-shadow: var(--shadow-sm);
        }

        .button-secondary {
            border: 1px solid var(--color-border);
            background: var(--color-surface);
            color: var(--color-text);
        }

        .button-danger {
            border: 1px solid rgba(180, 35, 24, 0.22);
            background: var(--color-danger-soft);
            color: var(--color-danger);
        }

        .metrics {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: var(--space-3);
        }

        .metric {
            border: 1px solid var(--color-border);
            border-radius: var(--radius-lg);
            background: var(--color-surface);
            padding: var(--space-4);
            box-shadow: var(--shadow-sm);
        }

        .metric-label {
            color: var(--color-text-muted);
            font-size: 12px;
            font-weight: 800;
        }

        .metric-value {
            margin-top: var(--space-2);
            font-size: 26px;
            line-height: 1;
            font-weight: 900;
        }

        .metric-help {
            margin-top: 7px;
            color: var(--color-text-muted);
            font-size: 12px;
        }

        .content-grid {
            display: grid;
            grid-template-columns: minmax(0, 1fr) 336px;
            gap: var(--space-5);
            align-items: start;
        }

        .panel {
            border: 1px solid var(--color-border);
            border-radius: var(--radius-lg);
            background: var(--color-surface);
            box-shadow: var(--shadow-sm);
            overflow: hidden;
        }

        .panel-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: var(--space-4);
            padding: var(--space-4) var(--space-5);
            border-bottom: 1px solid var(--color-border);
        }

        .panel-title {
            margin: 0;
            font-size: 15px;
            font-weight: 850;
        }

        .panel-subtitle {
            margin: 4px 0 0;
            color: var(--color-text-muted);
            font-size: 13px;
        }

        .quick-add {
            display: grid;
            grid-template-columns: minmax(180px, 1fr) 180px 132px auto;
            gap: var(--space-2);
            padding: var(--space-4) var(--space-5);
            border-bottom: 1px solid var(--color-border);
            background: #fbfcff;
        }

        .quick-add input,
        .quick-add select,
        .quick-add textarea,
        .edit-form input,
        .edit-form select,
        .edit-form textarea {
            width: 100%;
            min-height: 40px;
            border: 1px solid var(--color-border);
            border-radius: var(--radius-md);
            background: #ffffff;
            color: var(--color-text);
            padding: 0 12px;
        }

        .quick-add textarea,
        .edit-form textarea {
            min-height: 40px;
            padding-top: 10px;
            resize: vertical;
            line-height: 1.4;
        }

        .quick-add .note-field {
            grid-column: 1 / -1;
            min-height: 64px;
        }

        .form-error {
            display: none;
            grid-column: 1 / -1;
            color: var(--color-danger);
            font-size: 12px;
            font-weight: 760;
        }

        .form-error.is-visible { display: block; }

        .toolbar {
            display: grid;
            grid-template-columns: minmax(180px, 1fr) auto auto;
            gap: var(--space-3);
            align-items: center;
            padding: var(--space-4) var(--space-5);
            border-bottom: 1px solid var(--color-border);
        }

        .inline-search input,
        .sort-select {
            width: 100%;
            min-height: 38px;
            border: 1px solid var(--color-border);
            border-radius: var(--radius-md);
            background: #ffffff;
            color: var(--color-text);
            padding: 0 12px;
        }

        .tabs {
            display: flex;
            align-items: center;
            gap: var(--space-1);
            flex-wrap: wrap;
        }

        .tab {
            min-height: 34px;
            border: 1px solid transparent;
            border-radius: 999px;
            background: transparent;
            color: var(--color-text-muted);
            padding: 0 11px;
            font-size: 12px;
            font-weight: 820;
        }

        .tab.is-active,
        .tab:hover {
            border-color: var(--color-border);
            background: var(--color-surface-muted);
            color: var(--color-text);
        }

        .task-groups {
            display: grid;
            gap: var(--space-5);
            padding: var(--space-5);
            min-height: 460px;
        }

        .group-title {
            margin: 0 0 var(--space-2);
            color: var(--color-text-muted);
            font-size: 12px;
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .task-list {
            display: grid;
            gap: var(--space-2);
        }

        .task-item {
            display: grid;
            grid-template-columns: 28px minmax(0, 1fr) auto;
            gap: var(--space-3);
            align-items: start;
            border: 1px solid var(--color-border);
            border-radius: var(--radius-md);
            background: #ffffff;
            padding: var(--space-3);
        }

        .task-item.overdue {
            border-color: rgba(180, 35, 24, 0.28);
            background: #fffafa;
        }

        .task-item.completed {
            background: #fafbfc;
            opacity: 0.72;
        }

        .complete-box {
            width: 20px;
            height: 20px;
            margin-top: 2px;
            border: 1.5px solid var(--color-border-strong);
            border-radius: 50%;
            background: #ffffff;
        }

        .complete-box:hover {
            border-color: var(--color-primary);
            background: var(--color-primary-soft);
        }

        .task-title {
            margin: 0;
            font-size: 14px;
            line-height: 1.42;
            font-weight: 820;
            overflow-wrap: anywhere;
        }

        .completed .task-title {
            color: var(--color-text-muted);
            text-decoration: line-through;
        }

        .task-note {
            margin: 5px 0 0;
            color: var(--color-text-muted);
            font-size: 13px;
            line-height: 1.45;
            overflow-wrap: anywhere;
        }

        .task-meta {
            display: flex;
            flex-wrap: wrap;
            gap: var(--space-2);
            margin-top: var(--space-2);
            color: var(--color-text-muted);
            font-size: 12px;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            min-height: 22px;
            border-radius: 999px;
            padding: 0 8px;
            font-size: 11px;
            font-weight: 850;
        }

        .badge.upcoming { background: var(--color-primary-soft); color: #3730a3; }
        .badge.today { background: var(--color-warning-soft); color: var(--color-warning); }
        .badge.overdue { background: var(--color-danger-soft); color: var(--color-danger); }
        .badge.completed { background: var(--color-success-soft); color: var(--color-success); }
        .priority {
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .priority::before {
            content: "";
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #94a3b8;
        }

        .priority.high::before { background: var(--color-danger); }
        .priority.medium::before { background: var(--color-warning); }
        .priority.low::before { background: var(--color-success); }

        .task-actions {
            display: flex;
            gap: var(--space-1);
        }

        .icon-button {
            min-width: 34px;
            min-height: 32px;
            border: 1px solid var(--color-border);
            border-radius: var(--radius-sm);
            background: #ffffff;
            color: var(--color-text-muted);
            font-size: 12px;
            font-weight: 820;
        }

        .icon-button:hover { color: var(--color-text); border-color: var(--color-border-strong); }
        .icon-button.danger { color: var(--color-danger); }

        .overview {
            display: grid;
            gap: var(--space-4);
            padding: var(--space-5);
        }

        .focus-card {
            border: 1px solid var(--color-border);
            border-radius: var(--radius-md);
            background: var(--color-surface-muted);
            padding: var(--space-4);
        }

        .focus-label {
            color: var(--color-text-muted);
            font-size: 12px;
            font-weight: 850;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }

        .focus-text {
            margin: var(--space-2) 0 0;
            font-size: 15px;
            line-height: 1.45;
            font-weight: 820;
        }

        .completion-bar {
            height: 8px;
            border-radius: 999px;
            background: #e5e7eb;
            overflow: hidden;
            margin-top: var(--space-3);
        }

        .completion-fill {
            width: 0%;
            height: 100%;
            background: var(--color-primary);
        }

        .timeline {
            display: grid;
            gap: var(--space-2);
        }

        .timeline-item {
            display: grid;
            grid-template-columns: 10px minmax(0, 1fr);
            gap: var(--space-3);
            padding: var(--space-3);
            border: 1px solid var(--color-border);
            border-radius: var(--radius-md);
            background: #ffffff;
        }

        .timeline-dot {
            width: 8px;
            height: 8px;
            margin-top: 5px;
            border-radius: 50%;
            background: var(--color-primary);
        }

        .timeline-title {
            margin: 0;
            font-size: 13px;
            line-height: 1.4;
            font-weight: 800;
        }

        .timeline-meta {
            margin-top: 4px;
            color: var(--color-text-muted);
            font-size: 12px;
        }

        .empty-state,
        .loading-state,
        .error-state {
            display: grid;
            place-items: center;
            min-height: 360px;
            text-align: center;
            color: var(--color-text-muted);
        }

        .empty-box {
            max-width: 380px;
        }

        .empty-mark {
            width: 56px;
            height: 56px;
            display: grid;
            place-items: center;
            margin: 0 auto var(--space-3);
            border: 1px solid var(--color-border);
            border-radius: var(--radius-lg);
            background: #ffffff;
            color: var(--color-primary);
            font-weight: 900;
        }

        .empty-title {
            margin: 0;
            color: var(--color-text);
            font-size: 17px;
            font-weight: 850;
        }

        .empty-copy {
            margin: var(--space-2) 0 var(--space-4);
            line-height: 1.55;
        }

        .toast {
            position: fixed;
            right: var(--space-5);
            bottom: var(--space-5);
            z-index: 20;
            display: none;
            max-width: min(420px, calc(100vw - 40px));
            border: 1px solid var(--color-border);
            border-radius: var(--radius-md);
            background: #ffffff;
            box-shadow: var(--shadow-md);
            padding: var(--space-3) var(--space-4);
            font-size: 13px;
            font-weight: 780;
        }

        .toast.is-visible { display: block; }
        .toast.success { color: var(--color-success); background: var(--color-success-soft); }
        .toast.error { color: var(--color-danger); background: var(--color-danger-soft); }

        @media (max-width: 1180px) {
            .app-shell { grid-template-columns: 76px minmax(0, 1fr); }
            .brand span:last-child,
            .side-link span:first-child,
            .side-section-label,
            .developer-panel { display: none; }
            .sidebar { align-items: center; padding: var(--space-4) var(--space-3); }
            .side-link { justify-content: center; width: 44px; padding: 0; }
            .side-count { display: none; }
            .content-grid { grid-template-columns: 1fr; }
        }

        @media (max-width: 780px) {
            .app-shell { display: block; }
            .sidebar {
                position: static;
                height: auto;
                flex-direction: row;
                overflow-x: auto;
            }
            .brand span:last-child,
            .side-link span:first-child { display: inline; }
            .side-nav { display: flex; }
            .topbar {
                position: static;
                grid-template-columns: 1fr;
                padding: var(--space-4);
            }
            .top-actions { justify-content: space-between; }
            .page { padding: var(--space-4); }
            .page-header { display: grid; }
            .metrics { grid-template-columns: 1fr 1fr; }
            .quick-add,
            .toolbar { grid-template-columns: 1fr; }
            .task-item { grid-template-columns: 28px minmax(0, 1fr); }
            .task-actions { grid-column: 2; }
        }

        @media (max-width: 520px) {
            .workspace-chip { display: none; }
            .metrics { grid-template-columns: 1fr; }
            .header-meta { justify-content: start; }
            .button { width: 100%; }
            .top-actions .button { width: auto; }
        }
    </style>
</head>
<body>
    <div class="app-shell">
        <aside class="sidebar" aria-label="Application navigation">
            <a class="brand" href="/" aria-label="Task Scheduler home">
                <span class="brand-mark" aria-hidden="true">TS</span>
                <span>Task Scheduler</span>
            </a>
            <div class="side-section-label">Workspace</div>
            <nav class="side-nav">
                <button class="side-link is-active" type="button" data-nav-filter="all"><span>Dashboard</span><span class="side-count" id="nav-all">0</span></button>
                <button class="side-link" type="button" data-nav-filter="today"><span>Today</span><span class="side-count" id="nav-today">0</span></button>
                <button class="side-link" type="button" data-nav-filter="upcoming"><span>Upcoming</span><span class="side-count" id="nav-upcoming">0</span></button>
                <button class="side-link" type="button" data-nav-filter="completed"><span>Completed</span><span class="side-count" id="nav-completed">0</span></button>
            </nav>
            <details class="developer-panel">
                <summary>Developer</summary>
                <div class="developer-links">
                    <a href="/docs">API Docs</a>
                    <a href="/health">Health</a>
                    <a href="/api/tasks">Task JSON</a>
                </div>
            </details>
        </aside>

        <div class="main">
            <header class="topbar">
                <label class="search-wrap">
                    <span class="search-prefix" aria-hidden="true">S</span>
                    <span class="sr-only">Search tasks</span>
                    <input id="global-search" type="search" placeholder="Search tasks, notes, or priority">
                </label>
                <div class="top-actions">
                    <button class="button button-primary" id="quick-add-focus" type="button">Quick Add Task</button>
                    <span class="workspace-chip"><span class="live-dot" aria-hidden="true"></span><span id="system-status">Syncing</span></span>
                    <span class="avatar" aria-label="User avatar">A</span>
                </div>
            </header>

            <main class="page">
                <section class="page-header" aria-labelledby="page-title">
                    <div>
                        <div class="page-kicker">Task dashboard</div>
                        <h1 id="page-title">Today</h1>
                        <p class="page-subtitle">Focus on what needs your attention now.</p>
                    </div>
                    <div class="header-meta">
                        <span class="date-pill" id="today-label">Today</span>
                        <span class="date-pill">Local workspace</span>
                        <button class="button button-primary" id="header-add" type="button">Add task</button>
                    </div>
                </section>

                <section class="metrics" aria-label="Task metrics">
                    <div class="metric"><div class="metric-label">Pending</div><div class="metric-value" id="metric-pending">0</div><div class="metric-help">Open tasks</div></div>
                    <div class="metric"><div class="metric-label">Due now</div><div class="metric-value" id="metric-due">0</div><div class="metric-help">Need attention</div></div>
                    <div class="metric"><div class="metric-label">Overdue</div><div class="metric-value" id="metric-overdue">0</div><div class="metric-help">Past due</div></div>
                    <div class="metric"><div class="metric-label">Completed</div><div class="metric-value" id="metric-completed">0</div><div class="metric-help">Finished work</div></div>
                </section>

                <section class="content-grid">
                    <section class="panel" aria-label="Task workspace">
                        <div class="panel-header">
                            <div>
                                <h2 class="panel-title">Scheduled Work</h2>
                                <p class="panel-subtitle">Create, triage, and complete time-bound work.</p>
                            </div>
                            <button class="button button-secondary" id="refresh-button" type="button">Refresh</button>
                        </div>

                        <form class="quick-add" id="task-form" novalidate>
                            <input type="hidden" id="editing-id">
                            <label>
                                <span class="sr-only">Task title</span>
                                <input id="content" maxlength="180" placeholder="Add a task, for example: Review sprint notes">
                            </label>
                            <label>
                                <span class="sr-only">Due date and time</span>
                                <input id="due-at" type="datetime-local">
                            </label>
                            <label>
                                <span class="sr-only">Priority</span>
                                <select id="priority">
                                    <option value="high">High priority</option>
                                    <option value="medium" selected>Medium priority</option>
                                    <option value="low">Low priority</option>
                                </select>
                            </label>
                            <button class="button button-primary" id="submit-button" type="submit" disabled>Schedule</button>
                            <textarea class="note-field" id="note" maxlength="240" placeholder="Optional note or context"></textarea>
                            <div class="form-error" id="form-error">Task title and a future due time are required.</div>
                            <button class="button button-secondary" id="cancel-edit-button" type="button" hidden>Cancel edit</button>
                        </form>

                        <div class="toolbar">
                            <label class="inline-search">
                                <span class="sr-only">Search visible tasks</span>
                                <input id="list-search" type="search" placeholder="Search this list">
                            </label>
                            <div class="tabs" aria-label="Task filter">
                                <button class="tab is-active" type="button" data-filter="all">All</button>
                                <button class="tab" type="button" data-filter="today">Today</button>
                                <button class="tab" type="button" data-filter="upcoming">Upcoming</button>
                                <button class="tab" type="button" data-filter="overdue">Overdue</button>
                                <button class="tab" type="button" data-filter="completed">Completed</button>
                            </div>
                            <select class="sort-select" id="sort-select" aria-label="Sort tasks">
                                <option value="due">Sort by due time</option>
                                <option value="created">Sort by created time</option>
                                <option value="priority">Sort by priority</option>
                            </select>
                        </div>

                        <div class="task-groups" id="task-groups" aria-live="polite"></div>
                    </section>

                    <aside class="panel" aria-label="Today overview">
                        <div class="panel-header">
                            <div>
                                <h2 class="panel-title">Today Overview</h2>
                                <p class="panel-subtitle">Actionable summary for the next move.</p>
                            </div>
                        </div>
                        <div class="overview">
                            <div class="focus-card">
                                <div class="focus-label">Suggested focus</div>
                                <p class="focus-text" id="focus-text">No urgent task right now.</p>
                            </div>
                            <div class="focus-card">
                                <div class="focus-label">Completion rate</div>
                                <p class="focus-text"><span id="completion-rate">0</span>% completed</p>
                                <div class="completion-bar"><div class="completion-fill" id="completion-fill"></div></div>
                            </div>
                            <div>
                                <h3 class="group-title">Next due task</h3>
                                <div class="timeline" id="next-task"></div>
                            </div>
                            <div>
                                <h3 class="group-title">Small timeline</h3>
                                <div class="timeline" id="timeline"></div>
                            </div>
                        </div>
                    </aside>
                </section>
            </main>
        </div>
    </div>

    <div class="toast" id="toast" role="status" aria-live="polite"></div>

    <script>
        const form = document.getElementById("task-form");
        const editingIdInput = document.getElementById("editing-id");
        const contentInput = document.getElementById("content");
        const dueInput = document.getElementById("due-at");
        const priorityInput = document.getElementById("priority");
        const noteInput = document.getElementById("note");
        const submitButton = document.getElementById("submit-button");
        const cancelEditButton = document.getElementById("cancel-edit-button");
        const formError = document.getElementById("form-error");
        const refreshButton = document.getElementById("refresh-button");
        const taskGroups = document.getElementById("task-groups");
        const globalSearch = document.getElementById("global-search");
        const listSearch = document.getElementById("list-search");
        const sortSelect = document.getElementById("sort-select");
        const filterButtons = document.querySelectorAll("[data-filter]");
        const navButtons = document.querySelectorAll("[data-nav-filter]");
        const toast = document.getElementById("toast");

        let allJobs = [];
        let currentFilter = "all";
        let toastTimer = null;

        function defaultLocalDateTime() {
            const date = new Date();
            date.setMinutes(date.getMinutes() + 45, 0, 0);
            const offset = date.getTimezoneOffset();
            return new Date(date.getTime() - offset * 60000).toISOString().slice(0, 16);
        }

        function toLocalInputValue(iso) {
            const date = new Date(iso);
            const offset = date.getTimezoneOffset();
            return new Date(date.getTime() - offset * 60000).toISOString().slice(0, 16);
        }

        function toIsoFromLocal(value) {
            return new Date(value).toISOString();
        }

        function formatDateTime(iso) {
            return new Intl.DateTimeFormat("en", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }).format(new Date(iso));
        }

        function formatToday() {
            return new Intl.DateTimeFormat("en", { weekday: "long", month: "short", day: "numeric" }).format(new Date());
        }

        function minutesUntil(iso) {
            return Math.round((new Date(iso).getTime() - Date.now()) / 60000);
        }

        function relativeTime(iso) {
            const minutes = minutesUntil(iso);
            const abs = Math.abs(minutes);
            if (minutes < 0) return abs < 60 ? `${abs}m overdue` : `${Math.round(abs / 60)}h overdue`;
            if (minutes < 60) return `Due in ${Math.max(minutes, 1)}m`;
            if (minutes < 1440) return `Due in ${Math.round(minutes / 60)}h`;
            return `Due in ${Math.round(minutes / 1440)}d`;
        }

        function taskState(job) {
            if (job.status === "completed") return "completed";
            const minutes = minutesUntil(job.due_at);
            if (minutes < 0) return "overdue";
            if (minutes <= 1440) return "today";
            return "upcoming";
        }

        function priorityRank(priority) {
            return { high: 0, medium: 1, low: 2 }[priority || "medium"] ?? 1;
        }

        function showToast(message, type = "success") {
            clearTimeout(toastTimer);
            toast.textContent = message;
            toast.className = `toast is-visible ${type}`;
            toastTimer = setTimeout(() => { toast.className = "toast"; }, 3000);
        }

        function validateForm() {
            const due = dueInput.value ? new Date(dueInput.value) : null;
            const valid = Boolean(contentInput.value.trim()) && due && due > new Date();
            formError.classList.toggle("is-visible", !valid);
            return valid;
        }

        function updateFormState() {
            submitButton.disabled = !contentInput.value.trim() || !dueInput.value;
            if (formError.classList.contains("is-visible")) validateForm();
        }

        async function fetchJson(url, options = {}) {
            const response = await fetch(url, options);
            const contentType = response.headers.get("content-type") || "";
            const data = contentType.includes("application/json") ? await response.json() : { detail: await response.text() };
            if (!response.ok) throw new Error(data.detail || "Request failed");
            return data;
        }

        function setFilter(filter) {
            currentFilter = filter;
            filterButtons.forEach((button) => button.classList.toggle("is-active", button.dataset.filter === filter));
            navButtons.forEach((button) => button.classList.toggle("is-active", button.dataset.navFilter === filter || (filter === "all" && button.dataset.navFilter === "all")));
            renderTasks();
        }

        function visibleJobs() {
            const query = `${globalSearch.value} ${listSearch.value}`.trim().toLowerCase();
            let jobs = allJobs.filter((job) => {
                const state = taskState(job);
                if (currentFilter !== "all" && state !== currentFilter) return false;
                if (!query) return true;
                return `${job.content} ${job.note || ""} ${job.priority || ""}`.toLowerCase().includes(query);
            });
            if (sortSelect.value === "created") {
                jobs.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
            } else if (sortSelect.value === "priority") {
                jobs.sort((a, b) => priorityRank(a.priority) - priorityRank(b.priority) || new Date(a.due_at) - new Date(b.due_at));
            } else {
                jobs.sort((a, b) => new Date(a.due_at) - new Date(b.due_at));
            }
            return jobs;
        }

        function groupJobs(jobs) {
            const groups = [
                ["Overdue", jobs.filter((job) => taskState(job) === "overdue")],
                ["Today", jobs.filter((job) => taskState(job) === "today")],
                ["Upcoming", jobs.filter((job) => taskState(job) === "upcoming")],
                ["Completed", jobs.filter((job) => taskState(job) === "completed")],
            ];
            return groups.filter(([, items]) => items.length > 0);
        }

        function renderTasks() {
            const jobs = visibleJobs();
            taskGroups.innerHTML = "";
            if (jobs.length === 0) {
                taskGroups.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-box">
                            <div class="empty-mark">TS</div>
                            <h3 class="empty-title">No tasks match this view</h3>
                            <p class="empty-copy">Use Quick Add to schedule your next task, or clear search and filters.</p>
                            <button class="button button-primary" type="button" id="empty-add">Add a task</button>
                        </div>
                    </div>
                `;
                document.getElementById("empty-add").addEventListener("click", focusQuickAdd);
                return;
            }
            groupJobs(jobs).forEach(([label, items]) => {
                const group = document.createElement("section");
                const title = document.createElement("h3");
                title.className = "group-title";
                title.textContent = `${label} ${items.length}`;
                const list = document.createElement("div");
                list.className = "task-list";
                items.forEach((job) => list.appendChild(createTaskItem(job)));
                group.appendChild(title);
                group.appendChild(list);
                taskGroups.appendChild(group);
            });
        }

        function createTaskItem(job) {
            const state = taskState(job);
            const item = document.createElement("article");
            item.className = `task-item ${state}`;
            const complete = document.createElement("button");
            complete.className = "complete-box";
            complete.type = "button";
            complete.setAttribute("aria-label", `Complete task ${job.id}`);
            complete.disabled = job.status === "completed";
            complete.addEventListener("click", async () => {
                try {
                    await fetchJson(`/api/tasks/${job.id}/complete`, { method: "POST" });
                    showToast("Task completed.");
                    await refresh(false);
                } catch (error) {
                    showToast(error.message, "error");
                }
            });

            const body = document.createElement("div");
            body.innerHTML = `
                <p class="task-title"></p>
                ${job.note ? '<p class="task-note"></p>' : ''}
                <div class="task-meta">
                    <span class="badge ${state}">${state === "today" ? "Today" : state[0].toUpperCase() + state.slice(1)}</span>
                    <span>${formatDateTime(job.due_at)}</span>
                    <span>${relativeTime(job.due_at)}</span>
                    <span class="priority ${job.priority || "medium"}">${job.priority || "medium"}</span>
                </div>
            `;
            body.querySelector(".task-title").textContent = job.content;
            const note = body.querySelector(".task-note");
            if (note) note.textContent = job.note;

            const actions = document.createElement("div");
            actions.className = "task-actions";
            const edit = document.createElement("button");
            edit.className = "icon-button";
            edit.type = "button";
            edit.textContent = "Edit";
            edit.setAttribute("aria-label", `Edit task ${job.id}`);
            edit.addEventListener("click", () => startEdit(job));
            const remove = document.createElement("button");
            remove.className = "icon-button danger";
            remove.type = "button";
            remove.textContent = "Del";
            remove.setAttribute("aria-label", `Delete task ${job.id}`);
            remove.addEventListener("click", async () => {
                if (!window.confirm("Delete this task?")) return;
                try {
                    await fetchJson(`/api/tasks/${job.id}`, { method: "DELETE" });
                    showToast("Task deleted.");
                    await refresh(false);
                } catch (error) {
                    showToast(error.message, "error");
                }
            });
            actions.appendChild(edit);
            actions.appendChild(remove);
            item.appendChild(complete);
            item.appendChild(body);
            item.appendChild(actions);
            return item;
        }

        function renderOverview() {
            const total = allJobs.length;
            const pending = allJobs.filter((job) => job.status === "pending");
            const completed = allJobs.filter((job) => job.status === "completed");
            const overdue = allJobs.filter((job) => taskState(job) === "overdue");
            const today = allJobs.filter((job) => taskState(job) === "today");
            const upcoming = allJobs.filter((job) => taskState(job) === "upcoming");
            const dueNow = pending.filter((job) => minutesUntil(job.due_at) <= 60 && minutesUntil(job.due_at) >= 0);
            document.getElementById("metric-pending").textContent = pending.length;
            document.getElementById("metric-due").textContent = dueNow.length;
            document.getElementById("metric-overdue").textContent = overdue.length;
            document.getElementById("metric-completed").textContent = completed.length;
            document.getElementById("nav-all").textContent = total;
            document.getElementById("nav-today").textContent = today.length;
            document.getElementById("nav-upcoming").textContent = upcoming.length;
            document.getElementById("nav-completed").textContent = completed.length;
            const rate = total ? Math.round((completed.length / total) * 100) : 0;
            document.getElementById("completion-rate").textContent = rate;
            document.getElementById("completion-fill").style.width = `${rate}%`;
            const focus = document.getElementById("focus-text");
            if (overdue.length) focus.textContent = "Finish overdue tasks first.";
            else if (dueNow.length) focus.textContent = `${dueNow.length} task${dueNow.length === 1 ? "" : "s"} due within the next hour.`;
            else focus.textContent = "No urgent task right now.";
            renderTimeline(pending);
        }

        function renderTimeline(pending) {
            const sorted = [...pending].sort((a, b) => new Date(a.due_at) - new Date(b.due_at));
            const nextTask = document.getElementById("next-task");
            const timeline = document.getElementById("timeline");
            nextTask.innerHTML = "";
            timeline.innerHTML = "";
            if (!sorted.length) {
                nextTask.innerHTML = '<div class="timeline-item"><span class="timeline-dot"></span><div><p class="timeline-title">No next task</p><div class="timeline-meta">Your schedule is clear.</div></div></div>';
                timeline.innerHTML = '<div class="timeline-item"><span class="timeline-dot"></span><div><p class="timeline-title">Nothing scheduled</p><div class="timeline-meta">Add a task to start planning.</div></div></div>';
                return;
            }
            [sorted[0]].forEach((job) => nextTask.appendChild(createTimelineItem(job)));
            sorted.slice(0, 4).forEach((job) => timeline.appendChild(createTimelineItem(job)));
        }

        function createTimelineItem(job) {
            const item = document.createElement("div");
            item.className = "timeline-item";
            item.innerHTML = '<span class="timeline-dot"></span><div><p class="timeline-title"></p><div class="timeline-meta"></div></div>';
            item.querySelector(".timeline-title").textContent = job.content;
            item.querySelector(".timeline-meta").textContent = `${formatDateTime(job.due_at)} - ${relativeTime(job.due_at)}`;
            return item;
        }

        function focusQuickAdd() {
            contentInput.focus();
            form.scrollIntoView({ block: "center", behavior: "smooth" });
        }

        function resetForm() {
            editingIdInput.value = "";
            contentInput.value = "";
            dueInput.value = defaultLocalDateTime();
            priorityInput.value = "medium";
            noteInput.value = "";
            submitButton.textContent = "Schedule";
            cancelEditButton.hidden = true;
            formError.classList.remove("is-visible");
            updateFormState();
        }

        function startEdit(job) {
            editingIdInput.value = job.id;
            contentInput.value = job.content;
            dueInput.value = toLocalInputValue(job.due_at);
            priorityInput.value = job.priority || "medium";
            noteInput.value = job.note || "";
            submitButton.textContent = "Update";
            cancelEditButton.hidden = false;
            updateFormState();
            focusQuickAdd();
        }

        async function refresh(showLoading = true) {
            if (showLoading) taskGroups.innerHTML = '<div class="loading-state">Loading tasks...</div>';
            document.getElementById("system-status").textContent = "Syncing";
            try {
                const data = await fetchJson("/api/tasks");
                allJobs = data.jobs;
                renderOverview();
                renderTasks();
                document.getElementById("system-status").textContent = "Live";
            } catch (error) {
                taskGroups.innerHTML = `<div class="error-state"><div><h3 class="empty-title">Could not load tasks</h3><p>${error.message}</p></div></div>`;
                document.getElementById("system-status").textContent = "Offline";
                showToast(error.message, "error");
            }
        }

        form.addEventListener("submit", async (event) => {
            event.preventDefault();
            if (!validateForm()) {
                showToast("Add a task title and choose a future due time.", "error");
                return;
            }
            const editingId = editingIdInput.value;
            const payload = {
                content: contentInput.value.trim(),
                due_at: toIsoFromLocal(dueInput.value),
                priority: priorityInput.value,
                note: noteInput.value.trim()
            };
            submitButton.disabled = true;
            submitButton.textContent = editingId ? "Updating..." : "Scheduling...";
            try {
                await fetchJson(editingId ? `/api/tasks/${editingId}` : "/api/tasks", {
                    method: editingId ? "PATCH" : "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                showToast(editingId ? "Task updated." : "Task scheduled.");
                resetForm();
                await refresh(false);
            } catch (error) {
                showToast(error.message, "error");
            } finally {
                submitButton.textContent = editingIdInput.value ? "Update" : "Schedule";
                updateFormState();
            }
        });

        [contentInput, dueInput].forEach((input) => input.addEventListener("input", updateFormState));
        [globalSearch, listSearch, sortSelect].forEach((input) => input.addEventListener("input", renderTasks));
        sortSelect.addEventListener("change", renderTasks);
        refreshButton.addEventListener("click", () => refresh(true));
        document.getElementById("quick-add-focus").addEventListener("click", focusQuickAdd);
        document.getElementById("header-add").addEventListener("click", focusQuickAdd);
        cancelEditButton.addEventListener("click", resetForm);
        filterButtons.forEach((button) => button.addEventListener("click", () => setFilter(button.dataset.filter)));
        navButtons.forEach((button) => button.addEventListener("click", () => setFilter(button.dataset.navFilter)));
        document.getElementById("today-label").textContent = formatToday();
        resetForm();
        refresh(true);
    </script>
</body>
</html>
"""
