---
name: tdd
description: Spec-first TDD workflow. Use when implementing any feature or bugfix — before writing implementation code.
---

# TDD: Spec → Failing Tests → Green

## Step 1 — Restate the spec as testable claims
Before any code: list, as checkboxes, the behaviors the spec requires (happy path + edge cases + fault tolerance per the testing rules). Show me the list. If the spec is ambiguous on any point, STOP and ask — do not guess a requirement.

## Step 2 — Write failing tests
- One test per claim, names `test_<unit>_<scenario>_<expected>`.
- Run them. They must FAIL for the right reason (assertion, not import error). Report actual output.

## Step 3 — Implement minimal code to green
- Smallest implementation that turns the tests green. No speculative abstractions.
- Run tests, report the real output (N passed / M failed).

## Step 4 — Gap check
- Diff test claims against the original spec. List any requirement not covered as an explicit gap.
- If coverage was partial because scope was cut, say so — never imply full coverage.

## Rules
- Never write tests after implementation to match the code's behavior — that's tautology, not testing.
- A bugfix starts with a failing test that reproduces the bug, then the fix.
- Do not weaken an assertion to make a test pass. If the expectation is wrong, discuss it.
