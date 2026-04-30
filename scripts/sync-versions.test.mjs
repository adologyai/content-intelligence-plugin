import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { execSync } from 'node:child_process';

test('sync-versions propagates package.json#version to plugin.json and marketplace.json', async () => {
  const tmp = await fs.mkdtemp(path.join(os.tmpdir(), 'sync-test-'));
  try {
    await fs.writeFile(
      path.join(tmp, 'package.json'),
      JSON.stringify({ name: 'content-intelligence', version: '1.2.3' })
    );
    await fs.mkdir(path.join(tmp, '.claude-plugin'));
    await fs.writeFile(
      path.join(tmp, '.claude-plugin/plugin.json'),
      JSON.stringify({ name: 'content-intelligence', version: '0.0.0', description: 'x' })
    );
    await fs.writeFile(
      path.join(tmp, '.claude-plugin/marketplace.json'),
      JSON.stringify({
        name: 'adology-marketplace',
        plugins: [
          { name: 'content-intelligence', version: '0.0.0' },
          { name: 'other', version: '9.9.9' }
        ]
      })
    );

    const scriptPath = path.resolve('scripts/sync-versions.mjs');
    execSync(`node ${scriptPath}`, { cwd: tmp });

    const plugin = JSON.parse(await fs.readFile(path.join(tmp, '.claude-plugin/plugin.json'), 'utf8'));
    assert.equal(plugin.version, '1.2.3', 'plugin.json#version should be updated');
    assert.equal(plugin.description, 'x', 'plugin.json non-version fields should be preserved');

    const market = JSON.parse(await fs.readFile(path.join(tmp, '.claude-plugin/marketplace.json'), 'utf8'));
    const ci = market.plugins.find(p => p.name === 'content-intelligence');
    assert.equal(ci.version, '1.2.3', 'marketplace.json content-intelligence entry should be updated');
    const other = market.plugins.find(p => p.name === 'other');
    assert.equal(other.version, '9.9.9', 'other plugins should be untouched');
  } finally {
    await fs.rm(tmp, { recursive: true, force: true });
  }
});
