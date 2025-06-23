# Contributing

Thank you for wanting to contribute! Follow these steps to get started.

## Setup

Run the bootstrap script which sets up a virtual environment and installs dependencies:

```bash
./bootstrap.sh
```

You can then run lint and tests:

```bash
just lint
just test
```

## Commit

Use Commitizen to craft commit messages:

```bash
just commit
```

## Pull Requests

Before opening a PR ensure:

- `just lint && just test` run successfully
- Documentation and CHANGELOG are updated when relevant
- Labels are applied to help triage
- See [ADR 0007](docs/adr/0007-contributor-experience-kit.md#ignored-artefacts-strategy) for repository ignore rules.

## Story template

Use the [Story issue template](.github/ISSUE_TEMPLATE/story.yml) when proposing
new work. Each story should stand on its own with clear P0/P1 sections and
acceptance criteria.


