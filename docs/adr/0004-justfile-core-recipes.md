# 0004 – Justfile Core Recipes

*Status*: **Accepted**

## Context

Agents and humans need a single place to discover common commands. `make` is ubiquitous but tab-sensitive and less friendly on Windows; shell scripts scatter logic.

## Decision

Adopt **`just`**. Root `Justfile` exposes verbs:

```
just ball          # Complete build pipeline (bootstrap + all checks)
just check         # Run all checks (health, tests, lint, types)
just test          # Run test suite
just lint          # Run linting and formatting
just types         # Static type analysis
just health-check  # Check dev environment dependencies
just commit        # Interactive commit with Commitizen
```

## Alternatives Considered

| Option            | Pros                 | Cons                                      |
| ----------------- | -------------------- | ----------------------------------------- |
| Make              | Installed everywhere | Tabs, poor Windows UX                     |
| Nox sessions only | Python-native        | Requires `nox -s`, harder discoverability |
| Bash scripts      | Zero deps            | Spaghetti over time                       |

## Consequences

* Clear self-documenting CLI; `just --list` acts as help.
* Requires `just` binary on dev machines (install via `uv tool install just`).
* `just ball` provides complete setup for new contributors.
* `just check` enables fast iteration during development.
