# Available Fields Reference

What the server actually serves: the fields on an item, the filters each reader accepts, and the page limits. Every read is scoped by `projectId`.

## Item fields

### Base set — always returned by `analyze`

`id`, `brand`, `feedType`, `platform`, `headline`, `likes`, `views`, `shares`, `comments`, `engagementScore`, `isOutlier`, `outlierType`, `likesMultiple`, `createdAt`, `url`, `thumbnail`

Omit `fields` entirely and the item comes back with every analysis field it carries. Pass `fields` and you get the base set plus exactly what you named. Null and near-zero values are stripped, and `headline` is capped at 200 characters.

`engagementScore` is the interactions composite — likes + comments + shares. `createdAt` is the item's last active date. `isOutlier` marks a statistical standout and `outlierType` says whether it was engagement or longevity that made it one.

### Paid vs organic

`query_items` and `aggregate` carry the brand's own boosted declaration: every `query_items` row has a `boosted` flag, and both tools take `excludeBoosted: true` for an organic-only read. The rule is evaluated live from the brand's context, so posts fetched after it was written are classified without re-saving anything. When you exclude boosted posts, say so alongside the numbers.

### Performance and baseline fields (request via `fields`)

| Field | What it tells you |
|-------|-------------------|
| `viewsMultiple`, `commentsMultiple`, `sharesMultiple` | Item metric vs its source's baseline |
| `longevityMultiple` | Days alive vs the source's average |
| `sourceMedianLikes`, `sourceMedianViews`, `sourceMedianComments`, `sourceMedianShares` | The denominators behind the multiples |
| `sourceAvgLikes` | Source average likes |
| `sourceItemCount` | How many items back that baseline |
| `mediaType` | `image` or `video` |

Multiples are size-agnostic: 3x means the same on a 1K-follower account as on a 1M one. Never present a multiple without its `sourceMedian*` baseline. A multiple is null until the baseline batch has run for that source — sort by a `*Multiple` key to surface the rows that carry lift.

### Creative analysis fields (request via `fields`)

Not every item carries every field. Ad-schema items and organic creator items are analyzed by different prompts, so creator fields resolve to null on ads and vice versa.

**Content** — `transcript`, `adDescription`, `descriptionOfAd`, `contentSummary`, `descriptionOfScenes`, `mainMessage`, `oneLineInsight`, `noteworthy`, `collectiveMeaning`

**Hook** — `hookMechanism`, `hookCategory`, `hookVideoMechanism`, `hookImageMechanism`, `tagsHook`

**Visual** — `visualDescription`, `detailedVisualDescription`, `visualConcept`, `colorScheme`, `background`, `visualObjects`, `visualTechniques`, `cameraTechniques`, `textInFrame`, `tagsVisual`

**Creative and narrative** — `creativeConcept`, `creativeExecution`, `creativeRationale`, `narrativeStyle`, `narrativeFormat`, `productionStyle`, `tagsProduction`

**Emotion** — `emotionalMood`, `emotionalStrategy`, `emotionalTones`, `emotionalTension`, `humor`, `tagsEmotional`

**Strategy and positioning** — `brandPositioning`, `competitiveContext`, `strategyFunction`, `uniqueSellingProposition`, `messagingUsp`, `messagingMessageTypes`, `problemStatement`, `demandStyle`, `audienceActivation`, `interpretiveRisk`, `tagsPersuasive`

**Audience and product** — `targetAudienceAge`, `targetAudienceGender`, `targetAudienceLifestyle`, `productDescription`, `productBenefits`, `productDisplayStyle`, `categoryEntryPoints`, `features`

**CTA and offer** — `ctaText`, `ctaFraming`, `offerType`, `offerDelivery`

**Creator and community** (organic items) — `creatorType`, `creatorPersona`, `creatorSelfNarrative`, `creatorTargetCommunity`, `creatorAuthorityBasis`, `contentType`, `primaryTopic`, `viewerValue`, `worldview`, `captionStyle`, `rhetoricDevices`, `interactionBait`, `authenticitySignals`, `authenticityScore`, `authenticityRationale`, `integrityScore`, `communityMarkers`, `hashtags`, `links`, `location`, `tagsCreatorStyle`, `tagsCommunity`, `tagsContentType`, `tagsIntent`

