---
name: brand-builder
description: >
  Builds out a portfolio's tracked universe and the project scopes analysis reads from.
  Use when setting up a brand workspace, adding or removing brands, influencers, search
  terms, or discussions, narrowing a project, or acquiring data for new sources.
  Triggers on: "track competitor", "add brand", "add influencer", "monitor", "set up",
  "new project", "pull data".
---

# Building a Tracked Universe

Two layers, and keeping them straight is most of the job.

A **portfolio** declares what a brand tracks — the focal brand, competitors, influencers, searches, discussions. You edit it with `author_portfolio_context`.

A **project** is the working scope analysis reads from. A fresh project reads the portfolio's whole tracked universe; `update_project_scope` narrows or grows it. You analyze in projects, never in the portfolio directly.

## Step 1: Resolve the brands

`lookup_brands({ query })` searches the central brand directory and returns each match's category, website, and whatever handles are on file — Instagram, TikTok, YouTube, X, LinkedIn, and the Meta Ad Library page id — already normalized to the shape `author_portfolio_context` accepts. A brand may have only one or two channels on file.

It costs nothing and changes nothing, so run it for every name the user gives you, in parallel. When a brand is not in the directory, ask the user for the handles directly; explicit handles work exactly as well as directory ones.

## Step 2: Land in a portfolio

`list_portfolios` first — the brand may already have a workspace. `create_portfolio({ name, websiteUrl })` starts a new one; if a portfolio with that name exists it returns the existing id with `reused: true`, so never call it twice for the same brand.

## Step 3: Author the tracked universe

Read before you write: `read_portfolio_context({ portfolioId })` returns the current items and brand details. Then `author_portfolio_context` merge-writes — `upsertItems` (matched by id), `removeItemIds`, and a shallow `details` patch (category, industry, targetAudience, brandVoice).

Every item needs an `id` and a `kind`, and `kind` is one bare token: `brand`, `influencer`, `search`, `discussion`, `trend-term`, `niche`, or `seo`. Everything else about the item is its own field.

- A **brand** also needs `role` — `own` for the focal brand, `competitor`, `adjacent`, or `inspiration` — plus a `handles` object keyed by platform (`instagram`, `tiktok`, `facebook`, `youtube`, `adLibrary`), or `{}` when you found none.
- An **influencer** carries the same `handles` object.
- A **search** is a keyword; a **discussion** is a subreddit name without the `r/` prefix.

Confirm the roster with the user before writing it. This is the declaration the cockpit and every analysis read from.

## Step 4: Open a project

`list_projects({ portfolioId })` — reuse an existing project when the user wants to keep working in its scope. `create_project({ portfolioId, name })` starts a fresh one; name it for the question ("Q3 hydration competitive set"), not the brand.

`get_project` is the honest picture of what a project covers: its scope, plus `access.expiredSources` (data only through a date) and `access.ungrantedSources` (tracked but never acquired). Read it before analyzing so you know what the numbers rest on.

## Step 5: Shape the scope

`update_project_scope` edits which sources a project reads, without fetching anything. Sources are `{ scraper, id }` — `instagram-profile`, `tiktok-profile`, `facebook-page`, `youtube-channel`, `reddit-subreddit` — or `{ scraper, id, term }` for a search source like `tiktok-search`.

- `add` extends the scope with sources the pool already has coverage for. Free and instant.
- `remove` trims sources out.
- `replace` pins the scope to exactly the given sources. This is the way to NARROW a project — `add` only ever widens, so a project still inheriting the whole universe stays wide until you pin it. Pass `replace` alone.

The response routes what it could not simply add: `needsRefresh` sources were added and their existing data is fully usable, they just carry nothing newer than `coveredThrough`; `notOwned` sources were never completely fetched by anyone, so they were left out and need a pull.

## Step 6: Acquire what's missing — the only step that spends

`pull_data({ projectId, candidates })` plans without spending. Each candidate is `{ kind, handleOrTerm, platform }` where kind is `brand`, `influencer`, `discussion`, or `search`. It splits the targets:

- **readyNow** — coverage is current, so these are attached to the project immediately, free. Analyze them now.
- **the gap** — never completely fetched, or coverage has gone stale. This is frozen and quoted: `previewId` plus `estimatedCostCredits`.

Show the user both halves and the exact credit figure the tool returned. Only after they approve, call `confirm_pull({ previewId, projectId })` — that charges and starts the run. When `previewId` is null there is no gap and nothing to approve.

Tune the plan with `dateRangeDays` (default 90), `limit` (posts per source, default 50 — the cost is quoted off this), and `freshWithinDays` (default 14, how recent coverage must be to count as ready). Leave `sort` alone for a coverage ask; set `"top"` only when the user explicitly wants best-performing content.

The run streams in over a minute or two. `check_pull({ runId })` reports progress, but you usually just start reading what has landed.

## Complete setup flow

1. `lookup_brands` on every name the user gave, in parallel
2. `list_portfolios`, then `create_portfolio` if there's no home for this brand
3. `read_portfolio_context` → `author_portfolio_context` with the agreed roster
4. `create_project` (or reuse one from `list_projects`)
5. `pull_data` → show readyNow + the quoted gap → `confirm_pull` on approval
6. `get_project` to confirm what the project now covers, then analyze

## Error recovery

**Brand not in the directory.** Ask for the handles. `author_portfolio_context` accepts explicit handles for any brand.

**A source comes back `notOwned` from `update_project_scope`.** Nobody has ever completely fetched it, so adding it would show nothing. Route it through `pull_data` instead.

**A handle does not resolve during a pull.** It lands in the gap unresolved. Verify the handle exists on that platform, check for typos, and re-plan — do not confirm a pull built on a handle you are unsure of.

**A pull finished but reads come back empty.** Coverage can be current while the run is still settling. `check_pull` on the runId; a source with a fetch in flight reports as streaming, and re-pulling it buys the same data twice.

## Tips

- Two or three competitors is the floor for meaningful benchmarking; five or six reads much better.
- Specific search terms beat broad ones — "collagen supplement" over "health".
- Discussion sources carry consumer voice that no brand feed contains.
- Pin a project with `replace` before a scoped comment fetch, so you pay for one source instead of all of them.
- `delete_project` archives by default and requires `confirmedByUser: true` — name the project to the user and get an explicit yes first.
