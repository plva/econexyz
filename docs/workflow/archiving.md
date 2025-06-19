# Sprint Archiving

Use `./scripts/archive_sprint.sh <sprint-name>` to archive the current sprint.
The script moves all referenced issues into `sprints/archived/` and takes a
snapshot of `TODO.md`.

Completed tasks belonging to the sprint are removed from the top level `TODO.md`
as part of the archive process. Open tasks remain so they can be carried into the
next sprint or backlog.

Example:

```bash
./scripts/archive_sprint.sh sprint-3 --new sprint-4
```

This archives `sprint-3` and creates an empty `sprint-4` directory under
`sprints/open/`.
