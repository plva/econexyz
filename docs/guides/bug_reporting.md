# Bug Reporting Guide

This guide explains how to report and track bugs in the EcoNexyz workflow.

## Reporting a New Bug

1. Run `python scripts/create_issue.py bugs <issue-name> --template bug --priority high`.
2. Fill out the generated file under `issues/open/bugs/` using the bug template.
3. Commit the new issue and open a pull request describing the problem.

## Reopening a Closed Bug

If a previously closed issue resurfaces:

```bash
python scripts/create_issue.py --reopen bugs/<issue-name>
```

The script moves the closed issue back to `issues/open/` and updates planning files.

## Priority Levels

Bugs can be marked with `critical`, `high`, `medium`, or `low` priority using the `--priority` flag.

## Regression Tracking

When reopening issues, note in the description that it is a regression so it can be tracked separately.
