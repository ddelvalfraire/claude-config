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

# Commitments
- Follow through on stated actions. If you say you will do something, do it in the same turn. Do not announce an action and then substitute your own judgment about whether it's needed.
- If you believe a requested step should be skipped or changed, say why and ask. The decision is mine.

# Git workflow
- Create a branch before committing: git checkout -b <type>/<slug>, then commit.
- Push feature branches and open a PR. main receives changes only through PR merge.

## Code
- Keep functions under 40 lines and single-purpose. Split mixed concerns into separate modules.
- Write explicit, readable code. Use descriptive names in application code; short names are fine inside comprehensions.
- Change only the files the task requires. Mention needed drive-by fixes instead of making them.

## Verification
- Run the tests and build before calling work done. Report the command and the actual result: "17 passed, 1 skipped (pytest -q)".
- Report failures as failures. Never present an unexecuted or invented result as a real one.

## Rule: constants
_Applies to: **/*.py, **/*.ts, **/*.tsx_

# Constants

- Name every literal that carries meaning: extract it to a named constant where the value's name explains why it exists.
- Treat 0, 1, -1, "", true/false as the only self-explanatory literals; anything else in logic gets a name.
- Suffix constants with their unit: TIMEOUT_MS, CACHE_TTL_SECONDS, MAX_UPLOAD_BYTES. Unitless names like TIMEOUT hide the seconds-vs-milliseconds bug class.
- Define each constant once and derive related values from it (MAX_TOTAL_ITEMS = PAGE_SIZE * MAX_PAGES), so a single edit updates the whole family.
- Place constants at module scope or a dedicated constants module for the concern (config/limits.ts, constants.py); keep one home per concept instead of scattering copies.
- Group related values into an enum or object when they form a closed set with shared meaning (states, status codes); use individual named constants when values are independent.
- Comment a constant only when the value's origin is non-obvious: what measured threshold or external limit (RFC, vendor cap) it comes from.
- Typed constant sets use `as const` objects or unions in TypeScript and `Final`/`Literal`/`Enum` in Python.

```ts
// Bad - unnamed values, unit hidden, duplicated family
if (retries > 3) throw new Error('too many');
const timeout = 30000;

// Good - named, unit-suffixed, derived
const MAX_RETRY_ATTEMPTS = 3;
const REQUEST_TIMEOUT_MS = 30_000;
if (retries > MAX_RETRY_ATTEMPTS) throw new Error('too many');
const timeout = REQUEST_TIMEOUT_MS;
```

# Time and durations (JavaScript/TypeScript)

- Use Temporal for all time and duration values: `Temporal.PlainDate`, `Temporal.ZonedDateTime`, and especially `Temporal.Duration.from({ minutes: 30 })` in place of a `Date` plus a hardcoded millisecond count.
- Build durations from unit-named fields so the unit lives in the code: `Temporal.Duration.from({ minutes: 30 })` replaces `30 * 60 * 1000`, whose unit and intent are invisible.
- Install `temporal-polyfill` (global entrypoint) in environments without native Temporal; it uses the native implementation when present.
- Keep Date only at the edges: convert to Temporal when it enters the codebase (`Date.prototype.toTemporalInstant`) and convert back only when a dependent API demands it.
- Store and pass instants as `Temporal.Instant` or ISO strings with explicit timezone (`Temporal.ZonedDateTime` for wall-clock meaning); treat a bare millisecond integer as a defect to name and convert at the boundary.

```ts
// Bad - hardcoded millisecond math on Date
const cutoff = Date.now() + 30 * 24 * 60 * 60 * 1000;

// Good - unit-named duration math
const TRIAL_LENGTH = Temporal.Duration.from({ days: 30 });
const cutoff = Temporal.Now.instant().add(TRIAL_LENGTH).epochMilliseconds;
```

# Naming variables

- Name variables after the concept they hold, not their type or shape: `pendingInvites` over `inviteList2`, `isRetryable` over `flag`.
- Use domain vocabulary in names so the code reads like the problem: `retryDelayMs`, `webhookSecret`, not `tmp`, `data2`, `handleStuff`.
- Keep loop and comprehension locals short (`x`, `k`) and application-code names descriptive; the short name is earned by staying inside 2-3 lines.
- Name booleans as assertions (`isValid`, `hasAccess`, `canRetry`) so call sites read as conditions.
- Prefix private/enum internals with the language convention: `_leading_underscore` in Python, `#private` or underscore in TS, and let one naming scheme per file hold.

# Regex

- Compile or hoist every regex to a module-level named constant instead of inlining a pattern string in logic. Name it after what it matches: `SLUG_PATTERN`, `ISO_DATE_RE`, not `PATTERN1`.
- Attach flags once at the definition site so matching behavior lives in one place rather than being remembered per call site.
- Use named capture groups for any pattern with 3+ groups or one whose groups outlive the match line, so consumers read `match.group('year')` instead of counting parentheses.
- Write non-trivial patterns in verbose mode (`re.VERBOSE` in Python, string-built composition elsewhere) with one comment per logical chunk.
- Compose large patterns from small named fragment constants instead of one monolithic string, so each piece is testable and reviewable on its own.
- When a pattern's explanation runs past two sentences, replace it with a sequence of simple checks in ordinary code.
- Test every shared pattern with both a known-valid and a known-invalid input in the pattern's owning test file.

```python
# Bad - inline pattern, flags per call, positional groups
if re.search(r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$", email, re.IGNORECASE):
    ...

# Good - module-level compiled pattern, named group
EMAIL_RE = re.compile(r"^(?P<local>[\w.+-]+)@(?P<domain>[\w-]+\.[a-zA-Z]{2,})$", re.IGNORECASE)

if EMAIL_RE.match(email):
    ...
```

## Rule: python
_Applies to: **/*.py_

