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

# workflow/onboarding_for_agents_and_collaborators

Create or improve onboarding documentation for new agents and collaborators, including:
- Overview of the repository structure
- How to register and implement new agents
- How to contribute to the dashboard, message bus, or storage
- Coding standards and best practices
- Where to find help and documentation

This should be included in a dedicated onboarding section in the documentation. 
## Suggested Structure

- `docs/onboarding/overview.md`: high-level architecture and repo layout.
- `docs/onboarding/agents.md`: step-by-step guide for creating and registering a new agent using `AGENTS.md` as reference.
- `docs/onboarding/contributing.md`: guidelines on branching strategy, commit style, and PR review.
  Follow existing best practices where possible (keep it simple).
- Provide quickstart scripts: `scripts/setup_env.sh` and `scripts/run_demo.sh`.
- Add a backburner note about organizing scripts into directories such as
  `demo/`, `development/`, and `onboarding/`.
- Include FAQ covering common errors with message bus, storage, or tests.
- Create a backburner task for an agent that scans the FAQ and suggests
  improvements or automated checks.
