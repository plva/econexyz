# TODO

This repository tracks work items in the `issues/` directory. Each task below links to a markdown file that contains additional details.

## Dashboard
- [ ] [dashboard/frontend_react](issues/open/dashboard/frontend_react.md) - Implement a React-based dashboard frontend.
- [ ] [dashboard/color_palette](issues/open/dashboard/color_palette.md) - Apply the shared color palette to dashboard styling.
- [ ] [dashboard/view_tasks_and_sprint](issues/open/dashboard/view_tasks_and_sprint.md) - Show tasks and sprint in the dashboard.

## Agents
- [ ] [agents/enhance_sample_agent](issues/open/agents/enhance_sample_agent.md) - Improve the sample agent and create new agents (e.g., weather).
- [ ] [agents/multi_agent_cli](issues/open/agents/multi_agent_cli.md) - Provide CLI options to run multiple agents.

## Cross-cutting
- [ ] [cross/integration_tests](issues/open/cross/integration_tests.md) - Write integration tests for the message bus and knowledge store.
- [ ] [cross/logging_improvements](issues/open/cross/logging_improvements.md) - Enhance error handling and logging.
- [ ] [cross/script_lint_format_cleanup](issues/open/cross/script_lint_format_cleanup.md) - Lint, format, and clean up scripts for consistency and maintainability.

## Event Bus
- [ ] [bus/message_ttl](issues/open/bus/message_ttl.md) - Implement optional message TTL.
- [ ] [bus/queue_polling](issues/open/bus/queue_polling.md) - Provide a queue with polling and removal semantics.
- [ ] [bus/prod_backend](issues/open/bus/prod_backend.md) - Support a production-ready backend such as Redis or NATS.
- [ ] [bus/inject_bus_impl](issues/open/bus/inject_bus_impl.md) - Inject the chosen bus implementation into the agent runner and dashboard.
- [ ] [bus/message_pagination](issues/open/bus/message_pagination.md) - Add pagination to the `/messages` endpoint.

## Meta/Workflow
- [ ] [workflow/run_sprint_planning](issues/open/workflow/run_sprint_planning.md) - Run a sprint planning workflow.
- [ ] [workflow/run_backlog_grooming](issues/open/workflow/run_backlog_grooming.md) - Run a backlog grooming workflow.
- [ ] [workflow/run_sprint_retro](issues/open/workflow/run_sprint_retro.md) - Run a sprint retrospective.
- [ ] [workflow/manage_unassigned_backlog_tasks](issues/open/workflow/manage_unassigned_backlog_tasks.md) - Manage tasks not assigned to a sprint.
- [ ] [workflow/view_sprint_and_backlog](issues/open/workflow/view_sprint_and_backlog.md) - View the current sprint and unassigned tasks.
- [ ] [workflow/json_tasks_projection](issues/open/workflow/json_tasks_projection.md) - Provide a JSON projection of tasks.
- [ ] [workflow/remove_completed_sprint_todos_on_archive](issues/open/workflow/remove_completed_sprint_todos_on_archive.md) - Remove completed sprint TODOs from top level when archiving.
- [x] [workflow/view_workflow_diagrams](issues/closed/workflow/view_workflow_diagrams.md) - Provide docs and a script for viewing diagrams.
- [x] [workflow/workflow_diagrams](issues/closed/workflow/workflow_diagrams.md) - Document sprint, issue, and meta-sprint workflows.
- [ ] [workflow/document_development_process](issues/open/workflow/document_development_process.md) - Document the typical development process for contributors.
- [ ] [workflow/document_sprint_and_meta_sprint_process](issues/open/workflow/document_sprint_and_meta_sprint_process.md) - Document the sprint and meta-sprint process.
- [ ] [workflow/onboarding_for_agents_and_collaborators](issues/open/workflow/onboarding_for_agents_and_collaborators.md) - Create onboarding documentation for agents and collaborators.
- [ ] [workflow/improve_sprint_issue_scripts](issues/open/workflow/improve_sprint_issue_scripts.md) - Write or improve scripts for sprint and issue management.
- [ ] [workflow/add_contribution_templates](issues/open/workflow/add_contribution_templates.md) - Add templates for issues, PRs, and sprints.
