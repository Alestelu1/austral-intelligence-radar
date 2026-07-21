# Austral Intelligence Radar

Specialized AI agent for analyzing, classifying and preserving the provenance of southern Chilean and Antarctic information sources.

## Hackathon

- Event: Hackathon Kiro by Código Facilito and AWS
- Challenge: Reto 3 — Agentes especializados
- Development period: 20–27 July 2026
- Participant: Alexis Stelu
- Status: MVP in development

## Problem

Researchers, editors and developers working with territorial and Antarctic information must manually review scattered sources, identify their geographic scope, extract relevant entities, assess editorial value and preserve provenance. This process is repetitive, slow and prone to losing traceability.

## Proposed solution

Austral Intelligence Radar receives source content and produces a structured analysis containing:

- title;
- summary;
- territory;
- category;
- detected entities;
- original source;
- related Austral Beacon project;
- editorial relevance;
- confidence level;
- human-review requirement.

## MVP workflow

```text
Source text
    ↓
Specialized AI analysis
    ↓
Structured JSON result
    ↓
AWS persistence
    ↓
Human-readable result
```

## Planned stack

- Kiro IDE and Spec-Driven Development
- Python
- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- Amazon Bedrock or another AWS-compatible model service
- Minimal web interface

## Out of scope for the hackathon

- Full RAG platform
- Knowledge Graph
- Multiple autonomous agents
- Massive PDF ingestion
- Complete Austral Beacon editorial dashboard
- Authentication and multi-user management

## Repository structure

```text
.kiro/
├── steering/
└── specs/
    └── austral-intelligence-radar/
        ├── requirements.md
        ├── design.md
        └── tasks.md

docs/
src/
tests/
```

## Success criteria

- A user can submit source text.
- The agent returns valid structured analysis.
- The result preserves source provenance.
- Uncertain claims are marked for human review.
- The application is publicly demonstrable.
- AWS and Kiro usage are documented.

## License

MIT
