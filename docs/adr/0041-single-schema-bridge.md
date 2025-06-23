# 0041 – Single-Schema Bridge (Pydantic ↔ Strawberry)

*Status*: **Accepted**

## Context

We already model data in Pydantic; duplicating GraphQL types invites drift.

## Decision

Use **`strawberry.experimental.pydantic`** to auto-derive GraphQL types:

```python
@strawberry.experimental.pydantic.type(model=UserModel)
class User:
    pass
```

Schema builds directly from Pydantic, ensuring parity.

## Alternatives Considered

\| Hand-written Strawberry types | Full control | Drift risk, boilerplate |
\| datamodel-codegen | Generates code | Adds generation step |

## Consequences

* One source for REST, GraphQL, and OpenAI contracts.
* Experimental API may change; tracked via ADR.
