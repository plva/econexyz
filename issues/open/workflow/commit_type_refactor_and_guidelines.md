------------------------
status: open
category: workflow
tags:
- workflow
- meta
- devops
- documentation
created: 2025-06-19
last-updated: 2025-06-19
priority: high
assigned: unassigned
------------------------
# workflow/commit_type_refactor_and_guidelines

## Summary

Refactor commit message types, update templates and documentation, and consider creating a single COMMIT_GUIDELINES.md file as the canonical source for commit message standards.

## Motivation

- Current commit types are inconsistent or too verbose (e.g., `[bugfix]`, `[sprint-planning]`)
- Need to clarify `[workflow]` and add new types for refactor, perf, and deps
- Centralize and clarify commit message guidelines for all contributors and AI agents

## Proposed Changes

### 1. Refactor Commit Types
- Change `[sprint-planning]` → `[sprint]`
- Change `[bugfix]` → `[fix]`
- Add:
  - `[refactor]` — Pure code cleanup without behavior change
  - `[perf]` — Performance enhancements
  - `[deps]` — Dependency updates

### 2. Clarify `[workflow]`
- `[workflow]` – Changes specifically to AI-agent workflows, agent instructions, or documentation that directly affect agent behaviors.
- Example: `[workflow] Update agent task completion instructions`

### 3. Update Templates
- Update all templates in `docs/templates/commit_messages/` to use the new/refined types

### 4. Update Documentation
- Update `docs/guides/commit_messages.md` (or create `COMMIT_GUIDELINES.md`)
- Document all commit types, usage, and examples
- Link to the canonical guidelines from `README.md`, `AGENTS.md`, etc.

### 5. Migration Plan
- Update references in scripts, hooks, and docs
- Communicate changes to all contributors

## Acceptance Criteria
- [ ] All commit types are refactored and documented
- [ ] Templates and scripts are updated
- [ ] Canonical guidelines file exists and is referenced
- [ ] Contributors are informed of the changes

## Additional Context
- This will improve clarity, consistency, and automation for both human and AI contributors.
- See discussion in commit message and workflow documentation history. 