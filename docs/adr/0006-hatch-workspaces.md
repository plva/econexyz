# 0006 – Hatch Workspaces

*Status*: **Accepted**

## Context

Today we have one package; tomorrow we may split core, plugins, or shared proto models. Managing multiple `pyproject`s without pain is the goal.

## Decision

Enable **Hatch workspaces** in root `pyproject.toml`, allowing sub-packages under `packages/` to be built and tested together.

## Alternatives Considered

| Option                 | Pros       | Cons                          |
| ---------------------- | ---------- | ----------------------------- |
| Pants                  | Powerful   | Heavy, steeper learning curve |
| Poetry multi-project   | Familiar   | Limited workspace features    |
| Monorepo with sub-venv | Simple now | Dependency duplication later  |

## Consequences

* Easy path to multi-package repo.
* Developers must learn Hatch commands (`hatch run`, `hatch build`).
