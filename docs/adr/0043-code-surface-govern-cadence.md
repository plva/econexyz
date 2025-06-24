# 0043 – Code → Surface → Govern Cadence

*Status*: **Accepted**

## Context

Our development workflow revolves around a simple rhythm: implement code, surface the changes through documentation, and govern contributions via pull requests. While the practice exists informally, it is not explicitly documented.

## Decision

We adopt a "Code → Surface → Govern" cadence. Every significant code change must be surfaced in documentation and governed through a pull-request checklist. This ADR formalises the policy so that newcomers can easily follow it. The process aligns with [ADR 0001](0001-record-architecture-decisions.md), which defines how we manage ADRs overall.

## Alternatives Considered

- **Ad-hoc communication** – rely on memory or tribal knowledge; leads to drift and missed steps.
- **Fully automated enforcement** – strict CI gates could reject any undocumented change but add friction for rapid iteration.

## Consequences

- Contributors have a clear reminder to document and review their work.
- Pull requests include an explicit checkbox to confirm adherence.
- Slight overhead in ensuring docs stay in sync, balanced by greater project clarity.
