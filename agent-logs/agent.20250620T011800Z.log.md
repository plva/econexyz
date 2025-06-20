# Agent Log 2025-06-20

## Overview

Implemented the next step of the lockfile workflow by adding a pre-commit hook.
The hook warns when committing changes to files locked by someone else. Updated
`setup_hooks.sh` to install this hook, documented the behavior in `AGENTS.md`,
and wrote tests to verify the warning logic.
