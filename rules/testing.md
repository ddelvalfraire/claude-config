---
description: Test quality bar. Applies when writing or reviewing tests in any language.
paths:
  - "**/test*.py"
  - "**/*_test.go"
  - "**/*.test.ts"
  - "**/*.test.tsx"
  - "**/*.spec.ts"
---

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
