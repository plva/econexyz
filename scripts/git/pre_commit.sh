#!/bin/bash
# Pre-commit hook to update issue metadata and warn on locked files
set -e
REPO_ROOT="$(git rev-parse --show-toplevel)"
python3 "$REPO_ROOT/scripts/workflow/update_issue_dates.py"
python3 "$REPO_ROOT/scripts/git/pre_commit_lock.py"
