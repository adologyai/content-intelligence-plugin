# Installing the Adology Plugin in Claude Code

The Adology plugin runs as a Claude Code plugin that connects to the hosted Adology MCP server. Installation has two phases: install the plugin, then sign in via OAuth on the first tool call.

> For a step-by-step customer guide that also covers the Claude.ai connector, see [INSTALL.md](../INSTALL.md). This document is the reference detail for the Claude Code path.

## Prerequisites

- **Adology account**: sign up at <https://adologyai.com>
- **Claude Code**: latest version (`claude --version` to check)

The plugin uses OAuth 2.1 (Stytch). There is no API token to manage — credentials are negotiated in-browser on first tool call.

Plugins are installed inside a running Claude Code session via the `/plugin` slash command. Pick the option that matches how you obtained the plugin.

## Option 1: Install from the Claude plugin directory

Once the plugin is listed in the official directory, start Claude Code and run:

```
/plugin install content-intelligence
```

## Option 2: Install from a released zip

1. Download `content-intelligence-<version>.zip` from
   [https://github.com/adologyai/content-intelligence-plugin/releases](https://github.com/adologyai/content-intelligence-plugin/releases)
2. Extract the archive to a location of your choice, e.g.
   `~/.claude/plugins/content-intelligence-0.1.0/`
3. Start Claude Code, then register the extracted directory as a local
   marketplace and install:

```
/plugin marketplace add ~/.claude/plugins/content-intelligence-0.1.0
/plugin install content-intelligence@adology-marketplace
```

## Option 3: Install from source (for local development)

```bash
git clone https://github.com/adologyai/content-intelligence-plugin.git
cd content-intelligence-plugin
```

Then, from a Claude Code session started in any directory:

```
/plugin marketplace add /absolute/path/to/content-intelligence
/plugin install content-intelligence@adology-marketplace
```

## Authenticate

The plugin's `.mcp.json` declares the hosted Adology MCP server, and `plugin.json` declares OAuth 2.1 (Stytch) as the auth method. On the first Adology tool call, Claude Code:

1. Detects the 401 from the protected MCP endpoint.
2. Reads the OAuth metadata at `https://mcp.adologyai.com/.well-known/oauth-protected-resource`.
3. Opens a browser tab to the Adology / Stytch sign-in flow.
4. Stores the resulting access token locally for future sessions.

You can also trigger or inspect auth manually with `/mcp` — pick the `adology` server and re-authenticate if needed.

> **Note:** The MCP server URL is fixed in `.mcp.json` (`https://mcp.adologyai.com/mcp`) and no environment configuration is required.

## Verify the install

In a Claude Code session, run:

```
/plugin list
```

You should see Adology tools available. Then try a simple tool call:

```
Can you use the Adology whoami tool?
```

The agent should call the `whoami` MCP tool and return your workspace
information.

## Troubleshooting

See [`../SUPPORT.md`](../SUPPORT.md#troubleshooting) for common issues.
