# Analysis Patterns

Composed workflows for competitive analysis inside a project's scope. Each one names the calls that run together, what to do when the data is thin, and where it ends.

**Core principle:** labels tell you which category a creative belongs to. The creative itself — transcript, hook, visual description — tells you why it worked. Every pattern here ends in reading items, not in reporting a distribution.

All of these read what is already in the pool. Nothing here spends credits; acquiring new data is `pull_data` → `confirm_pull`, quoted and approved by the user first.

## Hook analysis

What openings earn attention in this set, and what the winning ones actually say.

**Together, first turn:**

- `list_labels` with `{ projectId }` — see whether this project carries a hook dimension at all, and how many items are labeled.
- `analyze` with `{ projectId, query: "opening hooks", distribution: "exhaustive", sortBy: "likesMultiple", limit: 40, fields: ["hookMechanism", "hookCategory", "transcript", "oneLineInsight"] }` — the ranked lift page with the creative attached.
- `aggregate` with `{ projectId, groupBy: ["brand"], measures: [{ field: "*", fn: "count", as: "n" }, { field: "likes", fn: "median", as: "medLikes" }] }` — who is even in this set, and at what scale.

**Then quantify.** `get_table_data` with `{ projectId, rows: ["Hook"], metrics: ["count", "useRate", "medianLikes", "viralRate"], topN: 15 }`, using whatever the hook dimension is actually called in this project.

If that dimension is absent or barely populated, drop the distribution step and work from lift alone: `analyze` with `outlierFilter: { metric: "likes", multipleGreaterThan: 3 }`, then read what comes back. Say in the answer that hook categories were unavailable and the read is from the creative itself.

**Then read.** `analyze` with `{ projectId, itemIds: [...] }` on the top three to five, and describe the opening line, the first visual, and the turn. Finish by connecting the two layers — the distribution says which family wins, the creative says which move inside that family does the work.

**End:** `save_to_collection` with `{ projectId, collectionName: "Hook studies", itemIds }`.

## Production and format comparison

**Together:** one `aggregate` grouped by `["platform"]` and another by `["format"]`, both with `measures: [{ field: "*", fn: "count", as: "n" }, { field: "likes", fn: "median", as: "medLikes" }]`, plus `analyze` with `distribution: "top"` and `fields: ["creativeConcept", "creativeExecution", "productionStyle", "visualDescription"]`.

Compare formats within a platform, never across platforms on raw counts — use the lift multiples for anything cross-platform. If one format holds most of the set, analyze the minority formats separately rather than letting the majority set the baseline. If a format has only a handful of items, `aggregate` places it in `directionalRows` on a ranking call, and that is where it should stay in your answer too.

**End:** save the clearest example of each format.

## Finding breakout content

The valuable question is not what performs well on average, but why a specific post broke out.

**Isolate the outliers.** `analyze` with `{ projectId, query: "breakout posts", distribution: "exhaustive", sortBy: "likesMultiple", outlierFilter: { metric: "likes", multipleGreaterThan: 5 }, fields: ["transcript", "hookMechanism", "adDescription", "sourceMedianLikes", "sourceItemCount"] }`. If fewer than three come back, lower `multipleGreaterThan` to 2 rather than widening the scope.

Check concentration before drawing anything: `aggregate` grouped by `["brand"]` over the same window. If one brand owns most of the outliers, say so, then re-run the read with `feedNames` set to the others.

**Read them in one turn** with `analyze` and `itemIds`, then get the contrast — the same brand's ordinary posts, via `analyze` with `distribution: "recent"` and `feedNames` set to that brand. The insight lives in the difference between the breakout and the brand's own baseline, not in the breakout alone.

**End:** save the outliers with a note naming the pattern.

## Covering a large scope

`analyze` returns the largest page that fits its response budget (default 40 items, max 80). For a full sweep, use `distribution: "exhaustive"` with a stable `sortBy`, keep `fields` tight so more rows fit, and loop on `offset: nextOffset` until `hasMore` is false. `totalEstimated` tells you up front how big the job is.

When you only need the flat post list with lift and no creative text, `query_items` covers the same ground with a larger page (`limit` up to 500) and `includeAnalysis: true` for a light analysis join. Use it for counting and ranking, and switch to `analyze` the moment you need to read the creative.

Some fields are null on some items — a transcript on an image post, a lift multiple on a source with no computed baseline. Skip those items quietly and work with the ones that carry the data; report the absence only when it is systematic.

## Brand versus brand

**Together:** `analyze` with `{ projectId, feedNames: ["Brand A"], distribution: "top", limit: 20 }` and the same call for Brand B, plus `get_table_data` with `{ projectId, rows: ["Hook"], columns: "focalVsRest", focalBrand: "Brand A", metrics: ["useRate", "medianLikes"] }`, which measures the focal brand against everyone else in one table.

If the two brands have very different item counts, weight the conclusions accordingly and say so. If they live on different platforms, compare only lift multiples, with their baselines cited.

