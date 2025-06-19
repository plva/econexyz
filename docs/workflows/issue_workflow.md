# Issue Workflow

```mermaid
flowchart TD
    start([Receive Issue]) --> isBug{Is it a bug?}
    isBug -->|Yes| checkClosed[Check closed issues]
    isBug -->|No| read[Read issue text]
    checkClosed --> existingBug{Found closed issue?}
    existingBug -->|Yes| reopen[Reopen issue with bug template]
    existingBug -->|No| newBug[Create new bug issue]
    reopen --> read
    newBug --> read
    read --> meta[Check priority & meta]
    meta --> category[Check category]
    category --> inSprint{Part of sprint?}
    inSprint -->|Yes| sprint[Sprint context]
    inSprint -->|No| offline[Work offline]
    sprint --> process[Process issue contents]
    offline --> process
    process --> amend{Need amendments?}
    amend -->|Yes| edit[Amend issue text]
    edit --> commit[Commit changes]
    amend -->|No| commit
    commit --> pr[Open PR]
    pr --> done([Issue complete])
```

## Bug Fix Process

When handling bugs:

1. First check if this is a regression (bug reappearing) by searching closed issues
2. If a related closed issue exists:
   - Reopen the issue using the bug template
   - Link to the original issue
   - Add any new context or information
3. If no related issue exists:
   - Create a new issue using the bug template
   - Set category to "bugs"
   - Add appropriate tags (bug, fix, critical if needed)
4. Follow normal issue workflow after bug issue is created

## Normal Issue Process

(Rest of existing content...)
