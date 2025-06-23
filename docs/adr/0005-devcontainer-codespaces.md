# 0005 – Dev-container / Codespaces

*Status*: **Accepted**

## Context

On-boarding should take minutes even on an iPad. GitHub Codespaces provides cloud VMs with VS Code in the browser; a `.devcontainer` spec pre-installs tools.

## Decision

Ship a checked-in `.devcontainer.json` that:

* Uses Debian slim image with system `git`, `curl`, `uv`.
* Runs `bootstrap.sh` on first start.
* Pre-installs VS Code extensions: Python, YAML, Docker, just-tasks.

## Alternatives Considered

* **Remote-Containers extension only** – works, but lacks 1-click Codespaces.
* **No dev-container** – fastest now, slower for every new contributor later.

## Consequences

* Near-zero setup in browser; demos run anywhere.
* Slight maintenance effort when base image needs patching.
