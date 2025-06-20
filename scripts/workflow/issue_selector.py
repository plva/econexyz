#!/usr/bin/env python3
"""
Issue Selector - Handles issue selection from current sprint with decision criteria.
"""

import json
import random
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add project root to path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


class IssueSelector:
    """Handles issue selection from the current sprint."""
    
    def __init__(self, root: Path):
        self.root = root
        self.sprints_dir = root / "sprints" / "open"
        self.issues_dir = root / "issues" / "open"
        
    def get_sprint_issues(self, sprint_name: str) -> List[Dict]:
        """Get all issues from the specified sprint."""
        sprint_meta = self.sprints_dir / sprint_name / "sprint-meta.md"
        if not sprint_meta.exists():
            print(f"❌ Sprint meta file not found: {sprint_meta}")
            return []
        
        issues = []
        issue_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        
        with open(sprint_meta) as f:
            for line in f:
                line = line.strip()
                if line.startswith('- [ ]'):  # Only open issues
                    match = issue_pattern.search(line)
                    if match:
                        issue_name = match.group(1)
                        issue_path = match.group(2)
                        
                        # Parse category and name from issue_name
                        if '/' in issue_name:
                            category, name = issue_name.split('/', 1)
                        else:
                            category = "unknown"
                            name = issue_name
                        
                        # Get issue details
                        issue_file = self.root / issue_path.lstrip('/')
                        issue_details = self.get_issue_details(issue_file)
                        
                        issues.append({
                            'category': category,
                            'name': name,
                            'path': issue_path,
                            'file': issue_file,
                            'details': issue_details,
                            'line': line
                        })
        
        return issues
    
    def get_issue_details(self, issue_file: Path) -> Dict:
        """Extract details from an issue file."""
        details = {
            'priority': 'medium',
            'tags': [],
            'summary': '',
            'status': 'open'
        }
        
        if not issue_file.exists():
            return details
        
        try:
            with open(issue_file) as f:
                content = f.read()
                
                # Extract metadata from frontmatter
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        metadata = parts[1]
                        for line in metadata.split('\n'):
                            if ':' in line:
                                key, value = line.split(':', 1)
                                key = key.strip()
                                value = value.strip()
                                
                                if key == 'priority':
                                    details['priority'] = value
                                elif key == 'tags':
                                    # Parse tags like "- workflow\n- automation"
                                    tags = []
                                    for tag_line in value.split('\n'):
                                        if tag_line.strip().startswith('-'):
                                            tag = tag_line.strip()[1:].strip()
                                            tags.append(tag)
                                    details['tags'] = tags
                                elif key == 'status':
                                    details['status'] = value
                
                # Extract summary from first heading
                lines = content.split('\n')
                for line in lines:
                    if line.startswith('# ') and not line.startswith('# ' + details['name']):
                        details['summary'] = line[2:].strip()
                        break
                        
        except Exception as e:
            print(f"Warning: Could not parse issue file {issue_file}: {e}")
        
        return details
    
    def filter_issues(self, issues: List[Dict], priority: Optional[str] = None, 
                     issue_type: Optional[str] = None) -> List[Dict]:
        """Filter issues based on criteria."""
        filtered = issues
        
        if priority:
            filtered = [i for i in filtered if i['details']['priority'] == priority]
        
        if issue_type:
            # Map issue types to categories/tags
            type_mapping = {
                'bug': ['bugs', 'bug'],
                'feature': ['feature', 'enhancement'],
                'workflow': ['workflow']
            }
            
            if issue_type in type_mapping:
                target_categories = type_mapping[issue_type]
                filtered = [i for i in filtered if 
                           i['category'] in target_categories or 
                           any(tag in target_categories for tag in i['details']['tags'])]
        
        return filtered
    
    def display_issues(self, issues: List[Dict]) -> None:
        """Display issues in a user-friendly format."""
        if not issues:
            print("❌ No issues found matching criteria")
            return
        
        print(f"\n📋 Available issues ({len(issues)}):")
        print("-" * 80)
        
        for i, issue in enumerate(issues, 1):
            priority_emoji = {
                'high': '🔴',
                'medium': '🟡', 
                'low': '🟢'
            }.get(issue['details']['priority'], '⚪')
            
            print(f"{i:2d}. {priority_emoji} {issue['category']}/{issue['name']}")
            if issue['details']['summary']:
                print(f"    {issue['details']['summary']}")
            if issue['details']['tags']:
                print(f"    Tags: {', '.join(issue['details']['tags'])}")
            print()
    
    def select_issue_interactive(self, issues: List[Dict]) -> Optional[Dict]:
        """Interactive issue selection."""
        self.display_issues(issues)
        
        while True:
            try:
                choice = input("Select issue number (or 'q' to quit): ").strip()
                
                if choice.lower() == 'q':
                    return None
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(issues):
                    selected = issues[choice_num - 1]
                    
                    # Show issue details for confirmation
                    print(f"\n📋 Selected: {selected['category']}/{selected['name']}")
                    print(f"Priority: {selected['details']['priority']}")
                    print(f"Tags: {', '.join(selected['details']['tags'])}")
                    if selected['details']['summary']:
                        print(f"Summary: {selected['details']['summary']}")
                    
                    confirm = input("\nConfirm selection? (y/N): ").strip().lower()
                    if confirm == 'y':
                        return selected
                    else:
                        self.display_issues(issues)
                else:
                    print(f"❌ Invalid choice. Please select 1-{len(issues)}")
                    
            except ValueError:
                print("❌ Please enter a valid number")
            except KeyboardInterrupt:
                print("\n❌ Selection cancelled")
                return None
    
    def select_random_issue(self, issues: List[Dict]) -> Optional[Dict]:
        """Select a random issue."""
        if not issues:
            return None
        
        selected = random.choice(issues)
        print(f"🎲 Randomly selected: {selected['category']}/{selected['name']}")
        return selected
    
    def select_issue(self, sprint_name: str, issue_spec: Optional[str] = None, 
                    random: bool = False, priority: Optional[str] = None, 
                    issue_type: Optional[str] = None) -> Optional[Dict]:
        """Main issue selection method."""
        print(f"🔍 Loading issues from {sprint_name}...")
        
        # Get all issues from sprint
        issues = self.get_sprint_issues(sprint_name)
        if not issues:
            print(f"❌ No open issues found in {sprint_name}")
            return None
        
        # Filter by criteria
        filtered_issues = self.filter_issues(issues, priority, issue_type)
        if not filtered_issues:
            print("❌ No issues match the specified criteria")
            return None
        
        # Handle specific issue selection
        if issue_spec:
            for issue in filtered_issues:
                if f"{issue['category']}/{issue['name']}" == issue_spec:
                    return issue
            print(f"❌ Issue '{issue_spec}' not found in current sprint")
            return None
        
        # Handle random selection
        if random:
            return self.select_random_issue(filtered_issues)
        
        # Interactive selection
        return self.select_issue_interactive(filtered_issues) 