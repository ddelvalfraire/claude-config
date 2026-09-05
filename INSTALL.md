# claude-config

Drop-in Claude Code agent configuration. Not an app — copy these files into any project (or `~/.claude/` for global) so every session starts with your conventions instead of re-explaining them.

## What's inside

```
CLAUDE.md                    communication style, comment rules, verification honesty
rules/react.md               React layering: hooks vs business vs UI (path-scoped to *.ts/tsx)
rules/python.md              Python module layout + conventions (path-scoped to *.py)
rules/testing.md             the test bar: happy path, edge cases, fault tolerance, input validation
skills/tdd/                  /tdd — spec → failing tests → green → gap check
skills/pr/                   /pr — terse standardized PRs, zero narration of trivial diffs
skills/handoff/              /handoff — writes HANDOFF.md so a new session resumes without re-briefing
skills/new-dep/              /new-dep — version/compat check + docs lookup before ANY new dependency
settings.json                hooks: format-on-edit, run tests before Claude stops
PULL_REQUEST_TEMPLATE.md     GitHub PR template matching the /pr skill
```

## Install into a project

```bash
# from this repo
cd /path/to/your-project
mkdir -p .claude
cp -r ~/code/github.com/ddelvalfraire/claude-config/rules .claude/
cp -r ~/code/github.com/ddelvalfraire/claude-config/skills .claude/
cp ~/code/github.com/ddelvalfraire/claude-config/settings.json .claude/   # merge if .claude/settings.json exists
cp ~/code/github.com/ddelvalfraire/claude-config/PULL_REQUEST_TEMPLATE.md .github/ 2>/dev/null || mkdir -p .github && cp ~/code/github.com/ddelvalfraire/claude-config/PULL_REQUEST_TEMPLATE.md .github/
# CLAUDE.md: merge the contents into the project's existing CLAUDE.md, or copy if none
```

Then **edit to taste per project** — these are defaults, not gospel. The rules files are path-scoped so they only load when matching files are touched.

## Install globally (all projects)

```bash
cp CLAUDE.md ~/.claude/CLAUDE.md                    # merge if it exists
cp -r skills ~/.claude/skills
cp -r rules ~/.claude/rules
cp settings.json ~/.claude/settings.json            # merge!
```

## Recommended global plugins (install once, not per-project)

```bash
# in claude:
/plugin marketplace add zilliztech/memsearch && /plugin install memsearch   # cross-session memory
/plugin marketplace add upstash/context7 && /plugin install context7        # version-specific library docs
# LSP plugin for your language (typescript-lsp / pyright) — type errors after every edit
# planning: install github/spec-kit for /speckit.* spec-driven workflow
```

Token-efficiency MCP servers (optional, measure with `/context` before and after):
- **serena** — semantic symbol-level code retrieval (benchmarked −66% code-read tokens)
- **rtk** — command-output compression

## Maintenance

These files drift. When you catch the agent violating a rule twice, add the rule. When a rule is obsolete, delete it. Review quarterly.
