#!/bin/bash
# Transactional git helper with start/finalize/rollback commands.

set -e

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
    if [[ -n $(git status --porcelain) ]]; then
      echo "Uncommitted changes detected. Stashing them temporarily."
      git stash push -u -m "transaction-$transaction_branch" >/dev/null
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
    if [ ! -e "$state_file" ]; then
      echo "No transaction state found" >&2
      exit 1
    fi
    source "$state_file"
    if [ "$#" -ge 1 ]; then
      commit_msg=$1
    fi
    git add -A
    if ! git diff --cached --quiet; then
      git commit -m "$commit_msg"
    fi
    git checkout "$orig_branch"
    git merge --squash "$transaction_branch"
    git commit -m "$commit_msg"
    git branch -D "$transaction_branch"
    if [ "$stash_saved" = true ]; then
      git stash pop --index --quiet "$stash_ref"
    fi
    rm "$state_file"
    echo "Transaction successfully completed and merged."
    ;;
  rollback)
    if [ ! -e "$state_file" ]; then
      echo "No transaction state found" >&2
      exit 1
    fi
    source "$state_file"
    git checkout "$orig_branch"
    git branch -D "$transaction_branch"
    git reset --hard HEAD
    git clean -fd
    if [ "$stash_saved" = true ]; then
      git stash pop --index --quiet "$stash_ref"
    fi
    rm "$state_file"
    echo "Transaction rolled back."
    ;;
  *)
    echo "Usage: $0 <start|finalize|rollback> [args]" >&2
    exit 1
    ;;
esac
