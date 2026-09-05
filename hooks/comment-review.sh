#!/bin/bash
# PreToolUse hook (matcher: Edit|Write): review comments in changed files against
# the comment rules in CLAUDE.md. Passes when comments explain why; flags comments
# that narrate the what. Exit 2 sends the feedback back to the agent for a fix.
input=$(cat)
file=$(printf '%s' "$input" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path","") or json.load(sys.stdin).get("tool_input",{}).get("filePath",""))' 2>/dev/null)

[ -f "$file" ] || exit 0

# Collect comment lines for common syntaxes
violations=""
while IFS= read -r line; do
  trimmed=$(printf '%s' "$line" | sed 's/^[[:space:]]*//')
  case "$trimmed" in
    \#*|//*|/\*|\*|<!--*)
      # skip shebangs, pragma-ish, and URLs inside strings
      case "$trimmed" in
        '#!'*|'#type'*|'// '*'http'*|'#'*'http'*) continue ;;
      esac
      # Banner/divider decorations
      printf '%s' "$trimmed" | grep -Eq '(={4,}|-{4,}|\*{4,}|={3,} .+ ={3,}|[A-Z][A-Z ]{6,}:?\s*=*)' && violations="${violations}${trimmed}\n"
      # Changelog/attribution comments
      printf '%s' "$trimmed" | grep -Eiq '(added|removed|updated|changed|fixed).*(20[0-2][0-9]|per [A-Z][a-z]+ .s request|TODO: remove|by @)' && violations="${violations}${trimmed}\n"
      # Commented-out code: a comment whose body looks like code
      printf '%s' "$trimmed" | sed 's|^[/#*!]*||' | grep -Eq '^\s*(const |let |var |def |return |if \(|for \(|import |from |function |class )' && violations="${violations}${trimmed}\n"
      ;;
  esac
done < "$file"

if [ -n "$violations" ]; then
  echo "COMMENT RULE VIOLATION in $file - fix these comments and re-save:"
  printf '%b' "$violations"
  echo "Rules: comments explain WHY the code is this way, never WHAT. No banner/divider blocks, no changelog or attribution comments, no commented-out code (delete it). Rewrite the flagged comments to explain rationale, or remove them if the code is self-evident."
  exit 2
fi

exit 0
