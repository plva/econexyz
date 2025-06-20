#!/usr/bin/env python3
"""
Pull-Issue Workflow - Main orchestrator for pulling and completing sprint issues.

This script provides a comprehensive workflow for:
1. Selecting issues from the current sprint
2. Setting up the development environment
3. Tracking work sessions
4. Running quality checks
5. Completing issues with proper documentation and commits
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add project root to path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.workflow.issue_selector import IssueSelector
from scripts.workflow.work_session import WorkSession
from scripts.workflow.issue_completer import IssueCompleter


class PullIssueWorkflow:
    """Main orchestrator for the pull-issue workflow."""
    
    def __init__(self):
        self.root = ROOT
        self.state_file = self.root / "state" / "sprint.json"
        self.sprints_dir = self.root / "sprints" / "open"
        self.issues_dir = self.root / "issues" / "open"
        self.selector = IssueSelector(self.root)
        self.session = WorkSession(self.root)
        self.completer = IssueCompleter(self.root)
        
    def get_current_sprint(self) -> Optional[str]:
        """Get the current sprint number from state."""
        if not self.state_file.exists():
            print("❌ No sprint state found. Please set up sprint state first.")
            return None
            
        try:
            with open(self.state_file) as f:
                state = json.load(f)
                return f"sprint-{state.get('current', 1)}"
        except (json.JSONDecodeError, KeyError) as e:
            print(f"❌ Error reading sprint state: {e}")
            return None
    
    def validate_environment(self) -> bool:
        """Validate the development environment before starting work."""
        print("🔍 Validating environment...")
        
        # Check git status
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"], 
                capture_output=True, 
                text=True, 
                cwd=self.root
            )
            if result.stdout.strip():
                print("⚠️  Warning: You have uncommitted changes.")
                response = input("Continue anyway? (y/N): ")
                if response.lower() != 'y':
                    return False
        except subprocess.CalledProcessError:
            print("❌ Error checking git status")
            return False
        
        # Check if tests are passing
        try:
            result = subprocess.run(
                ["./scripts/testing/run_all_tests.sh"],
                capture_output=True,
                text=True,
                cwd=self.root
            )
            if result.returncode != 0:
                print("❌ Tests are failing. Please fix them before starting work.")
                return False
            print("✅ Tests are passing")
        except subprocess.CalledProcessError:
            print("❌ Error running tests")
            return False
        
        return True
    
    def pull_issue(self, issue_spec: Optional[str] = None, random: bool = False, 
                   priority: Optional[str] = None, issue_type: Optional[str] = None) -> bool:
        """Pull an issue to work on."""
        print("🚀 Starting pull-issue workflow...")
        
        # Validate environment
        if not self.validate_environment():
            return False
        
        # Get current sprint
        sprint_name = self.get_current_sprint()
        if not sprint_name:
            return False
        
        # Select issue
        selected_issue = self.selector.select_issue(
            sprint_name, issue_spec, random, priority, issue_type
        )
        if not selected_issue:
            print("❌ No issue selected")
            return False
        
        # Start work session
        if not self.session.start_session(selected_issue):
            print("❌ Failed to start work session")
            return False
        
        print(f"✅ Started working on: {selected_issue['category']}/{selected_issue['name']}")
        print(f"📝 Work session log: {self.session.get_session_log_path()}")
        print("\nNext steps:")
        print("1. Work on the issue")
        print("2. Run tests: ./scripts/testing/run_all_tests.sh")
        print("3. Complete the issue: python scripts/workflow/pull_issue.py --complete")
        
        return True
    
    def complete_issue(self, quick: bool = False) -> bool:
        """Complete the current issue."""
        print("🏁 Completing current issue...")
        
        # Get current session
        current_session = self.session.get_current_session()
        if not current_session:
            print("❌ No active work session found")
            return False
        
        # Run quality checks
        if not quick:
            if not self.completer.run_quality_checks():
                print("❌ Quality checks failed")
                return False
        
        # Complete the issue
        if not self.completer.complete_issue(current_session):
            print("❌ Failed to complete issue")
            return False
        
        # End work session
        self.session.end_session()
        
        print("✅ Issue completed successfully!")
        return True
    
    def show_status(self):
        """Show current work session status."""
        current_session = self.session.get_current_session()
        if current_session:
            print(f"📋 Current issue: {current_session['category']}/{current_session['name']}")
            print(f"⏱️  Started: {current_session['start_time']}")
            print(f"📝 Log: {self.session.get_session_log_path()}")
        else:
            print("📋 No active work session")
    
    def log_progress(self, message: str):
        """Log progress to the current work session."""
        if not self.session.log_progress(message):
            print("❌ No active work session to log to")
        else:
            print(f"📝 Logged: {message}")


def main():
    parser = argparse.ArgumentParser(description="Pull-Issue Workflow")
    parser.add_argument("--issue", help="Specific issue to pull (category/name)")
    parser.add_argument("--random", action="store_true", help="Pull a random issue")
    parser.add_argument("--priority", choices=["high", "medium", "low"], help="Filter by priority")
    parser.add_argument("--type", choices=["bug", "feature", "workflow"], help="Filter by issue type")
    parser.add_argument("--complete", action="store_true", help="Complete current issue")
    parser.add_argument("--quick-complete", action="store_true", help="Quick complete (skip quality checks)")
    parser.add_argument("--status", action="store_true", help="Show current work session status")
    parser.add_argument("--log", help="Log progress message")
    
    args = parser.parse_args()
    
    workflow = PullIssueWorkflow()
    
    if args.status:
        workflow.show_status()
    elif args.log:
        workflow.log_progress(args.log)
    elif args.complete or args.quick_complete:
        workflow.complete_issue(quick=args.quick_complete)
    else:
        workflow.pull_issue(
            issue_spec=args.issue,
            random=args.random,
            priority=args.priority,
            issue_type=args.type
        )


if __name__ == "__main__":
    main() 