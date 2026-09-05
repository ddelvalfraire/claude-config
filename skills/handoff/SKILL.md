---
name: handoff
description: Write a session handoff file so the next session resumes without re-briefing. Use at the end of a long session, before /clear, or when context fills.
---

# Handoff

Write or update HANDOFF.md in the project root:

```markdown
# Handoff - <date>
## State
<what works now, what was just completed: 2-4 bullets>
## Decisions
<decision + one-line rationale, including rejected approaches>
## Next steps
<ordered list, each with target files>
## Key files
<path: one-line reason, max 8>
## Open questions
<or "None">
```

Rules:
- Keep it under 60 lines. Paths and pointers only, no file contents or logs.
- Include exact commands for tests and the dev server.
- Include the gotcha that cost the most time this session.
- End with one line: "Handoff written: N decisions, M next steps."
