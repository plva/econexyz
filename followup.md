# This file marks followup items that should be done off-band from commits
This in this file should be stored in other locations, i.e. issues should be created for handling them.
- there's a bug when creating an issue, since it stores the issue in the current sprint.
    - we should not pull in new issues into the sprint when creating them, we only add them to todo
- we also need to explore how to deal with potential merge conflicts when adding new issues, since they get added to the todo
    - maybe only add issues during a standup, and in the meantime we can have a sort of pending issue queue
    - the pending issue queue is a directory with md files in it, each file is an issue where we describe certain stuff about it
    - an agent will pick up all items in the pending issue queue and create issues as part of the standup step
    - these all get added as part of the same [standup] commit...so maybe theres no problem with also adding them to the todo file.
- add in information for the standup: the commit header should start with `[standup]`
    - we can therefore find the previous standup (and all commits since that standup) by looking for the last `[standup]` commit
- add in info for the sprint planning:
    - the sprint planning activities can be stored in a [sprint-planning] headered commit
