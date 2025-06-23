# 0019 – GitHub Label Strategy

*Status*: **Accepted**

## Context

Labels power automation: changelog categorisation, risk heat-maps, auto-routing.

## Decision

* Use GitHub Labeler Action to sync labels from `labels.yml`.
* Categories: `risk:high/med/low`, `type:feature/bug/docs`, `area:agent/core/docs`.

## Alternatives Considered

* Manual label curation – drifts over time.
* ZenHub or Jira fields – heavier process.

## Consequences

* Consistent labels for bots and humans.
* Contributors add new labels via PR to `labels.yml`.
