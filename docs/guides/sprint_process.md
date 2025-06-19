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
recent work. The typical steps are:

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
