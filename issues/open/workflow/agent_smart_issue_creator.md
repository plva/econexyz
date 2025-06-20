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

# workflow/agent_smart_issue_creator

Design an advanced agent that can generate new issues from a short task
description. Features should include:

- Searching the repository, open issues, and sprint metadata for
  relevant context.
- Suggesting appropriate categories and tags automatically.
- Expanding the description with implementation ideas or follow-up
  subtasks.
- Allowing a human reviewer to approve or modify the generated issue
  before it is committed.

This agent may require multiple iterations and could depend on a larger
language model or external services.

## Architectural Considerations

- This agent may call a language model API to interpret brief descriptions and produce a structured issue draft.
- It should integrate with `scripts/create_issue.py` to ensure metadata consistency.
- Support plugin-based strategies for context gathering (e.g., scanning git log, README, or TODO files).
- Keep a `issues/backburner/workflow/brainstorming.md` file to track overlap with
  `agent_autofill_issue_details` and other related automation ideas.
- Explore more advanced strategies (potentially with ChatGPT&nbsp;4.5) for the
  plugin system and record findings in the brainstorming file.
- Provide an approval workflow: generate issue -> open diff -> user accepts via CLI or web UI -> commit.
- Add a new backburner issue to design an interactive multi-commit workflow on a
  development branch that can later be squashed onto main.
- Store configuration for categories and tags in `config/issue_categories.yml` to reuse across the project.

## Implementation Plan (PR Breakdown)

### PR #1: Initial Agent Prototype
- [x] Create `SmartIssueCreatorAgent` with basic heuristics for category selection.
- [x] Load tag suggestions from `config/issue_categories.yml`.
- [x] Integrate with `create_issue.py` and prompt user for approval before writing files.

### PR #2: Context Plugins
- [ ] Define plugin interface for gathering repository context.
- [ ] Implement simple plugins for scanning README and open issues.
- [ ] Add unit tests for plugin loading and execution.

### PR #3: Advanced Language Model Support
- [ ] Add optional integration with a language model API for draft generation.
- [ ] Provide configuration and error handling for external service calls.
