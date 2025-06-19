---
status: open
category: workflow
tags:
  - devops
  - meta
  - workflow
created: 2025-06-18
last-updated: 2025-06-19
priority: medium
assigned: "plva + codex"
------------------------

# workflow/add_contribution_templates

Add templates for issues, pull requests, and sprints to standardize contributions, including:
- Issue templates for bugs, features, and documentation
- Pull request templates for code and documentation changes
- Sprint planning and retrospective templates

This will help ensure consistency and clarity in contributions and sprint planning. 
## Template Locations

- Store issue templates under `.github/ISSUE_TEMPLATE/` as YAML files.
- Place the pull request template in `.github/pull_request_template.md` with
  checklist sections.
- Provide sprint planning and retrospective templates under
  `.github/sprint_templates/` so they are easy for both humans and agents to
  locate.
- Ensure templates reference AGENTS guidelines for commit messages.
- Document usage in `docs/contributing/templates.md`.
