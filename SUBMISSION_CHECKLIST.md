# Pre-Submission Compliance Checklist

This checklist tracks the items required for Claude Plugin Directory approval.

## Manifest & metadata

- [x] `.claude-plugin/plugin.json` present and valid JSON
- [x] `name`, `version`, `description`, `author`, `homepage`
- [x] `license: "Apache-2.0"` with matching `LICENSE` file
- [x] `privacyPolicy` URL set
- [x] `termsOfService` URL set (resolves once Adology terms page is live)
- [x] `repository` field set
- [x] `icon` path set and file exists
- [x] `shortDescription` under 140 chars
- [x] `keywords` (5–12 terms)
- [x] `category` set
- [x] `bugs` contact populated
- [x] `compatibility.clients` enumerated

## Marketplace listing

- [x] `.claude-plugin/marketplace.json` present
- [x] Display name under 60 characters
- [x] Short description under 140 characters
- [x] Pricing URL
- [x] Auth requirements declared

## Documentation

- [x] `README.md` with quick start
- [x] Installation docs for Claude Code and Claude.ai connector
- [x] Tool reference documenting every MCP tool
- [x] Skill reference
- [x] `CHANGELOG.md`

## Legal & policy

- [x] `LICENSE` file (Apache 2.0)
- [x] `PRIVACY.md` plus canonical policy URL
- [x] `SECURITY.md` with disclosure flow and safe harbor
- [x] `SUPPORT.md` with contact routing
- [ ] Privacy Policy URL resolves: live at Termly
- [ ] Terms of Service URL resolves: pending Adology terms page
- [ ] Pricing URL resolves: pending Adology pricing page
- [ ] Support URL/contact resolves: confirm `hello@getadology.com` routed

## Server / OAuth compliance

- [x] MCP server at `https://mcp.adologyai.com/mcp`
- [x] Serves `/.well-known/oauth-protected-resource` (RFC 9728) — verified
- [ ] Authorization server metadata reachable at `https://login.adologyai.com/.well-known/oauth-authorization-server` (RFC 8414) — verify during pre-submission smoke
- [x] Bearer token authentication on every tool call
- [x] HTTPS enforced; no HTTP fallback
- [x] Tokens scoped per user/org; cross-tenant rejected
- [x] 401 responses include `WWW-Authenticate` header with `resource_metadata`
- [x] Errors return structured responses; no stack traces
- [x] Rate limiting / backpressure (HTTP 503 when saturated)
- [x] Request IDs logged for audit
- [x] Tool input validation with Zod schemas

## Security

- [x] No secrets, tokens, or credentials committed to the plugin bundle
- [x] Third-party processors enumerated in canonical privacy policy
- [x] Security disclosure email monitored: `hello@getadology.com`
- [x] Safe-harbor language in `SECURITY.md`

## Data handling

- [x] Clear declaration of what data is read
- [x] Clear declaration of what data is written
- [x] Data retention periods stated (in canonical privacy policy)
- [x] Deletion mechanism documented
- [x] No persistence of Claude conversation text beyond explicit user saves
- [x] No local filesystem or clipboard access

## Artifact

- [x] Reproducible build script (`scripts/export-plugin.sh`)
- [x] Distributable zip produced at `dist/content-intelligence-<ver>.zip`
- [x] SHA256 computed by build script
- [x] Release commit tagged as `plugin-v0.1.0` (cut by release.yml on first changeset merge)

## Reviewer enablement (Adology-internal)

- [ ] Reviewer Template workspace built with populated knowledge set
- [ ] Internal provisioning recipe documented (clone → token → send credentials)

## Nice-to-haves (not blocking)

- [ ] 3–5 product screenshots at 1280×800 PNG in `.claude-plugin/screenshots/`
- [ ] Short demo video linked from the listing
- [ ] Real Adology icon (replacing placeholder SVG)
- [ ] DNS alias `security@` → `hello@` (RFC 9116 convention)

---

**Summary**: All blocking repository items will be satisfied once this implementation plan completes. The remaining unchecked items are external commitments (URLs, mailbox routing, reviewer template) tracked in the design spec §4.
