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

# workflow/automate_todo_sprint_migration

Automate the migration of tasks between the top-level TODO.md and sprint TODO files, including:
- Moving tasks into the current sprint when planned
- Removing or archiving completed tasks
- Keeping TODO.md and sprint files in sync
- Providing a CLI or script for maintainers to use

This will reduce manual effort and ensure consistency across planning documents. 
## Implementation Approach

- Parse `TODO.md` and the current sprint's `sprint-meta.md` to identify tasks
  that should move between the global backlog and the sprint backlog.
- Use `scripts/ai_helper.py --fix` to normalize sprint files (ensuring
  consistent metadata formatting) before updates.
- Provide a command `scripts/migrate_todos.py` that offers interactive prompts for selecting tasks to move.
- Maintain a log of migrations in `state/migration-log.yml` for audit purposes.
- Add regression tests in `tests/test_migrate_todos.py`.
