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

## Implementation Plan (PR Breakdown)

### PR #1: Create ChatGPT API Integration Scaffolding
- [ ] Add `openai` dependency to `requirements.txt`
- [ ] Create `econexyz/agents/autofill_agent.py` with basic Agent class structure
- [ ] Create `config/openai_config.yml` for API key management
- [ ] Add environment variable support for `OPENAI_API_KEY`
- [ ] Create basic ChatGPT client wrapper in `econexyz/utils/openai_client.py`
- [ ] Add error handling for API rate limits and failures
- [ ] Create unit tests for OpenAI client wrapper
- [ ] Add documentation for onboarding and for setup, and validation that everything is ok (smoke testing)

### PR #2: Issue Detection and Context Gathering
- [ ] Implement issue scanning logic to find files with "TBD" content
- [ ] Create context gathering from related files (README, existing issues, code)
- [ ] Add file parsing utilities for markdown and code files
- [ ] Implement context summarization logic
- [ ] Add configuration for which directories/files to scan
- [ ] Create unit tests for context gathering

### PR #3: Issue Enhancement Logic
- [ ] Implement prompt engineering for issue expansion
- [ ] Create issue content enhancement using ChatGPT
- [ ] Add structured output parsing (JSON response format)
- [ ] Implement fallback logic when API is unavailable
- [ ] Add content validation and safety checks
- [ ] Create unit tests for enhancement logic

### PR #4: Git Integration and File Updates
- [ ] Add `gitpython` dependency to `requirements.txt`
- [ ] Implement in-place file updating with backup creation
- [ ] Add git staging and committing functionality
- [ ] Implement dry-run mode for manual review
- [ ] Add commit message templates
- [ ] Create rollback functionality for failed updates
- [ ] Add unit tests for git operations

### PR #5: Agent Integration and CLI
- [ ] Integrate agent into `scripts/run_agents.py`
- [ ] Create CLI interface for manual triggering
- [ ] Add scheduling options (on-demand vs periodic)
- [ ] Implement integration with `create_issue.py` workflow
- [ ] Add logging and monitoring capabilities
- [ ] Create configuration for agent behavior
- [ ] Add comprehensive integration tests

### PR #6: Documentation and Polish
- [ ] Update `AGENTS.md` with autofill agent documentation
- [ ] Create usage examples and best practices
- [ ] Add troubleshooting guide
- [ ] Update development process documentation
- [ ] Create performance benchmarks
- [ ] Add security considerations documentation

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

## Configuration Requirements

- OpenAI API key management
- Configurable scanning directories
- Prompt templates for different issue types
- Git commit message templates
- Error handling and retry logic
- Rate limiting and cost management
