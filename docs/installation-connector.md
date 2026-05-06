# Installing the Adology Connector in Claude.ai

Claude.ai (the web application) supports hosted MCP servers as **connectors**.
The Adology MCP server runs as an HTTPS service with OAuth 2.1 authentication,
ready to be added as a connector.

## Prerequisites

- An active Adology account — sign up at [https://getadology.com](https://getadology.com)
- A Claude.ai account with connector support enabled

## Add the connector

1. In Claude.ai, open **Settings → Connectors → Add custom connector**.
2. Enter the connector details:
   - **Name**: Adology
   - **URL**: `https://mcp.adologyai.com/mcp`
3. Click **Connect**. Claude.ai will fetch the OAuth metadata from the
   server's `/.well-known/oauth-protected-resource` endpoint and redirect you
   to the Adology / Stytch login flow.
4. Authenticate with your Adology credentials. Stytch will issue an OAuth 2.1
   access token scoped to your workspace.
5. On successful auth, the connector becomes available in the Claude.ai
   conversation tool panel.

## Scopes granted

By authorizing the connector, you grant Claude.ai permission — on your behalf —
to call Adology MCP tools that:

- Read your workspace (knowledge sets, items, labels, collections, conversations)
- Trigger scrape and analysis workflows scoped to your organization
- Write items you explicitly save (workbench entries, collections, ratings)

See `PRIVACY.md` for the full data handling notice.

## Revoking access

At any time you can:

- Disconnect the connector from Claude.ai's connectors settings (revokes the
  token on the client side)
- Revoke the token from the Adology dashboard at _Settings → Sessions_
  (invalidates the token on the server side regardless of client state)

## Auditing activity

Every tool call made through the connector is logged server-side with a request
ID, timestamp, user ID, tool name, and duration. Workspace admins can view the
audit log in the Adology dashboard under _Settings → Audit Log_.

## Troubleshooting

- **OAuth redirect loops**: clear Claude.ai cookies for `claude.ai` and retry.
  If the issue persists, contact support@getadology.com.
- **Connector returns 401**: your token has expired. Reconnect from the
  connectors settings.
- **Connector returns 503**: the server is rate-limiting. Retry after a few
  seconds.

See [`../SUPPORT.md`](../SUPPORT.md) for more help.
