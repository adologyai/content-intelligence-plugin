# Installing the Adology Content Intelligence Plugin

This guide walks you through installing the Adology Content Intelligence plugin in your AI agent of choice. You have two options depending on the client you use:

- **[Claude.ai connector](#option-a-claudeai-connector-recommended-for-most-users)** — zero-install, works in the Claude.ai web app. Recommended for most customers.
- **[Claude Code plugin](#option-b-claude-code-plugin)** — for developers and power users running Claude Code in a terminal.

Both options use the same hosted Adology MCP server (`https://mcp.adologyai.com/mcp`) and the same Adology account.

---

## Before you begin

You need an **Adology account** to use the plugin.

1. Go to <https://adologyai.com> and sign up (or log in if you already have an account).
2. Keep your login credentials handy — you'll sign in to Adology during the OAuth flow when your AI agent first connects.

---

## Option A: Claude.ai connector (recommended for most users)

The Adology MCP server is a hosted HTTPS service with OAuth 2.1 authentication, so Claude.ai can connect to it as a **custom connector**. No local installation required.

### Step 1 — Open Claude.ai connector settings

1. Sign in to <https://claude.ai>.
2. Click your profile picture (top-right) → **Settings**.
3. Open the **Connectors** tab.

### Step 2 — Add the Adology connector

1. Click **Add custom connector**.
2. Fill in:
   - **Name**: `Adology`
   - **URL**: `https://mcp.adologyai.com/mcp`
3. Click **Connect**.

Claude.ai will fetch the OAuth metadata from the server and redirect you to the Adology login flow (powered by Stytch).

### Step 3 — Authenticate

1. Sign in with your Adology credentials.
2. Approve the requested scopes (workspace read, scrape/analysis triggers, and writes for items you explicitly save).
3. You'll be redirected back to Claude.ai. The connector should now show as **Connected**.

### Step 4 — Verify

Open a new chat in Claude.ai and ask:

> Use the Adology `whoami` tool and tell me which workspace I'm connected to.

Claude should call the tool and reply with your workspace details. You're done.

---

## Option B: Claude Code plugin

For developers using [Claude Code](https://docs.claude.com/en/docs/claude-code) in a terminal. The recommended path installs directly from GitHub — no local clone required.

### Step 1 — Confirm prerequisites

- **Claude Code** is installed and up to date. Check with:
  ```bash
  claude --version
  ```
  Install or upgrade from <https://docs.claude.com/en/docs/claude-code/quickstart>.
- You have an **Adology account** (see [Before you begin](#before-you-begin)). No API token to manage — the plugin uses OAuth 2.1.

### Step 2 — Install from GitHub

Start Claude Code in any directory:

```bash
claude
```

Inside the Claude Code session, add the Adology marketplace using GitHub's `owner/repo` shorthand and install the plugin:

```
/plugin marketplace add adologyai/content-intelligence-plugin
/plugin install content-intelligence@adology-marketplace
```

Claude Code fetches the marketplace catalogue and plugin contents directly from GitHub. No clone, no local path management.

> Private network or air-gapped environment? See [Offline install](#offline-install-claude-code) below.

### Step 3 — Authenticate (first tool call)

The first time Claude Code calls an Adology tool, it will start the OAuth 2.1 flow against the hosted MCP server. Run `/mcp` to inspect connector status or trigger auth manually — Claude Code will open a browser tab, you sign in with your Adology credentials (powered by Stytch), and the token is stored locally for future sessions.

### Step 4 — Verify

In the same Claude Code session, list installed plugins:

```
/plugin list
```

You should see **Adology — Content Intelligence**. Then ask the agent:

> Use the Adology `whoami` tool.

If OAuth hasn't completed yet, Claude Code prompts you through the sign-in flow. After that, the tool returns your workspace info. You're done.

---

## Offline install (Claude Code)

If your environment can't reach GitHub from inside Claude Code (e.g., corporate proxy, air-gapped network), clone the repository on a machine that has GitHub access and point the marketplace at the local copy instead.

```bash
git clone https://github.com/adologyai/content-intelligence-plugin.git ~/.adology/content-intelligence-plugin
```

Then in a Claude Code session:

```
/plugin marketplace add ~/.adology/content-intelligence-plugin
/plugin install content-intelligence@adology-marketplace
```

Use the absolute path if `~` does not expand for you.

---

## Updating the plugin

### Claude.ai connector

Nothing to do — the server is hosted by Adology and updates automatically.

### Claude Code plugin (GitHub install)

In a Claude Code session:

```
/plugin marketplace update adology-marketplace
/plugin install content-intelligence@adology-marketplace
```

`/plugin marketplace update` refreshes the catalogue from GitHub; the second command installs the latest version.

### Claude Code plugin (offline install)

Pull the latest changes locally, then refresh:

```bash
cd ~/.adology/content-intelligence-plugin
git pull
```

```
/plugin marketplace update adology-marketplace
/plugin install content-intelligence@adology-marketplace
```

---

## Troubleshooting

### `401 Unauthorized` or "authentication failed"

Both clients use OAuth 2.1, so the recovery is the same: re-run the OAuth flow to get a fresh access token.

- **Claude.ai connector**: open **Settings → Connectors**, disconnect Adology, and reconnect.
- **Claude Code**: run `/mcp` in a session and re-authenticate the `adology` server. If the issue persists, fully quit Claude Code, relaunch, and try again — stale tokens can survive an in-session reconnect.

### Plugin doesn't appear in `/plugin list`

Confirm the marketplace was added:

```
/plugin marketplace list
```

If `adology-marketplace` isn't listed, repeat Step 2 (or the [Offline install](#offline-install-claude-code) steps, if you went that route).

### MCP server unreachable

Check connectivity to the hosted server:

```bash
curl -sS https://mcp.adologyai.com/.well-known/oauth-protected-resource
```

You should get back a JSON document. If this fails, the issue is network-level (firewall, VPN, DNS) rather than the plugin.

### Empty results from analysis tools

New knowledge sets need a few minutes to fetch data. Ask the agent to call `get_workflow_status` for your knowledge set — fetches typically take 5–15 minutes.

---

## Getting help

- **Email**: <hello@adologyai.com>
- **Bug reports**: <https://github.com/adologyai/content-intelligence-plugin/issues>
- **Full support guide**: [SUPPORT.md](./SUPPORT.md)

We aim to respond within one business day.
