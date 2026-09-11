---
description: Create a standardized PR. Use when asked to open a PR or when finishing work that needs one.
---

# PR workflow

1. Inspect `git status`, the diff, and recent history. Preserve unrelated changes; ask before moving or stashing user work.
2. Create or use a feature branch named <type>/<short-slug> (feat/fix/chore/refactor) before committing. Stage only intended files and commit in imperative mood, one concern per commit.
3. With a clean working tree, fetch and rebase the feature branch on the target branch. Run tests and linter; record the output. If a published branch would require a force-push, ask first.
4. Push the feature branch, then open the PR with this body:

```markdown
## What
<1-2 lines: what changes, user-visible effect if any>

## Why
<1-2 lines: the problem or requirement, link the issue>

## Tests
<command + result, e.g. "pytest -q -> 24 passed, 1 skipped">
<explicit gaps, if any>

## Risks / notes
<only for real risks: breaking changes, migrations, perf. Delete the section when empty.>
```

Rules:
- Keep the body under ~15 lines for anything but a genuinely complex change.
- Omit trivial changes (renames, extracted variables, added imports) from the body; the diff covers them.
- Write the title in imperative mood, 60 chars max.
- Describe the change, not the process: state what the code does now, skip the journey.

Task: $ARGUMENTS
