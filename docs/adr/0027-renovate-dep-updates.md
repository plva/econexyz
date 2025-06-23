# 0027 – Renovate Dependency Updates

*Status*: **Accepted**

## Context

Dependency drift is inevitable; batching updates reduces noise.

## Decision

Add Renovate GitHub app with config:

* Group deps by ecosystem and stability.
* Weekly “maintenance” PRs.
* Autoclose PR if tests fail.

## Alternatives Considered

\| Option | Pros | Cons |
\| Dependabot | Built-in, simpler | Limited grouping |
\| Update manually | Full control | Time-consuming |

## Consequences

* Predictable upgrade cadence.
* Occasional rebase conflicts; mitigated by weekly schedule.
