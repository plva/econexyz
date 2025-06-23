# 0039 – JSON-Schema Contract Tests

*Status*: **Accepted**

## Context

Internal message passing (e.g., agent → tool) needs validation too.

## Decision

Combine `jsonschema` with Hypothesis’ `from_schema` to generate arbitrary valid payloads; assert round-trip.

## Alternatives Considered

* Manual asserts | Simple | Coverage gaps |
* Pydantic `validate` only | Runtime | No fuzz coverage

## Consequences

* Tighter message guarantees; reproduces edge cases for free.
* Adds ≈ 3 s to test suite.
