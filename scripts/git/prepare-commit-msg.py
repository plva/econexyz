#!/usr/bin/env python3
"""Git prepare-commit-msg hook to add diff stats instead of full diff."""

import subprocess
import sys
from pathlib import Path

def get_diff_stats():
    """Get git diff stats for staged changes."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--stat"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""

def main():
    """Prepare commit message by replacing full diff with stats."""
    if len(sys.argv) < 2:
        return
    
    commit_msg_file = Path(sys.argv[1])
    if not commit_msg_file.exists():
        return
    
    # Read the current commit message
    content = commit_msg_file.read_text()
    lines = content.splitlines()
    
    # Find where the diff starts (after the separator line)
    diff_start = None
    for i, line in enumerate(lines):
        if line.startswith("diff --git"):
            diff_start = i
            break
    
    if diff_start is not None:
        # Keep everything up to the separator line
        separator_line = None
        for i, line in enumerate(lines):
            if line.startswith("# ------------------------ >8 ------------------------"):
                separator_line = i
                break
        
        if separator_line is not None:
            # Keep the header and add diff stats
            header_lines = lines[:separator_line]
            
            # Get diff stats
            diff_stats = get_diff_stats()
            
            # Write back the content with stats instead of full diff
            new_content = "\n".join(header_lines)
            if diff_stats:
                new_content += f"\n\n# Diff stats:\n# {diff_stats.replace(chr(10), chr(10) + '# ')}"
            
            commit_msg_file.write_text(new_content)

if __name__ == "__main__":
    main() 