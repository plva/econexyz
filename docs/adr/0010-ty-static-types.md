# 0010 – Ty Static Types

*Status*: **Accepted**

## Context

We want strict type checking but mypy’s performance can slow large codebases. `Ty` wraps mypy in Rust for speed.

## Decision

Use **Ty** (`uv tool install ty`). Run as a Nox session and pre-commit hook.

## Alternatives Considered

| Option   | Pros                 | Cons                                       |
| -------- | -------------------- | ------------------------------------------ |
| Raw mypy | Stable, feature-rich | 2-4× slower; higher CI time                |
| Pyright  | Fast                 | Slightly different type system; needs Node |
| None     | No overhead          | Bugs appear later                          |

## Consequences

* < 5 s type check in CI on current codebase.
* Ty is pre-release; if abandoned, fallback is to mypy with same flags.
