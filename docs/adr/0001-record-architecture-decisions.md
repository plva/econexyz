# 0001 – Record Architecture Decisions

*Status*: **Accepted**

## Context

Teams change, tools age, and “why did we do this?” is the most expensive question to answer from scratch. We need a lightweight, repeatable way to capture reasoning so future contributors—human or AI—can trace, critique, or reverse a choice without code archaeology.

## Decision

Adopt Michael Nygard–style Architecture Decision Records (ADRs) in `docs/adr/`, one Markdown file per major choice.

* Template lives at `docs/adr/_template.md`.
* Sequential IDs, kebab-case titles.
* Status field tracks lifecycle (Proposed → Accepted → Superseded).

## Alternatives Considered

* **Wiki pages** – easy to start, hard to version, harder to review.
* **Commit messages only** – context buried in logs; merges obscure history.
* **Inline docs in READMEs** – discoverability issues once several topics grow.

## Consequences

* Clear audit trail; design discussions become first-class artefacts.
* New joiners ramp faster; models can cite decisions directly.
* Slight paperwork overhead—acceptable given infrequent creation rate.
