---
name: data-explorer
description: >
  Guides querying, filtering, and curation across a project's scope. Use when users want
  to browse content, filter by specific criteria, pivot label data, search, or run custom
  analysis beyond standard insights. Triggers on: "filter", "show me items", "browse",
  "search for", "find content", "top performers", "breakdown by", "collection".
---

# Data Exploration

Every read takes a `projectId` and returns what that project's scope covers. Two levers decide whether you get a useful answer or a wall of noise: picking the right reader, and controlling which fields come back.

## Discover before you filter

Label dimensions vary by project — they depend on what has been analyzed. Call `list_labels({ projectId })` to see which dimensions exist and their top values before naming one in a filter; a dimension the data doesn't carry silently matches nothing. `get_table_data({ projectId, listDimensions: true })` answers the same question from the pivot side. `aggregate({ projectId, groupBy: ["brand"], measures: [{ field: "*", fn: "count", as: "n" }] })` tells you the exact entity names the scope tracks, which is what `feedNames` and `brand` filters match against.

## Choosing a reader

**`analyze`** is the primary content tool. Four distributions:

- `"balanced"` (default) — equal representation per feed, a mix of top and recent. The honest "what does this scope look like" read.
- `"top"` — highest engagement per feed; set `sortMetric` to change which metric.
- `"recent"` — newest per feed.
- `"exhaustive"` — no sampling. A deterministic ranked page over the full filtered set with `totalEstimated` and `nextOffset`, so you can page the whole thing. Pair with `sortBy`, including the lift keys (`likesMultiple`, `viewsMultiple`, …). This is the leaderboard and "give me all of X" mode.

The sampled distributions read the creative feeds — brand and influencer — unless you name `feedTypes` yourself, so raw search and discussion items don't crowd a "what hooks are working" sample. Exhaustive reads exactly what you filtered, nothing added.

Two other modes: `mode: "semantic"` finds posts by meaning from a natural-language `query` (it honors platform, feed type, dates, and `includeComments`; narrow further after the results come back), and passing `itemIds` runs a by-id deep dive that returns full creative, labels, and performance for specific posts.

**`aggregate`** answers analytical questions — trends, averages, "top platforms by median likes". It groups over `platform`, `brand`, `feedType`, `format`, and `time`, and always returns grouped rows, never items. Lift multiples are per-item and are rejected here; for lift, use `analyze` exhaustive sorted by a `*Multiple` key.

**`get_table_data`** builds label pivot tables: `rows` (one or two label dimensions) × `columns` (brand, platform, feedType, mediaType, timePeriod, or focalVsRest) × `metrics` (count, useRate, medianLikes, medianViews, medianShares, viralRate). Rows are always label dimensions, and it counts labeled items only — search and discussion items frequently carry no labels, so read those with `analyze` instead.

**`get_creative_dna`** goes past distribution to effect — which structural elements actually drive performance, with controlled lift, per-brand advantages and gaps, and evidence posts. Lock the axes with `focusCategories: ["Hook","Emotion","Production"]`.

**`search_all`** is keyword search within the project's scope, ranked by engagement. **`query_items`** lists rows over the same scope with a fixed shape.

## Field selection

`analyze` returns a base set on every item — id, brand, feedType, platform, headline, likes, views, shares, comments, engagementScore, isOutlier, outlierType, likesMultiple, createdAt, url, thumbnail — and two independent axes on top:

- **`fields`** adds creative analysis: `fields: ["hookMechanism", "creativeConcept", "ctaText"]`. Omit it and the item comes back with everything the analysis carries.
- **`labelFields`** chooses which label dimensions ride along: `labelFields: ["Hook", "Format"]`, or `[]` to suppress labels entirely.

Whenever you cite a lift multiple, request its denominator too (`sourceMedianLikes` beside `likesMultiple`) and state the baseline. A "5x" with no baseline is not a finding.

Filter parameter names differ between readers — `analyze` takes `platformFilter` and `feedNames`, `query_items` takes `platform` and `brand`, `aggregate` nests everything under `filters`. See the [available fields reference](references/available-fields.md) for the full field catalog, the per-tool filter names, sort keys, and page limits.

## Parallel reads

Independent reads run at once. Two brands side by side, two platforms, this quarter against last, a `get_table_data` pivot alongside the `analyze` sample that will illustrate it — issue them together rather than in sequence.

## Audience voice

Comments on Instagram and TikTok posts are fenced out of the default read so they don't drown brand analysis. To read them, ask for the discussion class explicitly: `analyze({ feedTypes: ["discussion"], includeComments: true, platformFilter: ["instagram"] })`, one call per platform. Reddit threads are always readable. Amazon product reviews land the same way — read them with `query_items({ feedType: ["discussion"], platform: "reviews" })`. Bringing new comments or reviews into the pool goes through `fetch_comments` / `fetch_reviews`, which quote first and charge only on a confirmed call; relay the exact figure the quote returns and wait for the user's yes.

## Read the envelope, not just the rows

- `scopeEmpty` means the project has no sources yet. Check `get_project` and offer to pull rather than reporting "nothing found".
- `totalEstimated` and `hasMore` say whether your page is the whole answer. Page with `nextOffset` before generalizing.
- `access` counts flag sources that are stale or never acquired — say so when the numbers depend on them.
- On ranking-shaped aggregates, `rows` cleared the reliability floor and `directionalRows` did not. Draw the ranking from `rows`; cite the rest as directional with their `n`.

## Curating

`save_to_collection({ projectId, collectionName, itemIds })` saves items into a named collection in the project's portfolio, creating it if needed. Item ids must come from reads in that same project. `list_collections` and `get_collection` bring a collection back, and its item ids feed straight into `analyze({ itemIds })` for a deep dive. Save the examples worth revisiting as you find them, not at the end.

## Error recovery

- **Zero items.** Broaden before concluding: drop the platform filter, widen the dates, remove the label filter. Then check `get_project` — the scope may cover sources whose data was never acquired.
- **`list_labels` returns nothing.** The scope has items but no analysis yet. Read on engagement, platform, and recency instead of label dimensions.
- **A label filter matches nothing.** The dimension or value name is off. Re-check it against `list_labels` rather than guessing a variant.
- **A brand name comes back unresolved.** The project doesn't track it. The response lists what IS in scope — offer that, or offer to add the brand and pull its data.
