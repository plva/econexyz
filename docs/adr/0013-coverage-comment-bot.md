# 0013 – Coverage Comment Bot

*Status*: **Accepted**

## Context

Private repos make external SaaS (Codecov) paid. We still want inline feedback.

## Decision

Use the **`python-coverage-comment` GitHub Action**. On PRs it:

1. Parses `.coverage` file.
2. Posts (or updates) a summary comment.
3. Uploads SVG badge to a `coverage-badge` branch.

## Alternatives Considered

* Codecov (paid) – nice UI, but outside budget.
* Bare artifacts – no inline diff; low visibility.

## Consequences

* Maintainers see coverage delta at a glance.
* One extra job (<30 s) in workflow.
