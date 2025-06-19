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

## Implementation Notes

- Start by scanning existing issue metadata headers to compile categories and tags.
- Example categories: `agents`, `dashboard`, `bus`, `workflow`, `cross`.
- Store the list in `config/issue_categories.yml` with a default set of tags for each category.
- Update `scripts/create_issue.py` to load this configuration and allow interactive selection via `inquirer` or similar library.
- Provide guidance in `docs/contributing/issue-categories.md` with examples.
- Add a backburner idea to explore offline interactive sessions (e.g., with
  ChatGPT&nbsp;4.5) for refining categories and tags.
