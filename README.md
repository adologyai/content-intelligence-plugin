# Adology — Content Intelligence

Competitive ad intelligence inside Claude and other AI agents. Discover brands, build knowledge sets, analyze ad content, coach creators, vet influencers, run audience deep-dives, and generate strategic insights — all powered by Adology's data platform.

## What This Plugin Does

The `content-intelligence` plugin connects your AI agent to your Adology workspace, giving you access to competitive ad intelligence directly in conversation. You can search for brands, manage knowledge sets, run content analysis, coach influencer accounts, vet creator partnerships, and produce strategy artifacts without leaving your AI agent.

## Capabilities

- **Knowledge Set Management** — Create, configure, and manage knowledge sets that track brands and competitors across ad platforms.
- **Brand Discovery** — Search for brands across TikTok, Instagram, Facebook, YouTube, and more.
- **Competitive Analysis** — Compare ad strategies, creative approaches, and content patterns across brands.
- **Content Intelligence** — Analyze ad content with AI-powered labeling, structural analysis, and pattern detection.
- **Creative Toolkits** — Build living libraries of hooks, angles, and scripts grounded in competitor + audience data, in the brand's actual voice.
- **Influencer Coaching & Vetting** — Coach creator accounts with personalized feedback, and score/vet influencer partners with evidence-based fit analysis.
- **Audience Deep Dives** — Produce behaviorally grounded audience profiles (empathy canvas, insight brief) backed by social + Reddit data.
- **Brand Marketing Mode** — Strategic brand thinking across positioning, competitive landscape, content strategy, and go-to-market.
- **Data Export** — Export filtered datasets, reports, and analysis results.

## What's Included

| Component       | Count | Description                                              |
| --------------- | ----- | -------------------------------------------------------- |
| MCP Tools       | 27    | Server-side tools for data access and operations         |
| Domain Skills   | 11    | Guided workflows for common analysis and strategy tasks  |
| Slash Commands  | 4     | Quick-access commands for frequent actions               |

### Skills

| Skill                  | Purpose                                                                        |
| ---------------------- | ------------------------------------------------------------------------------ |
| `getting-started`      | Onboarding walkthrough for first-time users                                    |
| `brand-builder`        | Build a knowledge set around a brand and its competitors                       |
| `content-strategist`   | Quick creative analysis: hooks, formats, CTAs                                  |
| `data-explorer`        | Query and explore Adology data fields directly                                 |
| `research-analyst`     | Multi-step research patterns; standard and heavy modes                         |
| `brand-marketing-mode` | Strategic brand thinking: positioning, landscape, content, go-to-market        |
| `audience-deep-dive`   | Behaviorally grounded audience profile + empathy canvas + insight brief        |
| `creative-toolkit`     | Living library of hooks/angles/scripts in the brand's voice, data-sourced      |
| `influencer-coach`     | Personalized creator coaching from knowledge set + account analysis            |
| `influencer-vetting`   | Score and select influencer/creator partners with evidence-based fit analysis  |
| `thumbnails`           | Reliable embedding of Adology thumbnails in generated documents                |

## Installation

See **[`INSTALL.md`](./INSTALL.md)** for a full step-by-step guide covering both the Claude.ai connector and the Claude Code plugin.

Quick links:

- **Claude.ai** — add `https://mcp.adologyai.com/mcp` as a custom connector under _Settings → Connectors_ and authenticate via Stytch.
- **Claude Code** — inside a session, run `/plugin marketplace add adologyai/content-intelligence-plugin` followed by `/plugin install content-intelligence@adology-marketplace`. No clone required.

## Account Setup

You need an Adology account to use this plugin. Visit <https://getadology.com> to create an account and generate your API token from the dashboard settings page.

## License

Apache 2.0 — see [`LICENSE`](./LICENSE).

The plugin code is freely usable under Apache 2.0. Access to the Adology service is governed by the [Adology Terms of Service](https://getadology.com/terms).

## Documentation

- [`INSTALL.md`](./INSTALL.md) — customer install guide (Claude.ai + Claude Code)
- [`docs/installation-claude-code.md`](./docs/installation-claude-code.md) — Claude Code install reference
- [`docs/installation-connector.md`](./docs/installation-connector.md) — Claude.ai connector reference
- [`docs/tools-reference.md`](./docs/tools-reference.md) — MCP tools reference
- [`docs/skills-reference.md`](./docs/skills-reference.md) — bundled skills reference

## Contact

- General: <hello@getadology.com>
- Privacy: see the [Privacy Policy](https://app.termly.io/policy-viewer/policy.html?policyUUID=1ae61180-1e11-43b8-9e28-0e872447a395)
- Issues: <https://github.com/adologyai/content-intelligence-plugin/issues>
