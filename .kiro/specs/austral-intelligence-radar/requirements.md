# Requirements

## 1. Purpose

Build a specialized AI agent that converts source text into a structured, traceable intelligence record for Austral Beacon Media.

## 2. Functional requirements

### FR-1 — Submit source content

The user must be able to submit source text and optionally a source URL.

**Acceptance criteria**

- WHEN the user submits non-empty text, THE SYSTEM SHALL accept it for analysis.
- WHEN the text is empty, THE SYSTEM SHALL return a clear validation error.

### FR-2 — Generate structured analysis

The system must return:

- title;
- concise summary;
- territory;
- category;
- detected entities;
- related Austral Beacon project;
- editorial relevance;
- confidence level;
- human-review flag;
- source provenance.

**Acceptance criteria**

- WHEN analysis succeeds, THE SYSTEM SHALL return valid JSON matching the defined schema.
- IF a field cannot be determined, THE SYSTEM SHALL use `unknown` or an empty collection instead of inventing data.

### FR-3 — Preserve provenance

The system must preserve the supplied URL or source identifier.

**Acceptance criteria**

- WHEN a URL is supplied, THE SYSTEM SHALL include it unchanged in the result.
- WHEN no URL is supplied, THE SYSTEM SHALL explicitly mark the source as user-provided text.

### FR-4 — Require human review when needed

The agent must detect uncertainty or unsupported claims.

**Acceptance criteria**

- IF confidence is low or conflicting claims are present, THE SYSTEM SHALL set `requires_human_review` to true.
- THE SYSTEM SHALL provide a short reason for the review flag.

### FR-5 — Persist analysis in AWS

The system must store successful analyses in an AWS data service.

**Acceptance criteria**

- WHEN an analysis succeeds, THE SYSTEM SHALL save a record with a unique identifier and timestamp.
- IF persistence fails, THE SYSTEM SHALL report the failure without exposing secrets.

### FR-6 — Provide a usable demo

The project must provide a public interface or executable user experience.

**Acceptance criteria**

- A reviewer SHALL be able to submit a source and inspect the result.
- The interface SHALL display errors and loading states clearly.

## 3. Non-functional requirements

- Responses should complete within a reasonable demo time.
- Secrets must be stored in environment variables or AWS configuration, never committed.
- The implementation must include basic logging and error handling.
- The codebase must remain small enough to complete and test during the hackathon.
- The README must document Kiro and AWS usage.

## 4. Out of scope

- PDF ingestion
- Full RAG
- Knowledge Graph
- Multiple autonomous agents
- Authentication
- Multi-tenant support
