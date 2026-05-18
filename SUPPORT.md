# Support

## Getting help

For questions, bug reports, and feature requests, email <hello@adologyai.com> or open an issue at <https://github.com/adologyai/content-intelligence-plugin/issues>.

We aim to respond within 1 business day.

## Troubleshooting

### Authentication errors

Verify that:

- Your `ADOLOGY_API_TOKEN` is set in your environment (or that you have completed the OAuth flow in your AI agent's connector settings)
- The token has not expired (regenerate from your Adology dashboard if needed)
- Your account is active

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
