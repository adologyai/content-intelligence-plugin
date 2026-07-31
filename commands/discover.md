---
name: discover
description: Find brands and creators worth tracking, and add them to a portfolio
argument-hint: "<category, brand, or keyword>"
---

When the user invokes `/discover`, follow this process:

## 1. Resolve names to real handles

Call `lookup_brands({ query })`. It searches Adology's central brand directory and returns, for each match, the category, website, domain, and whatever handles the directory holds — Instagram, TikTok, YouTube, X, LinkedIn, and the Ad Library page id — already normalized to the shape `author_portfolio_context` accepts. It is free, reads only, and adds nothing.

A directory entry may carry only one or two channels. That is the real state of the entry, not an error; report which channels exist rather than inventing the missing ones. If `hasMore` comes back true, the directory holds more matches than the page you asked for.

## 2. Find who is already doing the thing

When the ask is about content rather than company names — "who is running founder-led video", "which competitors talk about refill packs" — search the data instead of the directory. In a project that already has scope, `search_all({ projectId, query })` runs a keyword search over item analysis text and returns the matching posts ranked by engagement, each with its brand and URL. For a meaning-based recall rather than keyword matching, use `analyze({ projectId, query, mode: "semantic" })`.

The brand names on those results are discovery leads in their own right: someone whose content keeps surfacing is a candidate to track. Feed the promising names back through `lookup_brands` to get their handles.

Creators work the same way. If a creator is not in the directory, ask the user for the handle and platform — that is enough to track them.

## 3. Present the candidates

Number the list so the user can answer with numbers. For each candidate give the name, the category, the channels that actually exist for it, and one line on why it matches the ask. Keep content examples in a separate short list, with the brand behind each one named.

## 4. Add what the user picks

Tracking happens on the portfolio, not on a project. Read the current state first with `read_portfolio_context({ portfolioId })`, then merge the new entries with `author_portfolio_context({ portfolioId, upsertItems })`. Each item needs an `id`, a `kind` (`brand`, `influencer`, `search`, `discussion`, `trend-term`, `niche`, `seo`), and its identifiers. A brand also needs a `role` — `own` for the user's own brand, `competitor`, `adjacent`, or `inspiration` for the rest — and a `handles` object keyed by platform (`instagram`, `tiktok`, `facebook`, `youtube`, `adLibrary`), or `{}` when the directory had none. `kind` is one bare token; role and every other attribute is its own field.

Authoring the context declares what the portfolio tracks. It does not bring in any data.

## 5. Bring the data in, with the price on screen

Call `pull_data({ projectId, candidates })` for the new entries. It spends nothing and splits them two ways: `readyNow` sources are already covered in the shared pool and get attached to the project's scope for free, queryable immediately; the rest is the gap — never fetched, or covered only through an older date — and gets frozen and quoted.

Show the user what came back free, which sources need acquiring, the window the quote covers (`effectiveDays` can differ from what you asked for), and `estimatedCostCredits`. Only after they approve, call `confirm_pull({ previewId, projectId })`. That is the step that charges. It returns a `runId` immediately; the data streams in over the next minute or two, and `check_pull({ runId })` reports how much has landed. Anything marked `streaming` is already paid for and on its way — do not buy it again.

If everything came back `readyNow`, do not pull at all. Just analyze.

## 6. Follow up

Point at the next move: `/analyze` on a newly tracked brand once its data lands, `/compare` against the user's own brand, or another discovery pass in an adjacent category.

## When results are thin

Broaden the query before concluding nothing exists — a category term usually beats a niche phrase, and a parent company name often finds a brand that a product name misses. If a keyword search inside a project returns nothing, check with `get_project` whether the scope covers the sources you would expect; an empty scope and an absent trend look identical until you look.
