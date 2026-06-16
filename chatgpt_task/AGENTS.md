# AGENTS.md

## Project Identity

This project is **Task Scheduler**, a production-minded SaaS-style task scheduling dashboard.

It should not look like:

- an engineering demo
- an MCP Inspector replacement page
- a raw backend test UI
- a classroom assignment
- a generic admin template

It should look like a polished productivity product. Reference quality benchmarks include Linear-style workflow clarity, Todoist-style task management simplicity, Notion Calendar-style time awareness, and Vercel-style dashboard restraint. Do not copy any brand directly.

## Product Design Principles

### 1. App-first, not landing-page-first

This is a web app dashboard, not a marketing landing page.

Prioritize:

- task creation
- task visibility
- due time awareness
- task completion
- filtering and sorting
- daily overview

Avoid oversized hero sections that push real functionality below the fold.

### 2. Workflow clarity

Every screen should answer:

1. What do I need to do now?
2. What is due soon?
3. What is overdue?
4. What have I already completed?
5. What is the fastest next action?

The task list is the core of the product.

### 3. Production SaaS quality

Required qualities:

- clear visual hierarchy
- consistent spacing
- restrained color palette
- polished typography
- subtle borders
- useful light shadows
- strong empty states
- clear loading, success, and error states
- responsive behavior

Avoid:

- random spacing
- oversized cards
- decorative UI with no function
- unstyled browser defaults
- debug commands in primary user views
- inconsistent badges and buttons

## Information Architecture

Preferred app structure:

- Sidebar navigation: Dashboard, Today, Upcoming, Completed, Developer.
- Top bar: Search, Quick Add Task, workspace status, user avatar.
- Main content: compact page header, metrics summary, task workspace.
- Right insight panel: today overview, next due task, overdue warning, completion rate, timeline or focus suggestion.

## Task UX Requirements

Task creation should support:

- task title
- due date and time
- optional priority
- optional note
- clear validation
- loading state
- success state
- error state

Task display should support:

- title
- status badge
- due time
- relative due message
- priority indicator
- completed state
- overdue state
- quick actions: complete, edit, delete

Task filters should include:

- All
- Today
- Upcoming
- Overdue
- Completed

Sorting should include:

- due time
- created time
- priority

## Developer Information

Developer-only information must not dominate the product UI.

API docs, health status, uvicorn commands, and debug information should be:

- placed in a Developer section
- hidden behind a collapsible panel
- visually secondary
- never placed as the main dashboard content

The primary user should not need backend commands to use the product.

## Design System Rules

Use CSS variables for design tokens whenever possible.

Required token groups:

```css
:root {
  --color-bg: ;
  --color-surface: ;
  --color-surface-muted: ;
  --color-border: ;
  --color-text: ;
  --color-text-muted: ;
  --color-primary: ;
  --color-primary-muted: ;
  --color-success: ;
  --color-warning: ;
  --color-danger: ;

  --radius-sm: ;
  --radius-md: ;
  --radius-lg: ;
  --radius-xl: ;

  --shadow-sm: ;
  --shadow-md: ;

  --space-1: ;
  --space-2: ;
  --space-3: ;
  --space-4: ;
  --space-5: ;
  --space-6: ;

  --font-sans: ;
}
```

All buttons, inputs, badges, cards, tabs, empty states, loading states, and error states should use these tokens consistently.
