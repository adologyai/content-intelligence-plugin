---
name: analyze
description: Run a quick competitive analysis on a brand or topic in your knowledge set
argument-hint: "<brand or topic>"
---

When the user invokes `/analyze`, follow this process:

## 1. Establish Context (Parallel)

If no knowledge set has been established in this conversation, call **both in parallel**:
- `list_knowledge_sets` — to present options
- `whoami` — to understand the user's team context

Once the user picks a KS, remember it for subsequent commands.

## 2. Discover Dimensions

Call `list_labels` on the KS to see what label categories exist (HookType, ContentFormat, TonalQualities, etc.). This determines which `labelFields` are worth requesting in the analysis call. Do not guess at category names.

## 3. Run the Analysis

Call `analyze` with:
- The KS ID and user's query
- **`fields`** tailored to the question — e.g., `fields: ["hookMechanism", "creativeConcept", "viewsMultiple", "likesMultiple"]` for creative analysis, or `fields: ["engagementRate", "longevityMultiple"]` for performance analysis
- **`labelFields`** based on what `list_labels` revealed — e.g., `labelFields: ["HookType", "ContentFormat"]`

### Adapt Based on What You Find

- **Small KS (<50 items):** Every item matters. Don't summarize distributions — walk through the standouts individually.
- **Large KS (500+ items):** Focus on statistical patterns. Use `get_table_data` for aggregate breakdowns, then pull specific examples.
- **Sparse labels:** If most items lack labels, rely on engagement metrics and content fields instead. Don't report on label distributions when coverage is low.
- **Single platform:** Skip platform comparison. Go deeper on format, hook, and execution patterns within that platform.
- **Multi-platform:** Note platform-specific patterns but don't force comparisons between platforms with wildly different engagement scales — use multiples (`likesMultiple`, `viewsMultiple`) not raw counts.

## 4. Dig Into Top Performers

Do not just report label stats. Find what is actually working:
- Look at items with `isOutlier: true` or high `likesMultiple`/`viewsMultiple`
- Call `get_item_detail` on 2-3 top items to read the actual creative (transcript, hook, visual description)
- Understand WHY they worked, not just that they carry a certain label

## 5. Present Findings

**What's Working (and Why)** — Lead with breakout content. Describe what the winning creatives actually DO — the hook approach, the narrative, the visual style, the CTA. Back it up with performance numbers (`likesMultiple`, `viewsMultiple`, source baselines). Don't say "Question hooks outperform" — describe what the specific winning question hooks say.

**Category Patterns** — Label distributions for macro context. Which hooks, formats, tones over-index (`timesCategoryAvg > 1.5`). Only include this section if label coverage is sufficient.

**Actionable Recommendations** — 3-5 specific, data-backed recommendations. Reference actual items as examples. "Use [this specific approach] because [this specific item] got [X]x — here's what it does: [describe the creative]."

## 6. Save and Follow Up

Offer to save standout items to a collection via `save_to_collection` — share the returned URL so the user can view them in the app.

Suggest concrete next steps:
- "Want me to compare this with a competitor? Try `/compare [brand A] vs [brand B]`"
- "Want to save these standouts as a shareable collection? I can call `save_to_collection`."
- "Want to dig deeper into a specific pattern I found?"
- "Want to search across all of Adology's data, not just this KS? I can use `content_intelligence_search`"

## Error Recovery

- **Empty KS (0 items):** Check `get_knowledge_set` for feed configuration. If feeds exist but no items, data hasn't been scraped yet — suggest `trigger_fetch` or waiting.
- **No labels:** Fall back to engagement-based analysis. Report on performance metrics, platform mix, content fields — skip label distributions entirely.
- **Insufficient data for the query:** Be honest. "This KS only has 12 items matching that filter — not enough for pattern detection. Here's what I can see from these 12..." is better than fabricating trends.

## Anti-Patterns

- Do not lead with volume stats ("You have 847 items across 3 platforms"). Get to the insight.
- Do not echo every label category back to the user. Surface only the dimensions that reveal something non-obvious.
- Do not compare raw engagement numbers across platforms. Always use multiples.
- Every claim must trace to specific data returned by the tool. Do not speculate.
