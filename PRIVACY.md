# Privacy

The `content-intelligence` plugin reads and writes data only within the authenticated Adology workspace. It does not access local files, the clipboard, other MCP servers, or any data outside of Adology.

**Data the plugin reads:** knowledge sets, brand portfolios, analyzed items, labels, saved collections, and conversation history — all scoped to the caller's organization.

**Data the plugin writes:** workbench entries, collections, ratings, notes — only when the user explicitly saves something.

**Authentication:** OAuth 2.1 (RFC 9700) via Stytch B2B. Bearer tokens are introspected on every tool call and are not cached across requests.

**Canonical privacy policy:** the authoritative document is at <https://app.termly.io/policy-viewer/policy.html?policyUUID=1ae61180-1e11-43b8-9e28-0e872447a395>. It governs data handling, retention, deletion, third-party processors, and data subject rights (GDPR, CCPA).

**Contact:** <hello@getadology.com>.
