# claude-config

Drop-in Claude Code agent configuration. Copy these files into any project or into ~/.claude/ so every session starts with your conventions instead of re-explaining them.

## Contents

```
CLAUDE.md                    reply style, comment rules, verification honesty
rules/react.md               React layering: hooks vs business vs UI (loads on *.ts/tsx)
rules/python.md              Python layout and conventions (loads on *.py)
rules/testing.md             test bar: happy path, edge cases, fault paths, input validation
skills/tdd/                  /tdd: spec -> failing tests -> green -> gap check
skills/pr/                   /pr: terse standardized PRs
skills/handoff/              /handoff: writes HANDOFF.md for the next session
skills/new-dep/              /new-dep: version/compat/docs check before any dependency
settings.json                hooks: format on edit, run tests before stop
PULL_REQUEST_TEMPLATE.md     GitHub PR template matching /pr
```

## Install into a project

```bash
cd /path/to/project
mkdir -p .claude
cp -r ~/code/github.com/ddelvalfraire/claude-config/rules .claude/
cp -r ~/code/github.com/ddelvalfraire/claude-config/skills .claude/
cp ~/code/github.com/ddelvalfraire/claude-config/settings.json .claude/   # merge if one exists
mkdir -p .github && cp ~/code/github.com/ddelvalfraire/claude-config/PULL_REQUEST_TEMPLATE.md .github/
```

Merge CLAUDE.md into the project's existing CLAUDE.md, or copy it if none. Edit per project; these are defaults.

## Install globally

```bash
cp CLAUDE.md ~/.claude/CLAUDE.md      # merge if it exists
cp -r skills rules ~/.claude/
cp settings.json ~/.claude/settings.json   # merge
```

## Global plugins (once, not per project)

```
/plugin marketplace add zilliztech/memsearch && /plugin install memsearch   # cross-session memory
/plugin marketplace add upstash/context7 && /plugin install context7        # library docs on demand
```

Add the LSP plugin for your language (typescript-lsp, pyright). For planning, install github/spec-kit. Optional token savers: serena (symbol-level code retrieval) and rtk (command-output compression); measure with /context before and after.

## Maintenance

When the agent breaks a rule twice, write the rule down. Delete rules that no longer apply. Review quarterly.
