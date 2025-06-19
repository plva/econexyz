---
status: open
category: workflow
tags:
  - devops
  - workflow
created: 2025-06-19
last-updated: 2025-06-19
priority: medium
assigned: unassigned
------------------------

# workflow/run_tests_on_pr

Set up automation that runs unit tests when a pull request is opened. Failures
should be reported but do not necessarily block merging.

- Integrate with CI (e.g., GitHub Actions) to run `pytest -q`.
- Post results back to the PR for visibility.
- Allow maintainers to override failures when appropriate.
