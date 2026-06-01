# QR Code Generator BDD

## Feature: Browser QR Generation

### Scenario: Generate QR code for GitHub profile

Given the QR Code Generator server is running  
And I open `http://127.0.0.1:8001`  
And the URL field contains `https://github.com/cdexswzaq0110`  
When I click `Generate QR Code`  
Then the page should call `POST /links`  
And the QR preview should appear on the same page  
And the page should show a short URL  
And the page should show the token

## Feature: Link Creation API

### Scenario: Create a short link for a valid URL

Given the server is running  
When I send `POST /links` with:

```json
{
  "url": "https://github.com/cdexswzaq0110",
  "expires_at": null
}
```

Then the response status should be `200`  
And the response should include `token`  
And the response should include `short_url`  
And the response should include `qr_url`

### Scenario: Reject localhost URL

Given the server is running  
When I send `POST /links` with:

```json
{
  "url": "http://localhost:8000",
  "expires_at": null
}
```

Then the response status should be `400`  
And the response should explain that private hosts are not allowed

## Feature: QR Image

### Scenario: Fetch QR image

Given a short link exists  
When I request `GET /qr/{token}.png`  
Then the response status should be `200`  
And the content type should be `image/png`

## Feature: Redirect

### Scenario: Redirect active token

Given a short link exists for `https://github.com/cdexswzaq0110`  
When I request `GET /r/{token}`  
Then the response should redirect to `https://github.com/cdexswzaq0110`

### Scenario: Unknown token

Given no link exists for token `missing123`  
When I request `GET /r/missing123`  
Then the response status should be `404`

### Scenario: Expired token

Given a link exists with an `expires_at` value in the past  
When I request `GET /r/{token}`  
Then the response status should be `410`
