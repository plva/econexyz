Below are **ADR 0001 → ADR 0010** rewritten with fuller context, decisions, alternatives, and consequences.
Feel free to copy each into its own file (e.g., `docs/adr/0001-adr-process.md`, …).

---

# 0001 – ADR Process

*Status*: **Accepted**

## Context

Teams change, tools age, and “why did we do this?” is the most expensive question to answer from scratch. We need a lightweight, repeatable way to capture reasoning so future contributors—human or AI—can trace, critique, or reverse a choice without code archaeology.

## Decision

Adopt Michael Nygard–style Architecture Decision Records (ADRs) in `docs/adr/`, one Markdown file per major choice.

* Template lives at `docs/adr/_template.md`.
* Sequential IDs, kebab-case titles.
* Status field tracks lifecycle (Proposed → Accepted → Superseded).

## Alternatives Considered

* **Wiki pages** – easy to start, hard to version, harder to review.
* **Commit messages only** – context buried in logs; merges obscure history.
* **Inline docs in READMEs** – discoverability issues once several topics grow.

## Consequences

* Clear audit trail; design discussions become first-class artefacts.
* New joiners ramp faster; models can cite decisions directly.
* Slight paperwork overhead—acceptable given infrequent creation rate.

---

# 0002 – Bootstrap `sh` + `uv`

*Status*: **Accepted**

## Context

New contributors (and agents) must move from clone to usable environment in minutes. Traditional solutions—Poetry, virtualenv + requirements.txt—either install slowly or leave room for “works-on-my-machine” drift.

## Decision

Use **`uv venv`** for environment creation and **`uv pip --freeze`** for lockfile generation. Wrap both in `bootstrap.sh`, which:

1. Creates/updates the `.venv` in the repo root.
2. Installs dev tools from `pyproject.toml`.
3. Offers to run `pre-commit install`.

Cold install target: < 3 minutes on GitHub hosted runners.

## Alternatives Considered

| Option           | Pros                               | Cons                                               |
| ---------------- | ---------------------------------- | -------------------------------------------------- |
| Poetry           | Mature community, lockfile support | Slower (\~4×), global cache confusion              |
| pip + virtualenv | Familiar                           | Non-deterministic unless we add third-party locker |
| Conda            | Handles binaries                   | 100 MB+ install, licence confusion                 |

## Consequences

* Fast, deterministic setup; matches CI exactly.
* Dependent on `uv` maturity (still < 1.0). If `uv` stagnates, rollback path is to Poetry; lockfile translation possible via `deptree freeze`.

---

# 0003 – Optional Pre-commit Install

*Status*: **Accepted**

## Context

Some contributors prefer to review staged diffs before any auto-fix; others want hooks auto-installed. Enforcing hooks silently can break scripted commits (e.g., release bots).

## Decision

`bootstrap.sh` prints:

```
Install pre-commit hooks? [Y/n]:
```

* “Yes” → `pre-commit install --install-hooks`.
* “No” → sets Git config `core.hooksPath=.githooks_optional`. CI always runs hooks regardless.

## Alternatives Considered

* **Force install** – ensures consistency but surprises users.
* **Leave manual** – new contributors forget to install, leading to noisy CI failures.

## Consequences

* Local control, CI enforcement.
* Slight complexity in `bootstrap.sh`; acceptable.

---

# 0004 – Justfile Core Recipes

*Status*: **Accepted**

## Context

Agents and humans need a single place to discover common commands. `make` is ubiquitous but tab-sensitive and less friendly on Windows; shell scripts scatter logic.

## Decision

Adopt **`just`**. Root `Justfile` exposes verbs:

```
just lint      # Ruff
just test      # Nox default session
just bench     # Performance guard
just docs      # Build Sphinx site
```

## Alternatives Considered

| Option            | Pros                 | Cons                                      |
| ----------------- | -------------------- | ----------------------------------------- |
| Make              | Installed everywhere | Tabs, poor Windows UX                     |
| Nox sessions only | Python-native        | Requires `nox -s`, harder discoverability |
| Bash scripts      | Zero deps            | Spaghetti over time                       |

## Consequences

* Clear self-documenting CLI; `just --list` acts as help.
* Requires `just` binary on dev machines (install via `uv tool install just`).

---

# 0005 – Dev-container / Codespaces

