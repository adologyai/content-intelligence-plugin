# Claude Plugin Directory — Submission Packet

This document consolidates everything Anthropic's plugin directory review team needs to approve the `content-intelligence` plugin.

## 1. Identity

| Field                | Value                                                          |
| -------------------- | -------------------------------------------------------------- |
| Plugin name          | `content-intelligence`                                         |
| Display name         | Adology — Content Intelligence                                 |
| Marketplace          | `adology-marketplace`                                          |
| Publisher / company  | Adology, Inc.                                                  |
| Publisher website    | https://getadology.com                                         |
| Publisher contact    | hello@getadology.com                                           |
| Maintainer           | Haldun Anil <hal@getadology.com>                               |
| Current version      | 0.1.0                                                          |
| License              | Apache-2.0                                                     |
| Primary category     | Marketing                                                      |
| Secondary categories | Analytics, Research                                            |

## 2. Product description

**Short (one sentence)**: Competitive ad intelligence + creator coaching for marketers, powered by Adology.

**Medium (one paragraph)**: The `content-intelligence` plugin connects Claude to your Adology workspace, giving you access to competitive ad intelligence directly in conversation. Discover brands, build knowledge sets, analyze ad content, coach creator accounts, vet influencer partners, and produce strategy artifacts (briefs, toolkits, audit decks) without leaving Claude.

**Target user**: marketers, creative strategists, CMOs, influencer managers, performance teams, growth operators, DTC founders.

**Example use cases**:

1. "Build me a knowledge set tracking Glossier and its top 10 competitors across TikTok and Instagram."
2. "Coach my last five TikTok posts — why did the weekend post flop?"
3. "Vet these 20 creators against our Q3 wellness brief and give me a top-five with personalized outreach."
4. "Audience deep-dive on women 28–42 who buy premium skincare — empathy canvas and insight brief."
5. "Build a creative toolkit for our summer launch, sourcing hooks from the top 100 TikToks in our category."

## 3. Capabilities

- **27 MCP tools** (see `docs/tools-reference.md`) for workspace, knowledge-set, analysis, search, conversation, and action operations
- **10 bundled skills** (see `docs/skills-reference.md`)
- **4 slash commands**: `/analyze`, `/compare`, `/discover`, `/export`
- **0 subagents** — multi-step research is handled by `research-analyst` skill (with optional fork dispatch via Task tool)

## 4. Authentication & data access

| Property                    | Value                                                      |
| --------------------------- | ---------------------------------------------------------- |
| MCP endpoint                | `https://mcp.adologyai.com/mcp`                            |
| Auth required               | Yes                                                        |
| Auth protocol               | OAuth 2.1 (RFC 9700)                                       |
| Authorization server        | Stytch B2B                                                 |
| Token introspection         | Every tool call; tokens are not cached across requests     |
| Protected Resource Metadata | RFC 9728 — served at `/.well-known/oauth-protected-resource` |
| Transport                   | HTTPS / TLS 1.2+                                           |

**Data the plugin reads**: knowledge sets, brand portfolios, analyzed items, labels, saved collections, conversation history — all scoped to the caller's organization.

**Data the plugin writes**: workbench entries, collections, ratings, notes — only when the user explicitly saves something.

**Data the plugin does NOT access**: local files, clipboard, other MCP servers, any data outside the Adology workspace.

## 5. Compliance & policies

| Document            | Location                                             |
| ------------------- | ---------------------------------------------------- |
| Privacy policy      | https://app.termly.io/policy-viewer/policy.html?policyUUID=1ae61180-1e11-43b8-9e28-0e872447a395 |
| Terms of service    | https://getadology.com/terms                         |
| License             | Apache-2.0 — see `LICENSE` in bundle                 |
| Contact             | hello@getadology.com                                 |

**Regulatory posture**:

- GDPR: data subject rights honored, processor DPAs in place
- CCPA: compliant data handling and deletion flow via dashboard
- HIPAA: not applicable — no PHI is processed
- PCI: not applicable — payment processing is handled by Stripe

## 6. Operational readiness

| Property              | Status                                              |
| --------------------- | --------------------------------------------------- |
| Production MCP URL    | `https://mcp.adologyai.com/mcp` (live)              |
| Rate limiting         | Concurrency semaphore + HTTP 503 backpressure       |
| Error handling        | Structured `CallToolResult` with `isError: true`    |
| Monitoring            | Server-side request/duration/size logging           |
| Incident response     | Documented in `SECURITY.md`                         |

## 7. Branding assets

| Asset                 | Path / status                                       |
| --------------------- | --------------------------------------------------- |
| Icon (SVG, 512×512)   | `.claude-plugin/icon.svg` (placeholder; real mark post-launch) |
| Screenshots           | Optional — capture guide in `.claude-plugin/screenshots/README.md` |

## 8. Pricing

Subscription-based per the Adology Terms of Service. Annual contracts available. Pricing details at <https://getadology.com/pricing> — that URL is the single source of truth and we do not duplicate tier/price data here to avoid drift.

## 9. Bundle artifact

- Latest artifact: `dist/content-intelligence-0.1.0.zip`
- Build command: `./scripts/export-plugin.sh`
- SHA256: computed automatically by the build script and printed to stdout
- Release tag: `plugin-v0.1.0`

## 10. Changelog

See `CHANGELOG.md`.

## 11. Review notes for Anthropic

- This plugin is a thin client over a hosted MCP server with OAuth.
- All workspace data is scoped to the authenticated user's organization via Stytch B2B tenancy.
- The plugin does not bypass any Claude safety features and does not request file, clipboard, or network access beyond the declared MCP endpoint.
- Skills are instructional `SKILL.md` files; they do not execute code.
- License is Apache-2.0; the plugin code is freely usable. Access to the Adology service is governed by the Terms of Service, not the LICENSE.
- **Test account**: email `hello@getadology.com` to request reviewer credentials. We will provision a scoped workspace cloned from a pre-built "Reviewer Template" with at least one populated knowledge set (e.g., Glossier-DTC) so tools return real data immediately. Target turnaround: <30 min from email.
