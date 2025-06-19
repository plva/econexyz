---
status: open
category: issues 
tags:
  - devops 
  - meta
  - workflow 
created: 2025-06-19
last-updated: 2025-06-19
priority: high
assigned: "plva + codex"
------------------------
# workflow/manually-update-issue-metadata

All issues should have the proper issue metadata at the top

## definition of done
All issues in the `issues/{closed, open}/*`, `sprints/**/{archived, open}/*/issues/{closed,open}/*` directories should have the metadata section at the top.

It looks like:

```
---
status: open
category: issues 
tags:
  - devops 
  - meta
  - workflow 
created: 2025-06-19
last-updated: 2025-06-19
priority: high
assigned: "plva + codex"
------------------------
```
[keep in mind that paul is the human maintainer/coordinator, and his github alias is plva]

But:
- the status should reflect the status
- the category should reflect the issues category (we can use directory structure to determine it)
- tags should reflect any relations that the issue may share with other issues outside of its category (read the issue text and reason about it)
- create is typically based off of the creation timestamp of the file (but we can use offline reasoning if we have additional information)
- last-updated is when the issue was last touched
- priority is an educated guess about how important the issue is for bootstrapping further development.
    - If it clearly unblocks or outlines development workflows and task parallelizability for agents + paul(person), it is high
    - if it helps paul be more productive, it is medium
    - if it is a nice to have for later collaboration with other persons, it is low
- assigned will be based off of choosing the best agent from a list of agents (that will be tracked in a separate directory)
    - if that directory is created, we can assign it to the best guess from that list
    - for now though, most tasks should be assigned to "plva + codex"