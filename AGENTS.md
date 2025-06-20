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

## Commit Message Standards

All contributors must use the commit message template system and git commit-msg hook for validation. This ensures consistency and quality across all commits.

### Using the Commit Message Script

**For AI agents and contributors, always use the commit message script:**

```bash
# 1. Create a template for your commit type
python scripts/commit_message.py --template <type>

# 2. Edit the generated template file (in /tmp/commit_template_<type>.md)
# Add your description and details

# 3. Stage your changes
git add <files>

# 4. Commit using the template
git commit -F /tmp/commit_template_<type>.md
```

**Available commit types:**
- `fix` - Fixes a bug
- `feature` - Adds a new feature
- `workflow` - Changes to AI-agent workflows, agent instructions, or documentation that directly affect agent behaviors
- `issue` - Adds a new issue file to the repo
- `refactor` - Pure code cleanup without behavior change
- `perf` - Performance enhancements
- `deps` - Dependency updates
- `agents` - Changes to agent system
- `dashboard` - Changes to dashboard or UI
- `bus` - Changes to message bus system
- `cross` - Cross-cutting changes (tests, CI, etc.)
- `standup` - Cycle stand-up updates (TODO.md, sprint meta)
- `sprint` - Sprint planning activities
- `temp` - Temporary commits for testing

**Example workflow:**
```bash
# For a bug fix
python scripts/commit_message.py --template fix
# Edit /tmp/commit_template_fix.md with your description
git add scripts/my_script.py
git commit -F /tmp/commit_template_fix.md

# For a new feature
python scripts/commit_message.py --template feature
# Edit /tmp/commit_template_feature.md with your description
git add new_feature.py
git commit -F /tmp/commit_template_feature.md
```

**Note:** The script automatically cleans up temp template files after use.

### Validation

The git commit-msg hook validates:
- Header length (max 50 chars)
- Valid commit type format
- Body line length (max 72 chars)
- Proper commit type from our defined list

If validation fails, the commit will be rejected with helpful error messages.

### Documentation

- See `docs/guides/commit_messages.md` for full guidelines and usage examples.
- Git hooks are installed automatically via `./bootstrap.sh` or manually with `./scripts/setup_hooks.sh`.

---

## 📌 Example Agent

For practical references, review [`agents/sample.py`](/econexyz/agents/sample.py) and [`agents/weather.py`](/econexyz/agents/weather.py).

---

## 📌 Completing Tasks

When you finish a task, move its issue file from `issues/open/[category]/[issue-name].md` to `issues/closed/[category]/` using:

```bash
./scripts/close_issue.sh [category] [issue-name]
```

Then update `TODO.md` to mark it complete.

---

## 📌 Sprint Workflow

Sprint plans are stored in `sprints/open/` as directories. Upcoming sprints can
be queued in `sprints/upcoming/`, and the current sprint number is kept in
`state/sprint.json`. When a sprint ends, archive its directory with:

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

Additional project-wide tasks are tracked in [/TODO.md](/TODO.md).

## Creating Issues

To create a new issue and update the TODO lists, use:

```bash
python scripts/create_issue.py <category> <issue-name>
```

This automates issue file creation and ensures all tracking files are updated.

## Soft Lock Workflow

The project uses **soft locks** to avoid collisions on important files.
Each lock is a small YAML file describing who currently intends to edit a
particular resource.

Create a lock with:
```bash
./scripts/create_lock.sh <lock-name> <file-path> "<reason>"
```
The resulting file contains four fields:

```yaml
user: <git user.name>
timestamp: <UTC timestamp>
reason: <why the file is locked>
file: <path to the file>
```

Locks are stored in `locks/` and should only be committed when necessary. Check
existing locks before making large edits and remove outdated ones when the work
is finished. The only default lock protects `TODO.md` so that sprint planning
changes remain orderly.

A pre-commit hook installed with `scripts/setup_hooks.sh` checks your staged
files against the active locks. If you modify a file locked by someone else,
the hook prints a warning but allows the commit to proceed.

## Agent Logs and PR Documentation

When preparing a pull request, agents should document each step of their process in a file named `agent.<datetime string>.log.md` in the `/agent-logs` directory. For each step:

- Record what was done in the log file as the work progresses.
- After completing the steps, add a high-level overview of the work (avoid repeating details that can be inferred from the PR itself).

This practice ensures transparency and provides a clear audit trail of agent-driven contributions.

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

> **Important:** Do not update `/TODO.md` or sprint meta files during a normal task PR. These files should only be updated during a dedicated cycle stand-up PR to avoid merge conflicts. See [docs/guides/sprint_process.md](docs/guides/sprint_process.md#cycle-stand-up) for the full procedure.

## Bugfix Process

When encountering bugs, follow the **Bugfix Decision Flow** in `docs/guides/development.md`:

1. **Check for existing issues** - Look for open or closed issues first
2. **Assess complexity** - Trivial fixes can be done directly, complex bugs need issues
3. **Create issues when needed** - For user-affecting, security, or complex bugs
4. **Reference issues in commits** - Always link commits to relevant issues

See `docs/guides/development.md#bugfix-process` for the complete decision tree and examples.
