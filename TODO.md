# TODO

This repository tracks work items in the `issues/` directory. Each task below links to a markdown file that contains additional details.

## Dashboard
- [ ] [dashboard/frontend_react](issues/open/dashboard/frontend_react.md) - Implement a React-based dashboard frontend.
- [ ] [dashboard/color_palette](issues/open/dashboard/color_palette.md) - Apply the shared color palette to dashboard styling.

## Agents
- [ ] [agents/enhance_sample_agent](issues/open/agents/enhance_sample_agent.md) - Improve the sample agent and create new agents (e.g., weather).
- [ ] [agents/multi_agent_cli](issues/open/agents/multi_agent_cli.md) - Provide CLI options to run multiple agents.

## Cross-cutting
- [ ] [cross/integration_tests](issues/open/cross/integration_tests.md) - Write integration tests for the message bus and knowledge store.
- [ ] [cross/logging_improvements](issues/open/cross/logging_improvements.md) - Enhance error handling and logging.

## Event Bus
- [x] [bus/message_pagination](issues/open/bus/message_pagination.md) - Add pagination to the `/messages` endpoint.
- [ ] [bus/message_ttl](issues/open/bus/message_ttl.md) - Implement optional message TTL.
- [ ] [bus/queue_polling](issues/open/bus/queue_polling.md) - Provide a queue with polling and removal semantics.
- [ ] [bus/prod_backend](issues/open/bus/prod_backend.md) - Support a production-ready backend such as Redis or NATS.
- [ ] [bus/inject_bus_impl](issues/open/bus/inject_bus_impl.md) - Inject the chosen bus implementation into the agent runner and dashboard.

## Meta/Workflow
- [x] [issues/implement-issue-tracking-workflow](issues/open/issues/implement-issue-tracking-workflow.md) - Break down overall workflow issue into smaller tasks.
- [x] [issues/create-directory-structure](issues/open/issues/create-directory-structure.md) - Set up open and closed directories.
- [x] [issues/add-close-script](issues/open/issues/add-close-script.md) - Provide script to move issues to closed.
- [x] [issues/update-agents-instructions](issues/open/issues/update-agents-instructions.md) - Document completion workflow.
- [x] [issues/migrate-existing-issues](issues/open/issues/migrate-existing-issues.md) - Move current issues into new structure.
- [x] [workflow/implement-integrated-sprint-and-issue-workflow](issues/closed/workflow/implement-integrated-sprint-and-issue-workflow.md) - Implement integrated sprint and issue workflow with archival structure.
  - [x] Update Documentation & Agent Instructions (PR #3)
  - [x] Optional - AI Integration Helper (PR #4)
- [ ] [workflow/implement-git-transactions](issues/open/workflow/implement-git-transactions.md) - Implement transactional Git workflow scripts and documentation
- [ ] [workflow/sprint-file-validation](issues/open/workflow/sprint-file-validation.md) - Validate sprint files and warn on formatting errors.
