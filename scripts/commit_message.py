#!/usr/bin/env python3
"""Generate commit messages using the commit template."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "docs" / "templates" / "commit_messages"

COMMIT_TYPES = {
    "bugfix": "Fixes a bug",
    "feature": "Adds a new feature", 
    "workflow": "Changes to workflow, scripts, or documentation",
    "agents": "Changes to agent system",
    "dashboard": "Changes to dashboard or UI",
    "bus": "Changes to message bus system",
    "cross": "Cross-cutting changes (tests, CI, etc.)",
    "standup": "Cycle stand-up updates (TODO.md, sprint meta)",
    "sprint-planning": "Sprint planning activities",
    "temp": "Temporary commits for testing"
}

def get_commit_type_suggestions() -> str:
    """Return formatted commit type suggestions."""
    suggestions = []
    for commit_type, description in COMMIT_TYPES.items():
        suggestions.append(f"  [{commit_type}] - {description}")
    return "\n".join(suggestions)

def get_template_content(commit_type: str) -> Optional[str]:
    """Get template content for a commit type."""
    template_file = TEMPLATES_DIR / f"{commit_type}.md"
    if template_file.exists():
        return template_file.read_text()
    return None

def clean_template_content(content: str) -> str:
    """Remove comment lines (starting with #) from template content."""
    lines = []
    for line in content.splitlines():
        if not line.strip().startswith("#"):
            lines.append(line)
    return "\n".join(lines)

def validate_commit_message(header: str, body: Optional[str] = None) -> list[str]:
    """Validate commit message and return list of errors."""
    errors = []
    
    # Check header length
    if len(header) > 50:
        errors.append(f"Header too long ({len(header)} chars, max 50)")
    
    # Check header format
    if not header.startswith("["):
        errors.append("Header must start with commit type in brackets")
    elif not "]" in header:
        errors.append("Header must have closing bracket")
    else:
        # Extract type
        end_bracket = header.find("]")
        commit_type = header[1:end_bracket]
        if commit_type not in COMMIT_TYPES:
            errors.append(f"Unknown commit type: [{commit_type}]")
    
    # Check body line length
    if body:
        for i, line in enumerate(body.splitlines(), 1):
            if len(line) > 72:
                errors.append(f"Body line {i} too long ({len(line)} chars, max 72)")
    
    return errors

def generate_commit_message(commit_type: str, description: str, body: Optional[str] = None) -> str:
    """Generate a formatted commit message."""
    header = f"[{commit_type}] {description}"
    
    if body:
        return f"{header}\n\n{body}"
    else:
        return header

def interactive_commit_message() -> str:
    """Interactive commit message generation."""
    print("Commit Message Generator")
    print("=" * 50)
    print("\nAvailable commit types:")
    print(get_commit_type_suggestions())
    
    # Get commit type
    while True:
        commit_type = input("\nEnter commit type: ").strip()
        if commit_type in COMMIT_TYPES:
            break
        print(f"Unknown commit type: {commit_type}")
    
    # Get description
    description = input("Enter description: ").strip()
    if not description:
        print("Description is required")
        sys.exit(1)
    
    # Get optional body
    print("\nEnter commit body (optional, press Enter twice to finish):")
    body_lines = []
    while True:
        line = input()
        if line == "" and (not body_lines or body_lines[-1] == ""):
            break
        body_lines.append(line)
    
    body = None
    if body_lines and body_lines[-1] == "":
        body_lines.pop()  # Remove trailing empty line
    if body_lines:
        body = "\n".join(body_lines)
    
    # Generate message
    message = generate_commit_message(commit_type, description, body)
    
    # Validate
    errors = validate_commit_message(f"[{commit_type}] {description}", body)
    if errors:
        print("\nValidation errors:")
        for error in errors:
            print(f"  - {error}")
        print("\nMessage generated but has issues:")
    
    print(f"\nGenerated commit message:\n")
    print("-" * 50)
    print(message)
    print("-" * 50)
    
    return message

def create_template_file(commit_type: str) -> str:
    """Create a template file for the given commit type and return its path."""
    template_content = get_template_content(commit_type)
    if not template_content:
        print(f"No template found for commit type: {commit_type}")
        sys.exit(1)
    
    # Create temporary file with template content
    temp_file = Path(f"/tmp/commit_template_{commit_type}.md")
    temp_file.write_text(template_content)
    
    return str(temp_file)

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate commit messages")
    parser.add_argument("--type", help="commit type")
    parser.add_argument("--description", help="commit description")
    parser.add_argument("--body", help="commit body")
    parser.add_argument("--interactive", "-i", action="store_true", help="interactive mode")
    parser.add_argument("--output", "-o", help="output file (default: stdout)")
    parser.add_argument("--list-types", action="store_true", help="list available commit types")
    parser.add_argument("--template", "-t", help="create template file for commit type")
    parser.add_argument("--use-template", help="use template file for commit type")
    
    args = parser.parse_args()
    
    if args.list_types:
        print("Available commit types:")
        print(get_commit_type_suggestions())
        return
    
    if args.template:
        template_file = create_template_file(args.template)
        print(f"Template file created: {template_file}")
        print(f"Use: git commit -F {template_file}")
        return
    
    if args.use_template:
        template_file = create_template_file(args.use_template)
        print(f"Template file ready: {template_file}")
        print(f"Run: git commit -F {template_file}")
        return
    
    if args.interactive:
        message = interactive_commit_message()
    elif args.type and args.description:
        message = generate_commit_message(args.type, args.description, args.body)
    else:
        parser.print_help()
        return
    
    # Output message
    if args.output:
        Path(args.output).write_text(message + "\n")
        print(f"Commit message written to {args.output}")
    else:
        print(message)

if __name__ == "__main__":
    main() 