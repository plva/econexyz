#!/bin/bash

CATEGORY=$1
ISSUE_NAME=$2

if [ -z "$CATEGORY" ] || [ -z "$ISSUE_NAME" ]; then
  echo "Usage: $0 <category> <issue-name>" >&2
  exit 1
fi

OPEN_PATH="issues/open/$CATEGORY/${ISSUE_NAME}.md"
CLOSED_DIR="issues/closed/$CATEGORY"
TODO_FILE="TODO.md"

if [ ! -f "$OPEN_PATH" ]; then
  echo "Issue not found: $OPEN_PATH" >&2
  exit 1
fi

mkdir -p "$CLOSED_DIR"
mv "$OPEN_PATH" "$CLOSED_DIR/" || exit 1

echo "Moved ${ISSUE_NAME}.md to $CLOSED_DIR/"

# Update TODO.md to mark as complete
if [ -f "$TODO_FILE" ]; then
  # Replace the open checkbox with closed checkbox and update path
  # Handle both absolute paths (/issues/...) and relative paths (issues/...)
  sed -i.bak "s/- \[ \] \[$CATEGORY\/$ISSUE_NAME\]([^)]*issues\/open\/$CATEGORY\/$ISSUE_NAME\.md)/- [x] [$CATEGORY\/$ISSUE_NAME](\/issues\/closed\/$CATEGORY\/$ISSUE_NAME\.md)/g" "$TODO_FILE"
  rm -f "$TODO_FILE.bak"
  echo "Updated $TODO_FILE to mark issue as complete"
fi

# Update sprint meta files
for sprint_meta in sprints/open/*/sprint-meta.md; do
  if [ -f "$sprint_meta" ]; then
    # Replace the open checkbox with closed checkbox and update path
    sed -i.bak "s/- \[ \] \[$CATEGORY\/$ISSUE_NAME\]([^)]*issues\/open\/$CATEGORY\/$ISSUE_NAME\.md)/- [x] [$CATEGORY\/$ISSUE_NAME](\/issues\/closed\/$CATEGORY\/$ISSUE_NAME\.md)/g" "$sprint_meta"
    rm -f "$sprint_meta.bak"
    echo "Updated $sprint_meta to mark issue as complete"
  fi
done
