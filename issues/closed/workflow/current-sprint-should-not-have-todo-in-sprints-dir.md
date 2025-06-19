---
status: closed
category: workflow
tags:
  - bug 
created: 2025-06-19
last-updated: 2025-06-19
priority: medium
assigned: plva + codex 
------------------------

# workflow/current-sprint-should-not-have-todo-in-sprints-dir

The current sprint has its own TODO.md file. The current sprint's TODO is the same as the top level hierarchy TODO.md. We should only be moving a copy of the top level TODO to the archived sprint's directory when a sprint is over and archived, and not storing a copy before.

## Implementation Plan

### PR #1: Remove TODO.md from current sprint directory
- [x] Remove the empty TODO.md file from `sprints/open/sprint-3/`
- [x] Verify that `scripts/archive_sprint.py` already correctly copies TODO.md to archived sprints
- [x] Verify that `scripts/create_issue.py` doesn't create TODO.md in current sprint directories

**Files modified**:
- Deleted: `sprints/open/sprint-3/TODO.md`

**Testing completed**:
- [x] Verified the current sprint still works without the TODO.md file
- [x] Verified that archiving a sprint still creates the TODO.md copy correctly
- [x] Verified that creating new issues doesn't create TODO.md in sprint directories

## Definition of Done
- [x] Delete the current sprint's todo (making sure that anything there is tracked at the top level)
- [x] Amend scripts for issue creation, sprint archival, etc, to make sure these constraints are met

**Status**: ✅ COMPLETED - The issue has been resolved by removing the unnecessary TODO.md file from the current sprint directory. The archive_sprint.py script already correctly handles copying TODO.md to archived sprints, so no additional script changes were needed.
