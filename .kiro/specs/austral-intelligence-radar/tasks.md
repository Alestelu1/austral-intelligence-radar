# Tasks

## Phase 1 — Foundation

- [x] Initialize public repository.
- [x] Define project problem and MVP boundaries.
- [x] Add Kiro Steering context and editorial rules.
- [x] Define requirements and initial design.
- [ ] Add Python project structure and dependency management.
- [ ] Define the analysis JSON schema in code.

## Phase 2 — Local vertical slice

- [ ] Implement input validation.
- [ ] Implement a deterministic mock analyzer for UI development.
- [ ] Build the minimal web form and result view.
- [ ] Add tests for empty input and valid structured output.
- [ ] Demonstrate the complete flow locally without AWS persistence.

## Phase 3 — AI integration

- [ ] Confirm the AWS model service available to the account.
- [ ] Implement the model adapter.
- [ ] Create a constrained system prompt based on Steering rules.
- [ ] Parse and validate model JSON.
- [ ] Add safe fallback behavior for incomplete model output.
- [ ] Test with at least five representative sources.

## Phase 4 — AWS integration

- [ ] Create DynamoDB table design.
- [ ] Implement record persistence.
- [ ] Package the backend for AWS Lambda.
- [ ] Configure API Gateway.
- [ ] Configure least-privilege IAM permissions.
- [ ] Confirm CloudWatch logging without secrets.

## Phase 5 — Deployment and validation

- [ ] Deploy the public demo.
- [ ] Configure frontend API endpoint and CORS.
- [ ] Test success, validation and service-failure paths.
- [ ] Verify that every result preserves provenance.
- [ ] Verify that uncertain content triggers human review.

## Phase 6 — Deliverables

- [ ] Complete README installation and architecture sections.
- [ ] Add architecture diagram.
- [ ] Document Kiro Specs, Steering and development workflow.
- [ ] Document AWS services used.
- [ ] Remove secrets and inspect Git history.
- [ ] Prepare a video script under five minutes.
- [ ] Record the functional demo.
- [ ] Verify repository, demo and video links before submission.

## Implementation order

Work from a thin vertical slice and do not begin optional features until the following path works:

```text
submit text → receive valid analysis → display result → persist in AWS
```
