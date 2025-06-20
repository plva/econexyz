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
# workflow/add_issue_references_script

## Summary

Create a script to add references, blockers, and dependencies between issues.

## Motivation

Currently, adding references between issues (like blockers, dependencies, related issues) requires manual editing of issue files. This is error-prone and inconsistent. A script would ensure:
- Consistent formatting of references
- Proper issue path validation
- Automatic bidirectional linking
- Standardized reference types

## Requirements

### Core Features
- Add references between issues
- Support different reference types:
  - `blocks` - This issue blocks another
  - `blocked-by` - This issue is blocked by another
  - `depends-on` - This issue depends on another
  - `related-to` - This issue is related to another
- Update issue metadata with references
- Validate that referenced issues exist

### Command Line Interface
```bash
python scripts/add_issue_reference.py <category> <issue-name> <reference-type> <ref-category> <ref-issue-name>
# Examples:
python scripts/add_issue_reference.py workflow agent_smart_issue_creator blocked-by workflow create_dao_for_smart_agent_integration
python scripts/add_issue_reference.py workflow create_dao_for_smart_agent_integration blocks workflow agent_smart_issue_creator
```

### Reference Types
- `blocks` - Add to blocking issue: "This issue blocks: [ref-issue]"
- `blocked-by` - Add to blocked issue: "This issue is blocked by: [ref-issue]"
- `depends-on` - Add to dependent issue: "This issue depends on: [ref-issue]"
- `related-to` - Add to both issues: "Related issues: [ref-issue]"

## Implementation Plan

### PR #1: Basic Script
- [ ] Create `scripts/add_issue_reference.py`
- [ ] Basic CLI interface
- [ ] Issue metadata updates
- [ ] Reference validation

### PR #2: Reference Types
- [ ] Implement all reference types
- [ ] Bidirectional linking support
- [ ] Add unit tests

### PR #3: Advanced Features
- [ ] Bulk reference operations
- [ ] Reference visualization
- [ ] Circular dependency detection
- [ ] Integration with sprint planning

## Acceptance Criteria
- [ ] Script successfully adds references between issues
- [ ] Supports all reference types
- [ ] Proper validation and error handling
- [ ] Unit tests with good coverage
- [ ] Documentation and usage examples 