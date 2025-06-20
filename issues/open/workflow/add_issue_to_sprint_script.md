------------------------
status: open
category: workflow
tags:
- workflow
- meta
- devops
- automation
created: 2025-06-19
last-updated: 2025-06-19
priority: medium
assigned: unassigned
------------------------
# workflow/add_issue_to_sprint_script

## Summary

Create a script to add issues to sprints, updating both the sprint meta file and TODO.md.

## Motivation

Currently, adding issues to sprints requires manual editing of:
- `sprints/open/sprint-X/sprint-meta.md`
- `TODO.md`

This is error-prone and inconsistent. A script would ensure:
- Consistent formatting
- Proper issue path references
- Automatic TODO.md updates
- Validation of issue existence

## Requirements

### Core Features
- Add issue to specified sprint
- Update sprint meta file with proper formatting
- Update TODO.md to mark issue as assigned to sprint
- Validate that issue file exists
- Support for different issue categories (workflow, bugs, etc.)

### Command Line Interface
```bash
python scripts/add_issue_to_sprint.py <sprint-name> <category> <issue-name>
# Example:
python scripts/add_issue_to_sprint.py sprint-4 workflow create_dao_for_smart_agent_integration
```

### Validation
- Check that sprint exists and is open
- Verify issue file exists in correct category
- Ensure issue is not already assigned to another sprint
- Validate issue metadata format

## Implementation Plan

### PR #1: Basic Script
- [ ] Create `scripts/add_issue_to_sprint.py`
- [ ] Basic CLI interface
- [ ] Sprint meta file updates
- [ ] Issue existence validation

### PR #2: TODO.md Integration
- [ ] Update TODO.md to mark issue as assigned
- [ ] Handle different issue categories
- [ ] Add unit tests

### PR #3: Advanced Features
- [ ] Support for bulk operations
- [ ] Dry-run mode for testing
- [ ] Undo functionality
- [ ] Integration with existing sprint scripts

## Acceptance Criteria
- [ ] Script successfully adds issues to sprints
- [ ] Updates both sprint meta and TODO.md
- [ ] Proper error handling and validation
- [ ] Unit tests with good coverage
- [ ] Documentation and usage examples 