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

# workflow/run_sprint_planning

Provide a workflow for running sprint planning so that backlog items can be selected and prioritized for the upcoming sprint.

## Notes

- Identify backlog items in `issues/open/` and categorize them by priority and dependencies.
- Define a planning meeting script that loads existing sprint data using `scripts/ai_helper.py`.
- The script should present current progress and outstanding tasks so the team
  can reason about capacity and dependencies.
- Outline steps for selecting tasks:
  - Review carry-over items from the previous sprint.
    - If many items carry over, create a meta-sprint task to adjust the process.
  - Estimate effort using story points stored in issue metadata.
    - Effort represents how much work is required and whether tasks can run in
      parallel.
  - Map capacity to team members.
    - This remains fuzzy; track this in a backburner issue for future process
      improvements.
- Provide a summary of chosen tasks in `sprints/current/sprint-meta.md`.
- Automate updates to `TODO.md` via `scripts/create_issue.py` or manual editing.
- Only append new tasks to `TODO.md`; encapsulate other updates in dedicated
  scripts.
- Suggest building a CLI to run the planning process end-to-end.
  - Capture the flow in a simple Mermaid diagram as a proof of concept. Create a
    separate issue for this CLI design.
