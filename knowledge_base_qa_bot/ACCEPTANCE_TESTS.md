# Knowledge Base Q&A Bot BDD

## Feature: Health Check

### Scenario: Service is alive

Given the server is running  
When I request `GET /health`  
Then the response should be:

```json
{
  "status": "ok"
}
```

## Feature: Index Markdown Knowledge Base

### Scenario: Build index from Markdown files

Given `docs/sample/product.md` exists  
When I send `POST /index`  
Then the response status should be `200`  
And the response should include `status: indexed`  
And the response should include a section count greater than `0`  
And `.kb/index.json` should be created

## Feature: Ask Grounded Question

### Scenario: Ask whether paid APIs are required

Given the index has been built  
When I send `POST /chat` with:

```json
{
  "question": "Does this require paid APIs?"
}
```

Then the response status should be `200`  
And the answer should come from the indexed Markdown  
And the response should include source metadata  
And the source should include filename and heading

## Feature: Empty Index

### Scenario: Ask before indexing

Given `.kb/index.json` does not exist  
When I send `POST /chat` with:

```json
{
  "question": "What is this project?"
}
```

Then the response should say `Knowledge base is empty. Run /index first.`

## Feature: Weak Retrieval

### Scenario: Ask unrelated question

Given the index has been built  
When I send `POST /chat` with:

```json
{
  "question": "What is the weather tomorrow?"
}
```

Then the response should say `I cannot confirm the answer from the knowledge base.`  
And the response should not invent an answer
