---
description: Spec-first TDD workflow. Use when implementing any feature or bugfix, before writing implementation code.
---

# TDD: spec, failing tests, green

1. Restate the spec as a checkbox list of behaviors: happy path, edge cases, fault paths. Show the list. Ask about ambiguity instead of guessing a requirement.
2. Write one failing test per behavior, named test_<unit>_<scenario>_<expected>. Run them and confirm each fails on an assertion, not an import error. Report the output.
3. Write the smallest implementation that turns the tests green. Run and report the real result.
4. Diff the test list against the spec. List uncovered requirements as explicit gaps.

Rules:
- Write tests before implementation. For a bugfix, write the failing reproduction first.
- Change an assertion only by discussing it first; a failing expectation is a conversation, not an obstacle.

Task: $ARGUMENTS
