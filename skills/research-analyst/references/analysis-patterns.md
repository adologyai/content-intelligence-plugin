# Analysis Patterns

Executable workflows for competitive analysis and reporting. Every pattern specifies which steps run in parallel, what to do when data is insufficient, and ends with saving results.

**Core principle:** Labels tell you WHAT category a creative falls into. The actual content (transcript, hook, visual description) tells you WHY it works. Always dig into items, not just report label stats.

## Hook Analysis

Identify which opening techniques drive the most engagement.

**Step 1 (PARALLEL):**
- `get_items` with `fetchMethod: "top"`, `distribution: "balanced"`, limit=50
- `aggregate_items` with `groupBy: "Hook"`
- `list_labels` to see available hook subcategories

**Step 2:** Filter for items where `isOutlier: true` from the Step 1 results.

- IF < 5 outliers → expand to items with `likesMultiple > 2.0`
- IF no hook labels on items → skip to Step 3 using engagement multiples only, warn about label gaps

**Step 3 (PARALLEL):** `get_item_detail` on the top 3-5 outliers. Read the actual hooks — the transcript's first 2-3 seconds, the hookMechanism field, the opening visual.

**Step 4:** Connect content to labels. "Question hooks get 1.8x avg, and the top-performing ones specifically open with a personal vulnerability question before pivoting to product."

**Step 5:** `save_to_collection` with the standout hook examples. Share the collection URL.

**Anti-pattern:** Do not just report "Question hooks get 1.8x avg." That is a label stat anyone can see. Describe what the actual winning hooks SAY.

## Format Comparison

Compare creative formats by looking at real examples, not just labels.

**Step 1 (PARALLEL):**
- `get_items` filtered by each platform with `fetchMethod: "top"` (one call per platform, all parallel)
- `aggregate_items` with `groupBy: "Format"`

**Step 2 (PARALLEL):** `get_item_detail` on 3-5 items per format — look at transcript, visualDescription, adDescription.

- IF a format has < 5 items → note it as "limited sample" and do not draw conclusions
- IF one format dominates (> 70% of items) → flag the imbalance and analyze the minority formats separately

**Step 3:** Note production choices: pacing, talent usage, edit style. Check `VisualExecutionStyle` and `CreativeConcept` distributions for aggregate validation.

**Step 4:** Segment by platform — UGC performs differently on TikTok vs Instagram. Use multiples, not raw numbers, for cross-platform comparison.

**Step 5:** `save_to_collection` with the best example of each format.

## Finding Breakout Content

The most valuable analysis is identifying WHY specific posts broke out.

**Step 1 (PARALLEL):**
- `get_items` with `fetchMethod: "top"`, limit=50
- `aggregate_items` by Hook, Format, and Platform (three parallel calls)

**Step 2:** Filter for outliers (`isOutlier: true`). These are items that got 5x+ their source's average engagement.

- IF < 3 outliers → lower the threshold to `likesMultiple > 2.0`
- IF one brand owns > 60% of outliers → flag it, then re-analyze excluding that brand

**Step 3 (PARALLEL):** `get_item_detail` on 5-10 outliers (all parallel).

**Step 4:** Look for patterns across the outliers: common hooks, formats, topics, visual approaches, CTAs.

**Step 5:** Pull 3-5 LOW-performing items from the same brands via `get_items` with `fetchMethod: "bottom"`. The insight is in the DIFFERENCE between the outlier and the brand's typical content.

**Step 6:** `save_to_collection` with the outliers. Share the collection URL.

## Analyzing 150+ Items

For comprehensive analysis across many items, use a batch-and-summarize approach.

**Step 1 (PARALLEL):**
- `get_items` limit=50, fields=[], labelFields=[] (base set only, ~75KB)
- `get_items` limit=50, offset=50, fields=[], labelFields=[]
- `get_items` limit=50, offset=100, fields=[], labelFields=[]
- `aggregate_items` by 2-3 dimensions
- `list_labels`

This gives you 150 items scanned (~225KB) plus aggregate stats in a single turn.

**Step 2:** Scan headlines + adDescriptions from all three batches. Note interesting items and emerging patterns.

- IF patterns are unclear after 150 items → switch to targeted filters (specific brands, platforms, label values)
- IF a segment looks promising → `get_items` with specific `fields` (e.g., `["hookMechanism", "creativeConcept", "brandPositioning"]`) filtered to that segment

**Step 3 (PARALLEL):** `get_item_detail` on the 5-10 most interesting items from scanning.

**Step 4:** Synthesize scanning notes + deep reads + aggregate stats.

**Step 5:** `save_to_collection` with the curated standouts.

**When fields come back empty:** Some items may have null values for requested fields (e.g., `transcript` is null for image-only posts). Skip these items silently — do not report "field was empty." Focus on items where the requested data exists.

## Brand vs Brand Creative Comparison

Compare specific creative approaches between two or more brands.

