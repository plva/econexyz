# Scripts Guide

This guide covers the available scripts in the EcoNexyz project.

- Overview of available scripts
- How to use each script
- Best practices
- Troubleshooting

## Standup Automation

The `run_standup.py` script automates the cycle standup process:

```bash
# Run all standup activities
python scripts/workflow/run_standup.py --all

# Dry run to see what would be done
python scripts/workflow/run_standup.py --dry-run

# Generate commit message
python scripts/workflow/run_standup.py --generate-commit
```

### Standup Options

```bash
# Generate work delta summary
python scripts/workflow/run_standup.py --work-delta

# Check documentation for new features
python scripts/workflow/run_standup.py --check-docs

# Review blockers and dependencies
python scripts/workflow/run_standup.py --review-blockers

# Perform health checks
python scripts/workflow/run_standup.py --health-check
```

For complete documentation, see [`docs/workflows/standup_workflow.md`](docs/workflows/standup_workflow.md).

## Issue Management

### Creating Issues

```bash
python scripts/workflow/create_issue.py <category> <issue-name> [--tags tag1,tag2] [--priority level]
```

### Creating Bug Reports

```bash
python scripts/workflow/create_issue.py bugs <bug-name> --template bug --priority <level>
```

Examples:
```bash
python scripts/workflow/create_issue.py bugs dashboard_not_loading --template bug --priority high
python scripts/workflow/create_issue.py bugs test_failure --template bug --priority medium
```

### Reopening Issues

```bash
python scripts/workflow/create_issue.py --reopen <category>/<issue-name> --template <template>
```

Example:
```bash
python scripts/workflow/create_issue.py --reopen bugs/dashboard_not_loading --template bug
```

### Closing Issues

```bash
./scripts/workflow/close_issue.sh <category> <issue-name>
```

## Testing

Run all tests:

```bash
./scripts/testing/run_all_tests.sh
```

Test commit hooks:

```bash
python scripts/testing/test_commit_hook.py
```

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