# Viewing Workflow Diagrams

This directory contains mermaid diagrams describing how issues,
sprints, and meta-sprints are managed in the repository.

## Available Workflows

- `issue_workflow.md` - How issues are created, managed, and closed
- `sprint_workflow.md` - How sprints are planned and executed
- `meta_sprint_workflow.md` - How meta-sprints coordinate multiple sprints
- `standup_workflow.md` - How cycle standups synchronize project state

## Quick Start

Install Node.js so that the `npx` command is available. Then run
`/scripts/list_workflow_diagrams.sh` from the repository root. The
script uses the Mermaid CLI to render each workflow diagram as an SVG
under `/docs/workflows/rendered/` and prints a `file://` URL for each
generated image. Open those links in your browser to view the charts.
