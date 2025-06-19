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

# workflow/run_backlog_grooming

Document a backlog grooming workflow to regularly review and prioritize outstanding tasks.

## Detailed Steps

- Trigger grooming when the number of open tasks grows beyond a threshold; an
  agent can propose a meeting time rather than relying on a fixed weekly
  schedule.
- Review `issues/open/` to ensure tasks have accurate metadata (`priority`,
  `tags`), ideally automated by an agent.
- Automate detection of stale issues and move them to `issues/archived/` when
  they haven't been updated for a set period.
- Prioritize items for upcoming sprints based on multiple factors (business
  value, dependencies, and long-term goals) to avoid single-metric optimization.
- Update `last-updated` fields to track review activity.
- Summarize decisions in `docs/workflow/backlog-grooming.md` and keep a log of
  each grooming session for future reference.
