# Available Fields Reference

Reference for queryable fields, filter options, and data formats when browsing and exporting content from Adology.

## Field Selection

Use `fields` and `labelFields` params on get_items, search_items, analyze, get_item_detail.

### Base Set (always returned — no need to request)
`id`, `brand`, `feedType`, `platform`, `headline`, `likes`, `views`, `shares`, `comments`, `engagementScore`, `isOutlier`, `outlierType`, `likesMultiple`, `createdAt`, `adDescription`, `transcript`

### Content Analysis Fields
| Field | What it tells you |
|-------|-------------------|
| `hookMechanism` | How the hook grabs attention |
| `hookCategory` | Hook type classification |
| `visualDescription` | What the creative looks like |
| `visualConcept` | Visual concept/approach |
| `mainMessage` | Core message/takeaway |
| `creativeConcept` | Creative concept approach |
| `creativeExecution` | How the concept is executed |
| `creativeRationale` | Why this creative approach |
| `narrativeStyle` | Storytelling approach |
| `narrativeFormat` | Narrative structure |
| `productionStyle` | Production quality/approach |
| `emotionalMood` | Emotional tone |
| `emotionalStrategy` | Emotional persuasion approach |
| `emotionalTones` | Emotional tone tags |

### Strategy & Positioning Fields
| Field | What it tells you |
|-------|-------------------|
| `brandPositioning` | Brand positioning statement |
| `competitiveContext` | Competitive positioning |
| `strategyFunction` | Strategic purpose |
| `uniqueSellingProposition` | USP highlighted |
| `problemStatement` | Problem the ad solves |
| `demandStyle` | Push vs pull demand |
| `oneLineInsight` | One-line creative insight |
| `noteworthy` | What stands out |

### Audience & Product Fields
| Field | What it tells you |
|-------|-------------------|
| `targetAudienceAge` | Target age range |
| `targetAudienceGender` | Target gender |
| `targetAudienceLifestyle` | Target lifestyle/psychographic |
| `productDescription` | Product/service description |
| `productDisplayStyle` | How product is shown |
| `productBenefits` | Benefits highlighted |
| `categoryEntryPoints` | Category entry points |
| `features` | Product features |

### CTA & Offer Fields
| Field | What it tells you |
|-------|-------------------|
| `ctaText` | Call-to-action text |
| `ctaFraming` | CTA psychological framing |
| `offerType` | Type of offer |
| `offerDelivery` | How offer is delivered |

### Performance Fields
| Field | What it tells you |
|-------|-------------------|
| `viewsMultiple` | Views vs source average |
| `commentsMultiple` | Comments vs source average |
| `sharesMultiple` | Shares vs source average |
| `longevityMultiple` | Ad longevity vs source average |
| `sourceAvgLikes` | Source baseline avg likes |
| `sourceMedianLikes` | Source baseline median likes |
| `sourceP90Likes` | Source 90th percentile likes |
| `sourceItemCount` | Total items from this source |

### Label Dimensions (via `labelFields`)
**Standard taxonomy** (available on most KSs): Hook, Format, Emotion, Narrative, Production, Audio, Talent, Setting, Topic, Community, ContentType, CreatorIntent, CreatorPersona, DeliveryStyle, Editing, Mood, VisualStyle, Authenticity

**KS-specific** (discover via `list_labels`): Audience, Brand, CTA, Claims, Creative, DemandStyle, Features, Message, Offer, Persuasion, Problem, Solution, Trust, Visual, plus any custom dimensions

### Common Patterns
| Goal | fields | labelFields |
|------|--------|-------------|
| Quick scan | `[]` | `[]` |
| Hook deep dive | `["hookMechanism", "hookCategory"]` | `["Hook"]` |
| Creative strategy | `["creativeConcept", "narrativeStyle", "productionStyle"]` | `["Format", "Narrative"]` |
| Audience analysis | `["targetAudienceAge", "targetAudienceLifestyle"]` | `["Audience"]` |
| CTA optimization | `["ctaText", "ctaFraming", "offerType"]` | `["CTA"]` |
| Full creative review | `["hookMechanism", "visualDescription", "creativeConcept", "emotionalMood", "ctaText"]` | `["Hook", "Format", "Emotion"]` |
| Competitive positioning | `["brandPositioning", "competitiveContext", "uniqueSellingProposition"]` | `[]` |

### Retrieval Strategy

The agent can make multiple tool calls in parallel. Use this pattern for comprehensive analysis:

1. **Scan** — `get_items` limit=50, fields=[], labelFields=[] (~75KB, ~19K tokens)
2. **In parallel**: `aggregate_items` by relevant dimensions + `list_labels` to discover available dimensions
3. **Read** — `get_items` with targeted filters + specific fields + specific labelFields on the items that matter
4. **Deep dive** — `get_item_detail` on 3-5 specific items (returns all fields by default)

**Budget guide:**
- 3 calls of 50 base items = 150 items = ~225KB = ~56K tokens
- 5 calls of 30 selective items = 150 items = ~150KB = ~37K tokens
- For 200+ items, summarize between batches

## Item Fields

Every content item can include these fields (request via `fields` parameter):

