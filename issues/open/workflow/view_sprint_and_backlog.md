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

# workflow/view_sprint_and_backlog

Allow users to view the current sprint tasks alongside any unassigned backlog items.

## Implementation Ideas

- Provide a `dashboard` endpoint that aggregates `sprints/current/` and `state/backlog.json`.
- This is a large feature; track smaller subtasks in the backburner directory.
- Display tasks in a web view, grouped by status (planned, in progress, backlog).
- Offer filters for tags, assignees, and priority to quickly locate tasks.
- Consider a CLI option in `scripts/run_agents.py` to output a summary table.
- Ensure data is updated by calling `python scripts/ai_helper.py` when tasks change.
- Clarify when data might be stale and define triggers for running the helper
  script.
