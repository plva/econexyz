#!/bin/bash
# Setup script for EcoNexyz git hooks

set -e

echo "Setting up EcoNexyz git hooks..."

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Create hooks directory if it doesn't exist
HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
mkdir -p "$HOOKS_DIR"

# Install commit-msg hook
echo "Installing commit-msg hook..."
cp "$SCRIPT_DIR/commit-msg-hook.py" "$HOOKS_DIR/commit-msg"
chmod +x "$HOOKS_DIR/commit-msg"

# Install pre-commit hook for lock checking
echo "Installing pre-commit hook..."
cp "$SCRIPT_DIR/pre_commit_lock.py" "$HOOKS_DIR/pre-commit"
chmod +x "$HOOKS_DIR/pre-commit"

echo "✅ Git hooks installed successfully!"

echo "The commit-msg hook will now validate your commit messages."
echo "The pre-commit hook will warn if you modify locked files."
echo "To test, try making a commit with an invalid message or editing a locked file."
