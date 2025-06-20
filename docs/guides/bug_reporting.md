# Bug Reporting Guide

This guide explains how to report bugs and use the bug workflow in EcoNexyz.

## Quick Start

### Report a New Bug
```bash
# Create a new bug issue
python scripts/create_issue.py bugs <bug-name> --template bug --priority <level>

# Examples:
python scripts/create_issue.py bugs dashboard_not_loading --template bug --priority high
python scripts/create_issue.py bugs test_failure --template bug --priority medium
```

### Reopen a Closed Bug
```bash
# Reopen a previously closed bug
python scripts/create_issue.py --reopen bugs/<bug-name> --template bug

# Example:
python scripts/create_issue.py --reopen bugs/dashboard_not_loading --template bug
```

## Bug Priority Levels

- **critical**: System-breaking bugs that prevent core functionality
- **high**: Important bugs that significantly impact user experience
- **medium**: Moderate bugs that affect functionality but have workarounds
- **low**: Minor bugs, cosmetic issues, or enhancement requests

## Bug Report Template

When you create a bug issue, it will use the following template:

```markdown
# Bug Report

## Summary
(Briefly describe the bug)

## Steps to Reproduce
1. (First step)
2. (Second step)
3. (Third step)

## Expected Behavior
(What should happen)

## Actual Behavior
(What actually happens)

## Environment
- OS:
- Version:
- Other relevant details:

## Related Issues/PRs
(Link to related issues or PRs, especially if this is reopening a closed issue)

## Additional Context
(Stack traces, error messages, or other relevant information)
```

## Best Practices

### Writing Good Bug Reports

1. **Be specific**: Include exact steps to reproduce the issue
2. **Include environment details**: OS, version, browser, etc.
3. **Provide error messages**: Copy/paste exact error text
4. **Check for duplicates**: Search existing issues before creating new ones
5. **Use appropriate priority**: Don't mark everything as critical

### Bug Workflow

1. **Create the bug**: Use the script to create a properly formatted bug issue
2. **Fill in details**: Complete the template with specific information
3. **Assign priority**: Choose appropriate priority level
4. **Link related issues**: Reference any related bugs or PRs
5. **Update status**: Mark as resolved when fixed

### Regression Bugs

When a previously fixed bug reappears:

1. **Reopen the original issue**: Use `--reopen` flag to restore the closed issue
2. **Update the report**: Add new information about the regression
3. **Link to the fix**: Reference the PR or commit that originally fixed it
4. **Mark as regression**: Add regression tag and context

## Examples

### Example 1: New Bug Report
```bash
python scripts/create_issue.py bugs agent_crash_on_startup --template bug --priority high
```

This creates a high-priority bug issue with the proper template.

### Example 2: Reopening a Bug
```bash
python scripts/create_issue.py --reopen bugs/dashboard_not_loading --template bug
```

This reopens a previously closed dashboard loading issue.

### Example 3: Bug with Custom Tags
```bash
python scripts/create_issue.py bugs test_failure --template bug --priority medium --tags "test,regression"
```

This creates a medium-priority bug with additional tags.

## Integration with Development Workflow

- **During development**: Create bugs for issues you discover
- **During testing**: Use bug reports for test failures
- **During review**: Reference bug numbers in commit messages
- **During standup**: Review and update bug status

## Troubleshooting

### Common Issues

**Script not found**: Ensure you're in the project root directory
```bash
cd /path/to/econexyz
python scripts/create_issue.py bugs test_bug --template bug
```

**Template not found**: Check that the bug template exists
```bash
ls docs/templates/bug_template.md
```

**Category not found**: The bugs category should be automatically available
```bash
cat config/issue_categories.yml
```

### Getting Help

- Check the main [Scripts Guide](scripts.md) for general script usage
- Review the [Development Process](development.md) for workflow details
- Look at existing bug issues for examples
