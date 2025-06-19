---
status: open
category: workflow
tags:
  - devops
  - meta
  - workflow
created: 2025-06-18
last-updated: 2025-06-19
priority: medium
assigned: "plva + codex"
------------------------

# workflow/document_sprint_and_meta_sprint_process

Document the sprint and meta-sprint process, including:
- How to plan, run, and close sprints
- How to use scripts for sprint management (e.g., archiving, moving issues)
- How to handle meta-sprints and their relationship to regular sprints
- Where to find workflow diagrams and how to interpret them

This should be included in the documentation and referenced in onboarding materials. 
## Key Topics

- Define `sprint-meta.md` fields such as `start-date`, `end-date`, `capacity`, and `goals`.
- Clarify the difference between a sprint (regular feature work) and a meta-sprint (process or automation improvements).
- Describe the lifecycle:
  1. Planning using `scripts/ai_helper.py` to gather tasks.
  2. Execution with regular updates in `TODO.md`.
  3. Archiving via `scripts/archive_sprint.sh` which moves sprint files to `sprints/archived/`.
- Provide diagrams in `docs/diagrams/workflow/` to visualize the process.
- Include sample commands for starting a new sprint and linking issues.
