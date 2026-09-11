# Installing the Adology Content Intelligence Plugin

This guide walks you through installing the Adology Content Intelligence plugin in your AI agent of choice. Four install paths cover the supported clients:

- **[Claude.ai connector](#option-a-claudeai-connector-recommended-for-most-users)** — zero-install, works in the Claude.ai web app. Recommended for most customers.
- **[Claude Code plugin](#option-b-claude-code-plugin)** — for developers and power users running Claude Code in a terminal.
- **[Claude Cowork plugin](#option-c-claude-cowork-plugin)** — for Claude Desktop users on macOS or Windows running the Cowork agentic workspace.
- **[Google Gemini Enterprise](#option-d-google-gemini-enterprise)** — for organizations on Gemini Enterprise; a Google Cloud admin connects Adology once and every employee signs in once.

All four paths use the same hosted Adology MCP server (`https://mcp.adologyai.com/mcp`) and the same Adology account.

### Capability comparison

| Capability | Claude.ai connector | Claude Code plugin | Claude Cowork plugin | Gemini Enterprise |
|---|:---:|:---:|:---:|:---:|
| 44 MCP tools (`whoami`, portfolios, projects, search, analyze, …) | ✅ | ✅ | ✅ | ✅ |
| 11 domain skills (`brand-builder`, `audience-deep-dive`, …) | — | ✅ | ✅ | — |
| 4 slash commands | — | ✅ | ✅ | — |
| OAuth via Stytch | ✅ | ✅ | ✅ | ✅ (pre-issued client) |
| Runs on | Web (any browser) | macOS / Linux / Windows terminal | Claude Desktop on macOS / Windows | Gemini Enterprise web app |

Claude.ai and Gemini Enterprise give you the MCP tools but not the bundled skills and slash commands. Claude Code and Cowork install the full plugin bundle.

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

## Option C: Claude Cowork plugin

For Claude Cowork users running Claude Desktop on macOS or Windows. Cowork uses Claude Desktop's built-in plugin manager rather than a CLI command.

### Step 1 — Confirm prerequisites

- **Claude Desktop** for macOS or Windows. Install from <https://claude.ai/download>.
- **Cowork access** on your Claude account (Pro or Max). Cowork is desktop-only; it does not run on web or mobile.
- You have an **Adology account** (see [Before you begin](#before-you-begin)). No API token to manage — the plugin uses OAuth 2.1.

### Step 2 — Install from the plugin directory

1. Open Claude Desktop and switch to the **Cowork** tab.
2. Click **Customize** in the left sidebar.
3. Click **Browse plugins**.
4. Search for `Adology` or `content-intelligence` and click **Install** on the Adology Content Intelligence plugin.

> **Plugin not yet in the directory?** While the listing is pending approval, install manually instead:
>
> 1. Download `content-intelligence-<version>.zip` from <https://github.com/adologyai/content-intelligence-plugin/releases/latest>.
> 2. In Claude Desktop → **Cowork → Customize**, choose the option to **upload a custom plugin file** and select the downloaded zip.

### Step 3 — Authenticate (first tool call)

The first time Cowork calls an Adology tool, it kicks off the OAuth 2.1 flow against the hosted MCP server. A browser tab opens for you to sign in with your Adology credentials (powered by Stytch); the token is stored locally for future sessions.

### Step 4 — Verify

In a Cowork conversation, ask:

> Use the Adology `whoami` tool and tell me which workspace I'm connected to.

You should see your workspace info returned.

---

## Option D: Google Gemini Enterprise

For organizations rolling out [Gemini Enterprise](https://cloud.google.com/gemini/enterprise) (Standard, Plus, Frontline, or Business edition). Gemini Enterprise connects to the same hosted Adology MCP server as Claude, but Google registers it as a **Custom MCP Server data store** attached to your Gemini Enterprise app. Each employee signs in to Adology once, so every request runs with that person's own Adology access.

Google marks its custom MCP connector as Pre-GA. The steps below match Google's documentation as of September 2026; field labels may move as Google updates the console.

### What you need

- **An Adology OAuth client for your organization.** Gemini Enterprise does not register itself automatically the way Claude does — it needs a client ID and client secret issued in advance. Email <hello@adologyai.com> with your company name; we issue one client per organization and send the credentials back through a channel you choose. The client is bound to Google's callback address (`https://vertexaisearch.cloud.google.com/oauth-redirect`) and cannot be used anywhere else.
- **A Google Cloud administrator** with the **Discovery Engine Editor** role (`roles/discoveryengine.editor`) on the project behind your Gemini Enterprise app. If your organization restricts data sources or uses VPC Service Controls, that admin also needs to allow the `custom_mcp` data source and the three hostnames below.
- **An Adology account for each employee** who will use it (see [Before you begin](#before-you-begin)). Employees without an Adology account will reach the sign-in screen but cannot complete it.

Hostnames to allow if your Google Cloud organization restricts egress:

| Purpose | Hostname |
|---|---|
| MCP server | `mcp.adologyai.com` |
| Sign-in and consent page | `dash.adologyai.com` |
| Token exchange | `login.adologyai.com` |

### Step 1 — Add Adology as a Custom MCP Server data store (admin, once)

1. Open the [Google Cloud console](https://console.cloud.google.com/gemini-enterprise/start) in the project that runs your Gemini Enterprise app and go to **Gemini Enterprise**.
2. In the navigation menu, click **Data stores**, then **Create data store**.
3. Search for **Custom MCP Server** and click **Add MCP server**.
4. Fill in the connection:

   | Field | Value |
   |---|---|
   | **MCP Server URL** | `https://mcp.adologyai.com/mcp` |
   | **Authentication** | OAuth 2.0 |
   | **Authorization URL** | `https://dash.adologyai.com/oauth/authorize` |
   | **Authorization URL Parameters** | leave empty |
   | **Token URL** | `https://login.adologyai.com/v1/oauth2/token` |
   | **Client ID** | the client ID Adology sent you |
   | **Client Secret** | the client secret Adology sent you |
   | **Enable PKCE Support** | checked |
   | **Scopes** | `openid email profile offline_access` |

5. Choose the **Location** your organization uses for Gemini Enterprise data, name the connector `Adology`, and create it.

**Business edition instead?** The same values go into **Settings & help → Manage team → Connected apps → Add MCP Server**. Use `Adology` as the name and this description: "Competitive and audience intelligence: what brands and creators are posting, which ads and content perform, audience reactions, and SEO and AI-search visibility." Then skip to [Step 4](#step-4--each-employee-signs-in-once).

### Step 2 — Turn on the Adology actions (admin, once)

Google creates the data store with every action switched off.

1. Open the Adology data store you just created.
2. Click **Actions → Reload custom actions**. You will be asked to sign in to Adology — use your own Adology account and click **Accept and Continue**.
3. Select all the actions (Adology exposes 44, under Google's limit of 100 enabled actions) and click **Enable actions**.

### Step 3 — Connect the data store to your Gemini Enterprise app (admin, once)

1. In the navigation menu, click **Apps** and select your Gemini Enterprise app.
2. In the app's navigation menu, click **Connected data sources**.
3. Click **Add existing data stores**, select **Adology**, and click **Connect**.

From here the Gemini Enterprise assistant can use Adology directly. If you prefer a dedicated agent in your Agent Gallery (a named "Adology" agent with its own instructions and starter prompts), see [Optional: a dedicated Adology agent](#optional-a-dedicated-adology-agent) below.

### Step 4 — Each employee signs in once

1. Open your Gemini Enterprise web app.
2. Click **Manage your data**, find **Adology**, and click **Enable actions**.
3. Sign in with your Adology credentials and click **Accept and Continue** on the consent screen. You return to Gemini Enterprise with Adology switched on.

The sign-in is remembered; you will only see it again if you revoke access or your administrator resets the connection.

### Step 5 — Verify

In a new Gemini Enterprise chat, ask:

> Use the Adology `whoami` tool and tell me which workspace I'm connected to.

You should get back your workspace and team details. You're done.

### Optional: a dedicated Adology agent

Publishing a chat agent gives everyone a named entry in the Agent Gallery with instructions and starter prompts tuned for Adology.

1. In the Gemini Enterprise web app, click **+ Create agent → Chat agent**, then **Proceed to builder**.
2. Click the **My Agent** node. Set **Name** to `Adology` and paste these **Instructions**:

   > You are Adology, a competitive and audience intelligence analyst. Start each new conversation by calling `whoami`, then `list_portfolios` and `list_projects` to find the user's brands and working scope. Read tools (`query_items`, `aggregate`, `analyze`, `get_creative_dna`, `search_all`, the `seo_*` tools, and the paid-ads tools) are free — use them generously and cite the specific posts, ads, and numbers you found. Tools that bring new data in (`pull_data` → `confirm_pull`, `fetch_comments`, `fetch_reviews`) cost credits: quote the cost first and only proceed when the user confirms. Answer in plain language with concrete examples; say what you looked at and what would change your read.

3. Click **Add data sources & tools** and select the **Adology** data store.
4. Under **Personalization**, add starter prompts, for example:
   - "What are my competitors posting this week that's getting the most engagement?"
   - "Which of our ads are performing best right now, and why?"
   - "How is our brand showing up in AI search answers?"
5. Test in the **Preview** tab, then click **Create** to publish it to your organization's Agent Gallery. Employees find it under **Agents**.

### Gemini Enterprise troubleshooting

- **The data store fails to save with an authorization error.** Re-check the Authorization URL and Token URL exactly as written above (they are on two different hostnames), and confirm the client ID and secret were pasted without trailing spaces.
- **"redirect_uri mismatch" or "invalid client" during sign-in.** The client Adology issued is bound to Google's callback address. If Google changes its callback, or you are using a client issued for a different tool, email <hello@adologyai.com> and we will update it.
- **Sign-in completes but Adology reports no user.** The email you signed in with does not match an Adology account. Create the employee's Adology account (or invite them to your Adology team) and try again.
- **Adology does not appear under Manage your data.** Confirm Step 3 (the data store is connected to the app) and that your organization policy allows the `custom_mcp` data source.
- **No actions, or stale actions.** In the data store, click **Actions → Reload custom actions**, then **Enable actions** again.
- **The consumer Gemini app (gemini.google.com).** Custom MCP connections there are not available on work or school accounts. Use the Gemini Enterprise path above.

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

### Gemini Enterprise

Nothing to do — the server is hosted by Adology and updates automatically. New tools appear in the data store's action list; re-open the data store in the Google Cloud console if you want to review them.

### Claude Cowork plugin

If you installed via **Browse plugins**, Claude Desktop auto-updates the plugin to the latest version published in the directory — no action needed.

If you installed via **upload a custom plugin file**, download the new `content-intelligence-<version>.zip` from <https://github.com/adologyai/content-intelligence-plugin/releases/latest> and re-upload it via Claude Desktop → Cowork → Customize.

---

## Troubleshooting

### `401 Unauthorized` or "authentication failed"

All clients use OAuth 2.1, so the recovery is the same: re-run the OAuth flow to get a fresh access token.

- **Claude.ai connector**: open **Settings → Connectors**, disconnect Adology, and reconnect.
- **Claude Code**: run `/mcp` in a session and re-authenticate the `adology` server. If the issue persists, fully quit Claude Code, relaunch, and try again — stale tokens can survive an in-session reconnect.
- **Claude Cowork**: in Claude Desktop → **Cowork → Customize**, disable and re-enable the Adology plugin (or uninstall and reinstall). The next tool call triggers a fresh OAuth flow.
- **Gemini Enterprise**: open **Manage your data**, switch Adology off and on, and sign in to Adology again. If that does not clear it, your Google Cloud admin can open the data store and click **Actions → Reload custom actions**. See [Gemini Enterprise troubleshooting](#gemini-enterprise-troubleshooting) for the other cases.

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

New data pulls need a few minutes to land. Ask the agent to call `check_pull` for the run — fetches typically take 5–15 minutes.

---

## Getting help

- **Email**: <hello@adologyai.com>
- **Bug reports**: <https://github.com/adologyai/content-intelligence-plugin/issues>
- **Full support guide**: [SUPPORT.md](./SUPPORT.md)

We aim to respond within one business day.
