# Handoff - 2026-09-11

## State
- Reviewed Claude Code, Codex, and OpenCode instruction/hook integrations against current documentation.
- Fixed plugin API shape, saved-file review, local formatting, Git guard gaps, stop feedback, and frontmatter generation on `fix/agent-hook-compatibility`.
- Verification: `python3 -m unittest discover -s tests -v` (26 passed); `node --test tests/plugin.test.mjs` (5 passed).
- Build checks: `python3 -m compileall -q hooks scripts`, `node --check opencode/plugins/claude-config-hooks.js`, `git diff --check` passed. No app build or dev server exists.

## Decisions
- Share Python hook logic across hosts to prevent shell/JavaScript implementations drifting.
- Review saved files after editing; pre-edit disk inspection misses new content and can block corrective edits.
- Use installed Biome only and report failures; implicit package downloads and swallowed errors were rejected.
- Keep OpenCode test execution explicit; session.idle is not a synchronous blocking Stop hook.
- Supply separate project/global templates so script paths resolve correctly; preserve existing machine configuration during this repository review.

## Next steps
1. Open and merge the `fix/agent-hook-compatibility` PR; use `HOME=/root` for Git and GitHub CLI commands in this tool shell.
2. Install the merged bundle into Brindle using `INSTALL.md`, preserve its project conventions, run `pnpm typecheck && pnpm test` and `pnpm lint`, and open a Brindle PR without merging it.
3. Validate live discovery with Claude/Codex `/hooks`, Codex `/skills`, and OpenCode startup/debug output; restart OpenCode after installation.

## Key files
- `INSTALL.md`: complete installation commands, supported behavior, limitations, and verification.
- `hooks/run_hook.py`: shared hook entry point and error reporting.
- `hooks/git_guard.py`: working-directory-aware protected-branch checks.
- `hooks/file_checks.py`: saved-file comment review and local Biome execution.
- `hooks/stop_tests.py`: bounded Node test execution and recursion guard.
- `opencode/plugins/claude-config-hooks.js`: callable plugin factory and before/after adapters.
- `codex/`: project/global native hook templates.
- `tests/`: Python regressions, copied-installation tests, and Node plugin-contract tests.

## Open questions
- Existing Git/GitHub credentials work with `HOME=/root`; this tool shell initially had HOME unset.
- Regression gaps: subprocess timeouts, oversized payloads, exhaustive Git configuration/refspec cases.
- Live CLI versions/startup could not be verified: claude, codex, opencode, and bun are not on this session's PATH.
- Main gotcha: unset HOME hid existing Git identity and GitHub authentication; no credential setup was needed.

Handoff written: 5 decisions, 3 next steps.
