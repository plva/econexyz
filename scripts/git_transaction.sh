#!/bin/bash
# Transactional git helper with start/finalize/rollback commands.

# This script lets you group several commands into a single atomic
# commit. Use `start` to begin the transaction, make your changes,
# then run `finalize` to squash them into one commit. If things go
# wrong call `rollback` and your working tree will be restored.

set -e  # exit on first error

state_file=".git/transaction_state"

cmd=$1
shift || true

case "$cmd" in
  start)
    if [ -e "$state_file" ]; then
      echo "Transaction already in progress" >&2
      exit 1
    fi
    if [ "$#" -lt 1 ]; then
      echo "Usage: $0 start <commit-message>" >&2
      exit 1
    fi
    commit_msg=$1
    orig_branch=$(git rev-parse --abbrev-ref HEAD)
    transaction_branch="transaction-$(date +%Y%m%d%H%M%S)"
    stash_saved=false
    stash_ref=""
    # Save any outstanding changes so we start from a clean slate.
    if [[ -n $(git status --porcelain) ]]; then
      echo "Uncommitted changes detected. Stashing them temporarily."
      git stash push --include-untracked --message \
        "transaction-$transaction_branch" >/dev/null
      # To also stash ignored files, pass --all instead of --include-untracked.
      stash_saved=true
      stash_ref=$(git stash list | head -n1 | cut -d: -f1)
    fi
    git checkout -b "$transaction_branch"
    printf 'orig_branch=%s\n' "$orig_branch" >"$state_file"
    printf 'transaction_branch=%s\n' "$transaction_branch" >>"$state_file"
    printf 'stash_saved=%s\n' "$stash_saved" >>"$state_file"
    printf 'stash_ref=%s\n' "$stash_ref" >>"$state_file"
    printf 'commit_msg=%q\n' "$commit_msg" >>"$state_file"
    echo "Transaction started on branch $transaction_branch"
    ;;
  finalize)
    # Commit changes and squash them onto the original branch
    if [ ! -e "$state_file" ]; then
      echo "No transaction state found" >&2
      exit 1
    fi
    source "$state_file"
    if [ "$#" -ge 1 ]; then
      commit_msg=$1
    fi
    git add -A  # stage everything in the transaction
    if ! git diff --cached --quiet; then
      git commit -m "$commit_msg"
    fi
    git checkout "$orig_branch"
    git merge --squash "$transaction_branch"  # bring over changes as one commit
    git commit -m "$commit_msg"
    git branch -D "$transaction_branch"  # remove temporary branch
    if [ "$stash_saved" = true ]; then
      git stash pop --index --quiet "$stash_ref"  # restore saved changes
    fi
    rm "$state_file"  # cleanup state
    echo "Transaction successfully completed and merged."
    ;;
  rollback)
    # Discard the transaction branch and restore any stashed changes
    if [ ! -e "$state_file" ]; then
      echo "No transaction state found" >&2
      exit 1
    fi
    source "$state_file"
    git checkout "$orig_branch"
    git branch -D "$transaction_branch"  # drop temp branch
    git reset --hard HEAD  # discard any partial changes
    git clean -fd          # remove untracked files from transaction
    if [ "$stash_saved" = true ]; then
      git stash pop --index --quiet "$stash_ref"  # restore saved changes
    fi
    rm "$state_file"  # cleanup state
    echo "Transaction rolled back."
    ;;
  *)
    echo "Usage: $0 <start|finalize|rollback> [args]" >&2
    exit 1
    ;;
esac