*Status*: **Accepted**

## Context

On-boarding should take minutes even on an iPad. GitHub Codespaces provides cloud VMs with VS Code in the browser; a `.devcontainer` spec pre-installs tools.

## Decision

Ship a checked-in `.devcontainer.json` that:

* Uses Debian slim image with system `git`, `curl`, `uv`.
* Runs `bootstrap.sh` on first start.
* Pre-installs VS Code extensions: Python, YAML, Docker, just-tasks.

## Alternatives Considered

* **Remote-Containers extension only** – works, but lacks 1-click Codespaces.
* **No dev-container** – fastest now, slower for every new contributor later.

## Consequences

* Near-zero setup in browser; demos run anywhere.
* Slight maintenance effort when base image needs patching.

---

# 0006 – Hatch Workspaces

*Status*: **Accepted**

## Context

Today we have one package; tomorrow we may split core, plugins, or shared proto models. Managing multiple `pyproject`s without pain is the goal.

## Decision

Enable **Hatch workspaces** in root `pyproject.toml`, allowing sub-packages under `packages/` to be built and tested together.

## Alternatives Considered

| Option                 | Pros       | Cons                          |
| ---------------------- | ---------- | ----------------------------- |
| Pants                  | Powerful   | Heavy, steeper learning curve |
| Poetry multi-project   | Familiar   | Limited workspace features    |
| Monorepo with sub-venv | Simple now | Dependency duplication later  |

## Consequences

* Easy path to multi-package repo.
* Developers must learn Hatch commands (`hatch run`, `hatch build`).

---

# 0007 – Contributor Experience Kit

*Status*: **Accepted**

## Context

External contributors—including AI agents—benefit from clear templates and rules of engagement.

## Decision

* `CONTRIBUTING.md` – setup, lint, test, commit flow.
* Issue templates: bug, feature, question.
* PR template with checklist.
* Contributor Covenant 2.1 as `CODE_OF_CONDUCT.md`.

## Alternatives Considered

* **No templates** – fastest now, but yields low-quality issues.
* **Third-party bots for templates** – additional infra, latency.

## Consequences

* Higher-quality issues/PRs.
* Slight repo noise; acceptable trade-off.

---

# 0008 – Nox Runner

*Status*: **Accepted**

## Context

We need a task runner that can create disposable virtual envs for each session, handle matrix testing, and be scripted in Python.

## Decision

Adopt **Nox** over Tox. Reasons:

* Pure-Python config; easier dynamic logic.
* Re-use existing `.venv` when possible (`reuse_venv=True`).
* Plays well with `uv` inside sessions.

## Alternatives Considered

| Option       | Pros               | Cons                         |
| ------------ | ------------------ | ---------------------------- |
| Tox          | Mature, widespread | INI syntax, slower env reuse |
| Make         | Ubiquitous         | Harder matrix, shell-centric |
| Bash scripts | No deps            | Duplicated logic, OS quirks  |

## Consequences

* Single runner for tests, lint, docs, security scans.
* Contributors install `nox` (added to dev-dependencies).

---

# 0009 – BDD + Property Testing

*Status*: **Accepted**

## Context

Readable behaviour specs help non-coders (and agents) understand intent; property tests expose edge cases.

## Decision

Combine **pytest-bdd** for `.feature` files with **Hypothesis** for property strategies. Example directory layout:

```
tests/
  features/
    login.feature
  test_properties.py
```

## Alternatives Considered

* **Plain pytest only** – simpler, but loses Given/When/Then clarity.
* **Behave** – pure BDD but no Hypothesis integration.
* **Gherkin + external runner** – more moving parts.

## Consequences

* Shared language between PM-style feature files and code.
* Slight learning curve; justified by increased coverage.

---

# 0010 – Ty Static Types

*Status*: **Accepted**

## Context

We want strict type checking but mypy’s performance can slow large codebases. `Ty` wraps mypy in Rust for speed.

## Decision

Use **Ty** (`uv tool install ty`). Run as a Nox session and pre-commit hook.

## Alternatives Considered

| Option   | Pros                 | Cons                                       |
| -------- | -------------------- | ------------------------------------------ |
| Raw mypy | Stable, feature-rich | 2-4× slower; higher CI time                |
| Pyright  | Fast                 | Slightly different type system; needs Node |
| None     | No overhead          | Bugs appear later                          |

