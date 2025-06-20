#!/bin/bash
# Create a lock file in the locks directory.
# Usage: create_lock.sh <lock-name> <file-path> "<reason>"

set -e

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <lock-name> <file-path> \"<reason>\"" >&2
  exit 1
fi

LOCK_NAME="$1"
FILE_PATH="$2"
REASON="$3"

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
LOCK_DIR="$ROOT_DIR/locks"
mkdir -p "$LOCK_DIR"

USER_NAME="$(git config user.name 2>/dev/null || true)"
if [ -z "$USER_NAME" ]; then
  USER_NAME="$(whoami)"
fi
TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

LOCK_FILE="$LOCK_DIR/${LOCK_NAME}.lock"
cat >"$LOCK_FILE" <<EOF_LOCK
user: "$USER_NAME"
timestamp: "$TIMESTAMP"
reason: "$REASON"
file: "$FILE_PATH"
EOF_LOCK

echo "Created $LOCK_FILE"
