#!/usr/bin/env node
// Propagate package.json#version to .claude-plugin/plugin.json and .claude-plugin/marketplace.json
import fs from 'node:fs/promises';

const PLUGIN_NAME = 'content-intelligence';

const pkg = JSON.parse(await fs.readFile('package.json', 'utf8'));
const version = pkg.version;

if (!version) {
  console.error('ERROR: package.json has no version field');
  process.exit(1);
}

// Update plugin.json
const pluginPath = '.claude-plugin/plugin.json';
const plugin = JSON.parse(await fs.readFile(pluginPath, 'utf8'));
plugin.version = version;
await fs.writeFile(pluginPath, JSON.stringify(plugin, null, 2) + '\n');

// Update marketplace.json (only the content-intelligence entry)
const marketPath = '.claude-plugin/marketplace.json';
const market = JSON.parse(await fs.readFile(marketPath, 'utf8'));
market.plugins = market.plugins.map(p =>
  p.name === PLUGIN_NAME ? { ...p, version } : p
);
await fs.writeFile(marketPath, JSON.stringify(market, null, 2) + '\n');

console.log(`Synced version ${version} to plugin.json and marketplace.json`);
