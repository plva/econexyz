# 0012 – Coverage Baseline

*Status*: **Accepted**

## Context

We want to stop coverage from silently eroding as agents add code.

## Decision

Use **`pytest-cov`** to generate coverage XML; fail the session if total
coverage drops below the rolling average (`--cov-fail-under=$(cat .cov_target)`).
`.cov_target` is bumped only by an explicit PR.

## Alternatives Considered

* Hard-code 90 % threshold – brittle when test mix changes.
* Skip coverage – saves minutes, but lets dead code grow.

## Consequences

* Clear, adjustable target; agents can read file to know goal.
* Adds \~5–10 s to test run on current codebase.
