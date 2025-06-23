# 0037 – JSON-Schema Export

*Status*: **Accepted**

## Context

Tools declare input/output via Pydantic models; schemas needed for OpenAI function calling, docs, and tests.

## Decision

Each tool’s `schema.py` calls:

```python
model.schema_json(indent=2)
```

Outputs saved under `schemas/{slug}.json`. A Nox session verifies schemas diff.

## Alternatives Considered

* Runtime generation only | Fewer files | Hard to review in PR |
* Avro / Protobuf | Faster | Adds compiler, no human JSON

## Consequences

* Schemas provide contract diff surface.
* Adds small repo footprint (≈ 2 KB per tool).
