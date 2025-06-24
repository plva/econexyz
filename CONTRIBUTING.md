# Contributing

Thank you for wanting to contribute! Follow these steps to get started.

## Setup

For first-time setup or after pulling changes, run the complete build pipeline:

```bash
just ball
```

This will bootstrap the environment, run health checks, tests, linting, and type checking.

## Development Workflow

For regular development work, run checks without bootstrapping:

```bash
just check
```

This runs health checks, tests, linting, and type checking without reinstalling dependencies.

## Individual Commands

You can also run individual commands:

```bash
just test      # Run tests
just lint      # Run linting
just types     # Run type checking
just health-check  # Check dev environment
```

## Commit

Use Commitizen to craft commit messages:

```bash
just commit
```

## Pull Requests

Before opening a PR ensure:

- `just check` runs successfully
- Documentation and CHANGELOG are updated when relevant
- Labels are applied to help triage
- Follow the [Code → Surface → Govern cadence](docs/adr/0043-code-surface-govern-cadence.md)
- See [ADR 0007](docs/adr/0007-contributor-experience-kit.md#ignored-artefacts-strategy) for repository ignore rules.

## Story template

Use the [Story issue template](.github/ISSUE_TEMPLATE/story.yml) when proposing
new work. Each story should stand on its own with clear P0/P1 sections and
acceptance criteria.


