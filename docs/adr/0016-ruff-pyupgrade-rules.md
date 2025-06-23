# 0016 – Ruff Pyupgrade Rules

*Status*: **Accepted**

## Context

We want modern syntax without a separate tool.

## Decision

Enable Ruff’s `UP` ruleset and auto-fix in pre-commit (`ruff check --fix`).

## Alternatives Considered

* Stand-alone `pyupgrade` hook – another install step.
* Manual refactors – error-prone.

## Consequences

* New code converges on current Python best practices automatically.
