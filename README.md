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

**After running the script, follow the colored instructions to enter the virtual environment:**

```bash
source .venv/bin/activate
```

You will see this command highlighted in green in the output. Once inside the venv, you can use commands like:

```bash
just test    # Run tests
just lint    # Check code style
```

The script creates `.venv` with [uv](https://github.com/astral-sh/uv). It can optionally install git pre-commit hooks.
When run without flags you'll be asked:

```text
Install git pre-commit hooks? [y/N]
```

Use `--yes-hooks` or `--no-hooks` to skip the prompt. Run `./bootstrap.sh --help` for all options.

> Run `just test` or `just lint` for quick local testing.
> Multi-Python support will be enabled once CI is wired.

## Command palette

Run `./bootstrap.sh` to set up the environment. The script now installs the
[`just`](https://github.com/casey/just) task runner so you can execute recipes
defined in the `Justfile`:

```bash
just --list
```

The following recipes are now implemented and working:

```bash
just test    # Run the test suite with coverage
just lint    # Check code style with ruff
```

Additional recipes are available for development, documentation, and deployment tasks.

## How to contribute

We welcome contributions from everyone. Please read
[CONTRIBUTING.md](CONTRIBUTING.md) for setup and workflow details and review our
[Code of Conduct](CODE_OF_CONDUCT.md) before participating.


### Development container (preview)

Clone the repo with VS Code and choose **"Reopen in Container"**.
First boot runs `bootstrap.sh`; afterwards all `just` commands such as
`just test`, `just lint`, and `just docs` are available.

## Behaviour-Driven tests

Add behaviour specs under `tests/features/` using `.feature` files:

```gherkin
Scenario: add two numbers
  Given two integers
  When I add them
  Then the result equals the sum
```

Run the suite with:

```bash
just test
```

Non-developers can introduce new behaviour by copying a feature file and writing
English steps only.
