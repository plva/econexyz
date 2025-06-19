---
status: closed
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

# workflow/remove_completed_sprint_todos_on_archive

Remove completed sprint-related entries from the top level TODO.md when archiving a sprint.

## Details

- Extend `scripts/archive_sprint.sh` to parse `TODO.md` and remove entries marked as done within the archived sprint.
- A snapshot of `TODO.md` is stored in the archived sprint directory, so there's
  no need to keep completed tasks elsewhere.
- Update documentation in `docs/workflow/archiving.md` with usage instructions.
- Provide unit tests in `tests/test_archive_sprint.py` to validate the removal logic.
