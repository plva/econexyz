# 0002 – Bootstrap `sh` + `uv`

*Status*: **Accepted**

## Context

New contributors (and agents) must move from clone to usable environment in minutes. Traditional solutions—Poetry, virtualenv + requirements.txt—either install slowly or leave room for “works-on-my-machine” drift.

## Decision

Use **`uv venv`** for environment creation and **`uv pip --freeze`** for lockfile generation. Wrap both in `bootstrap.sh`, which:

1. Creates/updates the `.venv` in the repo root.
2. Installs dev tools from `pyproject.toml`.
3. Offers to run `pre-commit install`.

Cold install target: < 3 minutes on GitHub hosted runners.

## Alternatives Considered

| Option           | Pros                               | Cons                                               |
| ---------------- | ---------------------------------- | -------------------------------------------------- |
| Poetry           | Mature community, lockfile support | Slower (\~4×), global cache confusion              |
| pip + virtualenv | Familiar                           | Non-deterministic unless we add third-party locker |
| Conda            | Handles binaries                   | 100 MB+ install, licence confusion                 |

## Consequences

* Fast, deterministic setup; matches CI exactly.
* Dependent on `uv` maturity (still < 1.0). If `uv` stagnates, rollback path is to Poetry; lockfile translation possible via `deptree freeze`.