**Commercial and trend signals** — `monetizationSignals`, `isCommercial`, `isAdvertisement`, `contentRating`, `sensitiveContent`, `trendName`, `trendParticipation`, `seriesContext`

### Label dimensions (via `labelFields`)

Which dimensions exist depends on what has been analyzed in this project — there is no fixed list. Call `list_labels({ projectId })` (or `get_table_data({ projectId, listDimensions: true })`) and use the names it returns. `labelFields: []` suppresses labels; omitting it returns all of them.

### `query_items` row shape

`query_items` returns a fixed row rather than a selectable one: `itemId`, `externalUrl`, `platform`, `format`, `feedType`, `brand`, `firstActiveAt`, `lastActiveAt`, `headline`, `mediaType`, `likes`, `views`, `comments`, `shares`, the five `*Multiple` keys, `isOutlier`, `outlierType`, `sourceAvgLikes`, `sourceMedianLikes`, `sourceItemCount`, and `boosted`. Set `includeAnalysis: true` to add `hookCategory`, `mainMessage`, `narrativeStyle`, `emotionalMood`. Review items also carry `rating`, `reviewer`, and `product`.

## Filters by tool

The same concept has different parameter names per reader.

| Concept | `analyze` | `query_items` | `aggregate` (under `filters`) | `get_table_data` |
|---------|-----------|---------------|-------------------------------|------------------|
| Platform | `platformFilter: string[]` | `platform: string` (one) | `platform: string[]` | `platforms: string[]` |
| Entity / brand | `feedNames: string[]` | `brand: string[]` | `brand: string[]` | `brands: string[]` |
| Feed type | `feedTypes: string[]` | `feedType: string[]` | `feedType: string[]` | `feedTypes: string[]` |
| Media | `mediaTypeFilter: "video"\|"image"` | `mediaType: "video"\|"image"` | `format: string[]` | `mediaTypes: ("video"\|"image")[]` |
| Dates | `startDate` / `endDate` | `startDate` / `endDate` | `from` / `to` (half-open) + `timeField` | `startDate` / `endDate` |
| Labels | `labelFilter: {dimension,value}` or `{filters,mode}` | `labelFilters: [{category,values}]` + `labelMode` | — | `labelFilter: {filters,mode}` |
| Lift threshold | `outlierFilter: {metric, multipleGreaterThan}` | `outlierMetric` + `minOutlierMultiple` | — | — |
| Keyword | `query` (+ `mode:"semantic"` for meaning) | `query` | — | — |
| Paid vs organic | — | `excludeBoosted: true` | `excludeBoosted: true` | — |
| Comments | `includeComments: true` | `feedType: ["discussion"]` | `feedType: ["discussion"]` | — |

**Platforms:** `facebook`, `instagram`, `tiktok`, `youtube`, `twitter`, `linkedin`, `reddit`, `threads`.

**Feed types:** `brand`, `influencer`, `search`, `discussion`.

**Dates** are ISO-8601 strings. In `aggregate`, `from` is inclusive and `to` is exclusive.

**Defaults worth knowing.** `analyze`'s sampled distributions restrict to the creative feeds (brand and influencer) when `feedTypes` is omitted; `distribution:"exhaustive"` applies no such default. Semantic mode pushes down `platformFilter`, `feedTypes`, the date range, and `includeComments` — the other filters do not reach the search, so apply them by re-reading the hits rather than assuming they were honored.

**`search_all`** takes only `query`, `platformFilter`, and `limit`, and returns a compact row: `citation`, `itemId`, `platform`, `brand`, `headline`, `likes`, `views`, `likesMultiple`, `url`. Use `analyze` when you need fields, labels, or date and media filters.

## Sort keys

`query_items` (`sortBy`) and `analyze` with `distribution:"exhaustive"` (`sortBy`) share one key set:

`lastActiveAt` (default), `firstActiveAt`, `firstScrapedAt`, `likes`, `views`, `comments`, `shares`, `likesMultiple`, `viewsMultiple`, `commentsMultiple`, `sharesMultiple`, `longevityMultiple`

