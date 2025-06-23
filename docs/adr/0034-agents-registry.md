# 0034 – `AGENTS.md` Registry

*Status*: **Accepted**

## Context

Agents need a single discoverable list of available tools, their arguments, and owners.

## Decision

Plain-text Markdown table:

| Tool | Input Schema | Output Schema | Owner | Description |
| ---- | ------------ | ------------- | ----- | ----------- |

Updated by PR; generator script (`just agents`) inserts new rows.

## Alternatives Considered

\| YAML file | Easy parse | Less readable in GitHub preview |
\| Database | Queryable | Over-engineered for now |

## Consequences

* Humans skim; agents parse via Markdown AST.
* Diff reviews reveal contract changes.
