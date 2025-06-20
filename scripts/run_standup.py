#!/usr/bin/env python3
"""
Standup automation script for EcoNexyz.

This script helps automate the cycle standup process by:
1. Finding the last standup commit
2. Listing commits since then
3. Helping identify completed issues
4. Generating a standup commit message
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, capture_output=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        return result
    except Exception as e:
        print(f"Error running command '{cmd}': {e}")
        return None


def find_last_standup_commit():
    """Find the last commit with [standup] prefix."""
    result = run_command("git log --oneline --grep='^\\[standup\\]' -1")
    if not result or result.returncode != 0:
        print("Error: Could not find last standup commit")
        return None
    
    if not result.stdout.strip():
        print("No previous standup commits found")
        return None
    
    # Extract hash from output like "abc1234 [standup] message"
    hash_part = result.stdout.strip().split()[0]
    return hash_part


def get_commits_since(hash):
    """Get all commits since the given hash."""
    result = run_command(f"git --no-pager log --oneline {hash}..HEAD")
    if not result or result.returncode != 0:
        print(f"Error: Could not get commits since {hash}")
        return []
    
    return [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]


def analyze_commit(commit_line):
    """Analyze a commit line to determine what it might have completed."""
    parts = commit_line.split(' ', 1)
    if len(parts) < 2:
        return None
    
    hash_part, message = parts
    
    # Look for commit types that might indicate issue completion
    completion_indicators = {
        '[fix]': 'bug',
        '[workflow]': 'workflow',
        '[agents]': 'agents',
        '[feature]': 'feature',
        '[refactor]': 'refactor'
    }
    
    for indicator, category in completion_indicators.items():
        if indicator in message:
            return {
                'hash': hash_part,
                'message': message,
                'type': indicator,
                'category': category,
                'likely_completion': True
            }
    
    return {
        'hash': hash_part,
        'message': message,
        'type': 'other',
        'category': 'other',
        'likely_completion': False
    }


def suggest_completed_issues(commits):
    """Suggest which issues might be completed based on commits."""
    suggestions = []
    
    for commit in commits:
        analysis = analyze_commit(commit)
        if analysis and analysis['likely_completion']:
            suggestions.append(analysis)
    
    return suggestions


def generate_standup_summary(commits, suggestions):
    """Generate a summary for the standup commit."""
    summary = []
    
    # Count by type
    type_counts = {}
    for commit in commits:
        analysis = analyze_commit(commit)
        if analysis:
            commit_type = analysis['type']
            type_counts[commit_type] = type_counts.get(commit_type, 0) + 1
    
    summary.append(f"Total commits since last standup: {len(commits)}")
    summary.append("")
    
    if type_counts:
        summary.append("Commit breakdown:")
        for commit_type, count in type_counts.items():
            summary.append(f"  - {commit_type}: {count}")
        summary.append("")
    
    if suggestions:
        summary.append("Potential issue completions:")
        for suggestion in suggestions:
            summary.append(f"  - {suggestion['message']}")
        summary.append("")
    
    summary.append("Manual review needed:")
    summary.append("  - Check TODO.md for completed issues")
    summary.append("  - Update sprint metadata")
    summary.append("  - Close completed issues with ./scripts/close_issue.sh")
    summary.append("  - Run tests with ./scripts/run_all_tests.sh")
    
    return '\n'.join(summary)


def main():
    parser = argparse.ArgumentParser(description="Run a cycle standup")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--generate-commit", action="store_true", help="Generate standup commit message")
    
    args = parser.parse_args()
    
    print("🔍 Finding last standup commit...")
    last_standup = find_last_standup_commit()
    
    if not last_standup:
        print("❌ No previous standup found. This might be the first standup.")
        return 1
    
    print(f"✅ Last standup: {last_standup}")
    print()
    
    print("📋 Getting commits since last standup...")
    commits = get_commits_since(last_standup)
    
    if not commits:
        print("✅ No commits since last standup")
        return 0
    
    print(f"✅ Found {len(commits)} commits")
    print()
    
    print("🔍 Analyzing commits for potential issue completions...")
    suggestions = suggest_completed_issues(commits)
    
    print("📊 Commit Summary:")
    for commit in commits:
        analysis = analyze_commit(commit)
        if analysis and analysis['likely_completion']:
            print(f"  🎯 {commit}")
        else:
            print(f"  📝 {commit}")
    print()
    
    if suggestions:
        print("💡 Potential issue completions:")
        for suggestion in suggestions:
            print(f"  - {suggestion['message']}")
        print()
    
    summary = generate_standup_summary(commits, suggestions)
    
    if args.generate_commit:
        print("📝 Generating standup commit message...")
        commit_msg = f"""[standup] Cycle standup summary

# Summary of stand-up activities
# 
# - Commits reviewed: {len(commits)}
# - Potential completions: {len(suggestions)}
# 
# - Issues to check:
"""
        
        for suggestion in suggestions:
            commit_msg += f"#   - {suggestion['category']} (from {suggestion['message']})\n"
        
        commit_msg += """# 
# - TODO.md updates needed:
# - Sprint meta updates needed:
# - Other planning changes:
# 
# Lines starting with # will be removed from the final commit message.
"""
        
        # Write to temporary file
        with open('/tmp/standup_commit.txt', 'w') as f:
            f.write(commit_msg)
        
        print("✅ Commit message written to /tmp/standup_commit.txt")
        print("📝 Review and edit the message, then run:")
        print("   git add .")
        print("   git commit -F /tmp/standup_commit.txt")
    
    if not args.dry_run:
        print("🚀 Next steps:")
        print("1. Review the commits above")
        print("2. Close completed issues: ./scripts/close_issue.sh <category> <issue>")
        print("3. Update TODO.md")
        print("4. Update sprint metadata")
        print("5. Run tests: ./scripts/run_all_tests.sh")
        print("6. Create standup commit")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 