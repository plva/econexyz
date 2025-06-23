# 0025 – Commitizen Conventional Commits

*Status*: **Accepted**

## Context

Consistent commit messages enable automated changelogs, semantic versioning, and
easier blame. Asking agents to memorise a regex is fragile.

## Decision

Install **Commitizen** (`cz`). Developers run `cz commit`; agents are scripted
similarly. Enforce message lint in pre-commit (`commitizen check --allow-empty`).

## Alternatives Considered

\| Option | Pros | Cons |
\| commitlint + Husky | Popular in JS | Node dependency |
\| Conventional-Changelog CLIs | OK | No interactive wizard |

## Consequences

* Uniform messages, lower friction via wizard prompts.
* Occasionally agents need prompt engineering to answer wizard questions.
