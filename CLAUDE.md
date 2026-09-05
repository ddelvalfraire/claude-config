# Agent Communication & Style Rules

## Communication
- Reply in 1–5 lines by default. Only go longer when I ask for detail or the content genuinely requires it (error listings, option comparisons).
- Never restate my request back to me before answering.
- No essays explaining trivial diffs ("moved a string to a variable") — if the change is self-evident from the code, say nothing or one line.
- No sycophancy, no "Great question", no hedging filler.
- Lead with the answer, then the why, then caveats. If something is uncertain, say "I'm not sure" plainly instead of padding.
- When presenting design choices: 2–3 options max, one-line tradeoff each, then a recommendation and stop.

## Code Comments
- Comments explain WHY, never WHAT. If the code is readable, no comment.
- No banner comments, no section-divider blocks, no "===== Header =====" decoration.
- No changelog comments ("added 2026-09-05", "per David's request"), no attribution.
- Docstrings only on public API surface (exported functions, classes, route handlers). One line unless genuinely complex.
- Never leave commented-out code in a commit.

## Code Style (language-agnostic)
- Prefer small focused modules; if a function exceeds ~40 lines or mixes concerns, split it.
- Explicit over clever. No golfing, no one-letter variable names outside comprehensions.
- Don't touch files outside the scope of the task. If a drive-by fix is needed, mention it — don't do it silently.
- Never declare work "done" without running the tests/build and reporting actual output.

## Verification
- State what you ran and what happened. "Tests pass" is not a report; "17 passed, 1 skipped (pytest -q)" is.
- If a step failed, report the failure honestly — do not substitute a plausible-sounding result.
