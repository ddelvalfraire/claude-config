---
description: Constants, variable naming, and regex conventions. Auto-loads when .py or .ts/.tsx files are touched.
paths:
  - "**/*.py"
  - "**/*.ts"
  - "**/*.tsx"
---

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
