# econexyz

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

- `econexyz/` – core Python modules for agents, message bus, and storage.
- `dashboard/api/` – FastAPI server exposing simple monitoring endpoints.
- `dashboard/web/` – placeholder for a future React dashboard.
- `scripts/` – helper scripts to run agents and the dashboard.

## Quick Start

1. Install requirements:
   ```bash
   pip install fastapi uvicorn
   ```
2. Run the sample agent:
   ```bash
   python scripts/run_agents.py
   ```
3. Start the dashboard API:
   ```bash
   ./scripts/run_dashboard.sh
   ```

Visit `http://localhost:8000/status` to see agent status and `http://localhost:8000/messages` for recent bus messages.
