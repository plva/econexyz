# 0021 – CodeQL Analysis

*Status*: **Accepted**

## Context

Static analysis tools like Bandit catch common patterns, but we need deeper
taint-flow checks that follow data across functions, files, and third-party
calls. GitHub’s CodeQL provides that depth and runs free on public or private
repos.

## Decision

Enable the default **GitHub CodeQL workflow** for Python and
JavaScript (future front-end). Scan on every push to `main` and on pull
requests. Upload SARIF results for in-UI triage.

## Alternatives Considered

| Option            | Pros            | Cons                    |
| ----------------- | --------------- | ----------------------- |
| Semgrep OSS rules | Fast, low setup | Shallower flow analysis |
| LGTM (legacy)     | Historical      | Superseded by CodeQL    |
| Paid SAST (Snyk)  | Rich UI         | Budget impact           |

## Consequences

* One more security gate; runtime < 2 min on current code.
* False positives triaged via CodeQL dashboard and `codeql-yml` suppressions.
