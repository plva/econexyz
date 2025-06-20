#!/usr/bin/env bash
# Unified test runner for EcoNexyz

set -euo pipefail

GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m" # No Color

PASS=true

echo -e "${GREEN}==> Running Python tests${NC}"
if pytest; then
    echo -e "${GREEN}Python tests passed${NC}"
else
    echo -e "${RED}Python tests failed${NC}"
    PASS=false
fi

echo -e "${GREEN}==> Running commit hook tests${NC}"
set +e
PYTHONPATH="${PYTHONPATH:-}:$(pwd)" python scripts/testing/test_commit_hook.py
HOOK_STATUS=$?
set -e
if [ $HOOK_STATUS -eq 0 ]; then
    echo -e "${GREEN}Commit hook tests passed${NC}"
else
    echo -e "${RED}Commit hook tests failed${NC}"
    PASS=false
fi

if [ "$PASS" = true ]; then
    echo -e "${GREEN}All tests passed${NC}"
    exit 0
else
    echo -e "${RED}One or more tests failed${NC}"
    exit 1
fi
