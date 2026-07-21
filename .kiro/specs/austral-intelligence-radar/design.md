# Design

## 1. Architecture

```text
Browser UI
   ↓ HTTPS
Amazon API Gateway
   ↓
AWS Lambda
   ├── validate request
   ├── call AI model
   ├── validate structured output
   └── persist result
        ↓
Amazon DynamoDB
```

The model service should be available through AWS. Amazon Bedrock is preferred when account access and model availability permit it.

## 2. Request model

```json
{
  "source_text": "string",
  "source_url": "string | null"
}
```

## 3. Analysis record

```json
{
  "id": "uuid",
  "created_at": "ISO-8601 timestamp",
  "title": "string",
  "summary": "string",
  "territory": ["string"],
  "category": "string",
  "entities": [
    {
      "name": "string",
      "type": "place | institution | route | infrastructure | person | other"
    }
  ],
  "related_project": "string",
  "editorial_relevance": "low | medium | high",
  "confidence": "low | medium | high",
  "requires_human_review": true,
  "review_reason": "string",
  "source": {
    "type": "url | user_text",
    "url": "string | null"
  }
}
```

## 4. Backend responsibilities

- Reject empty or oversized input.
- Build a constrained analysis prompt from Steering rules.
- Request structured JSON from the model.
- Validate required fields and enumerations.
- Fall back safely when the model omits fields.
- Add server-generated ID and timestamp.
- Store the validated record in DynamoDB.
- Return a sanitized response to the UI.

## 5. Frontend responsibilities

- Provide source text and optional URL fields.
- Show loading, success and error states.
- Render the structured result in readable sections.
- Visually highlight confidence and human-review status.
- Avoid exposing AWS credentials or internal model prompts.

## 6. AWS resources

Minimum resources:

- API Gateway endpoint
- Lambda analysis function
- DynamoDB table
- CloudWatch logs
- IAM role using least privilege

## 7. Error handling

- `400`: invalid request.
- `422`: model output cannot be validated.
- `500`: unexpected processing or persistence failure.
- Logs must not contain secrets or entire sensitive source documents.

## 8. Security

- No credentials in Git.
- Use environment variables and IAM roles.
- Restrict CORS to the deployed frontend when practical.
- Define input-length limits.
- Escape rendered model output in the browser.
