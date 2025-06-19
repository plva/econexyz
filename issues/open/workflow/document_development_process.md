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

# workflow/document_development_process

Document the typical development process for contributors, including:
- How to set up the environment
- How to run agents and the dashboard
- How to add new agents or features
- How to use scripts for development and workflow
- Where to find and how to use documentation and diagrams

This should be included in the main README and/or a CONTRIBUTING.md file. 
## Outline for Documentation

1. Environment Setup
   - Use `bootstrap.sh` to install dependencies from `requirements.txt`.
   - Provide instructions for Python virtual environments.
2. Running Components
   - Use `scripts/run_agents.py` to start agents.
   - Launch the dashboard with `python dashboard/app.py`.
3. Adding Features
   - Follow guidelines in `AGENTS.md` when creating new agents.
   - Update `TODO.md` and create issues using `scripts/create_issue.py`.
4. Scripts
   - Document `scripts/close_issue.sh` and `scripts/archive_sprint.sh` usage.
5. Diagrams
   - Reference `docs/diagrams/` for workflow visuals.
   - Document the currently used development process with new diagrams if none
     exist.
   - Suggest using `scripts/view_diagrams.sh` if provided.

Add this content to `CONTRIBUTING.md` and link from `README.md`.
