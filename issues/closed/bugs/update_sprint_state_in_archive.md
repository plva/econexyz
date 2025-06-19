---
status: open
category: bugs
tags:
  - bug
  - fix
  - critical
created: 2025-06-19
last-updated: 2025-06-19
priority: high
assigned: unassigned
---

# bugs/update_sprint_state_in_archive

## Summary

The `archive_sprint.py` script does not update the `state/sprint.json` file when archiving a sprint and creating a new one. This causes the sprint state to become out of sync with the actual current sprint.

## Problem

When running `python scripts/archive_sprint.py sprint-3 --new sprint-4`:
- The script archives sprint-3 and creates sprint-4
- But `state/sprint.json` still shows `{"current": 3}`
- This causes confusion and potential issues with other scripts that rely on the current sprint state

## Implementation Plan

### PR #1: Update archive_sprint.py to manage sprint state
- [ ] Add sprint state management to `archive_sprint.py`
- [ ] Update `state/sprint.json` when creating a new sprint
- [ ] Add validation to ensure state consistency
- [ ] Add unit tests for state management
- [ ] Update documentation

**Files to modify**:
- `scripts/archive_sprint.py` - Add state update logic
- `state/sprint.json` - Will be updated by the script

**Testing**:
- [ ] Test archiving sprint-3 with new sprint-4
- [ ] Verify `state/sprint.json` is updated to `{"current": 4}`
- [ ] Test error handling for invalid sprint names
- [ ] Test without `--new` flag (should not update state)

## Definition of Done
- [ ] `archive_sprint.py` updates `state/sprint.json` when creating new sprints
- [ ] State remains consistent with actual sprint directories
- [ ] Error handling for edge cases
- [ ] Tests pass
- [ ] Documentation updated