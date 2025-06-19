#!/bin/bash

CATEGORY=$1
ISSUE_NAME=$2

if [ -z "$CATEGORY" ] || [ -z "$ISSUE_NAME" ]; then
  echo "Usage: $0 <category> <issue-name>" >&2
  exit 1
fi

OPEN_PATH="issues/open/$CATEGORY/${ISSUE_NAME}.md"
CLOSED_DIR="issues/closed/$CATEGORY"

if [ ! -f "$OPEN_PATH" ]; then
  echo "Issue not found: $OPEN_PATH" >&2
  exit 1
fi

mkdir -p "$CLOSED_DIR"
mv "$OPEN_PATH" "$CLOSED_DIR/" || exit 1

echo "Moved ${ISSUE_NAME}.md to $CLOSED_DIR/"
