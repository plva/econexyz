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

- `[fix]` - Fixes a bug
- `[feature]` - Adds a new feature  
- `[workflow]` - Changes to AI-agent workflows, agent instructions, or documentation that directly affect agent behaviors.
- `[issue]` - Adds a new issue file to the repo
- `[refactor]` - Pure code cleanup without behavior change
- `[perf]` - Performance enhancements
- `[deps]` - Dependency updates
- `[agents]` - Changes to agent system
- `[dashboard]` - Changes to dashboard or UI
- `[bus]` - Changes to message bus system
- `[cross]` - Cross-cutting changes (tests, CI, etc.)
- `[standup]` - Cycle stand-up updates (TODO.md, sprint meta)
- `[sprint]` - Sprint planning activities
- `[temp]` - Temporary commits for testing

## Bugfix Decision Flow

When encountering a bug, follow this decision tree:

### 1. Is there already an open issue for this bug?
- **Yes** → Fix directly and reference the issue in commit message
- **No** → Continue to step 2

### 2. Is there a closed issue for this bug?
- **Yes** → Reopen the issue, then fix and reference it
- **No** → Continue to step 3

### 3. Should this bug be tracked with an issue?
- **Yes** (complex bug, affects users, needs discussion) → Create new issue first, then fix
- **No** (trivial fix, internal cleanup, obvious error) → Fix directly with `[fix]` commit

### Examples:

**Fix directly (no issue needed):**
- Typo in comment or documentation
- Missing cleanup step in script
- Linter warning fix
- Obvious syntax error

**Create issue first:**
- Bug that affects functionality
- Security vulnerability
- Performance issue
- User-reported problem
- Complex bug requiring discussion

**Reference existing issue:**
```bash
[fix] fix issue path resolution in create_issue.py

Fixed bug where issue paths were being created as relative instead
of absolute paths. This caused issues when creating issues from
different directories.

Closes #45
```

## Template System

### Available Templates

We provide actual commit message templates in `docs/templates/commit_messages/`:

- `fix.md` - For bug fixes
- `feature.md` - For new features
- `workflow.md` - For workflow changes
- `standup.md` - For stand-up updates
- `issue.md` - For adding new issues
- `refactor.md` - For code refactoring
- `perf.md` - For performance improvements
- `deps.md` - For dependency updates

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
[fix] 



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
[fix] fix issue path resolution in create_issue.py

Fixed bug where issue paths were being created as relative instead
of absolute paths. This caused issues when creating issues from
different directories.

Closes #45
```

```