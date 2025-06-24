# GitHub Branch Protection Setup

This document explains how to set up GitHub branch protection rules to ensure code quality and prevent merging broken code.

## Current CI Status Check Names

After setting up the workflows in this repository, GitHub will emit these status check names:

### Required Checks (from `.github/workflows/ci.yml`)
- **tests** - Runs pytest with coverage on Python 3.11 and 3.12
- **lint** - Runs ruff for linting and format checking
- **types** - Runs ty for static type checking
- **security** - Runs bandit and pip-audit for security scanning

### Optional Checks
- **commit-style** - Validates commit message format (from `.github/workflows/commit-style.yml`)

## Setting Up Branch Protection Rules

### Step 1: Go to Repository Settings
1. Navigate to your repository on GitHub
2. Click **Settings** tab
3. In the left sidebar, click **Branches**

### Step 2: Add Branch Protection Rule
1. Click **Add rule** or **Add branch protection rule**
2. In **Branch name pattern**, enter: `main`
3. Check the following options:

#### Required Status Checks
- ✅ **Require status checks to pass before merging**
- ✅ **Require branches to be up to date before merging**
- ✅ **Require conversation resolution before merging**

#### Status Checks to Require
Add these exact check names:
- `tests`
- `lint`
- `types`
- `security`

#### Additional Settings
- ✅ **Require a pull request before merging**
- ✅ **Require approvals** (set to 1 or more)
- ✅ **Dismiss stale PR approvals when new commits are pushed**
- ✅ **Restrict pushes that create files that cannot be reviewed**

### Step 3: Save the Rule
Click **Create** or **Save changes**

## Verification

After setting up the rules:

1. **Create a test PR** with some changes
2. **Check the PR page** - you should see:
   - Required status checks listed
   - Checks running automatically
   - Merge button disabled until all checks pass

3. **Check the Checks tab** - you should see:
   - tests ✓
   - lint ✓
   - types ✓
   - security ✓
   - commit-style ✓ (optional)

## Troubleshooting

### "Waiting for status checks to pass"
If you see this message, it means:
1. The status check names in your branch protection rule don't match the actual check names
2. The workflows haven't run yet on the current commit

**Solution**: 
- Check the exact names in the PR's **Checks** tab
- Update the branch protection rule to match those exact names
- Push a new commit to trigger the workflows

### "No status checks are required"
This means the branch protection rule isn't properly configured.

**Solution**:
- Go back to Settings → Branches → Branch protection rules
- Edit the rule for `main`
- Make sure "Require status checks to pass before merging" is checked
- Add the correct status check names

## Local Development

To ensure your code passes all checks locally before pushing:

```bash
# Run all checks (same as CI) - no bootstrap
just check

# Run complete build pipeline (bootstrap + all checks)
just ball

# Run individual checks (same as CI jobs)
just test          # matches CI 'tests' job
just lint          # matches CI 'lint' job  
just types         # matches CI 'types' job
just security      # matches CI 'security' job
just commit-style  # matches CI 'commit-style' job

# Health check (not in CI but useful)
just health-check
```

### Pre-commit Workflow

Before pushing code, run:

```bash
# Quick check (recommended for most changes)
just check

# Full build (recommended for major changes or after pull)
just ball
```

This ensures your code will pass all CI checks before they run on GitHub.

## Workflow Dependencies

The CI workflows use:
- **uv** for dependency management (same as local development)
- **pytest** for testing
- **ruff** for linting and formatting
- **ty** for type checking
- **bandit** and **pip-audit** for security scanning

All these tools are configured in `pyproject.toml` and match your local development environment. 