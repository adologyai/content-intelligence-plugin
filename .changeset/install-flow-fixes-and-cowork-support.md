---
"content-intelligence": patch
---

Fixes that make remote installation actually work plus customer-facing install documentation.

### Fixed

- `marketplace.json`: plugin source switched from bare `"."` (rejected by Claude Code as an unknown source type) to the explicit `github` object form, then to `url` with an HTTPS URL so anonymous clones succeed without SSH keys.
- `plugin.json`: `repository` field flattened from an `{ type, url }` object to a plain URL string (the previous object form caused Claude Code's manifest validator to reject the plugin with `repository: Invalid input: expected string, received object`).
- All stale `adologyai/content-intelligence` repo URLs corrected to `adologyai/content-intelligence-plugin` across `plugin.json`, `marketplace.json`, `package.json`, `README.md`, `SUPPORT.md`, and `docs/installation-claude-code.md`.
- Authentication is now OAuth-only across all clients. The previous mixed flow (`Authorization: Bearer ${ADOLOGY_API_TOKEN}` injected by `.mcp.json` plus OAuth declared in `plugin.json`) caused Claude Code to receive valid OAuth credentials and then immediately reject them on reconnect because the static header clobbered the OAuth token. The `Authorization` header has been removed from `.mcp.json`; Claude clients now negotiate credentials via the Stytch OAuth flow on first tool call.

### Added

- `INSTALL.md` — customer-facing install guide covering Claude.ai connector, Claude Code plugin, and Claude Cowork plugin, with a capability comparison matrix and OAuth-aware troubleshooting.
- `README.md` quick-links list for the three install paths.

### Changed

- `.changeset/config.json` changelog plugin now points at the correct GitHub repo (`adologyai/content-intelligence-plugin`) so generated changelog entries link to real commits and PRs.
