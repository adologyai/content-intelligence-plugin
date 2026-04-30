# Changelog

All notable changes to this plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-04-30

Initial release of the Adology Content Intelligence plugin under the adology-marketplace marketplace.

### Added

- 27 MCP tools fronting the hosted Adology server at `https://mcp.adologyai.com/mcp`
- 11 bundled domain skills:
  - `getting-started`, `brand-builder`, `content-strategist`, `data-explorer`, `research-analyst`
  - `brand-marketing-mode`, `audience-deep-dive`, `creative-toolkit`
  - `influencer-coach`, `influencer-vetting`, `thumbnails`
- 4 slash commands: `/analyze`, `/compare`, `/discover`, `/export`
- OAuth 2.1 via Stytch B2B with RFC 9728 protected resource metadata
- Apache 2.0 license
- Reproducible build via `scripts/export-plugin.sh`
- Changesets-based versioning + GHA release automation
