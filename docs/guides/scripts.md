# Scripts Guide

This guide covers the helper scripts available for workflow and automation in EcoNexyz.

- Overview of available scripts
- How to use each script
- Best practices
- Troubleshooting

## Standup Automation

The `run_standup.py` script automates the cycle standup process:

### Basic Usage
```bash
# Run all enhanced standup features
python scripts/run_standup.py --all

# Basic analysis (dry run)
python scripts/run_standup.py --dry-run

# Generate commit message
python scripts/run_standup.py --generate-commit
```

### Individual Features
```bash
# Work delta summary
python scripts/run_standup.py --work-delta

# Documentation check
python scripts/run_standup.py --check-docs

# Blocker review
python scripts/run_standup.py --review-blockers

# Health checks
python scripts/run_standup.py --health-check
```

For complete documentation, see [`docs/workflows/standup_workflow.md`](docs/workflows/standup_workflow.md).

## Issue Management

### Creating Issues
```bash
python scripts/create_issue.py <category> <issue-name> [--tags tag1,tag2] [--priority level]
```

### Creating Bug Issues
```bash
# Create a new bug issue
python scripts/create_issue.py bugs <bug-name> --template bug --priority <level>

# Examples:
python scripts/create_issue.py bugs dashboard_not_loading --template bug --priority high
python scripts/create_issue.py bugs test_failure --template bug --priority medium
```

### Reopening Issues
```bash
# Reopen a closed issue (useful for regression bugs)
python scripts/create_issue.py --reopen <category>/<issue-name> --template <template>

# Example: Reopen a bug
python scripts/create_issue.py --reopen bugs/dashboard_not_loading --template bug
```

### Closing Issues
```bash
./scripts/close_issue.sh <category> <issue-name>
```

## Testing

### Run All Tests
```bash
./scripts/run_all_tests.sh
```

This runs both Python unit tests and commit hook validation tests.

## Sprint Management

### Archive Sprint
```bash
./scripts/archive_sprint.sh <sprint-name>
```

### AI Helper for Sprint Planning
```bash
python scripts/ai_helper.py
python scripts/ai_helper.py --fix  # Fix formatting issues
```

## Git Workflow

### Transactional Git Operations
```bash
./scripts/git_transaction.sh start "My commit message"
# ...make your changes...
./scripts/git_transaction.sh finalize
./scripts/git_transaction.sh rollback  # if needed
```

### Setup Git Hooks
```bash
./scripts/setup_hooks.sh
```

## Best Practices

1. **Use dry-run mode** when testing scripts
2. **Run tests** before committing changes
3. **Document new scripts** in this guide
4. **Use the standup script** for regular maintenance
5. **Check script permissions** if execution fails

## Troubleshooting

### Script Permission Issues
```bash
chmod +x scripts/*.sh
```

### Python Path Issues
```bash
export PYTHONPATH="${PYTHONPATH:-}:$(pwd)"
```

### Git Hook Issues
```bash
./scripts/setup_hooks.sh
python scripts/test_commit_hook.py
``` 