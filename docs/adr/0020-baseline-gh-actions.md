# 0020 – Baseline GitHub Actions

*Status*: **Accepted**

## Context

Need a skeleton workflow before adding specialised jobs.

## Decision

Create `.github/workflows/ci.yml` with stages:

1. Checkout, setup Python + `uv`.
2. Call Nox `lint`, `tests`, `security`, `docs`.
3. Upload coverage artifact.

## Alternatives Considered

* Separate workflow per job – slower, duplicate setup.
* Local runner – faster but infrastructure overhead.

## Consequences

* Single cache warm-up, faster overall.
* Easy to extend: later jobs append new Nox sessions.

## Governance

Protect the default branch under **Settings → Branches → Protect main**.
Enable **Require status checks to pass** so merges only happen when CI succeeds.
