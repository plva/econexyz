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

## Additional Notes

- Validate category names against a list in `config/issue_categories.yml`, but
  allow creation of new categories by prompting to append them to the file.
- Use Jinja2 templates for the metadata header and body to ensure consistency.
  Example:
  ```jinja
  ---
  status: open
  category: {{ category }}
  ...
  ```
- Optionally prompt the user for tags and priority if not provided.
- Avoid opaque IDs in filenames so issues remain readable when listed.
- Write unit tests in `tests/test_create_issue.py` to cover edge cases. Also
  create an issue to run unit tests on every build/PR and report failures without
  blocking the merge.
