# 0042 – Docs Hosting Strategy

*Status*: **Accepted**

## Context

We need a reliable place to publish documentation without maintaining custom infrastructure. Read the Docs offers automated builds and search while allowing easy migration to GitHub Pages if needed.

## Decision

Host `econexyz` documentation on **Read the Docs** for now. A simple GitHub Pages workflow will remain as a fallback should Read the Docs become unsuitable.

## Consequences

* Minimal setup; docs build on every push.
* If Read the Docs limits or tooling changes, we can switch to Pages with little effort.
