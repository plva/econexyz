# 0014 – Performance Regression Guard

*Status*: **Accepted**

## Context

Speed matters for agent inner loops. We need a tripwire for accidental slow-downs.

## Decision

Add `pytest-benchmark`. A Nox session runs benchmarks; results are compared to
the committed JSON baseline. Fail if any metric regresses >10 %.

## Alternatives Considered

| Option         | Pros            | Cons                          |
| -------------- | --------------- | ----------------------------- |
| asv (airspeed) | Rich dashboards | Heavy setup, uploads required |
| No guard       | Zero effort     | Latency creeps unnoticed      |

## Consequences

* Small JSON file under `benchmarks/`.
* Contributors update baseline only with intentional perf changes.
