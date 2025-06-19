# 🦾 EcoNexyz: Agent Development Guide (`AGENTS.md`)

This document provides guidelines, conventions, and examples for creating, registering, and managing AI agents in **EcoNexyz**.

---

## 📌 What is an Agent?

An **EcoNexyz Agent** is an autonomous unit of logic designed to perform specific tasks, communicate via the message bus, and interact with shared storage or knowledge repositories.

Agents should:

- Be self-contained Python classes derived from the `Agent` base class.
- Follow a clear lifecycle: initialization (`setup`), operational (`run` loop), and cleanup (`shutdown`).

---

## 📌 Agent Lifecycle Methods

Your agent class should implement these methods:

```python
class YourAgent(Agent):

    def setup(self):
        """
        Initialize resources, establish message bus subscriptions, and perform any startup tasks.
        """
        pass

    def run(self):
        """
        Core autonomous logic loop. Typically includes processing messages, performing tasks,
        and periodically publishing status updates.
        """
        pass

    def shutdown(self):
        """
        Cleanly terminate your agent, closing any connections or freeing resources.
        """
        pass
```

---

## 📌 Communication via Message Bus

Use the provided `MessageBus` abstraction for sending and receiving messages between agents:

```python
# Publishing messages
self.bus.publish(topic='status', message={'agent': 'MyAgent', 'status': 'running'})

# Subscribing to messages
def handle_message(msg):
    print(msg)

self.bus.subscribe(topic='commands', callback=handle_message)
```

Ensure message formats are consistent and documented.

---

## 📌 Persistent Storage (KnowledgeStore)

Agents can store and retrieve persistent data using the `KnowledgeStore` interface:

```python
# Saving data
self.storage.save(key='agent_state', data={'counter': 42})

# Loading data
state = self.storage.load(key='agent_state')
```

---

## 📌 Registering and Running Your Agent

Add your agent to the orchestration script (`scripts/run_agents.py`):

```python
from agents.your_agent import YourAgent

agent = YourAgent(bus=bus, storage=storage)
agent.setup()
agent.run()
```

---

## 📌 Best Practices and Guidelines

- Keep agent logic modular, testable, and independent.
- Clearly document message schemas your agent publishes and subscribes to.
- Write unit tests covering critical agent behaviors (`tests/`).

### git
- Limit the commit header to 50 characters or fewer
- Follow the header with a blank line before the commit body (if any).

- Wrap the commit body at 72 characters per line for readability.


---

## 📌 Example Agent

For practical references, review [`agents/sample.py`](econexyz/agents/sample.py) and [`agents/weather.py`](econexyz/agents/weather.py).

---

## 📌 Completing Tasks

When you finish a task, move its issue file from `issues/open/[category]/[issue-name].md` to `issues/closed/[category]/` using:

```bash
./scripts/close_issue.sh [category] [issue-name]
```

Then update `TODO.md` to mark it complete.

---

## 📌 Sprint Workflow

Sprint plans are stored in `sprints/open/` as directories. When a sprint ends,
archive its directory with:

```bash
./scripts/archive_sprint.sh <sprint-name>
```

The script creates `sprints/archived/<sprint-name>/` and moves the sprint
metadata there along with any referenced issue files. A snapshot of
`TODO.md` is also stored beside `sprint-meta.md`.

For AI tools that need structured sprint data, run:

```bash
python scripts/ai_helper.py
```

This outputs the current sprint plan as JSON.

You can also normalize sprint files with:

```bash
python scripts/ai_helper.py --fix
```


---


## 📌 Troubleshooting Common Issues

- **Message not arriving?** Verify subscriptions and topic names.
- **Unexpected crashes?** Implement exception handling within your `run()` method and log errors clearly.

---

## 🚀 Ready to create your agent?

Follow this guide, keep your implementations clean, and have fun building intelligent, autonomous behavior into the **EcoNexyz** ecosystem!

Additional project-wide tasks are tracked in [TODO.md](TODO.md).
