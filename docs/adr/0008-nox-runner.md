# 0008 – Nox Runner

*Status*: **Accepted**

## Context

We need a task runner that can create disposable virtual envs for each session, handle matrix testing, and be scripted in Python.

## Decision

Adopt **Nox** over Tox. Reasons:

* Pure-Python config; easier dynamic logic.
* Re-use existing `.venv` when possible (`reuse_venv=True`).
* Plays well with `uv` inside sessions.

## Alternatives Considered

| Option       | Pros               | Cons                         |
| ------------ | ------------------ | ---------------------------- |
| Tox          | Mature, widespread | INI syntax, slower env reuse |
| Make         | Ubiquitous         | Harder matrix, shell-centric |
| Bash scripts | No deps            | Duplicated logic, OS quirks  |

## Consequences

* Single runner for tests, lint, docs, security scans.
* Contributors install `nox` (added to dev-dependencies).
