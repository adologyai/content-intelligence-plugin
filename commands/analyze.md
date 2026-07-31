---
name: analyze
description: Analyze a brand or topic across a project's tracked scope
argument-hint: "<brand or topic>"
---

When the user invokes `/analyze`, follow this process:

## 1. Land in a scope

A read is only as good as what it is about. Orient with `whoami`, then `list_portfolios`, then `list_projects({ portfolioId })`. Reuse a project that already covers the subject, or `create_project` for a fresh one — there is no special home project.

Call `get_project` before analyzing. It returns the project's `dataScope` (the tracked set of sources it reads) plus per-source access: `expiredSources` have data only through a date, `ungrantedSources` are tracked but not yet acquired. That list is the denominator behind every number you are about to report. A project with an empty scope reads the portfolio's whole tracked universe until it is narrowed.

To point the project at exactly the sources this question is about, use `update_project_scope`: `add` extends, `remove` trims, `replace` pins the scope to exactly the sources you name. Adding sources the pool already covers is free and instant.

## 2. See which dimensions exist

Call `list_labels({ projectId })` for the label dimensions and top values actually present in this scope. Use those exact names in `labelFilter` and `get_table_data` rows — a dimension the scope does not carry matches nothing, so an invented name turns the whole read into an empty result. If `list_labels` reports nothing, the scope holds no labeled items yet: analyze on engagement and content instead, and say that labels are unavailable.

## 3. Read what is already there

`analyze({ projectId, query })` is the workhorse. It returns posts with their creative analysis — `hookMechanism`, `creativeConcept`, `adDescription`, `transcript`, `oneLineInsight` — from the resolved scope. Choose the retrieval that matches the question:

- `distribution: "balanced"` (default) for a representative read across sources.
- `distribution: "top"` (with `sortMetric`) for the highest-engagement content per source.
- `distribution: "exhaustive"` with `sortBy: "likesMultiple"` (or another `*Multiple`) for a real ranked leaderboard over the full filtered set, with `totalEstimated` and `nextOffset` for paging.
- `mode: "semantic"` when the ask is a meaning ("posts that make sustainability feel effortless") rather than a filter.

Narrow before you sample: `feedNames`, `platformFilter`, `startDate`/`endDate`, `mediaTypeFilter`, `labelFilter`, and `outlierFilter: { metric, multipleGreaterThan }` all apply before sampling. Read `itemsReturned`, `hasMore`, and `nextOffset` on the response and page when the answer needs the whole set.

For quantities rather than examples, use `get_table_data` (pivot tables over label dimensions, metrics like `count`, `useRate`, `medianLikes`, `viralRate`) or `aggregate` (group by `platform` / `brand` / `feedType` / `format` / `time` with your own measures). Every `aggregate` row carries `n`; a ranking-shaped call comes back split into `rows` (groups that clear the reliability floor) and `directionalRows` (below it). Draw the finding from `rows` and cite `directionalRows` as directional, with their `n`.

## 4. When the scope genuinely lacks the data

Only reach for a pull when the subject is missing, not merely thin. `pull_data({ projectId, candidates })` costs nothing: it attaches sources the pool already covers to the project for free, and quotes only the gap — sources never completely fetched, or whose coverage has gone stale. Show the user `readyNow`, the per-source gap, the window it is priced over, and `estimatedCostCredits`. Only after they say yes, call `confirm_pull({ previewId, projectId })` — that is the step that charges credits. The fetch streams in over a minute or two; `check_pull({ runId })` reports progress.

## 5. Dig into the standouts

Do not stop at distributions. Take the items with the highest `likesMultiple` / `viewsMultiple` or `isOutlier: true` and call `analyze({ projectId, itemIds })` for the by-id deep dive — full creative, labels, performance. Read what the winning post actually does before you explain why it won.

## 6. Present findings

**What's working, and why.** Lead with the breakout content and describe what it actually does — the hook, the narrative turn, the visual, the CTA. Back it with lift against the source baseline. "Question hooks over-index" is not a finding; "this hook asks whether the user's morning routine is wrong, and pulled 4.2x its source baseline" is.

**Category patterns.** Label distributions for macro context, included only when label coverage is real.

**Recommendations.** Three to five, each tied to a specific item and a specific number, each actionable this week.

Say what the answer covers. If you read 80 of 1,240 matching items, or the scope's coverage ends in May, say so in the same breath as the finding.

## 7. Save and follow up

Offer `save_to_collection({ projectId, collectionName, itemIds })` for the standouts so the user can review them in the app. Then suggest the natural next move: a head-to-head with `/compare`, a table with `/export`, or a deeper cut on one pattern.

## Anti-patterns

- Do not open with volume statistics. Get to the insight.
- Do not compare raw engagement across platforms or across sources of different size — use the multiples.
- Do not present an empty or thin result as the answer. Check `get_project` for what the scope covers, and say what is missing.
- Do not spend credits without a quote the user approved in the same turn.
- Every claim traces to data the tools returned. No speculation.
