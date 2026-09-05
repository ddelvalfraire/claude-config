#!/bin/bash
# PreToolUse hook: block commits and pushes directly to main/master.
# Reads Claude Code hook JSON on stdin; exit 2 blocks the tool call.
input=$(cat)
cmd=$(printf '%s' "$input" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null)

# Block push targeting main/master
if printf '%s' "$cmd" | grep -Eq 'git +push[^|;&]*(main|master)([^a-z]|$)|git +push +origin( +|$)'; then
  branch=$(git branch --show-current 2>/dev/null)
  if printf '%s' "$branch" | grep -Eq '^(main|master)$'; then
    echo "BLOCKED: never push directly to main. Create a branch, push it, open a PR: git checkout -b <type>/<slug> && git push -u origin <branch> && gh pr create" >&2
    exit 2
  fi
fi

# Block commits while on main/master
if printf '%s' "$cmd" | grep -Eq 'git +commit'; then
  branch=$(git branch --show-current 2>/dev/null)
  if printf '%s' "$branch" | grep -Eq '^(main|master)$'; then
    echo "BLOCKED: never commit on main. git checkout -b <type>/<slug> first, then commit." >&2
    exit 2
  fi
fi

exit 0
