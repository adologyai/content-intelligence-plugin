---
name: compare
description: Head-to-head comparison of two brands or topics
argument-hint: "<brand A> vs <brand B>"
---

When the user invokes `/compare`, follow this process:

## 1. Parse and Resolve

Split the input on "vs", "versus", "compared to", "and", or "against" to identify two brands or topics. If you cannot identify exactly two, ask: "Which two brands or topics would you like me to compare?"

Determine whether the brands live in the **same KS** or **different KSs**:
- Same KS: you will filter by `feedNames` within a single KS
- Different KSs: use `compare_knowledge_sets` for the cross-KS comparison

If no KS has been established, call `list_knowledge_sets` and ask.

## 2. Run Both Analyses in Parallel

**This is critical — do not run sequentially.**

For same-KS comparisons, call `analyze` twice **in parallel**:
- Brand A: `feedNames` filtered to brand A, `fields` and `labelFields` tailored to the comparison
- Brand B: `feedNames` filtered to brand B, same field selection

For cross-KS comparisons, call `compare_knowledge_sets` which handles the parallel data retrieval internally.

## 3. Pull Example Items in Parallel

Once you have the analysis results, call `get_items` for each brand **in parallel** to pull specific examples:
- Brand A's top 3 outliers (sorted by `likesMultiple` or `viewsMultiple`)
- Brand B's top 3 outliers

These concrete examples are what make the comparison actionable — without them, you are just reporting label distributions.

## 4. Build the Comparison

Present a side-by-side markdown table. Focus on dimensions where the brands actually differ — skip rows where they are essentially the same.

**When one brand dominates engagement:** Use multiples, not raw numbers. "Brand A averages 2.3x their baseline likes vs Brand B's 0.8x" is meaningful. "Brand A gets 45K likes vs Brand B's 12K" conflates audience size with content quality.

**When platforms differ:** Do not compare Brand A's TikTok directly to Brand B's YouTube. Compare each brand's performance relative to their own platform baselines.

## 5. Highlight Competitive Advantages

For each brand, call out where it outperforms with specific numbers from the analysis. Back every claim with a concrete example:
- "Brand A's question hooks outperform at 2.1x — see [specific item] which opens with '[actual hook text]' and pulled 3.4x likes"
- Not just "Brand A has better hooks"

## 6. Strategic Recommendations

3-5 actionable insights:
- What Brand A could learn from Brand B's top performers (cite the specific items)
- What Brand B could learn from Brand A
- Gaps neither brand is exploiting — use `content_intelligence_search` to find examples from other brands filling that gap
- Platform-specific strategies where one brand has a clear edge

## 7. Save and Follow Up

Offer to save each brand's top performers to separate collections via `save_to_collection` — share the returned URLs.

Suggest next steps:
- "Want me to go deeper on either brand? Try `/analyze [brand]`"
- "Want to save each brand's top performers to shareable collections? I can call `save_to_collection`."
- "Want to look at a specific platform or time period?"
- "Want to find how other brands handle [gap identified]? I can search the full Adology database."

## Anti-Patterns

- Do not compare raw engagement numbers across platforms or across brands with different audience sizes. Always use multiples.
- Do not list every label category side by side. Surface only dimensions where the brands meaningfully differ.
- Every claim must cite specific data or specific items. Vague comparisons ("Brand A has more engaging content") are not acceptable.
- Do not run the two brand analyses sequentially. They are independent — run them in parallel.
