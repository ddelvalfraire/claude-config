---
name: pr
description: Create a standardized PR. Use when asked to open a PR, or when finishing work that needs a PR.
---

# PR Workflow

## Pre-flight
1. `git status` — nothing uncommitted, no unrelated changes staged. Unrelated changes → separate branch/PR, mention it.
2. Rebase on the target branch; run tests + linter. Report real output in the PR.

## Branch & commit style
- Branch: `<type>/<short-slug>` (feat/fix/chore/refactor).
- Commits: imperative, one concern each, no "fix fix", no WIP dumps.

## PR body — this template, nothing more
```markdown
## What
<1–2 lines: what this changes, user-visible effect if any>

## Why
<1–2 lines: the problem or requirement. Link the issue if one exists.>

## Tests
<command run + result, e.g. "pytest -q → 24 passed, 1 skipped">
<explicit gaps: requirements not covered, if any>

## Risks / notes
<only if real — breaking changes, migrations, perf. Else omit this section entirely.>
```

## Hard rules
- **No narration of trivial changes.** "Extracted string to variable", "renamed x", "added import" get zero lines in the PR. The diff is right there; don't paraphrase it.
- Total body under ~15 lines unless it's a genuinely complex change.
- No AI-speak: no "This PR aims to...", no "In order to ensure...", no restating the diff file-by-file.
- No screenshots of code. Screenshots only for visual/UI changes.
- Title: imperative, ≤ 60 chars, no conventional-commit prefix unless the repo uses it.
