# 0038 – Schemathesis Contract Fuzz

*Status*: **Accepted**

## Context

When we add an HTTP API, we want blind spots found before staging.

## Decision

Write an OpenAPI stub even for early endpoints; run **Schemathesis** in CI:

```
schemathesis --workers 4 run openapi.yaml
```

Uses Hypothesis strategies to fuzz parameters and headers.

## Alternatives Considered

\| Postman/Newman | Visual | No property-based fuzz |
\| Dredd | Lightweight | Limited payload variation |

## Consequences

* Early API breakage caught automatically.
* Test suite runtime +30 s; acceptable for PRs.