### Identification

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | MongoDB document ID (hex string) |
| `brand` | string | Brand/feed name from knowledge set mapping |
| `feedType` | string | Feed category: `brand`, `influencer`, `search`, `discussion` |
| `platform` | string | Social media platform identifier |
| `sourceLabel` | string | Human-readable source label (e.g., "Meta Ad Library", "Instagram Profile") |

### Content

| Field | Type | Description |
|-------|------|-------------|
| `headline` | string | First 200 characters of post text |
| `transcript` | string? | Video/audio transcript (what is being said) |
| `adDescription` | string? | Best available ad summary/description |
| `url` | string | Direct URL to the original social media post |
| `thumbnail` | string | Public URL to the item's thumbnail image |
| `mediaType` | string | Media type of first asset: `image` or `video` |

### Engagement Metrics

| Field | Type | Description |
|-------|------|-------------|
| `likes` | number | Number of likes |
| `views` | number | Number of views |
| `shares` | number | Number of shares |
| `comments` | number | Number of comments |
| `engagementScore` | number | Composite: likes + views + shares |
| `engagementRate` | number? | (likes + comments) / views. Undefined if views = 0 |
| `timesAccountAvg` | number? | Post performance vs account average. 5.0 = 5x typical. Size-agnostic. |

### Performance Enrichment

Every item includes pre-computed performance multiples that compare the item's metrics to its source's baseline. These are size-agnostic -- a 3x likes multiple means the same thing whether the account has 1K or 1M followers.

| Field | Type | Description |
|-------|------|-------------|
| `likesMultiple` | number | Item likes / source median likes |
| `viewsMultiple` | number | Item views / source median views |
| `commentsMultiple` | number | Item comments / source median comments |
| `sharesMultiple` | number | Item shares / source median shares |
| `longevityMultiple` | number | Item days alive / source avg days alive |
| `isOutlier` | boolean | Pre-computed flag: true if the item is a statistical outlier |
| `outlierType` | string? | `"engagement"` or `"longevity"` -- what made it an outlier |

#### Source Baseline Context

Each item also carries the baseline stats for its source, so you can contextualize raw numbers without a separate lookup.

| Field | Type | Description |
|-------|------|-------------|
| `sourceItemCount` | number | Total items scraped from this source |
| `sourceAvgLikes` | number | Source average likes |
| `sourceMedianLikes` | number | Source median likes |
| `sourceStddevLikes` | number | Source standard deviation of likes |
| `sourceP90Likes` | number | Source 90th percentile likes |
| `sourceAvgViews` | number | Source average views |
| `sourceMedianViews` | number | Source median views |
| `sourceAvgComments` | number | Source average comments |
| `sourceMedianComments` | number | Source median comments |
| `sourceAvgShares` | number | Source average shares |
| `sourceMedianShares` | number | Source median shares |
| `sourceAvgDaysAlive` | number | Source average content longevity in days |

### Timing

| Field | Type | Description |
|-------|------|-------------|
| `createdAt` | string | ISO date string of post creation |

## Supported Platforms

| Platform ID | Display Name |
|-------------|-------------|
| `tiktok` | TikTok |
| `instagram` | Instagram |
| `youtube` | YouTube |
| `facebook` | Facebook |
| `twitter` | Twitter / X |
| `reddit` | Reddit |
| `linkedin` | LinkedIn |
| `threads` | Threads |

## Filter Options

### Feed Filter

Narrow results to specific feeds within a Knowledge Set:

- **paidBrandFeeds** -- Brand feeds filtered to Ad Library sources only
- **organicBrandFeeds** -- Brand feeds filtered to organic social sources only
- **personFeeds** -- Influencer feeds by name
- **searchFeeds** -- Search term feeds by term
- **discussionFeeds** -- Reddit subreddit feeds by name

### Platform Filter

An array of platform identifiers to include. When omitted, all platforms are included.

### Date Range

| Parameter | Format | Description |
|-----------|--------|-------------|
| `startDate` | ISO string (e.g., `2025-01-01`) | Include items from this date onward |
| `endDate` | ISO string (e.g., `2025-12-31`) | Include items up to this date |

### Media Format

Filter by content type: `image`, `video`, or `both`.

## Sort Options

Items from the analysis pipeline are sampled using an egalitarian strategy that balances representation across brands and feed types. Within the pipeline, engagement metrics (likes, views, shares) and recency (createdAt) are used for ranking.

## Label Dimensions

Content can be analyzed by any of the 50+ label categories applied during content classification. Key dimensions for filtering and analysis:

- HookPrimaryCategory, HookSecondaryCategory
- VisualExecutionStyle, CreativeConcept
- CTAActionType, CTAFraming
- TonalQualities, BrandVoice
- FunnelAlignment, MarketingObjective
- DemographicAge, DemographicLifestyle
- Platform, AspectRatio, VideoDurationCategory

Label data is available both as aggregate statistics in `tableData.labelDistributionsByFeedType` and per-item via the `labelFields` parameter on item-returning tools.

**Note on null fields:** Some fields may be null for certain items (e.g., `transcript` for image-only posts, `targetAudienceLifestyle` for unanalyzed items). Skip items with empty requested fields — focus on items where the data exists.

## Export Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| Spreadsheet | CSV | Tabular data for Excel, Google Sheets, BI tools |
| JSONL | .jsonl | One JSON object per line, for programmatic consumption |
| Text | .txt | Human-readable formatted summaries |
