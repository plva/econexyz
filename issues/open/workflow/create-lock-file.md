------------------------
status: open
category: workflow
tags:
- workflow
- meta
- devops
created: 2025-06-19
last-updated: 2025-06-19
priority: medium
assigned: plva + codex 
------------------------

# workflow/create-lock-file

# Issue: Implement Soft File-Locking Workflow

## Overview

We want to reduce merge conflicts by implementing a lightweight **soft-locking mechanism**. This mechanism will clearly communicate intent for editing critical files, helping both human and AI agents avoid concurrent edits.

Locks are informational, not strictly enforced, to ensure collaboration remains flexible.

## Lock File Structure

Locks are stored in the `locks/` directory, each lock named by the resource or conceptual area it's protecting (not strictly file paths).

Example lock file (`locks/config_parameters.lock`):

```yaml
user: "plva"
timestamp: "2025-06-20T14:30:00Z"
reason: "Updating critical parameters"
file: "configs/production.yaml"
```

## Workflow

- Locks are stable, changing infrequently.
- Developers can check lock status before editing critical files but normally would see a warning when committing due to commit hooks.
  - normally they would know which files are locked
- AI agents attempt to respect existing locks or explicitly note conflicts.

### Directory Structure Example

```
locks/
├── config_parameters.lock
├── database_schema.lock
└── core_agent_definitions.lock
```

## Git Hook for Lock Awareness

Implement a pre-commit git hook to warn developers if they're editing locked files without holding the lock themselves.

### Hook Functionality:

- Checks staged files against lock files.
- Warns if a file is locked by another user.

Example warning:

```
⚠️ Warning: You're modifying 'configs/production.yaml', currently locked by user 'plva' since '2025-06-20T14:30:00Z'.
Reason: Updating critical parameters.
```

## Implementation Steps (Pull Request Breakdown)

**PR #1: Add Lock Directory, Initial Lock Files, and Lock management script**
- Create `locks/` directory.
- Add initial lock files with YAML metadata.
- Add helper script:
  - `scripts/create_lock.sh <lock-name> <file-path> "<reason>"`
- Add documentation
- Update `AGENTS.md` and/or `CONTRIBUTING.md` with clear instructions on lock workflow.

**PR #3: Git Pre-commit Hook**
- Script to check staged files against active locks.
- Warn clearly when violations occur.
- Install hook in `.git/hooks/pre-commit`.


## AI Agent Instructions

AI agents should:
- Check `locks/` before making edits.
- Avoid locked files if possible.
- If unavoidable, document the lock conflict clearly in their agent log, e.g.:

```yaml
requested_lock: "config_parameters.lock"
agent: "Codex"
timestamp: "2025-06-20T15:00:00Z"
reason: "Automated parameter update"
action_taken: "Paused operation, awaiting lock release"
```

## Best Practices
- Clearly document locking workflow and expectations.
- Use automation (git hooks, helper scripts) to reinforce lock awareness.
- Regularly review and maintain lock files to ensure they reflect current needs accurately.

This soft-locking mechanism strikes a practical balance between flexibility, conflict prevention, and clear communication, suitable for collaborative environments involving both humans and automated agents.