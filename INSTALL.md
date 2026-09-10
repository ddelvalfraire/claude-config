# claude-config

Drop-in Claude Code agent configuration. Copy these files into any project or into ~/.claude/ so every session starts with your conventions instead of re-explaining them.

Also compatible with Codex and OpenCode: AGENTS.md carries the same rules for both, OpenCode gets slash commands and a hook plugin. See "Codex and OpenCode" below.

## Contents

```
CLAUDE.md                    reply style, comment rules, verification honesty
AGENTS.md                    generated: same rules for Codex and OpenCode (do not edit by hand)
scripts/generate-agents-md.py  regenerates AGENTS.md from CLAUDE.md + rules/ + skills/
rules/react.md               React layering: hooks vs business vs UI (loads on *.ts/tsx)
rules/python.md              Python layout and conventions (loads on *.py)
rules/testing.md             test bar: happy path, edge cases, fault paths, input validation
skills/tdd/                  /tdd: spec -> failing tests -> green -> gap check
skills/pr/                   /pr: terse standardized PRs
skills/handoff/              /handoff: writes HANDOFF.md for the next session
skills/new-dep/              /new-dep: version/compat/docs check before any dependency
opencode/command/            same four workflows as OpenCode slash commands
opencode/plugins/claude-config-hooks.js  block-main-commit + biome format as an OpenCode plugin
settings.json                hooks: format on edit, run tests before stop
PULL_REQUEST_TEMPLATE.md     GitHub PR template matching /pr
```

## Codex and OpenCode

Both read `AGENTS.md` from the project root (or `~/.codex/AGENTS.md` / `~/.config/opencode/AGENTS.md` globally). It is generated, so edit CLAUDE.md or rules/ and regenerate:

```bash
python3 scripts/generate-agents-md.py
```

### Codex

```bash
cp AGENTS.md /path/to/project/AGENTS.md     # or ~/.codex/AGENTS.md for global
```

Codex has no hook or skill system: the block-main-commit guard, biome format-on-edit, and test-on-stop hooks do not apply. The workflows (/tdd, /pr, etc.) are embedded in AGENTS.md as sections, so Codex follows them when the prompt names them ("use the tdd workflow from AGENTS.md").

### OpenCode

```bash
cd /path/to/project
cp ~/code/github.com/ddelvalfraire/claude-config/AGENTS.md AGENTS.md   # rules at project root
mkdir -p .opencode/command .opencode/plugins
cp ~/code/github.com/ddelvalfraire/claude-config/opencode/command/*.md .opencode/command/
cp ~/code/github.com/ddelvalfraire/claude-config/opencode/plugins/claude-config-hooks.js .opencode/plugins/
```

This gives you the four workflows as `/tdd`, `/pr`, `/handoff`, `/new-dep` commands, plus the plugin recreating block-main-commit (blocks commit/push on main) and biome format-on-edit. The plugin requires Bun (OpenCode's runtime). The Claude test-on-stop hook has no OpenCode equivalent event and is not ported.

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
