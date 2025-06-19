# Commit Message Guidelines

This guide covers our commit message standards and tools for generating consistent commit messages.

## Quick Start

### Using Templates (Recommended)

We provide pre-made commit message templates for different types of changes:

```bash
# Create a template file for a bugfix
python scripts/commit_message.py --template bugfix

# Use the template with git
git commit -F /tmp/commit_template_bugfix.md
```

### Interactive Mode

```bash
python scripts/commit_message.py --interactive
```

### Command Line

```bash
python scripts/commit_message.py --type bugfix --description "fix issue path resolution"
```

## Commit Types

We use the following commit types:

- `[bugfix]` - Fixes a bug
- `[feature]` - Adds a new feature  
- `[workflow]` - Changes to workflow, scripts, or documentation
- `[agents]` - Changes to agent system
- `[dashboard]` - Changes to dashboard or UI
- `[bus]` - Changes to message bus system
- `[cross]` - Cross-cutting changes (tests, CI, etc.)
- `[standup]` - Cycle stand-up updates (TODO.md, sprint meta)
- `[sprint-planning]` - Sprint planning activities
- `[temp]` - Temporary commits for testing

## Template System

### Available Templates

We provide actual commit message templates in `docs/templates/commit_messages/`:

- `bugfix.md` - For bug fixes
- `feature.md` - For new features
- `workflow.md` - For workflow changes
- `standup.md` - For stand-up updates

### Using Templates

1. **Create a template file:**
   ```bash
   python scripts/commit_message.py --template bugfix
   ```

2. **Edit the template file** (it will be in `/tmp/commit_template_bugfix.md`)

3. **Commit using the template:**
   ```bash
   git commit -F /tmp/commit_template_bugfix.md
   ```

### Template Format

Templates include:
- Pre-filled commit type header
- Placeholder for description
- Commented guidance (lines starting with `#`)
- Git automatically removes comment lines

Example template content:
```markdown
[bugfix] 



# Brief description of the bug fix
# 
# - What was the problem?
# - How was it fixed?
# - Any related issues or PRs?
# 
# Lines starting with # will be removed from the final commit message.
```

## Message Format

### Header
- Format: `[type] description`
- Max 50 characters
- Start with commit type in brackets
- Use imperative mood ("add" not "added")

### Body (Optional)
- Max 72 characters per line
- Explain what and why, not how
- Reference issues with `#123`

### Examples

```
[bugfix] fix issue path resolution in create_issue.py

Fixed bug where issue paths were being created as relative instead
of absolute paths. This caused issues when creating issues from
different directories.

Closes #45
```

```
[workflow] add commit message validation hook

Added git commit-msg hook to validate commit message format and
provide helpful error messages for common issues.

- Validates header length and format
- Checks body line length
- Provides suggestions for commit types
```

## Validation

The commit message script validates:
- Header length (max 50 chars)
- Commit type format
- Body line length (max 72 chars)
- Valid commit types

## Git Hooks

### Install Commit Message Hook

```bash
# Copy the hook script
cp scripts/commit-msg-hook.py .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

### Manual Validation

```bash
# Validate a commit message file
python scripts/commit-msg-hook.py commit_message.txt
```

## IDE Integration

### VS Code

Add to your VS Code settings:

```json
{
    "git.inputValidation": "always",
    "git.inputValidationLength": 50,
    "git.inputValidationSubjectLength": 50
}
```

### Pre-commit Hook

You can also use our commit message script in a pre-commit hook:

```bash
#!/bin/bash
# .git/hooks/prepare-commit-msg

# Generate commit message using template
python scripts/commit_message.py --template bugfix > $1
```

## Best Practices

1. **Use templates** for consistency
2. **Keep headers short** and descriptive
3. **Explain why** in the body, not just what
4. **Reference issues** with `#123`
5. **Use imperative mood** ("add" not "added")
6. **Test your message** with the validation script

## Troubleshooting

### Common Errors

- **"Header too long"** - Keep description under 50 chars
- **"Unknown commit type"** - Use one of the defined types
- **"Body line too long"** - Wrap long lines at 72 chars

### Getting Help

```bash
# List available commit types
python scripts/commit_message.py --list-types

# Show help
python scripts/commit_message.py --help
```

## Related Documentation

- [AGENTS.md](../AGENTS.md) - Agent development guidelines
- [Development Process](../development.md) - Overall development workflow
- [Sprint Process](../sprint_process.md) - Sprint and stand-up procedures 