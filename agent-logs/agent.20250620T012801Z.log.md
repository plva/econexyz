# Agent Log 2025-06-20

## Overview

Implemented the unified test runner described in `workflow/run_all_tests_script`.
Added `scripts/run_all_tests.sh`, a `Makefile` test target, and updated the
`README` with usage instructions. The script runs Python tests and the commit
hook checks, returning a non-zero status if any fail.
