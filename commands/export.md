---
name: export
description: Turn a scoped read into a table or CSV, with honest coverage
argument-hint: "<what to export>"
---

When the user invokes `/export`, you build the file yourself from what the read tools return. Every row you write has to come from a tool result, and the file has to say what it covers.

## 1. Decide what a row is

Ask that first, because it picks the tool:

- **One row per post** — `analyze({ projectId, query, distribution: "exhaustive", sortBy })`. The ranked page over the full filtered set, with the creative fields on each row (`hookMechanism`, `creativeConcept`, `oneLineInsight`, and more). Use `fields` to name exactly the columns you want.
- **One row per post, metrics only** — `query_items({ projectId })`, when the export is engagement rather than creative. Returns `itemId`, `externalUrl`, `platform`, `brand`, `feedType`, `mediaType`, `headline`, `firstActiveAt`, `lastActiveAt`, `likes`, `views`, `comments`, `shares`, the lift multiples (`likesMultiple`, `viewsMultiple`, `commentsMultiple`, `sharesMultiple`, `longevityMultiple`), `isOutlier`, `boosted`, and the source baselines (`sourceAvgLikes`, `sourceMedianLikes`, `sourceItemCount`). Set `includeAnalysis: true` to add `hookCategory`, `mainMessage`, `narrativeStyle`, and `emotionalMood`.
- **One row per label value** — `get_table_data({ projectId, rows, metrics })`. A pivot: `count`, `useRate`, `medianLikes`, `medianViews`, `medianShares`, `viralRate`, optionally pivoted across `columns` (`brand`, `platform`, `feedType`, `mediaType`, `timePeriod`, or `focalVsRest` with a `focalBrand`). Discover the row dimensions first with `listDimensions: true` or `list_labels`.
- **One row per group** — `aggregate({ projectId, groupBy, measures })`. Time series and dimensional cuts with your own measures, each row carrying its `n`.

## 2. Page until you have the set, or admit you did not

This is where exports go wrong. Every reader returns a page, not the world:

- `analyze` in exhaustive mode returns `itemsReturned`, `totalEstimated`, `hasMore`, and `nextOffset`, and caps at 80 items per call. It may also come back `byteTruncated: true`, meaning the server packed fewer items than the page held — continue from `nextOffset` rather than assuming the page was the limit.
- `query_items` returns `fetchedCount`, `totalEstimated`, `hasMore`, and `nextOffset`. Its `limit` goes to 500 (default 80). Loop with `offset: nextOffset` while `hasMore` is true.
- `get_table_data` returns `totalRows`, `rowOffset`, and `hasMoreRows` for paging (`topN` rows at a time, default 15, max 50), plus `scanned`, `totalInScope`, and `scanCapped`. It builds the pivot from a bounded working set of labeled items, so when `scanCapped` is true the percentages describe what was scanned, not the whole scope — say which.
- `aggregate` takes a `limit` up to 5,000, default 200. Its `total` and `totalGroups` count *groups*, not items; the item count behind each group is that row's `n`.
- `search_all` caps at 50 results and takes no offset, so its `hasMore` tells you the answer was cut off, not how to continue. Reach for `analyze` in exhaustive mode when the export needs the whole match set.

If a `totalEstimated` comes back `null`, you do not know the denominator — say "at least N", never "N total".

## 3. Write the file

Build the table from the returned rows and nothing else. Do not compute a column the tools did not give you, and do not fill a blank cell with a plausible value — an empty cell is the honest answer. Keep `itemId` and `externalUrl` in a post-level export so every row is traceable back to the post.

CSV for spreadsheets, a markdown table for something read in the conversation. Ask which one only if the destination is unclear.

## 4. State the coverage in the file

Put a header block at the top of the file, or a short note next to a markdown table, that answers four things without the user having to ask:

- **How many rows, of how many.** "412 rows — all items matching the filter" or "80 rows of 1,240 matching items, ranked by likesMultiple."
- **What the scope was.** The project name, and the sources it covers, from `get_project`. If the project's scope is empty, it read the portfolio's whole tracked universe — say that.
- **How fresh it is.** `get_project` reports `expiredSources` with the date their coverage ends and `ungrantedSources` that are tracked but not acquired. A source covered only through March cannot contribute an April row.
- **What is structurally missing.** Reads flag this in `dataNotes` — Facebook Ad Library items carry no engagement data, Reddit view counts come back as zero. A zero in an engagement column is not a performance finding when the platform never reported the number.

## 5. Offer the gap, do not close it silently

If the export is thin because sources are stale or untracked, name them and offer to fix it: `pull_data({ projectId, candidates })` quotes the gap for free and attaches whatever the pool already covers. Show the credit cost and get a yes before `confirm_pull`. Never widen an export by spending on the user's behalf.

## Sharing inside the app

A curated set of posts travels better as a collection than as a file. `save_to_collection({ projectId, collectionName, itemIds })` puts the items in the project's portfolio, where the team can review them in Adology; `list_collections` and `get_collection` read them back.
