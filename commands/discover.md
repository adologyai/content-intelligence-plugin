---
name: discover
description: Find brands to add to your knowledge set
argument-hint: "<category or keyword>"
---

When the user invokes `/discover`, follow this process:

## 1. Search Brands

Call `discover_brands` with the user's query.

If the user's query is more about content examples than entities to track, also run `content_intelligence_search` in parallel — it searches the entire Adology database using AI aspect decomposition and can surface brands the user hasn't considered.

## 2. Present Results

For each discovered brand, show:
- **Name** — brand name
- **Category** — industry or vertical
- **Available platforms** — where they are active
- **Relevance** — why this result matches the query

Format as a numbered list so the user can reference items by number.

If `content_intelligence_search` returned results, present those separately as "Content examples from brands you might want to track" — the brand names on those items become additional discovery leads.

## 3. Ask What to Add

Prompt: "Which of these would you like to add to a knowledge set? Give me the numbers, or say 'all' to add everything."

## 4. Batch Add Feeds

Once the user selects:
- Confirm which KS to add them to (use the active one if established, otherwise call `list_knowledge_sets` and ask)
- Use `batch_add_feeds` for multiple additions rather than calling `add_feed` one at a time
- For single additions, `add_feed` is fine
- Confirm what was added and note that data scraping will begin automatically

## 5. Credit-Aware Fetching

If the user wants to fetch data immediately via `trigger_fetch`:
- Note that fetches consume credits
- Use the `feedNames` parameter for selective refresh rather than fetching the entire KS
- Use `get_workflow_status` to monitor scraping progress

## Error Recovery

- **Brand not found:** Suggest alternative search terms. Try broader category terms ("fitness" instead of "CrossFit apparel"). Try the brand's parent company name.
- **Adding creators/influencers:** Creator discovery is not available via MCP. Ask the user for the creator's handle directly and add via `add_feed` with `feedType: 'influencer'`.
- **Content search returns 0 results:** Broaden the query. "Sustainable fashion ads" might return nothing while "sustainable fashion" or "eco-friendly clothing" does.

## Follow-Ups

- "Want to analyze these new brands once data comes in? Try `/analyze [brand]`"
- "Want to search for more brands in a different category?"
- "Use `get_workflow_status` to check when data scraping is complete"
