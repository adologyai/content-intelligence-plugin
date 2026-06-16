# Adology — Content Intelligence: Install Guide for AI Assistants

This file is written for an AI assistant (e.g. Cline) performing the installation.
Follow it exactly.

## Read this first

Adology is a **remote MCP server**. There is **no local package to install and
nothing to build**. Do **not** clone the repository, and do **not** run
`npm install`, `pip install`, `npx`, or `docker run`. Installation is two things:
register one remote URL, then let the user authenticate via OAuth.

| | |
|---|---|
| Name | Adology — Content Intelligence |
| Transport | Remote, Streamable HTTP |
| Endpoint | `https://mcp.adologyai.com/mcp` |
| Auth | OAuth 2.1 (browser-based, prompted on first tool call) |
| Prerequisite | An Adology account — sign up at `https://dash.adologyai.com` |
| Local deps | None |

## Installation steps

1. Add Adology to the Cline MCP settings as a **remote streamable-HTTP server**.
   The configuration entry should be equivalent to:

   ```json
   {
     "mcpServers": {
       "adology": {
         "type": "streamableHttp",
         "url": "https://mcp.adologyai.com/mcp"
       }
     }
   }
   ```

   No `command`, `args`, or `env` are needed. If Cline exposes a "remote MCP
   server" / "add server by URL" flow, use that and supply only the URL above.

2. Save the settings. Cline will connect to the endpoint.

3. On the first tool call, the server returns an OAuth authorization request.
   Tell the user to complete sign-in in their browser. Once authorized, the
   tools become available. If the user has no Adology account yet, point them to
   `https://adologyai.com` to create a free one, then retry.

4. Confirm success by listing tools. You should see ~27 tools spanning brand
   discovery, knowledge-set management, competitive analysis, Creative DNA
   breakdowns, audience deep-dives, influencer vetting, and pulling performance
   from the user's own connected ad accounts.

## Do not

- Do **not** attempt any local install (`npm`/`pip`/`npx`/`docker`). There is no
  local server.
- Do **not** add API keys or tokens to the config. Authentication is OAuth only.
- Do **not** alter the endpoint path. It is exactly `https://mcp.adologyai.com/mcp`.

## Troubleshooting

- **No tools listed** — confirm the transport is streamable HTTP and that the
  user completed the OAuth flow.
- **Auth fails or loops** — have the user sign in at `https://dash.adologyai.com`
  first, then retry the tool call.
- **Support** — `hello@getadology.com`
