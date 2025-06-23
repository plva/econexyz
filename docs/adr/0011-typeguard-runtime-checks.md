# 0011 – Typeguard Runtime Checks

*Status*: **Accepted**

## Context

Static analysis catches many type errors, but values can still go wrong at
runtime (e.g., data loaded from JSON). We want a lightweight check that runs
during tests without affecting production performance.

## Decision

Add **`pytest-typeguard`** (Typeguard in “importlib” mode). A Nox session
invokes:

```bash
pytest -m "not slow" --typeguard-packages=src
```

## Alternatives Considered

| Option                        | Pros          | Cons                                |
| ----------------------------- | ------------- | ----------------------------------- |
| No runtime check              | Zero overhead | Bugs surface in prod paths only     |
| Pydantic `validate_call`      | Rich errors   | Adds heavy dependency to every func |
| Monkeypatch `__annotations__` | DIY           | Fragile, hard to maintain           |

## Consequences

* Extra safety net during CI.
* Opt-out in performance-critical tests by using `@typechecked(always=False)`.
