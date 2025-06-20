#!/bin/bash
# Pre-commit hook to update issue metadata and warn on locked files
set -e
REPO_ROOT="$(git rev-parse --show-toplevel)"
python "$REPO_ROOT/scripts/update_issue_dates.py"
python "$REPO_ROOT/scripts/pre_commit_lock.py"
