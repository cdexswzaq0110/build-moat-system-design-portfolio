# ChatGPT Task Scheduler BDD

## Feature: Browser Task Management

### Scenario: Create and complete a task without npx

Given the FastAPI server is running on `http://127.0.0.1:8003`  
When I open the browser UI  
And I create a task with content `review PR #123` and a due time  
Then the task should appear in the scheduled work list  
And the summary should show one pending task  
When I click `Complete`  
Then the task should move to completed status

## Feature: MCP Tool Discovery

### Scenario: List available tools

Given the MCP server is running  
When MCP Inspector connects  
Then it should show these tools:

- `task.create`
- `task.list`
- `task.get`
- `task.complete`

## Feature: Task Creation

### Scenario: Create a task

Given the MCP server is running  
When I call `task.create` with:

```json
{
  "content": "review PR #123",
  "due_at": "2026-06-01T09:00:00+08:00"
}
```

Then the returned task should have status `pending`  
And it should include a UTC `due_at`  
And it should include a minute-level `due_bucket`

## Feature: Task Listing

### Scenario: List pending tasks

Given at least one pending task exists  
When I call `task.list` with:

```json
{
  "status": "pending"
}
```

Then the response should include pending tasks  
And each task should include `id`, `content`, `due_at`, `due_bucket`, and `status`

## Feature: Task Lookup

### Scenario: Get existing task

Given task `1` exists  
When I call `task.get` with:

```json
{
  "id": 1
}
```

Then the response should include task `1`

### Scenario: Get missing task

Given task `999999` does not exist  
When I call `task.get` with:

```json
{
  "id": 999999
}
```

Then the server should return a clear `job not found` error

## Feature: Task Completion

### Scenario: Complete existing task

Given a pending task exists  
When I call `task.complete` with that task id  
Then the returned task should have status `completed`

## Feature: Due Job Scan

### Scenario: Find due jobs

Given a pending task has `due_at` in the past  
When `find_due_jobs()` runs  
Then the task should be returned

### Scenario: Ignore future jobs

Given a pending task has `due_at` in the future  
When `find_due_jobs()` runs  
Then the task should not be returned
