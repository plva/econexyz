# 0040 – Hypothesis GraphQL Fuzz

*Status*: **Accepted**

## Context

GraphQL schema and resolvers diverge easily.

## Decision

Use **hypothesis-graphql** session to generate random queries against live schema; fail on resolver errors or mismatched types.

## Alternatives Considered

\| Option | Pros | Cons |
\| Manual introspection tests | Quick | Sparse coverage |
\| Apollo Fuzz | JS, good | Separate runtime stack |

## Consequences

* Finds SDL/runtime mismatches early.
* Requires running API in test mode; handled by Nox.
