#!/usr/bin/env python3
"""
Work Session - Handles work session tracking and logging.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Add project root to path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


class WorkSession:
    """Manages work sessions for issue development."""
    
    def __init__(self, root: Path):
        self.root = root
        self.session_file = root / "state" / "work_session.json"
        self.sessions_dir = root / "state" / "work_sessions"
        self.sessions_dir.mkdir(exist_ok=True)
        
    def start_session(self, issue: Dict) -> bool:
        """Start a new work session for an issue."""
        # Check if there's already an active session
        if self.get_current_session():
            print("⚠️  There's already an active work session")
            response = input("End current session and start new one? (y/N): ")
            if response.lower() != 'y':
                return False
            self.end_session()
        
        # Create session data
        session_data = {
            'issue': issue,
            'start_time': datetime.now().isoformat(),
            'status': 'active',
            'progress_log': [],
            'branch_name': f"issue/{issue['category']}/{issue['name']}"
        }
        
        # Create git branch
        if not self._create_branch(session_data['branch_name']):
            print("❌ Failed to create git branch")
            return False
        
        # Save session data
        try:
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            # Create session log file
            log_path = self.get_session_log_path()
            with open(log_path, 'w') as f:
                f.write(f"# Work Session: {issue['category']}/{issue['name']}\n")
                f.write(f"Started: {session_data['start_time']}\n")
                f.write(f"Branch: {session_data['branch_name']}\n\n")
                f.write("## Progress Log\n\n")
            
            print(f"✅ Started work session on branch: {session_data['branch_name']}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start work session: {e}")
            return False
    
    def end_session(self) -> bool:
        """End the current work session."""
        current_session = self.get_current_session()
        if not current_session:
            print("❌ No active work session to end")
            return False
        
        try:
            # Update session data
            current_session['end_time'] = datetime.now().isoformat()
            current_session['status'] = 'completed'
            
            # Save final session data
            with open(self.session_file, 'w') as f:
                json.dump(current_session, f, indent=2)
            
            # Archive session log
            log_path = self.get_session_log_path()
            if log_path.exists():
                archive_path = self.sessions_dir / f"{current_session['start_time'][:10]}_{current_session['issue']['name']}.md"
                log_path.rename(archive_path)
            
            # Clean up session file
            self.session_file.unlink(missing_ok=True)
            
            print("✅ Work session ended")
            return True
            
        except Exception as e:
            print(f"❌ Failed to end work session: {e}")
            return False
    
    def get_current_session(self) -> Optional[Dict]:
        """Get the current active work session."""
        if not self.session_file.exists():
            return None
        
        try:
            with open(self.session_file) as f:
                session_data = json.load(f)
                if session_data.get('status') == 'active':
                    return session_data
        except Exception as e:
            print(f"Warning: Could not read session file: {e}")
        
        return None
    
    def get_session_log_path(self) -> Path:
        """Get the path to the current session log file."""
        return self.root / "state" / "current_session.md"
    
    def log_progress(self, message: str) -> bool:
        """Log progress to the current work session."""
        current_session = self.get_current_session()
        if not current_session:
            return False
        
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'message': message
        }
        
        # Add to session data
        current_session['progress_log'].append(log_entry)
        
        # Update session file
        try:
            with open(self.session_file, 'w') as f:
                json.dump(current_session, f, indent=2)
            
            # Append to log file
            log_path = self.get_session_log_path()
            with open(log_path, 'a') as f:
                f.write(f"### {timestamp}\n")
                f.write(f"{message}\n\n")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to log progress: {e}")
            return False
    
    def get_session_summary(self) -> Optional[Dict]:
        """Get a summary of the current work session."""
        current_session = self.get_current_session()
        if not current_session:
            return None
        
        start_time = datetime.fromisoformat(current_session['start_time'])
        duration = datetime.now() - start_time
        
        return {
            'issue': current_session['issue'],
            'start_time': current_session['start_time'],
            'duration': str(duration),
            'progress_entries': len(current_session['progress_log']),
            'branch': current_session['branch_name']
        }
    
    def _create_branch(self, branch_name: str) -> bool:
        """Create a git branch for the work session."""
        try:
            # Check if we're on main/master
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                cwd=self.root
            )
            current_branch = result.stdout.strip()
            
            if current_branch not in ['main', 'master']:
                print(f"⚠️  Currently on branch '{current_branch}', switching to main first")
                subprocess.run(["git", "checkout", "main"], cwd=self.root, check=True)
            
            # Create and checkout new branch
            subprocess.run(["git", "checkout", "-b", branch_name], cwd=self.root, check=True)
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git error: {e}")
            return False
    
    def commit_work(self, message: str) -> bool:
        """Commit current work with a message."""
        try:
            # Check if there are changes to commit
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
            
            # Use commit_message script if message is not already formatted
            if not message.startswith('['):
                # Try to determine commit type from current session
                current_session = self.get_current_session()
                if current_session:
                    issue = current_session['issue']
                    commit_type = "feature"
                    if issue['category'] == 'bugs':
                        commit_type = "fix"
                    elif issue['category'] == 'workflow':
                        commit_type = "workflow"
                    
                    # Generate commit message using the script
                    try:
                        result = subprocess.run(
                            [
                                "python", "scripts/git/commit_message.py",
                                "--type", commit_type,
                                "--description", message
                            ],
                            capture_output=True,
                            text=True,
                            cwd=self.root
                        )
                        
                        if result.returncode == 0:
                            message = result.stdout.strip()
                    except subprocess.CalledProcessError:
                        # Fallback to original message
                        pass
            
            # Commit
            subprocess.run(["git", "commit", "-m", message], cwd=self.root, check=True)
            
            print(f"✅ Committed: {message}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to commit: {e}")
            return False
    
    def get_work_delta(self) -> str:
        """Get a summary of work done in this session."""
        current_session = self.get_current_session()
        if not current_session:
            return "No active work session"
        
        try:
            # Get diff since session start
            result = subprocess.run(
                ["git", "diff", "main..HEAD", "--stat"],
                capture_output=True,
                text=True,
                cwd=self.root
            )
            
            if result.stdout.strip():
                return f"Work delta:\n{result.stdout}"
            else:
                return "No changes yet"
                
        except subprocess.CalledProcessError:
            return "Could not determine work delta" 