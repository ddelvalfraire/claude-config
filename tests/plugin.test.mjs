import { test } from 'node:test';
import assert from 'node:assert/strict';
import * as plugins from '../opencode/plugins/claude-config-hooks.js';
import { mkdtemp, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { execFileSync } from 'node:child_process';

test('exports callable plugin factories accepted by OpenCode', async () => {
  for (const factory of Object.values(plugins)) {
    assert.equal(typeof factory, 'function');
    const hooks = await factory({ directory: process.cwd() });
    assert.equal(typeof hooks['tool.execute.before'], 'function');
    assert.equal(typeof hooks['tool.execute.after'], 'function');
  }
});

test('blocks bash commits using the plugin directory rather than process cwd', async (t) => {
  assert.equal(typeof plugins.ClaudeConfigHooks, 'function');
  const directory = await mkdtemp(join(tmpdir(), 'plugin-test-'));
  t.after(() => rm(directory, { recursive: true, force: true }));
  execFileSync('git', ['init', '-b', 'main', directory]);
  const hooks = await plugins.ClaudeConfigHooks({ directory });
  await assert.rejects(hooks['tool.execute.before']({ tool: 'bash' }, {
    args: { command: 'git commit -m test' },
  }), /BLOCKED/);
});

for (const tool of ['write', 'edit', 'apply_patch']) {
  test(`reviews saved ${tool} content using after-hook input arguments`, async (t) => {
    assert.equal(typeof plugins.ClaudeConfigHooks, 'function');
    const directory = await mkdtemp(join(tmpdir(), 'plugin-test-'));
    t.after(() => rm(directory, { recursive: true, force: true }));
    const filePath = join(directory, 'new file.ts');
    await writeFile(filePath, '// const obsolete = 1;');
    const hooks = await plugins.ClaudeConfigHooks({ directory });
    const args = tool === 'apply_patch'
      ? { patchText: '*** Begin Patch\n*** Add File: new file.ts\n+// const obsolete = 1;\n*** End Patch' }
      : { filePath };
    const output = { output: 'Saved file' };
    await hooks['tool.execute.after']({ tool, args }, output);
    assert.match(output.output, /^Saved file\n.*COMMENT RULE VIOLATION/s);
  });
}
