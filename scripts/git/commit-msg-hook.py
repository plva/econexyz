#!/usr/bin/env python3
"""Git commit-msg hook to validate commit messages."""

from __future__ import annotations

import sys
from pathlib import Path

# Import from our commit_message.py script
sys.path.append(str(Path(__file__).resolve().parents[1]))
from scripts.commit_message import validate_commit_message, COMMIT_TYPES

def main() -> None:
    """Validate commit message from git hook."""
    if len(sys.argv) < 2:
        print("Error: No commit message file provided")
        sys.exit(1)
    
    commit_msg_file = Path(sys.argv[1])
    if not commit_msg_file.exists():
        print(f"Error: Commit message file not found: {commit_msg_file}")
        sys.exit(1)
    
    # Read commit message
    message = commit_msg_file.read_text()
    lines = message.splitlines()
    
    if not lines:
        print("Error: Empty commit message")
        sys.exit(1)
    
    header = lines[0]
    body = None
    if len(lines) > 2:  # Has body (blank line + content)
        body = "\n".join(lines[2:])
    
    # Validate message
    errors = validate_commit_message(header, body)
    
    if errors:
        print("Commit message validation failed:")
        for error in errors:
            print(f"  - {error}")
        print("\nCommit message:")
        print("-" * 50)
        print(message)
        print("-" * 50)
        print("\nPlease fix the issues above and try again.")
        print("\nFor help, run: python scripts/commit_message.py --list-types")
        sys.exit(1)
    
    print("✓ Commit message validation passed")

if __name__ == "__main__":
    main() 