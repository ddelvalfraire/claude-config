---
name: pr
description: Create a standardized PR. Use when asked to open a PR or when finishing work that needs one.
---

# PR workflow

1. Check `git status`: everything committed, nothing unrelated staged. Move unrelated changes to a separate branch and mention it.
2. Rebase on the target branch. Run tests and linter; record the output.
3. Branch as <type>/<short-slug> (feat/fix/chore/refactor). Commit in imperative mood, one concern per commit.
4. Open the PR with this body:

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
