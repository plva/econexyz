#!/usr/bin/env python3
"""Git commit-msg hook to validate commit messages."""

from __future__ import annotations

import sys
from pathlib import Path

# Import from our commit_message.py script
sys.path.append(str(Path(__file__).resolve().parents[1]))
from scripts.git.commit_message import validate_commit_message, COMMIT_TYPES, get_commit_type_suggestions

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
    
    # Find the separator line and ignore everything below it
    separator_index = None
    for i, line in enumerate(lines):
        if line.startswith("# ------------------------ >8 ------------------------"):
            separator_index = i
            break
    
    # Only process lines up to the separator
    if separator_index is not None:
        lines = lines[:separator_index]
    
    # Find the first non-empty, non-comment line as the header
    header = None
    for line in lines:
        if line.strip() and not line.strip().startswith("#"):
            header = line.strip()
            break
    
    if not header:
        print("Error: No commit message found (first line is empty or commented)")
        print("Please add a commit message in the format: [type] description")
        sys.exit(1)
    
    # Find body lines (non-commented lines after the header)
    body_lines = []
    header_found = False
    for line in lines:
        if line.strip() == header:
            header_found = True
            continue
        if header_found and line.strip() and not line.strip().startswith("#"):
            body_lines.append(line.strip())
    
    body = None
    if body_lines:
        body = "\n".join(body_lines)
    
    # Validate message
    errors = validate_commit_message(header, body)
    
    if errors:
        print("Commit message validation failed:")
        for error in errors:
            print(f"  - {error}")
        
        # Show only the relevant parts of the commit message
        print("\nCommit message:")
        print("-" * 50)
        if header:
            print(header)
        if body:
            print()
            print(body)
        print("-" * 50)
        
        # Provide helpful guidance
        print("\nAvailable commit types:")
        print(get_commit_type_suggestions())
        print("\nExample: [workflow] improve commit message validation")
        print("\nPlease fix the issues above and try again.")
        print("\nFor help, run: python scripts/git/commit_message.py --list-types")
        sys.exit(1)
    
    print("✓ Commit message validation passed")

if __name__ == "__main__":
    main() 