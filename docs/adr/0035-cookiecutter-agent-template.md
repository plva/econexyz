# 0035 – Cookiecutter Agent Template

*Status*: **Accepted**

## Context

Creating a new agent should be deterministic: code, schema, tests, docs.

## Decision

Cookiecutter in `templates/agent/` with prompts:

```
agent_name: Weather
slug: weather
description: Returns forecast
```

Generates:

```
src/agents/weather/__init__.py
src/agents/weather/schema.py
tests/agents/test_weather.py
docs/agents/weather.md
```

## Alternatives Considered

\| Copier | Simple | Less widespread |
\| Manual copy | Zero deps | Drifts quickly |

## Consequences

* One-command scaffold via `just new-agent`.
* Template maintenance overhead when base patterns evolve.
