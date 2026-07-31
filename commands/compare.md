---
name: compare
description: Head-to-head comparison of two brands or topics
argument-hint: "<brand A> vs <brand B>"
---

When the user invokes `/compare`, follow this process:

## 1. Resolve both sides to tracked entities

Split the input on "vs", "versus", "compared to", "and", or "against". If you cannot identify exactly two subjects, ask which two.

Both sides have to be tracked before they can be compared. Orient with `list_portfolios` → `list_projects({ portfolioId })`, then call `get_project` and read its `dataScope`: the entity names it tracks are the names the read tools will match. `aggregate({ groupBy: ["brand"] })` is the fastest way to see which names actually carry items.

If one side is not tracked anywhere in the project, say so before analyzing. Resolve its real handles with `lookup_brands`, add it to the portfolio's tracked universe with `author_portfolio_context`, then `pull_data` → show the quote → `confirm_pull` once the user approves the credits. A comparison against a brand with no data is not a comparison.

If the two brands live in different projects, run the same reads once per project and compare the results — say plainly that the two sides were read from different scopes and note any difference in coverage window.

## 2. Bind each read to one entity

Each tool names the entity filter differently, and using the wrong one silently compares the whole scope against itself:

- `query_items({ brand: ["Sephora"] })` — the surest binding. It resolves the name against the project's tracked roster case-insensitively, and a name the project does not track comes back as an `entityScope` gap listing what *is* tracked, rather than as a scope-wide ranking dressed up as that brand's.
- `analyze({ feedNames: ["Sephora"] })` — applies in the sampled and exhaustive reads. Semantic mode retrieves by meaning across the scope and does not narrow on `feedNames`, so bind the entity a different way when you use it.
- `aggregate({ filters: { brand: [...] } })` — a case-insensitive name filter, or group by `brand` to get both sides in one call. A misspelled or untracked name yields empty groups rather than a gap notice, so confirm the spelling against a `groupBy: ["brand"]` pass first.
- `get_table_data({ brands: [...] })`, or better, `columns: "focalVsRest"` with `focalBrand` set.
- `get_creative_dna({ feedNames: [...] })` or `entities: [{ type, name }]`.

## 3. Run the two sides in parallel

They are independent reads — issue them together, not one after the other.

The most direct head-to-head is a single `get_table_data` call with `columns: "focalVsRest"`, `focalBrand: "<brand A>"`, and `expandRest: true`: it puts one brand's label mix against the field in one table. Follow it with `get_creative_dna`, whose VS CATEGORY section reports each brand's unique advantages and gaps against the rest of the scope, and whose OPPORTUNITY LABELS section names the lean-in and cut-back moves.

Then pull the evidence: `analyze({ feedNames: [...], distribution: "exhaustive", sortBy: "likesMultiple", limit: 10 })` for each brand. The concrete winning posts are what make the comparison actionable — a table of label percentages is not.

## 4. Build the comparison

Present a side-by-side table over the dimensions where the two actually diverge. Drop the rows where they are the same; a difference of two points is not a difference.

Compare lift, not totals. "Brand A's top posts run 2.3x their own baseline while Brand B's run 0.8x" is a statement about content. "Brand A gets 45K likes and Brand B gets 12K" is mostly a statement about audience size. The same rule holds across platforms: compare each brand against its own platform baselines rather than putting one brand's TikTok next to the other's YouTube.

Watch the `n` on every aggregate row. A ranking-shaped `aggregate` splits into `rows` (above the reliability floor) and `directionalRows` (below it) — a one-post group is a signal, not a result, and never a winner.

## 5. Show where each one wins

For each brand, name the advantage and prove it with a specific post: what the creative does, and the multiple it pulled. Use `analyze({ itemIds })` to read the full creative on the two or three posts you are going to cite.

## 6. Recommendations

Three to five moves, each tied to a finding:

- What Brand A should take from Brand B's top performers, citing the posts.
- What Brand B should take from Brand A.
- The space neither one occupies — the label combinations `get_creative_dna` flags as opportunity, or a search-demand gap from `seo_keywords` if the question is about categories rather than posts.

## 7. Save and follow up

Save each side's standouts to its own collection with `save_to_collection` so the user can review them in the app. Then offer the natural next step: `/analyze` on one brand, `/export` for the table, or a narrower cut by platform or window.

## Anti-patterns

- Do not compare raw counts across brands of different size or across platforms.
- Do not report a comparison where one side is thin without saying how thin — give the item count for both sides.
- Do not list every label dimension side by side. Show the ones where the two brands differ.
- Do not run the two sides sequentially. They are independent.
- Do not spend credits to fill a gap without quoting it and getting a yes first.
