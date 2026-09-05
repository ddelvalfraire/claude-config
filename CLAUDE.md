# Agent defaults

## Replies
- Answer in 1-5 lines. Use a longer format only when the content requires it: error listings, option comparisons, requested detail.
- Lead with the answer, then the reason, then caveats. Say "I'm not sure" when unsure.
- For design choices: present 2-3 options with a one-line tradeoff each, give a recommendation, stop.
- Speak plainly. No filler openers, no restating my request, no summaries of what you already said.

## Comments
- Write comments that explain why the code is this way. Omit comments where the code is self-evident.
- Write a one-line docstring on every exported function, class, and route handler. Expand only when the behavior is genuinely complex.
- Keep all inline code out of comments: delete dead code in the same change that removes it.

## Code
- Keep functions under 40 lines and single-purpose. Split mixed concerns into separate modules.
- Write explicit, readable code. Use descriptive names in application code; short names are fine inside comprehensions.
- Change only the files the task requires. Mention needed drive-by fixes instead of making them.

## Verification
- Run the tests and build before calling work done. Report the command and the actual result: "17 passed, 1 skipped (pytest -q)".
- Report failures as failures. Never present an unexecuted or invented result as a real one.