## Consequences

* < 5 s type check in CI on current codebase.
* Ty is pre-release; if abandoned, fallback is to mypy with same flags.

---

*(Next batch will cover ADR 0011 → 0020.)*
Below are **ADR 0011 → ADR 0020** with expanded details.

---

# 0011 – Typeguard Runtime Checks

*Status*: **Accepted**

## Context

Static analysis catches many type errors, but values can still go wrong at
runtime (e.g., data loaded from JSON). We want a lightweight check that runs
during tests without affecting production performance.

## Decision

Add **`pytest-typeguard`** (Typeguard in “importlib” mode). A Nox session
invokes:

```bash
pytest -m "not slow" --typeguard-packages=src
```

## Alternatives Considered

| Option                        | Pros          | Cons                                |
| ----------------------------- | ------------- | ----------------------------------- |
| No runtime check              | Zero overhead | Bugs surface in prod paths only     |
| Pydantic `validate_call`      | Rich errors   | Adds heavy dependency to every func |
| Monkeypatch `__annotations__` | DIY           | Fragile, hard to maintain           |

## Consequences

* Extra safety net during CI.
* Opt-out in performance-critical tests by using `@typechecked(always=False)`.

---

# 0012 – Coverage Baseline

*Status*: **Accepted**

## Context

We want to stop coverage from silently eroding as agents add code.

## Decision

Use **`pytest-cov`** to generate coverage XML; fail the session if total
coverage drops below the rolling average (`--cov-fail-under=$(cat .cov_target)`).
`.cov_target` is bumped only by an explicit PR.

## Alternatives Considered

* Hard-code 90 % threshold – brittle when test mix changes.
* Skip coverage – saves minutes, but lets dead code grow.

## Consequences

* Clear, adjustable target; agents can read file to know goal.
* Adds \~5–10 s to test run on current codebase.

---

# 0013 – Coverage Comment Bot

*Status*: **Accepted**

## Context

Private repos make external SaaS (Codecov) paid. We still want inline feedback.

## Decision

Use the **`python-coverage-comment` GitHub Action**. On PRs it:

1. Parses `.coverage` file.
2. Posts (or updates) a summary comment.
3. Uploads SVG badge to a `coverage-badge` branch.

## Alternatives Considered

* Codecov (paid) – nice UI, but outside budget.
* Bare artifacts – no inline diff; low visibility.

## Consequences

* Maintainers see coverage delta at a glance.
* One extra job (<30 s) in workflow.

---

# 0014 – Performance Regression Guard

*Status*: **Accepted**

## Context

Speed matters for agent inner loops. We need a tripwire for accidental slow-downs.

## Decision

Add `pytest-benchmark`. A Nox session runs benchmarks; results are compared to
the committed JSON baseline. Fail if any metric regresses >10 %.

## Alternatives Considered

| Option         | Pros            | Cons                          |
| -------------- | --------------- | ----------------------------- |
| asv (airspeed) | Rich dashboards | Heavy setup, uploads required |
| No guard       | Zero effort     | Latency creeps unnoticed      |

## Consequences

* Small JSON file under `benchmarks/`.
* Contributors update baseline only with intentional perf changes.

---

# 0015 – Ruff Lint + Format

*Status*: **Accepted**

## Context

Flake8 + Black + isort run in \~10 s locally; Ruff does all in \~200 ms.

## Decision

Adopt **Ruff** with `pyproject.toml`:

```toml
[tool.ruff]
select = ["E", "F", "UP", "I"]
line-length = 120
format = "ruff"
```

`UP` enables Pyupgrade rules.

## Alternatives Considered

* Keep existing trio – familiar but slower.
* `pylint` – thorough, but heavy and chatty.

## Consequences

* Faster feedback; single dependency.
* Some niche Flake8 plugins not yet ported (acceptable).

---

# 0016 – Ruff Pyupgrade Rules

*Status*: **Accepted**

## Context

We want modern syntax without a separate tool.

## Decision

Enable Ruff’s `UP` ruleset and auto-fix in pre-commit (`ruff check --fix`).

## Alternatives Considered

* Stand-alone `pyupgrade` hook – another install step.
* Manual refactors – error-prone.

## Consequences

* New code converges on current Python best practices automatically.

---