# Python layout

- Use app/ or src/<pkg>/ with one module per concern: models.py, services.py, routes.py, config.py.
- Split by domain instead of a utils.py dumping ground: text_utils.py, date_utils.py, or fold into the owning module.
- Keep one cohesive class or function family per module. Split modules over ~300 lines by responsibility.
- Mirror tests to the package: app/services.py maps to tests/test_services.py.

## Conventions
- Use snake_case for modules and functions, PascalCase for classes, UPPER_SNAKE for constants, _leading_underscore for private.
- Add full type hints to public functions and any function over 5 lines.
- Use explicit imports; each import names what it uses.
- Model stable data shapes with Pydantic or dataclasses rather than raw dicts.
- Raise specific exceptions and catch only what you handle.
- Use async for I/O-bound code and keep blocking calls (requests, time.sleep, sync file IO) out of async def.

## Tests
Use the testing rules in rules/testing.md for all test code.

## Rule: react
_Applies to: **/*.tsx, **/*.ts_

# React layout

Use feature-based structure:

```
src/
  features/<feature>/
    components/     # presentational: props in, JSX out
    hooks/          # state and side effects, no JSX
    api/            # network calls and serialization, no React imports
    types.ts        # domain types
    index.ts        # public surface of the feature
  components/       # shared generic UI (Button, Modal, ...)
  lib/              # pure utilities, zero React
```

## Separation
- Put data fetching, business logic, and store access in hooks or api/, and keep components rendering-only.
- Keep hooks free of JSX and free of imports from components/.
- Write business logic as plain testable functions in api/ or lib/.
- Split any component over ~150 lines or containing fetch/store logic: logic into a hook, markup into a component.

## Imports
- Prefer aliased paths over relative ones: use `@/lib/...`, `@/components/...`, `@features/<name>` style imports instead of `../../` chains.
- Import cross-feature and cross-layer modules by alias; reserve relative paths (`./`, `../`) for imports within the same feature directory.
- If a repo lacks path aliases, add `paths` to tsconfig.json and matching bundler/vitest resolution before importing across directories. Resolve paths relative to the tsconfig; do not introduce deprecated `baseUrl` on modern TypeScript.
- Reach another feature's public surface through its `index.ts` (`@features/x`); import internals only from within that feature.

