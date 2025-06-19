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
    temp_save_branch="save-$(date +%Y%m%d%H%M%S)"
    if [[ -n $(git status --porcelain) ]]; then
      echo "Uncommitted changes detected. Saving them temporarily."
      git checkout -b "$temp_save_branch"
      git add -A
      git commit -m "Temporary save before transaction ($temp_save_branch)"
      git checkout "$orig_branch"
      temp_created=true
    else
      temp_created=false
    fi
    git checkout -b "$transaction_branch"
    printf 'orig_branch=%s\n' "$orig_branch" >"$state_file"
    printf 'transaction_branch=%s\n' "$transaction_branch" >>"$state_file"
    printf 'temp_save_branch=%s\n' "$temp_save_branch" >>"$state_file"
    printf 'temp_created=%s\n' "$temp_created" >>"$state_file"
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
    if [ "$temp_created" = true ]; then
      git branch -D "$temp_save_branch"
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
    if [ "$temp_created" = true ]; then
      git merge "$temp_save_branch" --ff-only
      git branch -D "$temp_save_branch"
    fi
    git reset --hard HEAD
    git clean -fd
    rm "$state_file"
    echo "Transaction rolled back."
    ;;
  *)
    echo "Usage: $0 <start|finalize|rollback> [args]" >&2
    exit 1
    ;;
esac
