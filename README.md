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

> Run `nox -s tests` or `nox -s lint` locally.
> Multi-Python support will be enabled once CI is wired.

## Command palette

Run `./bootstrap.sh` to set up the environment. The script now installs the
[`just`](https://github.com/casey/just) task runner so you can execute recipes
defined in the `Justfile`:

```bash
just --list
```

The current recipes still print TODO placeholders until the next phase wires in
real commands.

## How to contribute

We welcome contributions from everyone. Please read
[CONTRIBUTING.md](CONTRIBUTING.md) for setup and workflow details and review our
[Code of Conduct](CODE_OF_CONDUCT.md) before participating.


### Development container (preview)

Clone the repo with VS Code and choose **"Reopen in Container"**.
First boot runs `bootstrap.sh`; afterwards all `just` commands such as
`just test`, `just lint`, and `just docs` are available.
