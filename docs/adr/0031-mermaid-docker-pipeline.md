# 0031 – Mermaid Docker Pipeline

*Status*: **Accepted**

## Context

Architecture diagrams help onboard humans and agents, but Node-based builds add weight. `sphinxcontrib-mermaid` is unmaintained, and local Node installs vary.

## Decision

Use **Mermaid CLI** in an official Docker image:

```
docker run --rm -v diagrams/:/data ghcr.io/mermaid-js/mermaid-cli/mermaid-cli -i diagram.mmd
```

* `docs/diagrams/*.mmd` source.
* Rendered SVGs committed under `docs/diagrams/rendered/`.
* Nox session `docs-diagrams` updates images; CI fails if SVGs drift.

## Alternatives Considered

| Option                | Pros         | Cons                            |
| --------------------- | ------------ | ------------------------------- |
| sphinxcontrib-mermaid | Inline build | Unmaintained, Node dep          |
| PlantUML + Java       | Mature       | Requires Java, different syntax |

## Consequences

* No local Node install; runs identically in CI.
* Contributors need Docker; acceptable given dev-container.
