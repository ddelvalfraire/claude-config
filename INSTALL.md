# claude-config

Shared instructions, skills, and lifecycle checks for Claude Code, Codex, and OpenCode.
Requires Python 3.10+, Git, and a POSIX shell. OpenCode loads the JavaScript plugin in its runtime; no additional npm dependencies are needed.

## Support

| Capability | Claude Code | Codex | OpenCode |
| --- | --- | --- | --- |
| Instructions | `CLAUDE.md` + `.claude/rules/` | `AGENTS.md` | `AGENTS.md` |
| Skills | `.claude/skills/`, `/tdd` etc. | `.agents/skills/`, `$tdd` etc. | `.opencode/skills/`; commands `/tdd` etc. |
| Protected-branch check | PreToolUse | PreToolUse | tool.execute.before |
| Comment review + local Biome | PostToolUse | PostToolUse (including apply_patch) | tool.execute.after (including apply_patch) |
| Tests on stop | Stop | Stop | Run explicitly; no blocking Stop hook installed |

Codex supports hooks in current releases. Review/trust them with `/hooks`; older releases may need upgrading. Project `.codex/` configuration must also be trusted. OpenCode has `session.idle` notifications, but those are not a synchronous, blocking equivalent of Stop.

## Installation

Run commands from this checkout and set `project` to an existing target project:

```bash
project=/absolute/path/to/project
```

Choose project or global installation per host. Hooks are additive across scopes; installing both can run the checks twice. **Merge existing instruction files and JSON hook arrays instead of overwriting them.** The copy commands below are for fresh destinations. Preserve existing plugins, permissions, MCP settings, and unrelated rules/skills.

### Claude Code: project

```bash
mkdir -p "$project/.claude" "$project/.github"
cp -R hooks rules skills "$project/.claude/"
cp settings.json "$project/.claude/settings.json"
cp CLAUDE.md "$project/CLAUDE.md"
cp PULL_REQUEST_TEMPLATE.md "$project/.github/"
```

### Claude Code: global

```bash
mkdir -p "$HOME/.claude"
cp -R hooks rules skills "$HOME/.claude/"
cp CLAUDE.md "$HOME/.claude/CLAUDE.md"
cp settings.global.json "$HOME/.claude/settings.json"
```

The global template resolves scripts from `$HOME`, not `$CLAUDE_PROJECT_DIR`.
Open `/hooks` in Claude Code to confirm the configured handlers.

### Codex: project

```bash
mkdir -p "$project/.codex" "$project/.agents/skills"
cp AGENTS.md "$project/AGENTS.md"
cp -R skills/. "$project/.agents/skills/"
cp -R hooks "$project/.codex/"
cp codex/hooks.json "$project/.codex/hooks.json"
```

Project hooks resolve from the Git root, so this installation requires a Git repository. Install at that root. For a non-Git directory, use the global configuration.

### Codex: global

```bash
mkdir -p "$HOME/.codex" "$HOME/.agents/skills"
cp AGENTS.md "$HOME/.codex/AGENTS.md"
cp -R skills/. "$HOME/.agents/skills/"
cp -R hooks "$HOME/.codex/"
cp codex/hooks.global.json "$HOME/.codex/hooks.json"
```

Open `/skills` to inspect skills and `/hooks` to review/trust the installed hook definitions. If `CODEX_HOME` is customized, adapt both the destination and script paths accordingly.

### OpenCode: project

```bash
mkdir -p "$project/.opencode/plugins" "$project/.opencode/command" "$project/.opencode/skills"
cp AGENTS.md "$project/AGENTS.md"
cp -R hooks "$project/.opencode/"
cp -R skills/. "$project/.opencode/skills/"
cp opencode/command/*.md "$project/.opencode/command/"
cp opencode/plugins/claude-config-hooks.js "$project/.opencode/plugins/"
```

### OpenCode: global

```bash
config="${XDG_CONFIG_HOME:-$HOME/.config}/opencode"
mkdir -p "$config/plugins" "$config/command" "$config/skills"
cp AGENTS.md "$config/AGENTS.md"
cp -R hooks "$config/"
cp -R skills/. "$config/skills/"
cp opencode/command/*.md "$config/command/"
cp opencode/plugins/claude-config-hooks.js "$config/plugins/"
```

Plugins are auto-discovered; no `plugin` config entry is needed. Keep the entire `hooks/` directory beside `plugins/`. If the same skills are already discoverable through `.claude/skills` or `.agents/skills`, omit the duplicate skill copy. **Quit and restart OpenCode after installing or updating configuration.**

## Hook behavior and limits

- The Git check catches ordinary `git commit`/`git push`, `git -C`, tool working directories, `cd` segments, and RTK wrappers. It blocks protected destinations from feature branches too. On main/master all pushes are conservatively blocked; create/switch branches in a separate tool call before committing. Aliases, nested shell scripts, dynamic shell expansion, and every possible Git refspec/configuration are not fully interpreted. Use remote branch protection for enforcement.
- Comment review runs after saved edits, so new files and corrective edits work. It reports mechanical patterns such as dead code and decorative dividers in source files; it is a heuristic, not a parser or a semantic judge of whether prose explains “why.” Markdown headings are excluded. Post-edit feedback cannot undo an edit.
- Formatting checks only edited/new/renamed files, including names containing spaces. It uses the nearest installed `node_modules/.bin/biome`; no package is downloaded. Missing Biome is skipped; failures are reported. Format and review run sequentially in one handler.
- Stop runs the nearest package's test script via its `packageManager` (otherwise pnpm when a pnpm lockfile exists, npm otherwise). Projects without a Node test script are skipped. Failures/timeouts request continuation once; `stop_hook_active` prevents repeated stop loops. Tests have a 120-second limit. Adapt this hook for longer suites or non-Node projects and always report explicit verification results.
- OpenCode appends post-edit feedback to the tool result. Run tests explicitly before finishing there.

## Maintenance and verification

`AGENTS.md` is generated from `CLAUDE.md`, `rules/`, and `skills/`; edit the sources and regenerate. Embedded workflows keep instructions available even when skills have not been installed.

```bash
python3 scripts/generate-agents-md.py
python3 -m unittest discover -s tests -v
node --test tests/plugin.test.mjs
python3 -m compileall -q hooks scripts
node --check opencode/plugins/claude-config-hooks.js
git diff --check
```

There is no app build or dev server. Tests use temporary repositories and local fixture executables; they do not commit, push, or invoke an LLM. For live verification, launch each CLI in an installed project, inspect hook/skill discovery, and trigger a harmless file edit. Check the CLI's debug output for plugin loading errors.

References: [Claude hooks](https://code.claude.com/docs/en/hooks), [Codex hooks](https://developers.openai.com/codex/hooks), [Codex skills](https://developers.openai.com/codex/build-skills), [OpenCode plugins](https://opencode.ai/docs/plugins/).
