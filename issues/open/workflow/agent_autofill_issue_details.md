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

## Agent Design

- Build on the `Agent` base class with a schedule to scan `issues/open/` for placeholders.
- Use natural language processing to summarize related files or previous issues.
- Explore calling a language model API (e.g., ChatGPT) to expand context and
  generate summaries. Create a separate issue to decide how API keys should be
  stored and shared with new collaborators.
- Update issue files in place and commit changes with a standard message via `gitpython`.
- Briefly, `gitpython` allows programmatic staging and committing so the agent
  can create commits without manual git commands.
- Provide a dry-run mode for manual review before committing.
- Consider integration with the `basic_issue_creator_script` to run immediately after issue creation.
