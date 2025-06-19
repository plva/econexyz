# TODO

This repository tracks work items in the `issues/` directory. Each task below links to a markdown file that contains additional details.

## Dashboard
- [ ] [dashboard/frontend_react](issues/dashboard/frontend_react.md) - Implement a React-based dashboard frontend.
- [ ] [dashboard/color_palette](issues/dashboard/color_palette.md) - Apply the shared color palette to dashboard styling.

## Agents
- [ ] [agents/enhance_sample_agent](issues/agents/enhance_sample_agent.md) - Improve the sample agent and create new agents (e.g., weather).
- [ ] [agents/multi_agent_cli](issues/agents/multi_agent_cli.md) - Provide CLI options to run multiple agents.

## Cross-cutting
- [ ] [cross/integration_tests](issues/cross/integration_tests.md) - Write integration tests for the message bus and knowledge store.
- [ ] [cross/logging_improvements](issues/cross/logging_improvements.md) - Enhance error handling and logging.

## Event Bus
- [x] [bus/message_pagination](issues/bus/message_pagination.md) - Add pagination to the `/messages` endpoint.
- [ ] [bus/message_ttl](issues/bus/message_ttl.md) - Implement optional message TTL.
- [ ] [bus/queue_polling](issues/bus/queue_polling.md) - Provide a queue with polling and removal semantics.
- [ ] [bus/prod_backend](issues/bus/prod_backend.md) - Support a production-ready backend such as Redis or NATS.
- [ ] [bus/inject_bus_impl](issues/bus/inject_bus_impl.md) - Inject the chosen bus implementation into the agent runner and dashboard.

## Meta/Workflow
- [x] [issues/implement-issue-tracking-workflow](issues/issues/implement-issue-tracking-workflow.md) - Break down overall workflow issue into smaller tasks.
- [ ] [issues/create-directory-structure](issues/issues/create-directory-structure.md) - Set up open and closed directories.
- [ ] [issues/add-close-script](issues/issues/add-close-script.md) - Provide script to move issues to closed.
- [ ] [issues/update-agents-instructions](issues/issues/update-agents-instructions.md) - Document completion workflow.
- [ ] [issues/migrate-existing-issues](issues/issues/migrate-existing-issues.md) - Move current issues into new structure.