## Barrel exports
- Treat a barrel (`index.ts`) as a public API boundary: create one where outside code consumes the folder (each feature's `index.ts`, shared `components/` and `lib/` entry points, published package entries), and rely on path aliases for short imports elsewhere.
- Re-export explicitly: `export { Button } from './Button'` keeps the public surface visible and avoids accidental API expansion. Both explicit and star re-exports can be tree-shaken; results depend on the bundler and module side effects.
- Keep barrels pure: limit them to re-exports, and put constants, logic, and side effects in their own modules. Mark type-only re-exports with `export type`.
- Inside the folder, import siblings directly (`./Button`); route imports through the barrel only from outside the folder, which keeps import cycles out.
- Split oversized modules rather than letting a barrel accumulate dozens of exports.

## Conventions
- Name component files in PascalCase (UserProfile.tsx), hooks useX.ts, everything else camelCase.
- One component per file. Colocate small private types; extract shared types at the second consumer.
- Type all props explicitly. Use context or a store instead of prop-drilling past two levels.
- Use named exports for components; allow a default export only at each feature index.ts.

## Ternaries
- Write conditional assignments as if/else statements or an early-return helper function. Reserve the ternary for single-line cases where both branches are simple: a single function call or a plain variable/constant.

```ts
// Bad - nested multi-line ternary
const slugError =
  slugIssue !== 'none'
    ? i18n._(orgSlugMessage(slugIssue, slug))
    : takenSlug === slug
      ? i18n._(orgSlugMessage('taken', slug))
      : null;

// Good - if/else
let slugError: string | null = null;
if (slugIssue !== 'none') {
  slugError = i18n._(orgSlugMessage(slugIssue, slug));
} else if (takenSlug === slug) {
  slugError = i18n._(orgSlugMessage('taken', slug));
}
```

## Rule: testing
_Applies to: **/test*.py, **/*_test.go, **/*.test.ts, **/*.test.tsx, **/*.spec.ts_

# Test bar

Cover, per requirement in the spec:
1. One test per requirement exercising the success case with realistic input (happy path first).
2. Edge cases enumerated from the spec: empty input, boundaries (0, -1, max, empty string/list), unicode, oversized input.
3. Fault paths for anything doing I/O (network, files, DB, subprocess): malformed input, timeout or refused connection, partial failure.
4. Input validation: assert that untrusted-input surfaces reject wrong types, oversized values, and injection-style payloads.

## Assertions
- Assert on observable behavior and outputs. Pair any mock-call check with an output assertion.
- Name the requirement each test covers; if you cannot name it, delete or rewrite the test.
- Make each test fail when the implementation is deleted or stubbed.

## Structure
- Follow Arrange-Act-Assert, one behavior per test.
- For Python, name tests test_<unit>_<scenario>_<expected> (e.g. test_parse_header_missing_returns_400). For JavaScript/TypeScript, use readable behavior descriptions in `test`/`it`; for Go, use `TestXxx` names recognized by `go test`.
- Write tests from the spec before the implementation; drive code to green. For bugfixes, write the failing reproduction first.

## Reporting
- Report the real test command output (N passed / M failed).
- List spec requirements left uncovered as explicit gaps.

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

# New dependency

Complete all steps before writing an import.

1. Look up the latest stable version in the registry (npm/PyPI), not from memory.
2. Check compatibility with the runtime and framework versions plus peer dependencies. Note the chosen version and reason.
3. Check maintenance: last release date, issue ratio, deprecation banners. Flag anything stale or deprecated and propose the maintained alternative before installing.
4. Fetch current docs for the specific APIs we will use (context7 when available) and confirm they match the installed version.
5. Name the 1-2 main alternatives and the reason this one wins. Skip if I already picked it.
6. Note the license (flag GPL/AGPL) and notable install or bundle size.

Report in one block, then install and add a test that exercises the library usage:

```
<dep>@<version> - reason
compat: <runtime/framework>
docs: <APIs confirmed current>
license: <x>, size: <y>
```

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

# TDD: spec, failing tests, green

1. Restate the spec as a checkbox list of behaviors: happy path, edge cases, fault paths (see testing rules). Show the list. Ask about ambiguity instead of guessing a requirement.
2. Write one failing test per behavior, using the language-specific naming conventions in the testing rules. Run them and confirm each fails on an assertion, not an import error. Report the output.
3. Write the smallest implementation that turns the tests green. Run and report the real result.
4. Diff the test list against the spec. List uncovered requirements as explicit gaps.

Rules:
- Write tests before implementation. For a bugfix, write the failing reproduction first.
- Change an assertion only by discussing it first; a failing expectation is a conversation, not an obstacle.
