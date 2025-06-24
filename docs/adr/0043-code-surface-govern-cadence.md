# 0043 – Code → Surface → Govern Cadence

*Status*: **Accepted**

## Context

We want a lightweight rhythm for evolving the project. Each feature or policy should start in code, then be surfaced in documentation, and finally governed through automation or review. ADR 0001 describes how we capture such decisions.

## Decision

Adopt the **Code → Surface → Govern** cadence:

1. **Code** – implement the change.
2. **Surface** – document it prominently so contributors understand the impact.
3. **Govern** – ensure compliance via PR templates, CI, or other checks.

## Alternatives Considered

- Do nothing – tribal knowledge would make onboarding difficult.
- Long policy documents – comprehensive but rarely read.

## Consequences

* Contributors have a clear workflow for rolling out policies.
* Documentation stays in sync with project practices.
* Governance steps can evolve as automation improves.

