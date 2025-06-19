# econexyz
![EcoNexyz](/img/robo_nexyz.png)
🌐 EcoNexyz: Autonomous AI-agent ecosystem seamlessly bridging tasks and knowledge

🧠 Conceptual Overview of EcoNexyz Repo
#### Main Idea:
EcoNexyz is an ecological system of autonomous AI agents that can be registered, communicate through a central message bus, store knowledge in a local/cloud-compatible repository, and visualize their activities on a dashboard—all wrapped behind minimal abstractions.

### Essential Components:

✅ Message Bus (local or cloud, e.g., Redis or NATS, mocked via in-memory queue initially).

✅ Knowledge Repository (local filesystem or cloud-compatible DB, mocked with SQLite initially).

✅ Agent Registration & Autonomy (simple Python interface for agents, lifecycle hooks).

✅ Dashboard/Visualization (minimal FastAPI backend + React/Next.js dashboard, initially simple API + minimal web front-end).

### Key Abstractions:
- `Agent`: Autonomous tasks encapsulated in Python classes with lifecycle (setup, run, shutdown).

- `MessageBus`: Pub/sub communication interface (send/receive).

- `KnowledgeStore`: Unified interface for storage/retrieval (key-value/document).

- `Dashboard` : API endpoints feeding real-time agent status.


## Repository Structure

- `econexyz/` – core Python modules for agents (including a sample and weather agent), message bus, and storage.
- `dashboard/api/` – FastAPI server exposing simple monitoring endpoints.
- `dashboard/web/` – minimal React dashboard displaying status and messages.
- `scripts/` – helper scripts to run agents and the dashboard.

## Quick Start

1. Bootstrap your environment and start the agents **and dashboard**:
   ```bash
   source bootstrap.sh
   ```
   This will create a virtual environment (if needed), install requirements, and launch the agents together with the FastAPI dashboard server.
2. Open `dashboard/web/index.html` in your browser to view agent status and messages.
   If you start the dashboard using `scripts/run_dashboard.sh` in a separate process,
   it won't display messages because the default in-memory bus isn't shared across
   processes.

Visit `http://localhost:8000/` for instructions, `http://localhost:8000/status` to see agent status and `http://localhost:8000/messages` for recent bus messages.

## bootstrap.sh: Environment Setup & Agent Runner

The `bootstrap.sh` script automates the following:
- Checks for Python 3 and required files
- Creates and activates a virtual environment (`.venv`)
- Installs all Python requirements
- Starts the agent runner script

**Usage:**
```bash
source bootstrap.sh
```

If any step fails, you'll see a clear error message. Always use `source` so your shell stays in the activated environment.

## Configuration

The repository includes a color palette definition at `config/color_palette.json`. These values are used by the dashboard for consistent styling.

Runtime logs are written to `~/tmp/econexyz.log` and are ignored by git. Agents log setup, shutdown, and message publishing events to help verify they are running correctly.

## Project TODOs

Ongoing development tasks are tracked in [/TODO.md](/TODO.md). Contributions and ideas are welcome!

## Creating Issues via Script

You can create new issue files and update TODO lists automatically using:

```bash
python scripts/create_issue.py <category> <issue-name>
```

- `<category>`: The issue category (e.g., dashboard, agents, workflow, etc.)
- `<issue-name>`: The name of the issue file (without `.md`)

This will:
- Create a new issue markdown file in `/issues/open/<category>/<issue-name>.md`
- Add a TODO entry to `/TODO.md`
- Add a reference to the current sprint's `sprint-meta.md` (if applicable)

## Sprint Workflow

Active sprints live in `sprints/open/` as directories containing `sprint-meta.md`.
Upcoming sprints can be staged in `sprints/upcoming/` and the current sprint
number is recorded in `state/sprint.json`.
When a sprint concludes, archive its directory with:

```bash
./scripts/archive_sprint.sh <sprint-name>
```

The script creates `sprints/archived/<sprint-name>/` containing the sprint
metadata, a snapshot of `TODO.md` and any referenced issue files.

To view the sprint plan in JSON form for AI tools, run:

```bash
python scripts/ai_helper.py
```

To normalize sprint files and fix minor formatting issues, pass `--fix`:

```bash
python scripts/ai_helper.py --fix
```

### Transactional Git helper

Run commands atomically using `git_transaction.sh`:

```bash
./scripts/git_transaction.sh start "My commit message"
# ...make your changes...
./scripts/git_transaction.sh finalize
```

If something goes wrong, run `./scripts/git_transaction.sh rollback`
to restore the previous state. The helper stashes any pre-existing
changes, uses a temporary branch for your edits and squashes the
result into a single commit. See `scripts/transaction_example.py` for
a Python example. Untracked files are stashed automatically;

## Documentation

Additional diagrams illustrating repository workflows live in
`docs/workflows/`. They include mermaid charts for the sprint cycle,
handling individual issues, and meta-sprint planning. See
`docs/workflows/README.md` for details on generating and viewing them.

## Agent Logs and PR Documentation

When an agent is preparing a pull request, it should document each step of its process in a file named `agent.<datetime string>.log.md` in the `/agent-logs` directory. For each step, the agent should:

- Record what was done in the log file as the work progresses.
- After completing the steps, add a high-level overview of the work (avoid repeating details that can be inferred from the PR itself).

This ensures transparency and provides a clear audit trail of agent-driven contributions.

Example log file:

```markdown
# Agent Log 2025-06-19

## Overview

Expanded the content of all open workflow issues to provide clearer guidance for future automation. Each issue now includes detailed bullets or design notes suitable for an AI or developer to implement. No issues were closed.

### Updated Issues
- `run_sprint_planning.md`
- `run_backlog_grooming.md`
...
```
