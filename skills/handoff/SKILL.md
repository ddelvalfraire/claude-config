---
name: handoff
description: Write a session handoff file so the next session can resume without re-explaining context. Use at the end of a long session, before /clear, or when context is filling up.
---

# Session Handoff

Write `HANDOFF.md` in the project root (or update it) with EXACTLY this structure, terse:

```markdown
# Handoff — <date>
## State
<What works now, what was just completed. 2–4 bullets.>
## Decisions made
<Each decision + one-line rationale. Include rejected approaches so they aren't re-tried.>
## In progress / Next steps
<Ordered list. Each item: what + which files.>
## Key files
<Path: 1-line why it matters. Max ~8.>
## Open questions / blockers
<Anything unresolved. "None" if empty.>
```

Rules:
- Under ~60 lines. This file is the rehydration point for a fresh context — a future session reads it FIRST and resumes without me re-explaining anything.
- Include exact commands to run the tests/dev server.
- Include gotchas discovered the hard way (the thing that ate 30 minutes).
- Never include full file contents or long logs — paths and pointers only.
- After writing it, confirm with one line: "Handoff written: N decisions, M next steps."