Engagement keys rank by absolute counts; `*Multiple` keys rank by lift against the source baseline. In the sampled distributions, `sortMetric` (`engagement`, `likes`, `views`, `shares`, `comments`) picks what `distribution:"top"` means.

## Aggregate vocabulary

- **`groupBy`** — `platform`, `brand`, `feedType`, `format`, `time`. Include `time` and set `timeBucket` to `day`, `week`, `month`, `quarter`, or `year`.
- **`filters.timeField`** — `lastActiveAt` (default), `firstActiveAt`, `firstScrapedAt`.
- **`measures`** — each takes `field` (`likes`, `views`, `comments`, `shares`, `engagementTotal`, or `*`) or a custom `expr` over those metrics with `+ - * /`, plus `fn` (`sum`, `avg`, `median`, `count`, `min`, `max`) and an optional alias `as`. An `expr` requires `as`.
- **`having`** — post-grouping filter on a measure alias, e.g. `[{measure:"n", op:">=", value:5}]`.
- **`sort`** — by a dimension name or a measure alias, `asc` or `desc`.

Every row carries `n`, the item count behind it, whether or not you asked for a count. `groupBy: ["brand"]` spans all feed types, so discussion sources appear under their subreddit name; add `filters.feedType: ["brand"]` for a competitor-only cut.

## Pivot vocabulary (`get_table_data`)

- **`rows`** — one label dimension, or two for a composite table.
- **`columns`** — `brand`, `platform`, `feedType`, `mediaType`, `timePeriod`, `focalVsRest`, or `none` (default). `timePeriod` needs `timePeriod: {granularity}` (`week` | `month` | `quarter`); `focalVsRest` needs `focalBrand`, and `expandRest: true` breaks out the other brands.
- **`metrics`** — up to four of `count`, `useRate`, `medianLikes`, `medianViews`, `medianShares`, `viralRate`. Default `["count","useRate"]`. The medians exclude zero-engagement Ad Library items; the counts include every labeled item.

## Page limits

| Tool | Page size | Paging |
|------|-----------|--------|
| `analyze` | default 40, max 80 | `offset` up to 4000; read `itemsReturned`, `hasMore`, `nextOffset` |
| `query_items` | default 80, max 500 | `offset`; read `fetchedCount`, `totalEstimated`, `hasMore`, `nextOffset` |
| `aggregate` | default 200 rows, max 5000 | — |
| `get_table_data` | `topN` default 15, max 50 | `rowOffset` |
| `list_labels` | 30 dimensions, 10 values each (`topValuesPerDimension` max 20) | `offset`, `hasMore` |
| `search_all` | default 20, max 50 | `totalEstimated`, `hasMore` |

`analyze` fits its page to a response-size budget, so a call can return fewer items than `limit` — loop on `nextOffset` until `hasMore` is false rather than assuming the first page is the whole set.

## Retrieval strategy

1. **Orient** — `get_project` for what the scope covers, in parallel with `list_labels` for the dimensions available.
2. **Quantify** — `aggregate` or `get_table_data` for the shape of the whole set. Grouped rows are cheap; items are not.
3. **Illustrate** — `analyze` with targeted filters and a short `fields` list on the items that matter.
4. **Deep dive** — `analyze({ itemIds })` on the three to five posts you will actually cite.

Fetch grouped math before item pages, keep `fields` narrow once you know what you are looking for, and summarize between batches on large sets rather than holding hundreds of items at once.

## Notes on missing values

Some platforms simply don't report a metric: Facebook Ad Library items carry no engagement data, and Reddit view counts are unavailable. `get_table_data`'s medians exclude those no-signal items rather than counting them as zero, while `count`, `useRate`, and `viralRate` include every labeled item — so a median and a count over the same cell can rest on different denominators. Say which you are quoting.

Fields resolve to null when the item's analysis doesn't carry them — `transcript` on an image post, creator fields on an ad, any analysis field on an item that hasn't been analyzed yet. Skip those items rather than treating a null as a finding, and check `access` in the response envelope when a whole source looks empty: it may be tracked but never acquired.
