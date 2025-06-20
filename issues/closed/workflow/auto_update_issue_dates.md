---
status: open
category: workflow
tags:
  - bug
  - fix
  - critical
created: 2025-06-19
last-updated: 2025-06-19
priority: medium
assigned: unassigned
---

# workflow/auto_update_issue_dates

## Summary

Issue files' `last-updated` field is not automatically updated when the issue file is modified, leading to outdated timestamps and confusion about when changes were actually made.

## Steps to Reproduce

1. Modify an issue file in `issues/open/` or `issues/closed/`
2. Commit the changes
3. Check the `last-updated` field in the issue file
4. Observe the date is not updated to reflect the current commit

## Expected Behavior

The `last-updated` field should automatically update to the current date when an issue file is modified and committed.

## Actual Behavior

The `last-updated` field remains unchanged, showing outdated information.

## Environment

- Repository: EcoNexyz
- Workflow: Git-based issue tracking
- Issue files: Markdown files in `issues/` directory

## Related Issues/PRs

- Related to AI agent workflow and issue management
- Builds on existing `scripts/close_issue.sh` and `scripts/create_issue.py`

## Additional Context

From AI agent PR notes: "The issue file's last-updated field was changed to '2025-06-20,' marking the first checklist item as complete. This date may not represent the current date."

## Implementation Plan

### PR #1: Create Git Pre-commit Hook for Issue Date Updates
- [ ] Create `scripts/update_issue_dates.py` script
- [ ] Add logic to detect modified issue files in staged changes
- [ ] Implement automatic `last-updated` field updates
- [ ] Add validation for issue file format
- [ ] Create unit tests for the script

### PR #2: Integrate with Git Hooks
- [ ] Create `.git/hooks/pre-commit` hook
- [ ] Call `update_issue_dates.py` from the hook
- [ ] Add error handling and rollback on failure
- [ ] Test hook integration

### PR #3: Documentation and Configuration
- [ ] Update `docs/guides/development.md` with hook setup
- [ ] Add configuration options for hook behavior
- [ ] Create troubleshooting guide
- [ ] Update `AGENTS.md` with new workflow

## Technical Approach

**Leverage Existing Infrastructure:**
- Use existing issue file parsing from `scripts/close_issue.sh`
- Build on the metadata header format already established
- Integrate with existing git workflow patterns

**Script Design:**
```python
def update_issue_dates():
    """Update last-updated field for modified issue files."""
    # Get staged files
    # Filter for issue files
    # Update last-updated field
    # Stage the changes
```

**Git Hook Integration:**
```bash
#!/bin/bash
# .git/hooks/pre-commit
python scripts/update_issue_dates.py
```

## Definition of Done
- [ ] Git pre-commit hook automatically updates `last-updated` for modified issue files
- [ ] Hook handles errors gracefully without blocking commits
- [ ] Documentation updated for contributors
- [ ] Tests pass
- [ ] Hook works for both open and closed issues