# 0017 – Bandit Security Scan

*Status*: **Accepted**

## Context

Static analysis for Python-specific security issues (e.g., `subprocess` misuse).

## Decision

Run **Bandit** as a Nox session on `src/**.py`, exclude tests.

## Alternatives Considered

* Skip – rely on CodeQL only; misses Python heuristics.
* Snyk CLI – paid for private repos.

## Consequences

* One more line of defence, \~2 s runtime.
* Occasional false positives; handled via `# nosec` with comment.

---

# 0018 – pip-audit Scan

*Status*: **Accepted**

## Context

Lockfile needs CVE scanning; Safety is slower and paid for GitHub integration.

## Decision

Add **pip-audit** run inside Nox, pointed at `uv.lock`. Fail on high-severity
unpatched CVEs.

## Alternatives Considered

* Safety – requires token for full DB.
* OSV-scanner – language-agnostic, but pip support still maturing.

## Consequences

* Early warning on vulnerable transitive deps.
* False positives possible until fix metadata propagates.

---

# 0019 – GitHub Label Strategy

*Status*: **Accepted**

## Context

Labels power automation: changelog categorisation, risk heat-maps, auto-routing.

## Decision

* Use GitHub Labeler Action to sync labels from `labels.yml`.
* Categories: `risk:high/med/low`, `type:feature/bug/docs`, `area:agent/core/docs`.

## Alternatives Considered

* Manual label curation – drifts over time.
* ZenHub or Jira fields – heavier process.

## Consequences

* Consistent labels for bots and humans.
* Contributors add new labels via PR to `labels.yml`.

---

# 0020 – Baseline GitHub Actions

*Status*: **Accepted**

## Context

Need a skeleton workflow before adding specialised jobs.

## Decision

Create `.github/workflows/ci.yml` with stages:

1. Checkout, setup Python + `uv`.
2. Call Nox `lint`, `tests`, `security`, `docs`.
3. Upload coverage artifact.

## Alternatives Considered

* Separate workflow per job – slower, duplicate setup.
* Local runner – faster but infrastructure overhead.

## Consequences

* Single cache warm-up, faster overall.
* Easy to extend: later jobs append new Nox sessions.

---

*(Next batch will cover ADR 0021 → 0030.)*

Below are **ADR 0021 → ADR 0030** with expanded details.

---

# 0021 – CodeQL Analysis

*Status*: **Accepted**

## Context

Static analysis tools like Bandit catch common patterns, but we need deeper
taint-flow checks that follow data across functions, files, and third-party
calls. GitHub’s CodeQL provides that depth and runs free on public or private
repos.

## Decision

Enable the default **GitHub CodeQL workflow** for Python and
JavaScript (future front-end). Scan on every push to `main` and on pull
requests. Upload SARIF results for in-UI triage.

## Alternatives Considered

| Option            | Pros            | Cons                    |
| ----------------- | --------------- | ----------------------- |
| Semgrep OSS rules | Fast, low setup | Shallower flow analysis |
| LGTM (legacy)     | Historical      | Superseded by CodeQL    |
| Paid SAST (Snyk)  | Rich UI         | Budget impact           |

## Consequences

* One more security gate; runtime < 2 min on current code.
* False positives triaged via CodeQL dashboard and `codeql-yml` suppressions.

---

# 0022 – Trivy SBOM & Image Scan

*Status*: **Accepted**

## Context

Container images must be scanned for OS-level CVEs and accompanied by a
Software Bill of Materials (SBOM) for supply-chain audits.

## Decision

Add **Trivy** GH Action step:

```
trivy image --severity HIGH,CRITICAL --exit-code 1 $IMAGE
trivy image --format cyclonedx --output sbom.xml $IMAGE
```

Results are uploaded as artifacts; CI fails on unpatched High/Critical CVEs.

## Alternatives Considered

\| Option | Pros | Cons |
\| Anchore Grype | Good SBOM | Heavier image, slower |
\| Dockle + Clair | Granular checks | Multiple tools to maintain |

## Consequences

* Provides CycloneDX SBOM for downstream consumers.
* Adds ≈ 30 s to container workflow.

---

# 0023 – Gitleaks Secret Scan

*Status*: **Accepted**

## Context

Accidentally committed credentials are costly to rotate. We want detection both
locally and in CI.

## Decision

