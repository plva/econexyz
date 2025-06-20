#!/usr/bin/env python3
"""Get-issue workflow script to provide task descriptions based on issue numbers."""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Get-issue workflow script")
    parser.add_argument("issue_number", help="Issue number (e.g., 12341, 21421)")
    
    args = parser.parse_args()
    
    issue_num = args.issue_number
    
    print(f"Issue #{issue_num}")
    print("=" * 50)
    
    # Provide task description based on issue number
    if issue_num == "12341":
        print("TASK: Implement a script that lists every markdown file in the repository.")
        print()
        print("Requirements:")
        print("- Create a script that recursively searches the entire repository")
        print("- Find all files with .md extension")
        print("- Output the list of markdown files to the command line")
        print("- Skip files in .git directory")
        print("- Sort the output alphabetically")
        print()
        print("Example output format:")
        print("  docs/guides/development.md")
        print("  docs/templates/commit_messages/fix.md")
        print("  README.md")
        print("  ...")
        
    elif issue_num == "21421":
        print("TASK: Implement a script that returns the first 3 lines of every markdown file in the docs directory.")
        print()
        print("Requirements:")
        print("- Create a script that searches the docs/ directory of the repository")
        print("- Find all files with .md extension in docs/ and subdirectories")
        print("- Read the first 3 lines of each markdown file")
        print("- Output should show the file path followed by its first 3 lines")
        print("- Handle files that might have fewer than 3 lines")
        print()
        print("Example output format:")
        print("  docs/guides/development.md:")
        print("  # Development Guide")
        print("  This guide covers...")
        print("  ...")
        print()
        print("  docs/templates/commit_messages/fix.md:")
        print("  [fix]")
        print("  ")
        print("  # Brief description...")
        
    else:
        print(f"No specific task description for issue #{issue_num}")
        print("This script provides task descriptions for specific issue numbers.")
        print("Available issue numbers: 12341, 21421")


if __name__ == "__main__":
    main() 