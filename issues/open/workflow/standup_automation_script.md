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
# workflow/standup_automation_script

## Summary

Create comprehensive documentation and automation for the cycle standup process.

## Motivation

The cycle standup process was previously documented in basic form but lacked:
- Detailed step-by-step instructions
- Visual workflow diagrams
- Automation scripts
- Clear commit message templates
- Troubleshooting guidance

This makes standups error-prone and inconsistent across contributors.

## Requirements

### Documentation
- [x] Create detailed standup workflow document (`docs/workflows/standup_workflow.md`)
- [x] Add mermaid diagram showing the complete process
- [x] Document all scripts and commands used
- [x] Include troubleshooting section
- [x] Add to workflows README

### Automation Script
- [x] Create `scripts/run_standup.py` automation script
- [x] Find last standup commit automatically
- [x] List and analyze commits since last standup
- [x] Suggest potential issue completions
- [x] Generate standup commit message template
- [x] Provide dry-run mode for testing

### Features
- [x] Commit analysis by type ([fix], [workflow], [agents], etc.)
- [x] Issue completion detection
- [x] Commit message generation
- [x] Step-by-step guidance
- [x] Error handling and validation

## Implementation

### PR #1: Documentation
- [x] Create `docs/workflows/standup_workflow.md`
- [x] Add comprehensive mermaid diagram
- [x] Document all steps and best practices
- [x] Update workflows README

### PR #2: Automation Script
- [x] Create `scripts/run_standup.py`
- [x] Implement commit analysis
- [x] Add issue completion detection
- [x] Generate commit message templates
- [x] Add dry-run and help options

### PR #3: Integration
- [ ] Add script to bootstrap process
- [ ] Update development guide references
- [ ] Add unit tests for script
- [ ] Create usage examples

## Usage

### Basic Usage
```bash
# Run standup analysis
python scripts/run_standup.py --dry-run

# Generate commit message
python scripts/run_standup.py --generate-commit
```

### Manual Process
1. Run `python scripts/run_standup.py --dry-run`
2. Review suggested completions
3. Close completed issues: `./scripts/close_issue.sh <category> <issue>`
4. Update TODO.md and sprint metadata
5. Run tests: `./scripts/run_all_tests.sh`
6. Generate and commit: `python scripts/run_standup.py --generate-commit`

## Acceptance Criteria
- [x] Comprehensive documentation with visual workflow
- [x] Working automation script with dry-run mode
- [x] Commit message generation
- [x] Issue completion detection
- [x] Clear usage instructions
- [x] Integration with existing workflow