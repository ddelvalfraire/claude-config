---
description: Test quality bar. Applies when writing or reviewing tests in any language.
paths:
  - "**/test*.py"
  - "**/*_test.go"
  - "**/*.test.ts"
  - "**/*.test.tsx"
  - "**/*.spec.ts"
---

# Test Quality Bar

Every test suite written by the agent MUST meet all of these. A test file failing this bar is not done.

## Required coverage
1. **Happy path first** — every requirement in the spec has at least one test exercising the success case with realistic input. Not stubs, not mocks of the thing under test.
2. **Edge cases** — empty input, boundary values (0, -1, max, empty string/list), unicode, huge input where relevant. Enumerate them from the spec, don't guess.
3. **Fault tolerance** — for anything doing I/O (network, files, DB, subprocess): malformed input, timeout/refused connection, and partial failure paths are tested.
4. **Input validation** — if a function accepts untrusted input, tests assert it rejects bad input (wrong types, injection-ish payloads, oversized values), not just that it handles good input.

## Assertions
- Assert on **observable behavior/outputs**, not implementation details. A test that only checks "the mock was called" tests nothing without an output assertion.
- Every test asserts a requirement: before writing a test, know which spec/requirement line it covers. If you can't name it, the test is suspect.
- No tautological tests (`assert result == result`), no tests that would pass if the function were deleted.

## Structure
- Arrange–Act–Assert, one behavior per test, descriptive names: `test_<unit>_<scenario>_<expected>` (e.g. `test_parse_header_missing_returns_400`).
- Fixtures/helpers over copy-paste setup, but each test still readable standalone.
- When implementing a feature: write the failing tests from the spec FIRST, get them to green. Do not write tests after the fact to match whatever the code happens to do.

## Reporting
- Report the actual test command output (N passed / M failed), not "tests pass".
- List spec requirements NOT covered by tests as explicit gaps — never silently claim full coverage.
