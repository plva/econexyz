------------------------
status: open
category: workflow
tags:

- workflow

- meta

- devops

- testing

created: 2025-06-19
last-updated: 2025-06-19
priority: medium
assigned: unassigned
------------------------
# workflow/run_all_tests_script

# Create Comprehensive Test Runner Script

## Summary

Create a unified test runner script that executes all project tests including Python unit tests and the commit-msg hook validation tests.

## Steps to Reproduce / Implementation Plan

### Option A: Shell Script (`run_all_tests.sh`)
1. Create `scripts/run_all_tests.sh` with:
   - Python test execution (pytest or unittest)
   - Commit hook test execution (`python scripts/test_commit_hook.py`)
   - Clear output formatting and error reporting
   - Exit code handling for CI integration

### Option B: Makefile Target
1. Add test target to `Makefile`:
   ```makefile
   test:
       pytest
       python scripts/test_commit_hook.py
   ```

### Option C: Both (Recommended)
1. Create both `run_all_tests.sh` and `Makefile` for flexibility
2. Update documentation to mention both options
3. Add to CI pipeline configuration

## Implementation Details

### Shell Script Features
- Clear section headers for each test type
- Proper exit code handling (fail fast on first error)
- Color-coded output (green for pass, red for fail)
- Summary report at the end
- Support for different Python test runners

### Integration Points
- Update `README.md` with test running instructions
- Add to `bootstrap.sh` as optional test verification
- Consider adding to pre-commit hooks for automated testing
- Document in development workflow guides

## Additional Context

Currently developers need to run tests separately:
- `pytest` for Python unit tests
- `python scripts/test_commit_hook.py` for commit hook validation

This creates friction and potential for missed test failures. A unified runner will:
- Improve developer experience
- Ensure all tests are run consistently
- Reduce CI failures from missed local testing
- Provide clear feedback on test status

## Acceptance Criteria
- [ ] Single command runs all tests
- [ ] Clear output showing which tests passed/failed
- [ ] Proper exit codes for CI integration
- [ ] Documentation updated with usage instructions
- [ ] Works on both Unix and Windows (if using shell script)