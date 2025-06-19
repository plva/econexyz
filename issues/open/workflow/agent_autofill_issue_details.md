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

# workflow/agent_autofill_issue_details

Create an agent that expands new issue stubs into fuller descriptions.
The agent should:

- Detect newly created issues that still contain placeholder text.
- Inspect related code, documentation, and existing issues to gather
  context.
- Replace the `TBD` section with a brief outline of tasks and update the
  `last-updated` field.
- Run either on demand or as part of the issue creation workflow.

This agent streamlines the process of fleshing out minimal issue drafts.
