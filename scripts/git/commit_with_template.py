#!/usr/bin/env python3
"""Wrapper script to create template, modify it, commit, and cleanup."""

import argparse
import subprocess
import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.git.commit_message import create_template_file, cleanup_template_file

def modify_template_file(template_file: str, header: str, body: str | None = None) -> None:
    """Modify the template file with the provided header and body."""
    content = Path(template_file).read_text()
    lines = content.splitlines()
    
    # Replace the first line with the header
    if lines:
        lines[0] = header
    
    # Add body after the header if provided
    if body:
        # Find the first empty line after the header
        body_start = 1
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "":
                body_start = i
                break
        
        # Insert body after the empty line
        body_lines = body.splitlines()
        lines = lines[:body_start] + body_lines + lines[body_start:]
    
    # Write back the modified content
    Path(template_file).write_text("\n".join(lines))

def main():
    parser = argparse.ArgumentParser(description="Create template, modify, commit, and cleanup")
    parser.add_argument("commit_type", help="commit type")
    parser.add_argument("--header", help="commit header (will be prefixed with [type])")
    parser.add_argument("--body", help="commit body")
    parser.add_argument("--dry-run", action="store_true", help="show what would be committed without doing it")
    
    args = parser.parse_args()
    
    try:
        # Create template file
        template_file = create_template_file(args.commit_type)
        print(f"Template file created: {template_file}")
        
        # Modify template with provided content
        if args.header:
            header = f"[{args.commit_type}] {args.header}"
            modify_template_file(template_file, header, args.body)
            print(f"Template modified with header: {header}")
            if args.body:
                print(f"Body: {args.body}")
        
        # Show what will be committed
        print("\nCommit message:")
        print("-" * 50)
        print(Path(template_file).read_text())
        print("-" * 50)
        
        if args.dry_run:
            print("\nDry run - would commit with the above message")
            return
        
        # Commit using the template
        print("\nCommitting with template...")
        
        # Stage all changes first
        subprocess.run(["git", "add", "."], cwd=ROOT, check=True)
        
        subprocess.run(["git", "commit", "-F", template_file], cwd=ROOT, check=True)
        
        print("✅ Commit successful!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Commit cancelled")
    finally:
        # Clean up template file
        cleanup_template_file(args.commit_type)

if __name__ == "__main__":
    main() 