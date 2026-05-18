# Support

## Getting help

For questions, bug reports, and feature requests, email <hello@adologyai.com> or open an issue at <https://github.com/adologyai/content-intelligence-plugin/issues>.

We aim to respond within 1 business day.

## Troubleshooting

### Authentication errors

The plugin uses OAuth 2.1 (Stytch). Recovery:

- Re-run the OAuth flow: in Claude Code, run `/mcp` and re-authenticate the `adology` server; in Claude.ai, disconnect and reconnect the Adology connector under _Settings → Connectors_.
- Confirm your Adology account is active by signing in to <https://dash.adologyai.com>.
- If a stale token survives an in-session reconnect, fully quit and relaunch your AI agent.

### Empty results from analysis tools

Check `get_workflow_status` for any feeds you have added — data fetches typically take 5–15 minutes. If a knowledge set has feeds configured but no items, run `trigger_fetch` and wait for completion.

### MCP server connectivity

The MCP endpoint is `https://mcp.adologyai.com/mcp`. Verify reachability:

```bash
curl -sS https://mcp.adologyai.com/.well-known/oauth-protected-resource
```

This should return a JSON document conforming to RFC 9728.

## Account management

Pricing, plans, and account-level questions: <https://getadology.com/pricing> or email <hello@getadology.com>.
