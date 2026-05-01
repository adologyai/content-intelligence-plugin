# Installing the Adology Plugin in Claude Code

The Adology plugin runs as a Claude Code plugin that connects to the hosted
Adology MCP server. Installation takes two steps: installing the plugin
and providing credentials.

## Prerequisites

- **Adology account**: sign up at [https://getadology.com](https://getadology.com)
- **Adology API token**: generate from _Dashboard → Settings → API Tokens_
- **Claude Code**: latest version (`claude --version` to check)

Plugins are installed inside a running Claude Code session via the
`/plugin` slash command. Pick the option that matches how you obtained
the plugin.

## Option 1: Install from the Claude plugin directory

Once the plugin is listed in the official directory, start Claude Code
and run:

```
/plugin install content-intelligence
```

Claude Code will prompt for the two required environment variables.

## Option 2: Install from a released zip

1. Download `content-intelligence-<version>.zip` from
   [https://github.com/adologyai/content-intelligence/releases](https://github.com/adologyai/content-intelligence/releases)
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
git clone https://github.com/adologyai/content-intelligence.git
cd content-intelligence
```

Then, from a Claude Code session started in any directory:

```
/plugin marketplace add /absolute/path/to/content-intelligence
/plugin install content-intelligence@adology-marketplace
```

## Configure credentials

The plugin supports two auth flows. Most Claude Code users will only
use one of them:

- **Long-lived API token** (recommended for Claude Code): set
  `ADOLOGY_API_TOKEN` in your environment and `.mcp.json` will send it
  on every tool call as a bearer token. This is the simplest path if
  you already generated a token from _Dashboard → Settings → API
  Tokens_.
- **OAuth 2.1 (Stytch B2B)**: declared in `plugin.json` and used by
  default in clients that support it (e.g., the Claude.ai connector).
  In Claude Code, OAuth will only be triggered if `ADOLOGY_API_TOKEN`
  is unset and your client has been built to handle the flow — most
  users should rely on the env-var token instead.

Export the required environment variable before launching Claude Code:

```bash
export ADOLOGY_API_TOKEN="<your-token>"
```

Place this in `~/.zshrc`, `~/.bashrc`, or your preferred shell profile to
persist across sessions.

> **Note:** The MCP server URL is fixed in `.mcp.json`
> (`https://mcp.adologyai.com/mcp`) and does not need any environment
> configuration. Only the bearer token is interpolated at runtime — it
> is read from `$ADOLOGY_API_TOKEN` and injected into the
> `Authorization: Bearer …` header that `.mcp.json` sends to the MCP
> server.

## Verify the install

In a Claude Code session, run:

```
/plugin list
```

You should see Adology tools available. Then try a simple tool call:

```
Can you use the Adology whoami tool?
```

Claude should call the `whoami` MCP tool and return your workspace
information.

## Troubleshooting

See [`../SUPPORT.md`](../SUPPORT.md#troubleshooting) for common issues.
