# 🦾 EcoNexyz: Agent Development Guide (`AGENTS.md`)

Use GitHub issues for instructions. If you have an issue number, fetch its body with:

```bash
curl -sL https://api.github.com/repos/plva/econexyz/issues/<NUMBER>
```

For background on our tooling choices see [docs/adr/index.md](docs/adr/index.md). Any design decision affecting repository tooling must include a new ADR.

## Quickstart

Clone the repository and run the bootstrap script:

```bash
git clone https://github.com/plva/econexyz
cd econexyz
./bootstrap.sh
```

Run a task inside the environment:

```bash
./bootstrap.sh test
```

The script creates `.venv` with [uv](https://github.com/astral-sh/uv). It can optionally install git pre-commit hooks.
When run without flags you'll be asked:

```text
Install git pre-commit hooks? [y/N]
```

Use `--yes-hooks` or `--no-hooks` to skip the prompt. Run `./bootstrap.sh --help` for all options.

## Command palette

A `Justfile` in the repo root defines commands like `just test` and `just lint`. These recipes currently print TODO messages and will be wired up in a future phase.

