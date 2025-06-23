# 🦾 EcoNexyz: Agent Development Guide (`AGENTS.md`)

Use GitHub issues for instructions. If you have an issue number, fetch its body with:

```bash
curl -sL https://api.github.com/repos/plva/econexyz/issues/<NUMBER>
```

## Development Commands

For first-time setup or complete rebuild:
```bash
just ball
```

For regular development checks:
```bash
just check
```

For individual operations:
```bash
just test          # Run tests
just lint          # Run linting
just types         # Run type checking
just health-check  # Check dev environment
just commit        # Interactive commit
```

## Environment Setup

The project uses `uv` for dependency management and `just` for task running. The bootstrap script sets up the virtual environment and installs all dependencies.

For background on our tooling choices see [docs/adr/index.md](docs/adr/index.md). Any design decision affecting repository tooling must include a new ADR.

When crafting the commit message, make sure to reference it in the commit header, and if all phases have been completed, that this commit closes it (e.g. "Closes #57)