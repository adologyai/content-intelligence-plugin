# MCP Tools Reference

The Adology MCP server exposes **27 tools** organized into seven groups.
All tools are authorized against the caller's workspace — cross-tenant access
is rejected at the data layer.

## Identity

| Tool      | Purpose                                                  |
| --------- | -------------------------------------------------------- |
| `whoami`  | Return the authenticated user, organization, team, plan |

## Knowledge sets

| Tool                       | Purpose                                                        |
| -------------------------- | -------------------------------------------------------------- |
| `list_knowledge_sets`      | List all knowledge sets in the workspace                       |
| `get_knowledge_set`        | Return a specific knowledge set with its feeds and stats       |
| `create_knowledge_set`     | Create a new knowledge set with a name and description         |
| `add_feed`                 | Add a brand, influencer, search, or discussion feed to a set   |
| `batch_add_feeds`          | Add multiple feeds in a single call                            |
| `remove_feed`              | Remove a feed from a knowledge set                             |
| `compare_knowledge_sets`   | Compare two knowledge sets side by side                        |
| `trigger_fetch`            | Trigger a scrape/enrichment workflow for a knowledge set       |
| `list_workflows`           | List active scrape/analysis workflows                          |
| `get_workflow_status`      | Return the status of a running workflow                        |

## Discovery

| Tool              | Purpose                                                     |
| ----------------- | ----------------------------------------------------------- |
| `discover_brands` | Discover brands across TikTok, Instagram, Facebook, YouTube |
| `get_suggestions` | Return suggested feeds/creators relevant to a seed          |

## Analysis

| Tool             | Purpose                                                      |
| ---------------- | ------------------------------------------------------------ |
| `analyze`        | Run structured analysis over items matching a filter         |
| `list_labels`    | List label categories and values in a knowledge set          |
| `aggregate_items`| Aggregate counts/metrics of items by label or field          |
| `get_table_data` | Return tabular item data (for dashboards and exports)        |

## Content search

| Tool                              | Purpose                                                  |
| --------------------------------- | -------------------------------------------------------- |
| `search_items`                    | Keyword + filter search within a knowledge set           |
| `search_all`                      | Cross-workspace search                                   |
| `content_intelligence_search`     | Semantic + label-filtered content search (pgvector)      |
| `get_items`                       | Batch fetch items by id                                  |
| `get_item_detail`                 | Full detail for a single item (analysis, labels, media)  |

## Conversations

| Tool                   | Purpose                                               |
| ---------------------- | ----------------------------------------------------- |
| `list_conversations`   | List saved chatbot conversations                      |
| `get_conversation`     | Return a specific conversation with messages          |

## Actions / workbench

| Tool                 | Purpose                                                  |
| -------------------- | -------------------------------------------------------- |
| `save_to_collection` | Save an item or insight to a collection                  |
| `list_collections`   | List the user's collections                              |
| `get_collection`     | Return a collection with its contents                    |

## Rate limiting

The server enforces a global concurrency semaphore. Requests that exceed the
configured concurrency limit receive an HTTP 503 with a JSON-RPC error message
indicating the server is busy; clients should retry with backoff.

## Error handling

All tools return structured `CallToolResult` responses. Errors are returned as
`isError: true` with a text description; internal details (stack traces, DB
errors) are not exposed to clients.
