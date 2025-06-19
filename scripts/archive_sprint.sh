#!/bin/bash

SPRINT_NAME=$1

if [ -z "$SPRINT_NAME" ]; then
  echo "Usage: $0 <sprint-name>" >&2
  exit 1
fi

CURRENT_PATH="sprints/current/${SPRINT_NAME}.md"
ARCHIVE_DIR="sprints/archive"

if [ ! -f "$CURRENT_PATH" ]; then
  echo "Sprint not found: $CURRENT_PATH" >&2
  exit 1
fi

mkdir -p "$ARCHIVE_DIR"
mv "$CURRENT_PATH" "$ARCHIVE_DIR/" || exit 1

echo "Archived ${SPRINT_NAME}.md to $ARCHIVE_DIR/"
