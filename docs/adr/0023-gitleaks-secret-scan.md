# 0023 – Gitleaks Secret Scan

*Status*: **Accepted**

## Context

Accidentally committed credentials are costly to rotate. We want detection both
locally and in CI.

## Decision

* Local: pre-commit hook `gitleaks detect --staged`.
* CI: `gitleaks/gitleaks-action@v2` on each PR; fail job on secret match.
* Custom allow-list `.gitleaks.toml` for test fixtures.

## Alternatives Considered

\| Option | Pros | Cons |
\| GH Push Protection | Built-in | Only after push; no local check |
\| TruffleHog OSS | Broad regex | Higher false-positive rate |

## Consequences

* Stops secrets before they hit `main`.
* Occasional tuning of regex allow-list required.
