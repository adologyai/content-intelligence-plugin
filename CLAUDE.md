# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is a **Claude Code plugin** (`content-intelligence`), not an application. It ships three things to AI agents — **skills**, **slash commands**, and an **MCP server reference** — plus the manifests and tooling to package and release them.

The MCP server is **remote and hosted** (`https://mcp.adologyai.com/mcp`, OAuth 2.1 via Stytch). The ~27 MCP tools live server-side and are **not** in this repo. There is nothing to build or run locally for the server — `.mcp.json` just points at the hosted endpoint. This repo is the distributable plugin package only.

This is a **public repository**. Do not put internal references (Slack links, ticket URLs, private channel names, internal threads) in commits, PR titles/bodies, issues, or committed files.

## Layout

- `.claude-plugin/plugin.json` + `marketplace.json` — plugin + marketplace manifests (validated as JSON in CI).
- `.mcp.json` — points the plugin at the remote MCP server.
- `skills/*/SKILL.md` — domain skills (markdown with `---` frontmatter; many have `references/`, `assets/`, or `scripts/` subdirs). This is where most of the substance lives.
- `commands/*.md` — slash commands (thin entrypoints that lean on the skills).
- `scripts/` — `sync-versions.mjs` (version propagation) and `export-plugin.sh` (build the `.zip`); `*.test.mjs` are the only unit tests.
- `docs/` — user-facing install + reference docs. `INSTALL.md` / `SUBMISSION*.md` at root are customer/registry-facing.

## Commands

```bash
npm test                       # node --test scripts/*.test.mjs (the only test suite)
node --test scripts/sync-versions.test.mjs   # run a single test file
npm run changeset              # add a changeset (required for any release-cutting PR)
npm run version                # apply changesets + sync versions across manifests
./scripts/export-plugin.sh             # build dist/*.zip (version from plugin.json)
./scripts/export-plugin.sh --preview   # PR preview build (suffixed with PR + SHA)
```

## Versioning (important)

`package.json#version` is the **source of truth**. It must stay in sync with `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`. Never hand-edit the version in the two manifests — run `npm run version` (or `node scripts/sync-versions.mjs`), which propagates it. Releases are driven by **changesets**: a PR that cuts a release must include a `.changeset/*.md` file.

## What CI enforces on PRs (`.github/workflows/pr.yml`)

- `plugin.json` and `marketplace.json` are valid JSON.
- Every `skills/*/SKILL.md` starts with `---` frontmatter (first line).
- `npm test` passes.
- The preview artifact builds, and changeset PRs must produce a `.zip`.

Match these locally before pushing — especially valid JSON manifests and SKILL.md frontmatter.