Any brand you name must be tracked in the project. On `query_items`, a `brand` that does not resolve returns `entityScope` with `unresolved` and what is `inScope` — relay that instead of answering with a scope-wide ranking. On `analyze` and `get_creative_dna`, an unresolved `feedNames` just returns no items, so verify the name against the tracked roster before reading an empty result as silence.

**End:** save a curated set that shows the contrast, not just the winners.

## Controlled lift with creative DNA

Distributions tell you what co-occurs with performance. `get_creative_dna` tells you what survives controlling for everything else.

`get_creative_dna` with `{ projectId, metric: "like", focusCategories: ["Hook", "Emotion"], startDate, endDate }` returns marginal averages beside ridge-regression coefficients, per-brand advantages and gaps, a trajectory section comparing the window against the equal-length prior window when both dates are set, and prioritized lean-in and cut-back moves with evidence post ids.

Use the display name of a dimension, not its discriminator form — "Hook", not "Hook#1". One category anchors the analysis; two or more lock a grid. Add `excludeBoosted: true` when the question is about what wins organically, and say that you did.

Feed the evidence post ids straight into `analyze` with `itemIds`. The coefficient tells you a lever exists; the creative tells you how to pull it.

## Trend over time

`aggregate` with `{ projectId, groupBy: ["time"], timeBucket: "week", measures: [{ field: "*", fn: "count", as: "n" }, { field: "likes", fn: "median", as: "medLikes" }], filters: { from, to, timeField: "lastActiveAt" } }`. Add `"brand"` to `groupBy` to see who drives a shift.

Before making a trend claim, check freshness. `get_project` lists `expiredSources` with the date their coverage ends; a series that flattens at the end usually means coverage stopped, not that the category went quiet. Say which it is, and offer `pull_data` to refresh.

## Audience voice

Discussion items — Reddit threads, comments, reviews — are a separate class, and creative reads fence them out by default so they do not crowd a hooks-and-concepts sample. To read them, ask for them: `analyze` with `{ projectId, feedTypes: ["discussion"], includeComments: true, platformFilter: ["instagram"] }`, or `query_items` with `{ projectId, feedType: ["discussion"], platform: "instagram" }`. Without the discussion class the reader returns nothing, even when the items are there.

If the project has no comment or review data yet, `fetch_comments` and `fetch_reviews` acquire it. Both charge credits and both quote first, but their confirm shapes differ. `fetch_comments`: the preview call (no `confirmedByUser`) returns a quote with a `quoteToken`; confirm with `confirmedByUser: true`, that exact `quoteToken`, and `maxCredits` set to the approved amount, keeping the same sources and budget you quoted. `fetch_reviews`: the unconfirmed call refuses with the cost in its message (there is no token); confirm with `confirmedByUser: true` and `maxCredits` at the approved amount. In both, if the run would cost more than `maxCredits`, nothing is charged and a requote comes back to re-confirm.

## Report structure

1. **What the read covers** — the project's scope, the window, the sample size, and any coverage gap from `get_project`. One short paragraph, not a section.
2. **What is working** — start from the outliers you actually read. Describe what the creatives do, with the lift and its baseline.
3. **The patterns behind it** — the three to five distributions that carry the story, with `n` on each. Groups below the reliability floor appear as directional context or not at all.
4. **Where the focal brand stands** — the focal-versus-rest comparison, with uneven sample sizes called out.
5. **Deep dives** — three to five items examined closely: the opening, the structure, the offer, and why it works.
6. **Whitespace** — techniques that perform in the category and the focal brand has not used.
7. **Recommendations** — each tied to a specific item and a specific number, briefable as written.
8. **The gallery** — `save_to_collection` with everything you cited, so the user can browse the evidence.

## Metric glossary

| Metric | What it tells you |
|--------|-------------------|
| `likesMultiple`, `viewsMultiple`, `commentsMultiple`, `sharesMultiple` | The item's metric against its own source baseline — the only cross-account comparison that holds. Null means the source has no computed baseline yet. |
| `longevityMultiple` | How long the item stayed active against its source norm. High longevity is an evergreen signal. |
| `isOutlier`, `outlierType` | Pre-computed breakout flag, and whether the breakout was engagement or longevity. |
| `sourceMedianLikes`, `sourceMedianViews`, `sourceMedianComments`, `sourceMedianShares`, `sourceItemCount` | The denominators behind the multiples. Cite the baseline every time you cite a lift. |
| `n` (on `aggregate` rows) | Items behind the group, always computed. Compare it against `reliabilityFloor` before treating a row as a finding. |
| `useRate` (on `get_table_data`) | Share of labeled items carrying the value — context for performance. Low use plus high performance is an opportunity. |
| `viralRate` (on `get_table_data`) | Share of items with the value that broke out. |
| `medianLikes`, `medianViews`, `medianShares` (on `get_table_data`) | Medians over items with a real engagement signal; items reporting none are excluded rather than counted as zero. |
| `totalEstimated`, `hasMore`, `nextOffset` | Whether you saw the whole set or a page of it. |
| `labeledItems` (on `list_labels`) | How much of the scope any label distribution actually describes. |