* Local: pre-commit hook `gitleaks detect --staged`.
* CI: `gitleaks/gitleaks-action@v2` on each PR; fail job on secret match.
* Custom allow-list `.gitleaks.toml` for test fixtures.

## Alternatives Considered

\| Option | Pros | Cons |
\| GH Push Protection | Built-in | Only after push; no local check |
\| TruffleHog OSS | Broad regex | Higher false-positive rate |

## Consequences

* Stops secrets before they hit `main`.
* Occasional tuning of regex allow-list required.

---

# 0024 – License Compliance

*Status*: **Accepted**

## Context

Some licences (e.g., GPL-3.0) conflict with planned distribution models.
Compliance must be automated.

## Decision

Run `pip-licenses --format=json` in Nox; compare IDs against
`licenses_allowlist.txt` (SPDX identifiers). Fail CI if new package is not
approved. Manual review + ADR required to add an exception.

## Alternatives Considered

* FOSSA SaaS – rich UI, paid tier needed.
* Manual spreadsheet – error-prone.

## Consequences

* Early alert on incompatible licences.
* Requires periodic update of allow-list as SPDX adds new IDs.

---

# 0025 – Commitizen Conventional Commits

*Status*: **Accepted**

## Context

Consistent commit messages enable automated changelogs, semantic versioning, and
easier blame. Asking agents to memorise a regex is fragile.

## Decision

Install **Commitizen** (`cz`). Developers run `cz commit`; agents are scripted
similarly. Enforce message lint in pre-commit (`commitizen check --allow-empty`).

## Alternatives Considered

\| Option | Pros | Cons |
\| commitlint + Husky | Popular in JS | Node dependency |
\| Conventional-Changelog CLIs | OK | No interactive wizard |

## Consequences

* Uniform messages, lower friction via wizard prompts.
* Occasionally agents need prompt engineering to answer wizard questions.

---

# 0026 – Semantic-release

*Status*: **Accepted**

## Context

Manual version bumps and CHANGELOG edits are error-prone. With Conventional
Commits we can derive both automatically.

## Decision

Use **python-semantic-release** in CI:

* Analyse commits since last tag.
* Decide version bump (major/minor/patch).
* Tag, push, and write `CHANGELOG.md`.

## Alternatives Considered

\| Option | Pros | Cons |
\| Standard-Version (JS) | Mature | Node runtime |
\| Manual bump | Simple | Human toil, skipped steps |

## Consequences

* Releases reflect actual change scope.
* Requires commit history to stay linear (no squash of multiple types).

---

# 0027 – Renovate Dependency Updates

*Status*: **Accepted**

## Context

Dependency drift is inevitable; batching updates reduces noise.

## Decision

Add Renovate GitHub app with config:

* Group deps by ecosystem and stability.
* Weekly “maintenance” PRs.
* Autoclose PR if tests fail.

## Alternatives Considered

\| Option | Pros | Cons |
\| Dependabot | Built-in, simpler | Limited grouping |
\| Update manually | Full control | Time-consuming |

## Consequences

* Predictable upgrade cadence.
* Occasional rebase conflicts; mitigated by weekly schedule.

---

# 0028 – Sphinx + MyST + Furo Docs

*Status*: **Accepted**

## Context

We want a documentation site that accepts Markdown, supports API auto-docs, and
can publish to GitHub Pages.

## Decision

* **Sphinx** as engine.
* **MyST** for GitHub-flavoured Markdown.
* **Furo** for accessible dark/light theme.

`docs/Makefile html` or `just docs` builds site; a GitHub Pages workflow deploys
on `main`.

## Alternatives Considered

\| Option | Pros | Cons |
\| MkDocs Material | Beautiful | Autodoc via plugins, less mature |
\| Docusaurus | React, MDX | Node build, heavier |

## Consequences

* Authors write Markdown in the repo they already use.
* Adds \~20 s build step; acceptable.

---

# 0029 – Autodoc + Napoleon

*Status*: **Accepted**

## Context

API reference should generate from docstrings—once—without duplicate typing.

## Decision

Enable Sphinx extensions:

```
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
]
napoleon_google_docstring = True
```

Napoleon parses Google/NumPy style strings; autosummary stubs are generated
during `make html`.

## Alternatives Considered

