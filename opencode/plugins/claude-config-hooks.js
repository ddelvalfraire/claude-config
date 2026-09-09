/**
 * OpenCode plugin port of claude-config hooks (settings.json).
 *
 * Ported hooks:
 * - block-main-commit.sh (PreToolUse: Bash) -> block commit/push on main
 * - biome format on Edit/Write (PostToolUse)
 * - Stop hook: run tests before stop is not portable here; OpenCode plugins
 *   have no Stop-equivalent event, so it is intentionally omitted.
 *
 * Install: copy to <project>/.opencode/plugins/ or ~/.config/opencode/plugins/
 * Docs: https://opencode.ai/docs/plugins
 */

async function currentBranch() {
  const proc = Bun.spawn(["git", "branch", "--show-current"], {
    cwd: process.cwd(),
    stdout: "pipe",
    stderr: "ignore",
  })
  const out = await new Response(proc.stdout).text()
  await proc.exited
  return out.trim() || null
}

export const BlockMainCommit = {
  name: "block-main-commit",
  hooks: {
    "tool.execute.before": async (input, output) => {
      const tool = output?.tool ?? input?.tool
      const callArgs = output?.args ?? {}
      if (tool !== "bash") return

      const cmd = callArgs?.command ?? ""
      const branch = await currentBranch()
      if (!branch) return
      if (!/^(main|master)$/.test(branch)) return

      if (/git\s+push[^|;&]*(main|master)([^a-z]|$)|git\s+push\s+origin(\s|$)/.test(cmd)) {
        throw new Error(
          "BLOCKED: never push directly to main. Create a branch, push it, open a PR: " +
            "git checkout -b <type>/<slug> && git push -u origin <branch> && gh pr create"
        )
      }
      if (/git\s+commit/.test(cmd)) {
        throw new Error(
          "BLOCKED: never commit on main. git checkout -b <type>/<slug> first, then commit."
        )
      }
    },
  },
}

export const FormatOnEdit = {
  name: "format-on-edit",
  hooks: {
    "tool.execute.after": async (input, output) => {
      const tool = output?.tool ?? input?.tool
      const callArgs = output?.args ?? {}
      if (tool !== "edit" && tool !== "write") return

      const file = callArgs?.filePath ?? callArgs?.file_path ?? ""
      if (!/\.(ts|tsx|js|jsx|json)$/.test(file)) return

      const proc = Bun.spawn(["npx", "biome", "check", "--write", "--silent", file], {
        cwd: process.cwd(),
        stdout: "ignore",
        stderr: "ignore",
      })
      await proc.exited
      return
    },
  },
}

export const ClaudeConfigHooks = [BlockMainCommit, FormatOnEdit]
