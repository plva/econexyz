---
status: open
category: issues 
tags:
  - devops 
  - meta
  - workflow 
created: 2025-06-18
priority: high
assigned: "plva + codex"
------------------------

# Issue: Implement Issue Tracking Workflow

## Overview

We currently track issues and tasks as markdown files (`.md`) organized into category directories. The directory structure clearly separates open and closed issues, making the system easy to manage, navigate, and parse (including by automated agents).

## Recommended Directory Structure

Maintain a mirrored category structure inside `open` and `closed` directories:

```
issues/
├── open/
│   ├── devops/
│   │   ├── fix-deploy-script.md
│   │   └── setup-docker.md
│   ├── frontend/
│   │   └── add-login-page.md
│   └── agents/
│       └── weather-agent-improvements.md
└── closed/
    ├── devops/
    ├── frontend/
    └── agents/
```

## Workflow for Completing an Issue

When an agent or developer finishes working on an issue:

1. **Move Issue**: Move the issue markdown file from `open` to `closed`, preserving its category path.

   Example:

   ```bash
   mv issues/open/devops/fix-deploy-script.md issues/closed/devops/
   ```

2. **Update To-Do List**: In your main to-do markdown file (e.g., `TODO.md`), find the related entry and tick the checkbox.

   Example:

   Before:

   ```markdown
   - [ ] Fix deploy script (`devops/fix-deploy-script.md`)
   ```

   After:

   ```markdown
   - [x] Fix deploy script (`devops/fix-deploy-script.md`)
   ```

## Creating a Bash Script for Automation

To streamline this process, create a simple bash script `close_issue.sh`:

### Script Content

```bash
#!/bin/bash

CATEGORY=$1
ISSUE_NAME=$2
ISSUE_PATH="issues/open/$CATEGORY/$ISSUE_NAME.md"

if [ ! -f "$ISSUE_PATH" ]; then
  echo "Issue not found: $ISSUE_PATH"
  exit 1
fi

mkdir -p "issues/closed/$CATEGORY"
mv "$ISSUE_PATH" "issues/closed/$CATEGORY/"
echo "Moved $ISSUE_NAME.md to issues/closed/$CATEGORY/"
```

### Usage

```bash
./close_issue.sh devops fix-deploy-script
```

## Update AGENTS.md with Workflow Instructions

Add the following instructions clearly under a new section titled **Completing Tasks**:

---

### Completing Tasks

When an agent completes its coding task, follow these steps:

* Move the markdown file representing your task from `issues/open/[category]/[issue-name].md` to `issues/closed/[category]/` using the provided script:

```bash
./close_issue.sh [category] [issue-name]
```

Example:

```bash
./close_issue.sh agents weat
```
