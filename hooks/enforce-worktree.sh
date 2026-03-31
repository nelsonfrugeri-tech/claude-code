#!/bin/bash
# Enforce worktree isolation — blocks sessions not running in a worktree.
# Deterministic: no prompt can bypass this.

INPUT=$(cat)
CWD=$(echo "$INPUT" | jq -r '.cwd // empty')

# If we can't read cwd, allow (don't break things)
if [ -z "$CWD" ]; then
  exit 0
fi

# Check if running inside a git worktree
if git -C "$CWD" rev-parse --is-inside-work-tree &>/dev/null; then
  TOPLEVEL=$(git -C "$CWD" rev-parse --show-toplevel 2>/dev/null)
  GIT_DIR=$(git -C "$CWD" rev-parse --git-dir 2>/dev/null)

  # A worktree has a .git FILE (not directory) pointing to the main repo
  if [ -f "$TOPLEVEL/.git" ]; then
    exit 0  # We're in a worktree
  fi

  # Main repo .git is a directory — NOT a worktree
  echo "BLOCKED: Session must run in a git worktree." >&2
  echo "Restart with: claude --worktree <name>" >&2
  echo "Example: claude --worktree fix-bug-123" >&2
  exit 2
fi

# Not a git repo at all — allow (might be a non-git directory)
exit 0
