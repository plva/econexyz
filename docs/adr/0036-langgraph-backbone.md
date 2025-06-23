# 0036 – LangGraph Backbone

*Status*: **Accepted**

## Context

We need a structured orchestration layer that handles tool calls, retries,
and memory more transparently than raw prompt templates.

## Decision

Adopt **LangGraph** (StructuredTool + graph composition). Each registered tool
from `AGENTS.md` becomes a node; edges handle success/failure branches.

## Alternatives Considered

\| Option | Pros | Cons |
\| LangChain Agents | Popular | Less deterministic planning |
\| Home-grown loop | Full control | Reinvents planner, retries |

## Consequences

* Easier reasoning about agent plans; visible graph.
* Dependency on a still-young library; mitigated by ADR and swap path.
