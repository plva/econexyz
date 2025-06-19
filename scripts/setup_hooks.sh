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

echo "✅ Git hooks installed successfully!"
echo ""
echo "The commit-msg hook will now validate your commit messages."
echo "It checks:"
echo "  - Header length (max 50 chars)"
echo "  - Valid commit types"
echo "  - Body line length (max 72 chars)"
echo ""
echo "To test, try making a commit with an invalid message." 