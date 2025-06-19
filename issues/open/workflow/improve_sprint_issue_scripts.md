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

# workflow/improve_sprint_issue_scripts

Write or improve scripts for sprint and issue management, including:
- Archiving sprints and moving issues
- Generating sprint and backlog reports
- Automating the creation of new sprints and issue templates
- Normalizing and validating sprint files

This will help automate and standardize the workflow for all contributors. 
## Ideas

- Convert `archive_sprint.sh` to Python for better cross-platform support.
  Create a backburner task to gradually migrate frequently used shell scripts to
  Python.
- Implement unit tests in `tests/test_sprint_scripts.py` covering edge cases.
- Provide a new script `scripts/normalize_issues.py` to update metadata headers
  automatically (e.g., ensuring `last-updated` and `priority` fields exist).
- Use YAML configuration files in `config/` for default sprint lengths and
  backlog locations. Sprint length is measured in cycles rather than absolute
  clock time.
- Consider packaging these scripts as a CLI tool (`econexyz-cli`). Add this idea
  to the backburner for further brainstorming.
