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

# Error handling (JavaScript/TypeScript)

When neverthrow is already a project dependency, write business logic as Results:

- Return `Result<T, E>` from functions for recoverable failures: `ok(value)` / `err(error)` put failure in the type signature so callers must handle it.
- Use `ResultAsync` (`ResultAsync.fromPromise` / `fromSafePromise`) for async operations that can fail; bridge sync-to-async with `.asyncAndThen` / `.asyncMap` and end the chain at the consumer.
- Pick `.map` for transformations that cannot fail and `.andThen` for steps that return their own Result; mixing them up hides which steps carry failure paths.
- Use `safeTry` with `yield*` inside a generator when a flow chains several Results; it short-circuits on the first Err and reads like Rust's `?`. Prefer it over an `isErr()` ladder after each call.
- Wrap throwing third-party APIs with `Result.fromThrowable` / `ResultAsync.fromThrowable` where they enter the codebase, converting exceptions into typed values at the edge.
- Type the E channel as a literal union or discriminated union (`'NotFound' | 'Unauthorized'`), one type per function's return signature; v7.1+ infers `err('NotFound')` narrowly, so lean on inference and only annotate when the compiler needs it.
- Consume Results with `.match(okBranch, errBranch)` or `.unwrapOr(default)` so both branches are handled at once; reserve `_unsafeUnwrap` for tests and treat `unwrapOr` defaults as an explicit product decision.
- Aggregate independent Results with `Result.combine` (short-circuits on first Err) or `Result.combineWithAllErrors` (collects all) instead of nesting chains.
- Keep pipeline stages small and named: extract each `andThen` step into its own function so the chain reads as the business flow and each stage is testable in isolation.

When neverthrow is absent, keep the same shape with plain TypeScript plus these rules:

- Confine `try`/`catch` to boundary layers (HTTP handlers, message consumers, CLI entry points, top-level server setup) where the alternative is process death or a 500 response; the catch translates the error into a response or log, then control returns.
- Write business logic exception-free: functions either return a typed error value (discriminated union with a `success`/`error` variant) or let the boundary's catch handle the escape. A try/catch inside a service function signals a missing error type in that layer's API.
- Prefer `Promise.reject` with a typed Error subclass over throwing bare strings; a thrown string carries no type information for the boundary's catch.

```ts
// Bad - try/catch threaded through business logic, errors untyped
async function registerUser(input: RegistrationInput) {
  try {
    const user = await createUserInDb(input);
    await sendWelcomeEmail(user);
    return user;
  } catch (e) {
    throw new Error(`registration failed: ${e}`);
  }
}

// Good - typed Results (with neverthrow), catch only at the HTTP boundary
type RegisterError = 'EmailTaken' | 'WeakPassword' | 'EmailError';

function registerUser(input: RegistrationInput): ResultAsync<User, RegisterError> {
  return safeTry(async function* () {
    const user = yield* createUserInDb(input);
    yield* sendWelcomeEmail(user);
    return ok(user);
  });
}

app.post('/register', async (req, res) => {
  const result = await registerUser(parseInput(req.body));
  result.match(
    (user) => res.json(user),
    (error) => res.status(400).json({ error }),
  );
});
```

```ts
// Good - same shape without neverthrow: typed error value, catch at the boundary
type RegisterResult =
  | { ok: true; user: User }
  | { ok: false; error: 'EmailTaken' | 'WeakPassword' | 'EmailError' };

async function registerUser(input: RegistrationInput): Promise<RegisterResult> {
  const existing = await db.users.findByEmail(input.email);
  if (existing) return { ok: false, error: 'EmailTaken' };
  if (!isStrongPassword(input.password)) return { ok: false, error: 'WeakPassword' };
  const user = await db.users.create(input);
  const delivery = await mailer.sendWelcome(user).then(
    () => ({ ok: true as const }),
    () => ({ ok: false as const, error: 'EmailError' as const }),
  );
  if (!delivery.ok) return delivery;
  return { ok: true, user };
}

app.post('/register', async (req, res) => {
  const result = await registerUser(parseInput(req.body));
  if (result.ok) return res.json(result.user);
  res.status(400).json({ error: result.error });
});
```

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
