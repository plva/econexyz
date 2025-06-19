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

# workflow/issue_category_tag_list

Provide a reusable list of issue categories and tags for the creation
script. Suggested steps:

- Gather existing categories and common tags across the repository.
- Store them in a simple JSON or YAML file within `config/`.
- Update `create_issue.py` to present these options via an interactive
  prompt or fuzzy finder when a new issue is generated.
- Document the available categories and tags so contributors understand
  how to use them.

With a standard list, new issues will be more consistent and easier to
search.
