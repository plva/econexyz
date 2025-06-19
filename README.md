# econexyz
![EcoNexyz](img/robo_nexyz.png)
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

1. Bootstrap your environment and start the agents:
   ```bash
   source bootstrap.sh
   ```
   This will create a virtual environment (if needed), install requirements, and launch the agents.
2. Start the dashboard API and web UI:
   ```bash
   ./scripts/run_dashboard.sh
   ```
   Then open `dashboard/web/index.html` in your browser.

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

Ongoing development tasks are tracked in [TODO.md](TODO.md). Contributions and ideas are welcome!
