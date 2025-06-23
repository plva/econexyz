# 0018 – pip-audit Scan

*Status*: **Accepted**

## Context

Lockfile needs CVE scanning; Safety is slower and paid for GitHub integration.

## Decision

Add **pip-audit** run inside Nox, pointed at `uv.lock`. Fail on high-severity
unpatched CVEs.

## Alternatives Considered

* Safety – requires token for full DB.
* OSV-scanner – language-agnostic, but pip support still maturing.

## Consequences

* Early warning on vulnerable transitive deps.
* False positives possible until fix metadata propagates.
