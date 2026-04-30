# Installing the Adology Plugin in Claude Code

The Adology plugin runs as a Claude Code plugin that connects to the hosted
Adology MCP server. Installation takes two steps: installing the plugin
and providing credentials.

## Prerequisites

- **Adology account**: sign up at [https://getadology.com](https://getadology.com)
- **Adology API token**: generate from _Dashboard → Settings → API Tokens_
- **Claude Code**: latest version (`claude --version` to check)

## Option 1: Install from the Claude plugin directory

Once the plugin is listed in the official directory:

```bash
claude /plugin install adology
```

Claude Code will prompt for the two required environment variables.

## Option 2: Install from a released zip

1. Download `adology-plugin-<version>.zip` from
   [https://github.com/adology/adology-backend/releases](https://github.com/adology/adology-backend/releases)
2. Extract the archive to a location of your choice, e.g.
   `~/.claude/plugins/adology-plugin-0.2.0/`
3. Point Claude Code at the plugin directory:

```bash
claude --plugin-dir ~/.claude/plugins/adology-plugin-0.2.0
```

## Option 3: Install from source (for local development)

```bash
git clone https://github.com/adology/adology-backend.git
cd adology-backend
claude --plugin-dir ./packages/cowork-plugin
```

## Configure credentials

Export the required environment variables before launching Claude Code:

```bash
export ADOLOGY_MCP_URL="https://mcp.adologyai.com/mcp"
export ADOLOGY_API_TOKEN="<your-token>"
```

Place these in `~/.zshrc`, `~/.bashrc`, or your preferred shell profile to
persist across sessions.

## Verify the install

In a Claude Code session, run:

```
/plugin list
```

You should see `adology` in the output. Then try a simple tool call:

```
Can you use the Adology whoami tool?
```

Claude should call the `whoami` MCP tool and return your workspace
information.

## Troubleshooting

See [`../SUPPORT.md`](../SUPPORT.md#troubleshooting) for common issues.
