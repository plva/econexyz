# 0015 – Ruff Lint + Format

*Status*: **Accepted**

## Context

Flake8 + Black + isort run in \~10 s locally; Ruff does all in \~200 ms.

## Decision

Adopt **Ruff** with `pyproject.toml`:

```toml
[tool.ruff]
select = ["E", "F", "UP", "I"]
line-length = 120
format = "ruff"
```

`UP` enables Pyupgrade rules.

## Alternatives Considered

* Keep existing trio – familiar but slower.
* `pylint` – thorough, but heavy and chatty.

## Consequences

* Faster feedback; single dependency.
* Some niche Flake8 plugins not yet ported (acceptable).
