# 0017 – Bandit Security Scan

*Status*: **Accepted**

## Context

Static analysis for Python-specific security issues (e.g., `subprocess` misuse).

## Decision

Run **Bandit** as a Nox session on `src/**.py`, exclude tests.

## Alternatives Considered

* Skip – rely on CodeQL only; misses Python heuristics.
* Snyk CLI – paid for private repos.

## Consequences

* One more line of defence, \~2 s runtime.
* Occasional false positives; handled via `# nosec` with comment.
