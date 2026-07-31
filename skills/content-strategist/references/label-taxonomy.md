# Working With Labels

Adology classifies content along label dimensions — the structural axes of a creative, such as its hook, its emotional register, its production style. Those dimensions are built for the portfolio they belong to, so the set that exists in one project is not the set that exists in another. A beverage brand's taxonomy and a B2B software brand's taxonomy describe different things, and both are correct for their category.

The rule that follows: **discover the dimensions live, then filter on what you found.** A dimension name you assumed rather than read matches nothing — the filter is required, so the read comes back empty ("No items matched the label filter") even when the scope is full of relevant items.

## Discover what this project carries

`list_labels` with `{ projectId }` is the census. It is much lighter than a content read and it is the right first call before any label work.

```
list_labels({ projectId, topValuesPerDimension: 10, limit: 30, offset: 0 })
```

- `dimensions` comes back compact — each entry is the dimension name, its number of distinct values, and its top values with item counts, ordered by how heavily each dimension is used.
- `totalDimensions` and `hasMore` tell you whether 30 covered it; page with `offset`.
- `labeledItems` is the number that matters for honesty: it is how much of the scope any distribution you report actually describes.
- `feedTypes` narrows the census to a content class — creative feeds carry different dimensions than discussion items do.
- If the project has no labeled items yet, the call says so directly. That means the scope needs data (`pull_data` → `confirm_pull`, quoted and approved) or that labeling has not finished, and it is a finding to relay rather than a hole to write around.

Names come back in display form — `Hook`, not `Hook#1`. Use that display form everywhere: in filters, in `focusCategories`, and in what you write.

For a second census that respects the filters you are about to apply, `get_table_data` with `{ projectId, listDimensions: true }` returns the dimensions present within that filtered set, with counts. It answers "which dimensions survive once I cut to TikTok video from the last 90 days", which is often a smaller list than the project-wide census.

## Filter by a dimension and value

The three readers take label filters in slightly different shapes. Match the shape to the tool.

`analyze` accepts a single-dimension form or a multi-dimension one:

```
analyze({ projectId, query: "...", labelFilter: { dimension: "Hook", value: "Question" } })

analyze({ projectId, query: "...", labelFilter: {
  filters: [
    { dimension: "Hook",    values: ["Question", "Bold Claim"] },
    { dimension: "Emotion", values: ["Humorous"] }
  ],
  mode: "and"
}})
```

Values inside one dimension are combined with OR. `mode` combines across dimensions — `"and"` (the default) requires every dimension to match, `"or"` accepts any.

`get_table_data` takes the same multi-dimension shape under `labelFilter: { filters, mode }`, applied before the table is computed.

`query_items` uses its own naming — `labelFilters: [{ category: "Hook", values: ["Question"] }]` with `labelMode: "and" | "or"`. Same semantics, different key: `category` there, `dimension` in the other two.

To control which dimensions ride along on returned items rather than which items come back, use `labelFields` on `analyze`. It is an independent axis from `fields`.

## Quantify a dimension

`get_table_data` is the pivot. `rows` takes one dimension, or two for a composite read:

```
get_table_data({
  projectId,
  rows: ["Hook"],
  columns: "brand",
  metrics: ["count", "useRate", "medianLikes", "viralRate"],
  topN: 15,
  sortBy: "medianLikes",
  sortOrder: "desc"
})
```

- `columns` slices the table by `brand`, `platform`, `feedType`, `mediaType`, `timePeriod` (pair with `timePeriod: { granularity }`), or `focalVsRest` (pair with `focalBrand`, and `expandRest` to break the rest out by brand).
- `metrics` picks up to four of count, useRate, medianLikes, medianViews, medianShares, viralRate.
- `brands`, `platforms`, `feedTypes`, `mediaTypes`, `startDate`, `endDate` narrow the item set first.
- `topN` and `rowOffset` page the rows.

`rows: ["Hook", "Emotion"]` gives the composite cut — which pairing over-indexes, not just which single value does. Treat a combination as real only when enough items sit behind it; a cell with two items is a curiosity.

## Separate correlation from lift

A high median inside a distribution can come from the dimension itself or from whoever happens to use it. `get_creative_dna` separates the two, returning marginal averages beside controlled ridge-regression coefficients, per-brand advantages and gaps, and a ranked set of lean-in and cut-back moves with evidence post ids.

```
get_creative_dna({ projectId, metric: "like", focusCategories: ["Hook", "Emotion"], excludeBoosted: true })
```

`focusCategories` takes display names. One category anchors the analysis; two or more lock a grid; omitting it lets the analysis expand on its own. `metric` selects which engagement signal is being explained — `"view"` for reach questions, `"engagement_total"` for the interactions composite. Combinations whose confidence does not clear the brand's measurement bar are withheld rather than shown hedged, and the provenance footer says when that happened.

## Read label numbers honestly

- `useRate` is a share of **labeled** items, not of all items. When `labeledItems` is well below the scope's item count, say what the distribution covers.
- The medians exclude items that report no engagement signal at all, so they describe items that actually carry the metric rather than being dragged toward zero by items that never reported one.
- A dimension present on a handful of items is not a pattern. Name it as an emerging signal with its count, or leave it out.
- Distributions describe co-occurrence. The moment you write "drives" or "causes", you owe the reader either a controlled-lift result or a softer verb.
- Add `excludeBoosted: true` when the question is about organic performance, and say that you did — it changes what the numbers mean.

## Turn a distribution into a brief

A label finding is the start of the work, not the end of it. Take the value that leads its dimension, filter to it, read three to five of the items behind it, and describe what those creatives actually do — the opening line, the framing, the pacing, the claim. The dimension tells the team where to aim. The creative tells them what to make.