* pdoc | Simple CLI | Limited cross-linking
* MkDocs-gen-docs | Works | Same Node concern as above

## Consequences

* Accurate, versioned API docs; docstring drift spotted in PR diff.

---

# 0030 – sphinx-click CLI Docs

*Status*: **Accepted**

## Context

Our Typer CLI should appear in docs without hand-written tables.

## Decision

Add **`sphinx-click`**. In `docs/cli.md`:

````
```{autocli} app.cli:app
:prog: mycli
````

```

Build renders commands, options, env-vars.

## Alternatives Considered  
* Manually copy `--help` output – stale quickly.  
* Typer’s built-in doc generator – creates extra files, harder integration.

## Consequences  
* CLI docs update automatically when code changes.  
* Requires `sphinx-click` extension import; negligible cost.

---

```
*(Next batch will cover ADR 0031 → 0041.)*

Below are **ADR 0031 → ADR 0041** with fuller context, decisions, alternatives, and consequences.

---

# 0031 – Mermaid Docker Pipeline

*Status*: **Accepted**

## Context

Architecture diagrams help onboard humans and agents, but Node-based builds add weight. `sphinxcontrib-mermaid` is unmaintained, and local Node installs vary.

## Decision

Use **Mermaid CLI** in an official Docker image:

```
docker run --rm -v diagrams/:/data ghcr.io/mermaid-js/mermaid-cli/mermaid-cli -i diagram.mmd
```

* `docs/diagrams/*.mmd` source.
* Rendered SVGs committed under `docs/diagrams/rendered/`.
* Nox session `docs-diagrams` updates images; CI fails if SVGs drift.

## Alternatives Considered

| Option                | Pros         | Cons                            |
| --------------------- | ------------ | ------------------------------- |
| sphinxcontrib-mermaid | Inline build | Unmaintained, Node dep          |
| PlantUML + Java       | Mature       | Requires Java, different syntax |

## Consequences

* No local Node install; runs identically in CI.
* Contributors need Docker; acceptable given dev-container.

---

# 0032 – Docker + K8s Image

*Status*: **Accepted**

## Context

Prod deploy will run in Kubernetes. Image size and provenance matter.

## Decision

* Base: `gcr.io/distroless/python3-debian12`
* Build multi-stage: wheels → distroless.
* Sign image with **cosign**; generate CycloneDX SBOM via Trivy.
* Tag scheme: `ghcr.io/org/app:${SEMVER}`

## Alternatives Considered

\| Option | Pros | Cons |
\| Alpine Python | Small | Segfault risk with glibc wheels |
\| Full Debian | Familiar | 3× size |
\| Kaniko build | Rootless | Needs extra infra |

## Consequences

* 70 MB image, verifiable signature, SBOM attached.
* Slight complexity in Dockerfile; hidden by `just image`.

---

# 0033 – Tilt Dev Loop

*Status*: **Accepted**

## Context

Waiting 20 s for `kubectl apply` kills feedback loops. We want < 2 s local sync.

## Decision

Introduce **Tilt** with `Tiltfile`:

```python
k8s_yaml('manifests/')
docker_build('app', '.', live_update=[sync('.', '/app'), run('bootstrap.sh')])
```

Auto-reload when Python files change.

## Alternatives Considered

\| Option | Pros | Cons |
\| Skaffold | Google-backed | Slower live sync (\~5 s) |
\| Telepresence | Full remote | Network complexity |

## Consequences

* Devs run `tilt up`; browser dashboard shows live logs.
* Requires Docker Desktop or Colima.

---

# 0034 – `AGENTS.md` Registry

*Status*: **Accepted**

## Context

Agents need a single discoverable list of available tools, their arguments, and owners.

## Decision

Plain-text Markdown table:

| Tool | Input Schema | Output Schema | Owner | Description |
| ---- | ------------ | ------------- | ----- | ----------- |

Updated by PR; generator script (`just agents`) inserts new rows.

## Alternatives Considered

\| YAML file | Easy parse | Less readable in GitHub preview |
\| Database | Queryable | Over-engineered for now |

## Consequences

* Humans skim; agents parse via Markdown AST.
* Diff reviews reveal contract changes.

---

# 0035 – Cookiecutter Agent Template

*Status*: **Accepted**

## Context

Creating a new agent should be deterministic: code, schema, tests, docs.

## Decision

Cookiecutter in `templates/agent/` with prompts:

```
agent_name: Weather
slug: weather
description: Returns forecast
```

Generates:

```
src/agents/weather/__init__.py
src/agents/weather/schema.py
tests/agents/test_weather.py
docs/agents/weather.md
```

## Alternatives Considered

\| Copier | Simple | Less widespread |
\| Manual copy | Zero deps | Drifts quickly |

## Consequences

* One-command scaffold via `just new-agent`.
* Template maintenance overhead when base patterns evolve.

---

# 0036 – LangGraph Backbone

*Status*: **Accepted**

## Context

We need a structured orchestration layer that handles tool calls, retries,
and memory more transparently than raw prompt templates.

## Decision

Adopt **LangGraph** (StructuredTool + graph composition). Each registered tool
from `AGENTS.md` becomes a node; edges handle success/failure branches.

## Alternatives Considered

\| Option | Pros | Cons |
\| LangChain Agents | Popular | Less deterministic planning |
\| Home-grown loop | Full control | Reinvents planner, retries |

## Consequences

* Easier reasoning about agent plans; visible graph.
* Dependency on a still-young library; mitigated by ADR and swap path.

---

# 0037 – JSON-Schema Export

*Status*: **Accepted**

## Context

Tools declare input/output via Pydantic models; schemas needed for OpenAI function calling, docs, and tests.

## Decision

Each tool’s `schema.py` calls:

```python
model.schema_json(indent=2)
```

Outputs saved under `schemas/{slug}.json`. A Nox session verifies schemas diff.

## Alternatives Considered

* Runtime generation only | Fewer files | Hard to review in PR |
* Avro / Protobuf | Faster | Adds compiler, no human JSON

## Consequences

* Schemas provide contract diff surface.
* Adds small repo footprint (≈ 2 KB per tool).

---

# 0038 – Schemathesis Contract Fuzz

*Status*: **Accepted**

## Context

When we add an HTTP API, we want blind spots found before staging.

## Decision

Write an OpenAPI stub even for early endpoints; run **Schemathesis** in CI:

```
schemathesis --workers 4 run openapi.yaml
```

Uses Hypothesis strategies to fuzz parameters and headers.

## Alternatives Considered

\| Postman/Newman | Visual | No property-based fuzz |
\| Dredd | Lightweight | Limited payload variation |

## Consequences

* Early API breakage caught automatically.
* Test suite runtime +30 s; acceptable for PRs.

---

# 0039 – JSON-Schema Contract Tests

*Status*: **Accepted**

## Context

Internal message passing (e.g., agent → tool) needs validation too.

## Decision

Combine `jsonschema` with Hypothesis’ `from_schema` to generate arbitrary valid payloads; assert round-trip.

## Alternatives Considered

* Manual asserts | Simple | Coverage gaps |
* Pydantic `validate` only | Runtime | No fuzz coverage

## Consequences

* Tighter message guarantees; reproduces edge cases for free.
* Adds ≈ 3 s to test suite.

---

# 0040 – Hypothesis GraphQL Fuzz

*Status*: **Accepted**

## Context

GraphQL schema and resolvers diverge easily.

## Decision

Use **hypothesis-graphql** session to generate random queries against live schema; fail on resolver errors or mismatched types.

## Alternatives Considered

\| Option | Pros | Cons |
\| Manual introspection tests | Quick | Sparse coverage |
\| Apollo Fuzz | JS, good | Separate runtime stack |

## Consequences

* Finds SDL/runtime mismatches early.
* Requires running API in test mode; handled by Nox.

---

# 0041 – Single-Schema Bridge (Pydantic ↔ Strawberry)

*Status*: **Accepted**

## Context

We already model data in Pydantic; duplicating GraphQL types invites drift.

## Decision

Use **`strawberry.experimental.pydantic`** to auto-derive GraphQL types:

```python
@strawberry.experimental.pydantic.type(model=UserModel)
class User:
    pass
```

Schema builds directly from Pydantic, ensuring parity.

## Alternatives Considered

\| Hand-written Strawberry types | Full control | Drift risk, boilerplate |
\| datamodel-codegen | Generates code | Adds generation step |

## Consequences

* One source for REST, GraphQL, and OpenAI contracts.
* Experimental API may change; tracked via ADR.

---

