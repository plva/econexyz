# Development Process Guide

This document describes the typical development process for EcoNexyz contributors.

- Setting up your environment
- Running agents and the dashboard
- Adding new features or agents
- Using scripts for workflow
- Testing and validation 

# Bugfix Process

## Bugfix Decision Flow

When encountering a bug, follow this decision tree:

### 1. Is there already an open issue for this bug?
- **Yes** → Fix directly and reference the issue in commit message
- **No** → Continue to step 2

### 2. Is there a closed issue for this bug?
- **Yes** → Reopen the issue using the bug workflow, then fix and reference it
- **No** → Continue to step 3

### 3. Should this bug be tracked with an issue?
- **Yes** (complex bug, affects users, needs discussion) → Create new bug issue first, then fix
- **No** (trivial fix, internal cleanup, obvious error) → Fix directly with `[fix]` commit

### Bug Workflow Commands

**Create a new bug issue:**
```bash
python scripts/workflow/create_issue.py bugs <bug-name> --template bug --priority <level>
```

**Reopen a closed bug:**
```bash
python scripts/workflow/create_issue.py --reopen bugs/<bug-name> --template bug
```

For detailed bug reporting instructions, see the [Bug Reporting Guide](bug_reporting.md).

### Examples:

**Fix directly (no issue needed):**
- Typo in comment or documentation
- Missing cleanup step in script
- Linter warning fix
- Obvious syntax error

**Create bug issue first:**
- Bug that affects functionality
- Security vulnerability
- Performance issue
- User-reported problem
- Complex bug requiring discussion

**Reference existing issue:**
```bash
[fix] fix issue path resolution in create_issue.py

Fixed bug where issue paths were being created as relative instead
of absolute paths. This caused issues when creating issues from
different directories.

Closes #45
```

## Bugfix Workflow Integration

- **Trivial fixes**: Can be included in regular feature PRs or as standalone commits
- **Complex bugs**: Should be tracked as separate issues and may require dedicated PRs
- **Security bugs**: Always create issues and follow security disclosure procedures
- **Performance bugs**: Create issues to track impact and optimization efforts
- **Regression bugs**: Use the reopen functionality to track when previously fixed bugs reappear

# Cycle-Based Development Workflow

## Overview

We structure our development process around **cycles**. A cycle consists of a group of tasks that:

- Can be completed independently and in parallel.
- Correspond to approximately one day of focused work.
- Conclude with a stand-up meeting ("cycle stand-up") to synchronize changes and resolve merge conflicts.

This structure supports parallelized development efforts, enabling multiple contributors (human or AI agents) to collaborate efficiently.

## Concept: Cycle and Stand-up

**Cycle**:
- Clearly defined, independent tasks selected at the start of the day.
- Tasks can be completed concurrently by multiple agents.
- Each task results in a **Pull Request (PR)** submitted by an agent.

**Cycle Stand-up**:
- Occurs at the end of each cycle.
- Reviews completed PRs.
- Resolves merge conflicts collectively at once.
- Updates planning and tracking documents (e.g., TODO.md, sprint files).

## Directory & Git Structure

Maintain a consistent and structured Git branch and directory organization:

```
sprints/
├── current/
│ ├── TODO.md
│ └── sprint-meta.md
└── archived/
└── sprint-001/
├── TODO.md (snapshot)
├── sprint-meta.md
└── issues/
├── open/ (scope reduced or deferred tasks)
└── closed/ (completed tasks)
```
- **Current sprint** tracks active work in `sprints/current/`.
- The completed sprint moves to `sprints/archived/` after the sprint ends.
- Tasks left incomplete or scoped down remain clearly identified.
## Best Practices for Task Isolation
To avoid merge conflicts during a cycle:

- Ensure each task is clearly scoped and isolated.
- Tasks touching the same files/modules should be coordinated explicitly or scheduled in separate cycles.
- Adhere strictly to small, manageable pull requests per task.
- This may imply needing to first restructure tasks (issues) and the current sprint
    - We can split an issue up into multiple issues
    - We can clearly outline multiple steps that should be completed for an issue (implying multiple PRs)
    - We can defer an issue to a future sprint, or reduce the scope
    - This means we have a blocker for the cycle, and must wait for the cycle stand-up to resolve the blocker
        - We no-op with PRs in retro, but track this offline by writing our agent name and what happend in an append-only log
        - Currently the append-only log is managed by a person offline (paul)

## Recommended Git Branching for Cycles

- Each agent creates task branches from `main` at cycle start:
```
main
├─ cycle-20250620-agentA-task1
└─ cycle-20250620-agentB-task2
```
- Branches named clearly by date, agent, and task.
- Agents submit Pull Requests against the `main` branch.
- During the stand-up, maintainers merge all PRs and resolve conflicts explicitly.
    - Ideally there should be no conflicts, as all the conflicts are done in one PR 
    - Completed issues are marked as done in the same documents (sprint/todo md) at the same time
    - If there was a merge conflict this implies lack of foresight in planning parallel tasks during a cycle
        - This will be brought up in the sprint retro and a task created to amend the workflow process to prevent future conflicts
        - When enough conflict-pressure accumulates, a process sprint is inserted before the next sprint
            - The process sprint uses a letter schema after the previous sprint number
                - (e.g. 3a, 3.2b, 3.1c, etc) for now, but a better scheme can be designed and backported later
            - Since sprints are lightweight and are not bound by calendar time, there is limited cost to adding an extra one
            - The benefits are clarity and clearly bounded task organization
**During the Cycle**:
- Agents independently create feature branches and work on tasks.
- Agents submit clearly-scoped PRs to the main branch.

**Cycle Stand-up (End of Cycle)**:
- Review and merge all completed PRs.
- Update `TODO.md` to mark tasks complete and adjust any scope changes.
- Resolve conflicts and integration issues in one step.

## Trade-offs and Considerations

| Benefit                              | Trade-off                           |
|--------------------------------------|-------------------------------------|
| Efficient parallelization of work.   | Requires careful task scoping.      |
| Reduced continuous merge conflicts.  | Conflicts concentrated at stand-up. |
| Clear cycle-level accountability.    | Need for disciplined PR practices.  |

## Instructions for AI Agents

AI agents should follow these practices:

- **Branching**: Create a clearly-named branch per task:  
`git checkout -b cycle-<date>-<agent>-<task>`
- **Atomic commits**: Each PR should clearly address one task.
    - It is better to create a new independent PR for an unrelated task rather than grouping it in
- **Submit PRs Early**: Open PR as soon as ready to integrate at stand-up.
- **Update Documents**: Always reflect task completion clearly in related issue documentation (i.e. the metadata at the top of an issue).
    - Leave the todo.md and sprint updates to be done in the cycle stand-up
    - In future, we will be adding an agent journal directory where agents can provide updates and keep track of their work independently of each other

## Example Agent PR Branching and Submission

```bash
git checkout main
git checkout -b cycle-20250620-AgentX-logging-enhancement

# perform changes...
git commit -am "Improve logging robustness"
git push origin cycle-20250620-AgentX-logging-enhancement
```
- Open PR clearly labeled: [Cycle 2025-06-20][AgentX] Logging Enhancement
- PR should clearly describe the task, changes, and reference any issues it closes.