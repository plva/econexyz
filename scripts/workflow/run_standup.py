#!/usr/bin/env python3
"""
Standup automation script for EcoNexyz.

This script helps automate the cycle standup process by:
1. Finding the last standup commit
2. Listing commits since then
3. Helping identify completed issues
4. Generating a standup commit message
5. Creating work delta summary
6. Checking documentation for new features
7. Reviewing blockers and dependencies
8. Performing health checks
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
import re


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


def create_work_delta_summary(commits, suggestions):
    """Create a summary of work completed since last standup."""
    summary = []
    
    # Group by category
    by_category = {}
    for suggestion in suggestions:
        category = suggestion['category']
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(suggestion['message'])
    
    summary.append("## Work Delta Summary")
    summary.append("")
    
    for category, messages in by_category.items():
        summary.append(f"### {category.title()} Changes")
        for msg in messages:
            # Clean up the message for summary
            clean_msg = msg.split('] ', 1)[-1] if '] ' in msg else msg
            summary.append(f"- {clean_msg}")
        summary.append("")
    
    # Add metrics
    summary.append("### Metrics")
    summary.append(f"- Total commits: {len(commits)}")
    summary.append(f"- Likely completions: {len(suggestions)}")
    
    return '\n'.join(summary)


def check_documentation_for_new_features(commits):
    """Check if new features have proper documentation."""
    issues = []
    
    # Look for new scripts
    for commit in commits:
        if any(keyword in commit.lower() for keyword in ['script', 'tool', 'utility']):
            # Check if there's documentation
            if '[workflow]' in commit or '[feature]' in commit:
                issues.append(f"New feature detected: {commit} - check for documentation")
    
    # Check for new workflows
    for commit in commits:
        if 'workflow' in commit.lower():
            issues.append(f"New workflow detected: {commit} - check docs/workflows/")
    
    return issues


def review_blockers_and_dependencies():
    """Review blockers and dependencies in the repository."""
    issues = []
    
    # Check for issues marked as blocked
    result = run_command("grep -r 'blocked' issues/open/ || true")
    if result and result.stdout.strip():
        issues.append("Found issues marked as blocked:")
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                issues.append(f"  - {line.strip()}")
    
    # Check for unassigned issues
    result = run_command("grep -r 'assigned: unassigned' issues/open/ || true")
    if result and result.stdout.strip():
        unassigned_count = len(result.stdout.strip().split('\n'))
        if unassigned_count > 0:
            issues.append(f"Found {unassigned_count} unassigned issues")
    
    # Check for aging issues (older than 7 days)
    # This would require more complex date parsing, simplified for now
    issues.append("Review aging issues manually (older than 7 days)")
    
    return issues


def perform_health_checks():
    """Perform comprehensive health checks on the repository."""
    results = []
    
    # Run tests
    print("🔍 Running health checks...")
    
    # Test 1: Run all tests
    test_result = run_command("./scripts/testing/run_all_tests.sh")
    if test_result and test_result.returncode == 0:
        results.append("✅ All tests passing")
    else:
        results.append("❌ Tests failing")
    
    # Test 2: Check git hooks
    hook_result = run_command("python scripts/testing/test_commit_hook.py")
    if hook_result and hook_result.returncode == 0:
        results.append("✅ Git hooks working correctly")
    else:
        results.append("❌ Git hook issues detected")
    
    # Test 3: Check script permissions
    script_result = run_command("find scripts/ -name '*.sh' -exec test -x {} \\; -print")
    if script_result and script_result.returncode == 0:
        results.append("✅ All shell scripts are executable")
    else:
        results.append("❌ Some shell scripts may not be executable")
    
    # Test 4: Check for obvious issues
    todo_result = run_command("test -f TODO.md && echo 'exists'")
    if todo_result and todo_result.stdout.strip():
        results.append("✅ TODO.md exists")
    else:
        results.append("❌ TODO.md missing")
    
    return results


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
    summary.append("  - Run tests with ./scripts/testing/run_all_tests.sh")
    summary.append("  - Review documentation for new features")
    summary.append("  - Check for blockers and dependencies")
    summary.append("  - Perform health checks")
    
    return '\n'.join(summary)


def main():
    parser = argparse.ArgumentParser(description="Run a cycle standup")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--generate-commit", action="store_true", help="Generate standup commit message")
    parser.add_argument("--work-delta", action="store_true", help="Create work delta summary")
    parser.add_argument("--check-docs", action="store_true", help="Check documentation for new features")
    parser.add_argument("--review-blockers", action="store_true", help="Review blockers and dependencies")
    parser.add_argument("--health-check", action="store_true", help="Perform health checks")
    parser.add_argument("--all", action="store_true", help="Run all standup steps")
    
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
    
    # Work Delta Summary
    if args.work_delta or args.all:
        print("📈 Creating work delta summary...")
        work_summary = create_work_delta_summary(commits, suggestions)
        print(work_summary)
        print()
    
    # Documentation Check
    if args.check_docs or args.all:
        print("📚 Checking documentation for new features...")
        doc_issues = check_documentation_for_new_features(commits)
        if doc_issues:
            print("⚠️  Documentation issues found:")
            for issue in doc_issues:
                print(f"  - {issue}")
        else:
            print("✅ No obvious documentation issues")
        print()
    
    # Blocker Review
    if args.review_blockers or args.all:
        print("🚧 Reviewing blockers and dependencies...")
        blocker_issues = review_blockers_and_dependencies()
        if blocker_issues:
            print("⚠️  Blocker issues found:")
            for issue in blocker_issues:
                print(f"  - {issue}")
        else:
            print("✅ No obvious blocker issues")
        print()
    
    # Health Checks
    if args.health_check or args.all:
        health_results = perform_health_checks()
        print("🏥 Health check results:")
        for result in health_results:
            print(f"  {result}")
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
# - Work delta summary:
# - Documentation updates needed:
# - Blocker review findings:
# - Health check results:
# - TODO.md updates needed:
# - Sprint meta updates needed:
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
        print("5. Run tests with ./scripts/testing/run_all_tests.sh")
        print("6. Review documentation for new features")
        print("7. Check for blockers and dependencies")
        print("8. Perform health checks")
        print("9. Create standup commit")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 