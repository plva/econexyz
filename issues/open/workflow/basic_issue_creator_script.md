---
status: open
category: workflow
tags:
  - devops
  - meta
  - workflow
created: 2025-06-19
last-updated: 2025-06-19
priority: medium
assigned: unassigned
------------------------

# workflow/basic_issue_creator_script

Develop a CLI script that automates the creation of new issue files.
The script should:

- Accept a category and issue name as arguments.
- Generate `issues/open/<category>/<name>.md` with the standard metadata
  header and a top-level heading.
- Append an entry to `/TODO.md` and to the current sprint metadata so the
  new task appears in planning documents.
- Leave the issue body as placeholder text until further automation is
  implemented.

This provides a minimal workflow for quickly adding structured issues.
