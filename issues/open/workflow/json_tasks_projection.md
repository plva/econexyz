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

# workflow/json_tasks_projection

Generate a JSON projection of the current TODO items for integration with other tools.

## Design Outline

- Read `TODO.md`, `sprints/*/sprint-meta.md`, and `issues/open/*` to build a structured representation of tasks.
- Output should include fields: `title`, `status`, `priority`, `assignee`, `tags`, and file path.
- Provide a CLI option `scripts/ai_helper.py --tasks-json` to produce the JSON.
- Ensure the output is stable for use by external dashboards or agents.
- Consider caching results in `state/tasks.json` to avoid recomputation. Cache
  invalidation can use an md5 hash of source files.
- Support a fuzzy projection mode that attempts to parse incomplete task entries
  and includes the raw text in a separate field.