**Step 1 (PARALLEL):**
- `get_items` with `feedNames: ["Brand A"]` limit=20, `fetchMethod: "top"`
- `get_items` with `feedNames: ["Brand B"]` limit=20, `fetchMethod: "top"`
- `aggregate_items` with `groupBy: "Hook"` (overall)
- `aggregate_items` with `groupBy: "Format"` (overall)

**Step 2:** Request strategy-relevant fields on the interesting items: `fields: ["hookMechanism", "creativeConcept", "narrativeStyle", "ctaText"]`.

- IF brands have very different item counts (e.g., 200 vs 30) → note the imbalance and weight conclusions accordingly
- IF brands are on different platforms → do not compare raw numbers. Use multiples only.

**Step 3 (PARALLEL):** `get_item_detail` on 3-5 standout items per brand (all parallel).

**Step 4:** Compare: what does Brand A do that Brand B does not? Where do they overlap? What is working for one but not the other?

**Step 5:** `save_to_collection` with a curated set showing the contrast.

## Cross-KS Research

Search beyond a single Knowledge Set for inspiration, benchmarks, or competitive examples.

**Step 1:** `content_intelligence_search` with a descriptive query. This searches the entire Adology database using AI aspect decomposition.

- IF < 5 results → try broader/different query terms
- IF results span many unrelated categories → narrow with more specific queries

**Step 2:** Examine results — they include full performance enrichment (`likesMultiple`, `isOutlier`, etc.).

**Step 3 (PARALLEL):** `get_item_detail` on the top 3-5 results for full creative context.

**Step 4:** Compare cross-KS findings with the user's KS-specific data. Are there patterns in the broader market that the user's brands are missing?

**Step 5:** `save_to_collection` with standout cross-KS items. Share the returned `url` deep link.

**Step 6:** Use findings to inform recommendations — "Across the broader market, testimonial hooks with before/after structure are getting 3.2x. Your brands have not tried this format."

## Proactive Competitive Alerts

Things to flag during any analysis, without being asked:

- **Temporal shifts** — if recent items (last 30 days) show different patterns than older items, call it out. "Short-form testimonials are emerging in the last month — they were not present 60 days ago."
- **Format emergence** — if a format has low `useRate` but high `timesCategoryAvg`, flag it as an opportunity. "Only 8% of content uses carousel format, but it gets 2.4x the category average."
- **Brand strategy shifts** — if a brand's recent content looks different from their historical patterns, note it. "Nike shifted from athlete-focused to community UGC in the last 3 weeks."
- **Competitive gaps** — labels where the focal brand underindexes vs the category. Use `focalBrandComparison` when available.
- **Engagement concentration** — if 1-2 posts account for a disproportionate share of total engagement, warn that averages may be misleading.

## Competitive Report Structure

A strong competitive report follows this flow. Include quality caveats at every stage.

1. **Landscape Overview** — brands, content volume, platform mix, date range. State the sample size and any coverage gaps ("Label coverage is 72% for hooks, 45% for format — hook analysis is high-confidence, format analysis is directional").
2. **What's Actually Working** — start with outliers and breakout content. Read the items. Describe what the winning creatives DO, not just their label categories. State how many outliers you examined.
3. **Category Patterns** — cherry-pick the 3-5 label distributions that tell a story. Use `timesCategoryAvg` and `viralityRate` to quantify. Skip categories with < 10 items. Note freshness ("based on content from the last N days").
4. **Brand Comparison** — how the focal brand indexes vs competitors. Use `focalBrandComparison` for label-level gaps. Note if brand sample sizes are uneven.
5. **Content Deep Dives** — pick 3-5 standout items and analyze them in detail. What is the hook? What is the narrative structure? What is the CTA? Why does it work?
6. **Whitespace** — labels with high performance but low usage by the focal brand. Content themes competitors own that the focal brand does not.
7. **Recommendations** — specific creative directions backed by both content examples AND performance data. "Do this [specific creative approach] because [specific example] got [X]x performance."
8. **Save & Share** — `save_to_collection` with all referenced standout items. Share the collection URL so stakeholders can browse the gallery.

## Key Metrics

| Metric | Why It Matters |
|--------|---------------|
| `timesCategoryAvg` | Normalizes for category baseline — shows true outperformance |
| `viralityRate` | Reveals which creative choices have breakout potential |
| `timesAccountAvg` | Size-agnostic performance signal for individual posts |
| `useRate` | Context for performance — low use + high performance = opportunity |
| `shareOfEngagement` | Shows which labels drive disproportionate engagement share |
| `likesMultiple` | Item likes divided by source baseline — >1 means outperforming |
| `viewsMultiple` | Item views divided by source baseline |
| `commentsMultiple` | Item comments divided by source baseline |
| `sharesMultiple` | Item shares divided by source baseline |
| `longevityMultiple` | How long the item sustained engagement vs source norm |
| `isOutlier` | Boolean flag for statistically significant outperformers |
| `outlierType` | "engagement" or "longevity" — what kind of outperformance |
| `sourceAvgLikes`, `sourceMedianLikes`, `sourceP90Likes` | Source baseline context for interpreting multiples |
