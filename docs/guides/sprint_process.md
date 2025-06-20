# Sprint & Meta-Sprint Process

This guide explains how to plan, run, and close sprints and meta-sprints in EcoNexyz.

- Sprint planning
- Running a sprint
- Sprint retrospectives
- Meta-sprint overview
- Using scripts for sprint management
- Linking to workflow diagrams

## Cycle Stand-Up

Use a cycle stand-up to sync the repository's planning files with
recent work. 

### Automated Standup (Recommended)

The enhanced standup script automates most of the process:

```bash
# Run all enhanced standup features
python scripts/run_standup.py --all

# Or run individual features as needed
python scripts/run_standup.py --dry-run --generate-commit
```

This script will:
1. **Review commits** since the last stand-up to identify completed issues
2. **Create work delta summary** of completed work
3. **Check documentation** for new features
4. **Review blockers and dependencies**
5. **Perform health checks** including running tests
6. **Generate commit message** for the standup

For detailed usage examples and options, see [`docs/workflows/standup_workflow.md`](docs/workflows/standup_workflow.md).

### Manual Standup Process

If you prefer to run the standup manually, follow these steps:

1. **Review commits** since the last stand-up to identify completed
   issues.
2. **Run the test suite** with `pytest -q` to ensure new changes
   pass.
3. **Close finished issues** using `./scripts/close_issue.sh <category>
   <issue-name>`.
4. **Update planning files**:
   - Mark the issue as completed in `/TODO.md`.
   - Update the current sprint's `sprint-meta.md` entry.
5. **Document usage** of any new scripts or features in the
   appropriate README or guide.

Only during a cycle stand-up should `/TODO.md` or sprint metadata be
edited. This prevents merge conflicts when multiple PRs are in flight.
