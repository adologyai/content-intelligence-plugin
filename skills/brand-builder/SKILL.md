---
name: brand-builder
description: >
  Guides knowledge set construction including feed management and brand discovery.
  Use when creating knowledge sets, adding or removing brands, influencers, search terms,
  or discussion feeds. Triggers on: "create knowledge set", "add brand", "add influencer",
  "track competitor", "monitor", "build a KS".
---

# Building Knowledge Sets

## Step 1: Discovery

Start by running `discover_brands` to find brands by name, category, or URL. This gives you a picture of the competitive landscape before building anything.

## Step 2: Credit Awareness

After discovery, call `whoami` to check the user's available credits. Before calling `trigger_fetch`, estimate the cost based on the number of feeds being fetched. Inform the user of the expected credit usage before proceeding. Never trigger a fetch without the user understanding the cost.

## Step 3: Create and Populate the Knowledge Set

Use `create_knowledge_set` with a descriptive name ("DTC Skincare Competitors", "Q2 Campaign Benchmarks", "Protein Brand Landscape").

**When adding 3+ feeds, use `batch_add_feeds` instead of individual `add_feed` calls.** This is faster and reduces round-trips. Only use individual `add_feed` for single additions or when you need to handle each feed's response separately.

### Conditional Logic by Input Type

**User gives a brand name:**
1. Run `discover_brands` to find it and resolve platform handles
2. Check `list_knowledge_sets` to see if the brand already exists in another KS
3. If found elsewhere, inform the user before duplicating

**User gives a URL:**
1. Extract the platform and handle from the URL
2. Add directly via `add_feed` -- no discovery step needed

**User gives a category (e.g., "energy drinks"):**
1. Run `discover_brands` by category to get a list of brands
2. Present the options and let the user pick
3. Suggest related brands they may not have considered

## Step 4: Trigger Data Collection

Call `trigger_fetch` to start scraping. This runs asynchronously via Temporal workflows. You can use the `feedNames` parameter to selectively refresh specific feeds instead of the entire Knowledge Set.

Check progress with `get_workflow_status`. Scraping typically takes a few minutes per feed depending on content volume.

## Step 5: Get Suggestions and Fill Gaps

After feeds are added, call `get_suggestions` to identify gaps in the Knowledge Set:
- Missing platforms for existing brands (e.g., brand has Instagram but not TikTok)
- Missing feed types (e.g., no search terms, no discussion feeds)
- Related brands the user might want to track

Review the suggestions with the user and add recommended feeds using `batch_add_feeds`.

## Complete Onboarding Flow

The full sequence:

1. **Discover** -- `discover_brands`
2. **Check credits** -- `whoami`
3. **Create KS** -- `create_knowledge_set`
4. **Add feeds** -- `batch_add_feeds` with all selected brands, creators, search terms, discussions
5. **Fetch data** -- `trigger_fetch` (after confirming credit cost)
6. **Monitor** -- `get_workflow_status` until complete
7. **Fill gaps** -- `get_suggestions` to identify missing coverage
8. **Expand** -- `batch_add_feeds` with suggestions, then `trigger_fetch` again

## Feed Types Reference

### Brand Feeds
Track paid ads and organic social content. Sources: `facebook-ad-library`, `tiktok-ad-library`, `instagram-profile`, `tiktok-profile`, `youtube-channel`, `facebook-page`, `twitter-profile`, `linkedin-profile`, `threads-profile`.

### Influencer Feeds
Track a specific creator's content. Sources: `instagram-profile`, `tiktok-profile`, `youtube-channel`, `twitter-profile`, `threads-profile`.

### Search Feeds
Monitor keywords across platforms. Sources: `tiktok-search`, `instagram-search`, `youtube-search`.

### Discussion Feeds
Track Reddit subreddits. Provide the subreddit name without the r/ prefix.

## Error Recovery

**Brand not found in discovery DB:**
Ask the user for the brand's social media handles directly. You can add feeds with explicit handles even if the brand is not in the discovery database.

**Creator not in discovery database:**
Creator discovery is not available via MCP. Ask the user for the creator's handle directly and add via `add_feed` with `feedType: 'influencer'`.

**add_feed with invalid handle:**
The tool will return an error. Inform the user the handle could not be resolved. Ask them to verify the handle exists on the platform, check for typos, and try again.

## Tips

- Add at least 2-3 competitors for meaningful competitive benchmarking
- Search terms work best when specific ("collagen supplement" > "health")
- Subreddit monitoring captures authentic consumer voice that brand content misses
- You can update a Knowledge Set at any time to add or remove feeds
