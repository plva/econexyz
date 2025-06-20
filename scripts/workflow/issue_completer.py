#!/usr/bin/env python3
"""
Issue Completer - Handles issue completion with quality checks and documentation updates.
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


class IssueCompleter:
    """Handles issue completion with quality checks and documentation updates."""
    
    def __init__(self, root: Path):
        self.root = root
        self.issues_dir = root / "issues" / "open"
        self.closed_dir = root / "issues" / "closed"
        self.todo_file = root / "TODO.md"
        
    def run_quality_checks(self) -> bool:
        """Run all quality checks before completing an issue."""
        print("🔍 Running quality checks...")
        
        checks = [
            ("Tests", self._run_tests),
            ("Linting", self._run_linting),
            ("Git hooks", self._check_git_hooks),
            ("Documentation", self._check_documentation),
        ]
        
        all_passed = True
        for check_name, check_func in checks:
            print(f"  {check_name}...", end=" ")
            if check_func():
                print("✅")
            else:
                print("❌")
                all_passed = False
        
        if not all_passed:
            print("\n❌ Quality checks failed. Please fix issues before completing.")
            return False
        
        print("✅ All quality checks passed!")
        return True
    
    def complete_issue(self, session_data: Dict) -> bool:
        """Complete an issue with proper documentation and cleanup."""
        issue = session_data['issue']
        print(f"🏁 Completing issue: {issue['category']}/{issue['name']}")
        
        # Generate commit message
        commit_message = self._generate_commit_message(session_data)
        
        # Commit current work
        if not self._commit_work(commit_message):
            print("❌ Failed to commit work")
            return False
        
        # Update documentation
        if not self._update_documentation(issue):
            print("❌ Failed to update documentation")
            return False
        
        # Close the issue
        if not self._close_issue(issue):
            print("❌ Failed to close issue")
            return False
        
        # Update TODO.md
        if not self._update_todo(issue):
            print("❌ Failed to update TODO.md")
            return False
        
        # Update sprint meta
        if not self._update_sprint_meta(issue):
            print("❌ Failed to update sprint meta")
            return False
        
        # Merge to main
        if not self._merge_to_main(session_data['branch_name']):
            print("❌ Failed to merge to main")
            return False
        
        print("✅ Issue completed successfully!")
        return True
    
    def _run_tests(self) -> bool:
        """Run the test suite."""
        try:
            result = subprocess.run(
                ["./scripts/testing/run_all_tests.sh"],
                capture_output=True,
                text=True,
                cwd=self.root
            )
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False
    
    def _run_linting(self) -> bool:
        """Run linting checks."""
        try:
            # Check for common Python issues
            result = subprocess.run(
                ["python", "-m", "py_compile", "scripts/workflow/pull_issue.py"],
                capture_output=True,
                text=True,
                cwd=self.root
            )
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False
    
    def _check_git_hooks(self) -> bool:
        """Check if git hooks are properly set up."""
        hooks_dir = self.root / ".git" / "hooks"
        required_hooks = ["pre-commit", "commit-msg"]
        
        for hook in required_hooks:
            hook_file = hooks_dir / hook
            if not hook_file.exists():
                print(f"❌ Git hook {hook} not found")
                return False
        
        return True
    
    def _check_documentation(self) -> bool:
        """Check documentation completeness."""
        # Check if README files exist and are not empty
        readme_files = [
            self.root / "README.md",
            # self.root / "docs" / "README.md"
        ]
        
        for readme in readme_files:
            if readme.exists() and readme.stat().st_size > 0:
                continue
            return False
        
        return True
    
    def _generate_commit_message(self, session_data: Dict) -> str:
        """Generate a commit message using the commit_message script."""
        issue = session_data['issue']
        start_time = datetime.fromisoformat(session_data['start_time'])
        duration = datetime.now() - start_time
        
        # Get work delta
        work_delta = self._get_work_delta()
        
        # Determine commit type based on issue category
        commit_type = "feature"
        if issue['category'] == 'bugs':
            commit_type = "fix"
        elif issue['category'] == 'workflow':
            commit_type = "workflow"
        
        # Generate description
        description = f"complete {issue['name']}"
        
        # Build body
        body_lines = [
            f"Closes: {issue['category']}/{issue['name']}",
            f"Duration: {duration}",
            f"Progress entries: {len(session_data['progress_log'])}",
            "",
            "Work completed:",
            work_delta
        ]
        body = "\n".join(body_lines)
        
        # Use the commit_message script
        try:
            result = subprocess.run(
                [
                    "python", "scripts/git/commit_message.py",
                    "--type", commit_type,
                    "--description", description,
                    "--body", body
                ],
                capture_output=True,
                text=True,
                cwd=self.root
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"Warning: Commit message script failed: {result.stderr}")
                # Fallback to manual generation
                return f"[{commit_type}] {description}\n\n{body}"
                
        except subprocess.CalledProcessError as e:
            print(f"Warning: Could not run commit message script: {e}")
            # Fallback to manual generation
            return f"[{commit_type}] {description}\n\n{body}"
    
    def _get_work_delta(self) -> str:
        """Get a summary of work done."""
        try:
            result = subprocess.run(
                ["git", "diff", "main..HEAD", "--stat"],
                capture_output=True,
                text=True,
                cwd=self.root
            )
            
            if result.stdout.strip():
                return result.stdout.strip()
            else:
                return "No changes detected"
                
        except subprocess.CalledProcessError:
            return "Could not determine work delta"
    
    def _commit_work(self, message: str) -> bool:
        """Commit current work."""
        try:
            # Check if there are changes
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.root
            )
            
            if not result.stdout.strip():
                print("ℹ️  No changes to commit")
                return True
            
            # Add all changes
            subprocess.run(["git", "add", "."], cwd=self.root, check=True)
            
            # Commit
            subprocess.run(["git", "commit", "-m", message], cwd=self.root, check=True)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to commit: {e}")
            return False
    
    def _update_documentation(self, issue: Dict) -> bool:
        """Update relevant documentation."""
        try:
            # Update development guide if needed
            dev_guide = self.root / "docs" / "guides" / "development.md"
            if dev_guide.exists():
                # Add usage example if this is a new workflow
                if issue['category'] == 'workflow':
                    self._add_workflow_example(dev_guide, issue)
            
            # Update scripts guide
            scripts_guide = self.root / "docs" / "guides" / "scripts.md"
            if scripts_guide.exists():
                self._add_script_example(scripts_guide, issue)
            
            return True
            
        except Exception as e:
            print(f"Warning: Could not update documentation: {e}")
            return True  # Don't fail completion for doc updates
    
    def _add_workflow_example(self, dev_guide: Path, issue: Dict):
        """Add workflow example to development guide."""
        # This would add usage examples for new workflows
        pass
    
    def _add_script_example(self, scripts_guide: Path, issue: Dict):
        """Add script example to scripts guide."""
        # This would add usage examples for new scripts
        pass
    
    def _close_issue(self, issue: Dict) -> bool:
        """Close the issue using the close_issue script."""
        try:
            category = issue['category']
            name = issue['name']
            print(f"DEBUG: Attempting to close issue with category: {category}, name: {name}")
            print(f"DEBUG: Running ./scripts/workflow/close_issue.sh {category} {name}")
            result = subprocess.run(
                ["./scripts/workflow/close_issue.sh", category, name],
                capture_output=True,
                text=True,
                cwd=self.root
            )
            print(f"DEBUG: close_issue.sh stdout: {result.stdout}")
            print(f"DEBUG: close_issue.sh stderr: {result.stderr}")
            print(f"DEBUG: close_issue.sh returncode: {result.returncode}")
            return result.returncode == 0
        
        except subprocess.CalledProcessError as e:
            print(f"DEBUG: Exception in _close_issue: {e}")
            return False
    
    def _update_todo(self, issue: Dict) -> bool:
        """Update TODO.md to mark issue as completed."""
        if not self.todo_file.exists():
            return True
        
        try:
            with open(self.todo_file, 'r') as f:
                content = f.read()
            
            # Find and mark the issue as completed
            issue_pattern = f"- [ ] {issue['category']}/{issue['name']}"
            replacement = f"- [x] {issue['category']}/{issue['name']}"
            
            if issue_pattern in content:
                content = content.replace(issue_pattern, replacement)
                
                with open(self.todo_file, 'w') as f:
                    f.write(content)
                
                return True
            else:
                print(f"Warning: Issue not found in TODO.md")
                return True  # Don't fail for missing TODO entry
                
        except Exception as e:
            print(f"Warning: Could not update TODO.md: {e}")
            return True  # Don't fail completion for TODO update
    
    def _update_sprint_meta(self, issue: Dict) -> bool:
        """Update sprint meta to mark issue as completed."""
        try:
            # Get current sprint
            state_file = self.root / "state" / "sprint.json"
            if not state_file.exists():
                return True
            
            with open(state_file) as f:
                state = json.load(f)
            
            sprint_name = f"sprint-{state.get('current', 1)}"
            sprint_meta = self.root / "sprints" / "open" / sprint_name / "sprint-meta.md"
            
            if not sprint_meta.exists():
                return True
            
            with open(sprint_meta, 'r') as f:
                content = f.read()
            
            # Mark issue as completed
            issue_pattern = f"- [ ] [{issue['category']}/{issue['name']}]"
            replacement = f"- [x] [{issue['category']}/{issue['name']}]"
            
            if issue_pattern in content:
                content = content.replace(issue_pattern, replacement)
                
                with open(sprint_meta, 'w') as f:
                    f.write(content)
                
                return True
            else:
                print(f"Warning: Issue not found in sprint meta")
                return True
                
        except Exception as e:
            print(f"Warning: Could not update sprint meta: {e}")
            return True
    
    def _merge_to_main(self, branch_name: str) -> bool:
        """Merge the feature branch to main."""
        try:
            # Switch to main
            subprocess.run(["git", "checkout", "main"], cwd=self.root, check=True)
            
            # Merge the feature branch
            subprocess.run(["git", "merge", branch_name], cwd=self.root, check=True)
            
            # Delete the feature branch
            subprocess.run(["git", "branch", "-d", branch_name], cwd=self.root, check=True)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to merge: {e}")
            return False 