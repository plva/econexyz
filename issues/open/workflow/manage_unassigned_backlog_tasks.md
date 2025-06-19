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

# workflow/manage_unassigned_backlog_tasks

Create a process for tracking tasks that are not yet assigned to a sprint and moving them into a sprint backlog when ready.

## Proposal

- Maintain a `backlog.json` in `state/` listing all unassigned tasks with metadata.
- Add a backburner topic exploring "offline sprints" that exist outside the
  normal sprint cycle; these may help split the project into sub-teams later.
- Provide a script `scripts/backlog.py` to add, remove, or move tasks.
- Create a follow-up issue for an agent that suggests tasks from `backlog.json`
  when a sprint is created.
- Update `TODO.md` and sprint files accordingly.
- Clarify that tasks moved from the backlog should appear in both `TODO.md` and
  the current sprint's metadata with matching status fields.
- Consider using labels or tags to categorize backlog items (e.g., `tech-debt`, `feature`).
- Add a backburner note to examine the difference between labels (type of task)
  and tags (modules or processes affected).
- Document the process in `docs/workflow/backlog-management.md`.
