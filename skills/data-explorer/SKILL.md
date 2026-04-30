---
name: data-explorer
description: >
  Guides advanced data querying, filtering, and export workflows. Use when users want
  to browse content, filter by specific criteria, export data, or perform custom analysis
  beyond standard insights. Triggers on: "export", "download", "filter", "show me items",
  "browse", "search for", "find content", "CSV", "gallery".
---

# Data Exploration and Export

Your primary lever for controlling what you get back from every tool is **field selection**. Master `fields` and `labelFields` before anything else — they determine whether you get a useful, focused response or a wall of noise.

## Field Selection (Start Here)

All item-returning tools (`get_items`, `search_items`, `analyze`, `get_item_detail`) accept two parameters that control what comes back:

- **`fields`** — Which item-level properties to include. Default base set: id, brand, platform, headline, engagement metrics, isOutlier, likesMultiple, createdAt, adDescription, transcript. Add more as needed (e.g., `fields: ["hookMechanism", "creativeConcept", "viewsMultiple"]`). Pass `fields: []` to suppress all item fields (stats-only mode).
- **`labelFields`** — Which label dimensions to include on each item. Pass specific categories (e.g., `labelFields: ["HookType", "ContentFormat"]`) or `labelFields: []` to suppress labels entirely.

**Use `list_labels` to discover available dimensions.** Before requesting label fields, call `list_labels` on the knowledge set. It returns every label category and its values — this tells you what dimensions exist so you don't guess at field names.

**Never use `compact: true`** — use `fields: []` and `labelFields: []` instead for the same effect with precise control. `compact` is a legacy toggle superseded by field selection.

See the [available fields reference](references/available-fields.md) for the full 45+ field catalog, sort options, and filter formats.

## Browsing Content

`get_items` provides paginated browsing with filters. `search_items` handles semantic/natural-language queries. Each item can include:

- **Identification** — id, brand, feedType, platform, sourceLabel
- **Content** — headline (first 200 chars of post text), transcript, adDescription, url
- **Engagement** — likes, views, shares, comments, engagementScore, engagementRate
- **Performance** — timesAccountAvg, likesMultiple, viewsMultiple, commentsMultiple, sharesMultiple, longevityMultiple, isOutlier, outlierType
- **Source Baselines** — sourceItemCount, sourceAvgLikes, sourceMedianLikes, sourceStddevLikes, sourceP90Likes, sourceAvgViews, sourceMedianViews, sourceAvgComments, sourceMedianComments, sourceAvgShares, sourceMedianShares, sourceAvgDaysAlive
- **Media** — thumbnail URL, mediaType (image/video)
- **Timing** — createdAt (ISO date string)

### Filters

- **Platform** — tiktok, instagram, youtube, facebook, twitter, reddit, linkedin, threads
- **Feed filter** — Narrow to specific brand feeds, influencer feeds, search feeds, or discussion feeds
- **Date range** — ISO date strings for start/end
- **Media format** — image, video, or both

### Parallel Browsing

When comparing content across different dimensions, run multiple `get_items` calls in parallel with different filters. Examples:

- Brand A's TikTok content + Brand A's Instagram content (platform comparison)
- Brand A's outliers + Brand B's outliers (competitive comparison)
- Last 30 days + previous 30 days (trend detection)

Each call is independent — do not wait for one to finish before starting the next.

## Cross-KS Content Search

`content_intelligence_search` searches the **entire Adology database** using AI-powered aspect decomposition — not scoped to any Knowledge Set. Use it when:

- The user wants inspiration beyond their tracked brands
- You need examples of a specific creative approach across the market
- The user's KS doesn't have enough data on a topic

Results include full performance enrichment (multiples, outlier flags, source baselines).

## Saving and Sharing

`save_to_collection` organizes items into named collections. The response includes a `url` field — a shareable gallery deep link to the collection in the Adology app. Use this whenever you find noteworthy content during browsing or analysis:

- Competitive examples worth revisiting
- Inspiration references for a creative brief
- Top performers to share with a team

Always share the returned URL so the user can view the collection directly.

## Export

Bulk data export is available through the Adology web UI. Use `save_to_collection` to curate items into shareable collections when the user needs to share specific findings.

## Analysis Patterns

- **Stats-only** — `get_table_data` for aggregate numbers without individual items
- **Content-first** — `get_items` with filters or `search_items` for semantic queries
- **Full pipeline** — `analyze` returns sampled items + tableData + stats; drill into standouts with `get_item_detail`
- **Dimension discovery** — `list_labels` to see what label categories exist before filtering or requesting label fields

## Error Recovery

- **0 results from `get_items`** — Broaden filters: remove platform constraint, widen date range, drop feed filter. If the KS is new, check `get_knowledge_set` for item counts — data may not have been scraped yet.
- **`list_labels` returns empty** — The KS has items but they haven't been analyzed yet. Fall back to field-based browsing (engagement metrics, platform) without label dimensions.
- **Unknown label category** — Always call `list_labels` first rather than guessing category names. The available categories vary by KS depending on which analysis pipeline ran.
