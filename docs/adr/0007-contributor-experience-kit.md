# 0007 – Contributor Experience Kit

*Status*: **Accepted**

## Context

External contributors—including AI agents—benefit from clear templates and rules of engagement.

## Decision

* `CONTRIBUTING.md` – setup, lint, test, commit flow.
* Issue templates: bug, feature, question.
* PR template with checklist.
* Contributor Covenant 2.1 as `CODE_OF_CONDUCT.md`.

## Alternatives Considered

* **No templates** – fastest now, but yields low-quality issues.
* **Third-party bots for templates** – additional infra, latency.

## Consequences

* Higher-quality issues/PRs.
* Slight repo noise; acceptable trade-off.

## Ignored Artefacts Strategy

Ephemeral build outputs and editor settings clutter reviews. We only version
source files so that diffs stay focused on real changes.

- *Python build & cache* – caches and virtual environments.
- *Packaging artifacts* – wheels, eggs and build dirs.
- *Editor/IDE noise* – local IDE state like `.vscode`.
- *Container & SBOM outputs* – SBOM and container caches.
- *Docs & coverage artefacts* – built docs and coverage reports.

New patterns must update this list and `.gitignore`. IDE-specific rules belong
under the "Editor/IDE noise" block.
