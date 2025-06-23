# 0003 – Optional Pre-commit Install

*Status*: **Accepted**

## Context

Some contributors prefer to review staged diffs before any auto-fix; others want hooks auto-installed. Enforcing hooks silently can break scripted commits (e.g., release bots).

## Decision

`bootstrap.sh` prints:

```
Install pre-commit hooks? [Y/n]:
```

* “Yes” → `pre-commit install --install-hooks`.
* “No” → sets Git config `core.hooksPath=.githooks_optional`. CI always runs hooks regardless.

## Alternatives Considered

* **Force install** – ensures consistency but surprises users.
* **Leave manual** – new contributors forget to install, leading to noisy CI failures.

## Consequences

* Local control, CI enforcement.
* Slight complexity in `bootstrap.sh`; acceptable.
