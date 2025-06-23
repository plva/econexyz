# 0026 – Semantic-release

*Status*: **Accepted**

## Context

Manual version bumps and CHANGELOG edits are error-prone. With Conventional
Commits we can derive both automatically.

## Decision

Use **python-semantic-release** in CI:

* Analyse commits since last tag.
* Decide version bump (major/minor/patch).
* Tag, push, and write `CHANGELOG.md`.

## Alternatives Considered

\| Option | Pros | Cons |
\| Standard-Version (JS) | Mature | Node runtime |
\| Manual bump | Simple | Human toil, skipped steps |

## Consequences

* Releases reflect actual change scope.
* Requires commit history to stay linear (no squash of multiple types).
