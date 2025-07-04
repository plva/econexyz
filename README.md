# 🦾 EcoNexyz: Agent Development Guide (`AGENTS.md`)
[![build / Hello World](https://github.com/plva/econexyz/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/plva/econexyz/actions/workflows/ci.yml)
[![docs](https://img.shields.io/badge/docs-live-blue)](https://plva.github.io/econexyz/)

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
nox -s docs  # Build docs
```

The script creates `.venv` with [uv](https://github.com/astral-sh/uv) and automatically installs git pre-commit hooks.
Use `--no-hooks` to skip hook installation. Run `./bootstrap.sh --help` for all options.

> Run `just test` or `just lint` for quick local testing.
> Multi-Python support will be enabled once CI is wired.
> Edit `api/openapi.yaml`; run `nox -s api-contract` to fuzz the API with Schemathesis.

## Repository variables

Repository owner and name live in `.github/repo_vars.yml`. Workflows load these
values via the composite workflow `./.github/workflows/_setup-repo-vars.yml`.
When forking or templating this project, adjust `owner` and `repo` in
`repo_vars.yml` to point to the new repository.

## Command palette

Run `./bootstrap.sh` to set up the environment. The script installs the
[`just`](https://github.com/casey/just) task runner so you can execute recipes
defined in the `Justfile`:

```bash
just --list
```

### Common recipes

- `just ball` — Full build: bootstraps, checks dependencies, runs tests, lint, and type checks. Use this after pulling new changes, updating dependencies, or for a full CI check.
- `just check` — Quick check: runs health check, tests, lint, and type checks (no bootstrapping or dependency updates). Use this when iterating locally and you haven't changed dependencies.
- `just test` — Run the test suite
- `just lint` — Check code style
- `just types` — Static type analysis

**Tip:**
- Bootstrap (`./bootstrap.sh`) only needs to be run once (successfully) per repository clone. After that, you can use `just ball` for a full check, or `just check` for fast iteration if you haven't changed dependencies.

See the Justfile for more available recipes.

### Commit workflow

```bash
git add .
just commit        # interactive wizard
```

Secrets are blocked by Gitleaks. False positives? Add an allow-rule to
`.gitleaks.toml` with a justification.

Every push and pull request runs a `secret-scan` job in CI to ensure no leaks
land in the repository. This step uses the automatically created `GITHUB_TOKEN`
to comment on pull requests. It fails the workflow if any secrets are detected
and must pass before the test job runs.

Local scan command:

```bash
uv tool run gitleaks detect --source . --redact
```

Direct `git commit -m` is allowed but must follow Conventional Commit rules.
Headers must stay ≤ 52 characters; CI will block longer ones.

## Quality & Security
![coverage](https://raw.githubusercontent.com/plva/econexyz/gh-pages-coverage/coverage.svg)

| Command | Purpose |
| ------- | ------- |
| `just lint` | Check code style with ruff |
| `just test` | Run the test suite with coverage |
| `just types` | strict static type-check (Ty) |
| `nox -s security` | runs pip-audit against the lock file |

Additional recipes are available for development, documentation, and deployment tasks.

Coverage threshold: **≥ 80 %** (`nox -s tests` generates htmlcov/)

## Project conventions

Architecture Decision Records live under [`docs/adr/`](docs/adr/index.md).
They capture the context and consequences of major engineering choices.
See [ADR 0043](docs/adr/0043-code-surface-govern-cadence.md) for our Code → Surface → Govern cadence.
Create a new entry with:

```bash
just adr-new "Use Read the Docs for hosting"
```
Validate all ADRs with:

```bash
nox -s adr_lint
```

## How to contribute

We welcome contributions from everyone. Please read
[CONTRIBUTING.md](CONTRIBUTING.md) for setup and workflow details and review our
[Code of Conduct](CODE_OF_CONDUCT.md) before participating.

## Branch protection

To keep `main` healthy, maintainers should enable a branch protection rule that
*requires status checks to pass before merging*. Navigate to
**Settings → Branches → Protect main** and tick "Require status checks to pass".
For a detailed walkthrough see
[docs/github-branch-protection.md](docs/github-branch-protection.md).


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

Runtime type checks (Typeguard) run automatically.
Disable locally: `pytest -q -p no:pytest_typeguard`

Non-developers can introduce new behaviour by copying a feature file and writing
English steps only.
# test
