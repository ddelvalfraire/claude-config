import { spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const installed = fileURLToPath(new URL('../hooks/run_hook.py', import.meta.url));
const source = fileURLToPath(new URL('../../hooks/run_hook.py', import.meta.url));

function runHook(action, args, directory) {
  return new Promise((resolve, reject) => {
    const script = existsSync(installed) ? installed : source;
    const child = spawn('python3', [script, action], {
      cwd: directory,
      stdio: ['pipe', 'ignore', 'pipe'],
    });
    let feedback = '';
    child.stderr.on('data', (chunk) => { feedback += chunk; });
    child.on('error', reject);
    child.stdin.on('error', reject);
    child.on('close', (code) => {
      if (code === 0) resolve();
      else reject(new Error(feedback || `claude-config hook exited ${code}`));
    });
    child.stdin.end(JSON.stringify({ cwd: directory, tool_input: args }));
  });
}

/** Connect shared checks to OpenCode's tool lifecycle. */
export const ClaudeConfigHooks = async ({ directory }) => ({
  'tool.execute.before': async (input, output) => {
    if (input.tool === 'bash') await runHook('guard', output.args, directory);
  },
  'tool.execute.after': async (input, output) => {
    if (!['edit', 'write', 'apply_patch'].includes(input.tool)) return;
    try {
      await runHook('after', input.args, directory);
    } catch (error) {
      // The edit already succeeded; keep its result and append actionable feedback.
      output.output = `${output.output ?? ''}\n${error.message}`;
    }
  },
});
