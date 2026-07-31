---
name: weekly-brief
description: >
  Build a 3-page Adology Weekly Competitive Intelligence Brief (PDF) from a project's scope.
  Produces Page 1 (Visual Scoreboard + Intel Strip), Page 2 (Market Signals), and
  Page 3 (Social Trends + Coaching) — each built independently, then assembled into
  a single QA'd PDF with real thumbnails. Use this skill whenever the user says
  "weekly brief", "competitive brief", "run the brief", "weekly report",
  "competitive recap", "generate the report", "build the brief", or references
  the 3-page Adology report. Also trigger when the user asks for a competitive
  intelligence PDF, a weekly scoreboard, or says "brief me on [brand]".
  Trigger liberally — if it sounds like they want a multi-page competitive
  analysis document from Adology data, this is the skill.
---

# Weekly Competitive Intelligence Brief

Build a polished 3-page PDF competitive intelligence report from an Adology project's scope.
Each page is a self-contained "slide" with its own data pipeline, rendered as HTML via
WeasyPrint, then merged into a single PDF. Every page includes real post thumbnails.

## Architecture Rules

**DO NOT use subagents.** Build all 3 pages yourself, sequentially, in the main thread.
Subagents caused cascading failures in production — they made unchecked decisions,
crashed the sandbox disk, and couldn't be course-corrected.

**Thumbnails are MANDATORY.** Every scoreboard card, spotlight, trend card, and coaching
card must have a real thumbnail image from the actual post. The skill includes a bundled
script (`scripts/download_thumbnails.py`) that handles downloading, resizing, and
base64-encoding. You run this script — it produces a JSON file mapping image URLs to
small base64 data URIs. Then you insert those data URIs into the HTML `<img>` tags.
There is no alternative to this. Do not skip thumbnails. Do not use CSS placeholders.
Do not use colored rectangles with initials. Download the real images.

**Coverage is part of the brief, not a caveat you drop.** A weekly brief is a claim about
a window. Say which sources actually cover that window and name the ones that don't — by
name, on the page. A stale source that goes unmentioned turns a data gap into a false
finding ("Brand X went quiet this week" when nobody fetched Brand X).

## Path Conventions

This skill's shell examples use two literal placeholders that you must substitute
before running any command:

- `{skill_path}` — the absolute path to this skill's directory (the directory
  containing this `SKILL.md`). At runtime this resolves to something like
  `/Users/<you>/.../skills/weekly-brief`. Use it to invoke bundled scripts under
  `scripts/` and to read reference files under `references/`.
- `{output_dir}` — the working/output directory for this brief's HTML, JSON,
  and final PDF artifacts. Pick a fresh directory per run (e.g.
  `outputs/<project_name>-<week_end>/`) and substitute it consistently across the
  whole workflow.

If you see either placeholder in a command, **replace it with the actual path
before executing**. Do not pass the literal string `{skill_path}` to a shell.

## Overview

The brief has three pages:

- **Page 1 — Visual Scoreboard + Intel Strip**: Top 6 posts across brands (scoreboard
  grid with real thumbnails), primary brand spotlight, stat pills, insight bar, and a
  3-column intel strip with hook/creative/AI analysis.
- **Page 2 — Market Signals**: Industry news headlines with strategic signals, audience
  conversation, hook performance charts, brand engagement leaderboard, paid presence,
  and a 3-card action board (Defend / Attack / Watch).
- **Page 3 — Social Trends + Coaching**: 5 trend cards (with real thumbnails and source
  links), plus 3 coaching cards with real thumbnails showing how to optimize existing
  primary brand posts with specific data-backed tweaks.

## Workflow

### Phase 0 — Orient and Fix the Scope

1. **Ask for inputs** (if not already provided):
   - `primary_brand` — the brand being briefed
   - the portfolio or project to brief on
   - `week_start` / `week_end` — the Monday–Sunday window (default: last full week)

2. **Orient**: `whoami` → `list_portfolios` → `list_projects({ portfolioId })`. Reuse an
   existing project whose scope matches the brief, or `create_project` for a fresh one.
   The project IS the scope — everything the brief reports comes from what that project
   covers.

3. **Read the scope and its coverage**: `get_project({ projectId })` returns `dataScope`
   plus the full per-source access state — `access.expiredSources` (covered only through
   a date) and `access.ungrantedSources` (tracked but never acquired). Write these two
   lists down now; they become the coverage note on the delivered brief. A project with
   an empty scope reads the portfolio's whole tracked universe; `update_project_scope`
   with `replace` pins it to exactly the sources this brief is about.

4. **Check the window has enough behind it**: `aggregate` over the brief window —
   `groupBy: ['brand']`, `filters: { feedType: ['brand'], from: week_start, to: week_end }`,
   `measures: [{ field: '*', fn: 'count', as: 'n' }]`. Three or more brands and 20+ items
   is a workable brief. Below that, say so before building.

5. **If the window is thin because coverage is stale**, plan a pull: `pull_data({ projectId,
   candidates })` splits the targets into `readyNow` (attached free, already current) and
   the gap it quotes. **`confirm_pull` charges credits** — show the user the quoted cost
   and the sources it covers, and call it only after they approve. Then `check_pull({ runId })`
   to watch it land. If they decline, build the brief on what's covered and name the gap.

### Phase 1 — Pull Shared Data (One Pass)

Pull the core data once; multiple pages read from it. This keeps the pages consistent with
each other and keeps the round-trips down.

**Step 1A — Discover the label vocabulary.** Call `list_labels({ projectId })` (or
`get_table_data({ projectId, listDimensions: true })`) to see which dimensions this scope
actually carries. Use those exact dimension names in every later call — a dimension the
scope doesn't have produces an empty table, not an error.

**Step 1B — Time series and leaderboard (P1 stat pills + P2 leaderboard).**
`aggregate` with `groupBy: ['time','brand']`, `timeBucket: 'week'`,
`measures: [{ field:'*', fn:'count', as:'n' }, { field:'likes', fn:'median', as:'medianLikes' }]`,
`filters: { feedType:['brand'], from: week_start, to: week_end }`. Every row carries `n`.
A ranking call comes back split: `rows` cleared the reliability floor, `directionalRows`
sat below it. **Rank from `rows`.** A `directionalRows` entry may appear as texture with
its `n` stated ("two posts, so read it as a signal"), never as a leaderboard position.

Run the same call with `filters.excludeBoosted: true` for the organic-only cut. The
difference between the two is the paid-presence read on Page 2 — and if you report the
organic number, say that you excluded boosted posts.

**Step 1C — This week's outliers (P1 scoreboard + P3 trends).**
`query_items` with `projectId`, `feedType: ['brand']`, `startDate`/`endDate` set to the
window, `sortBy: 'likesMultiple'`, and `outlierMetric: 'likes'` + `minOutlierMultiple: 2`.
This ranks posts by lift against their own source baseline, so a small brand's breakout
can outrank a big brand's routine post — which is what a competitive brief is for. Each
row carries `likesMultiple` alongside `sourceMedianLikes`: **never print a lift multiple
without its baseline.** Rows also carry `isOutlier`, `boosted`, and `externalUrl`.

Walk the ranked list top-down and keep the first post per brand until you have 6 unique
brands other than `primary_brand`. Repeat the call with `brand: [primary_brand]` for the
spotlight candidates. Collect the `itemId` values.

**Step 1D — Hydrate the chosen posts (thumbnails + creative).**
`analyze({ projectId, itemIds: [...] })` — the by-id deep dive returns each item's full
creative read. Every row carries the base set including `url` and `thumbnail` (a poster
image; video items resolve to their still frame). Add `fields` for the creative language
the pages need: `['hookMechanism','creativeConcept','oneLineInsight','mediaType','narrativeFormat']`,
and `labelFields` for the dimensions you found in 1A. This is where the brief's thumbnail
URLs come from.

If a post comes back with an empty `thumbnail`, swap it for the next-ranked post that has
one — every card in the final report needs a real image.

**Step 1E — Label performance (P1 insight bar + P2 charts + P3 gaps).**
`get_table_data` with `projectId`, `rows: ['<hook dimension>']`, `columns: 'focalVsRest'`,
`focalBrand: primary_brand`, `feedTypes: ['brand']`,
`metrics: ['count','useRate','medianLikes','viralRate']`, `topN: 15`, and the window dates.
Repeat with the creative/format dimension, and once with `rows: ['<hook>','<format>']` for
the composite hook × format read Page 2 charts.

**Step 1F — Audience voice (P2 community intelligence).**
`analyze({ projectId, query: '<what the audience is saying about the category>',
feedTypes: ['discussion'], distribution: 'top', limit: 20 })`. Reddit threads read
straight through. If the brief needs comments on the brand's own TikTok/Instagram posts,
`fetch_comments` brings them into the pool — it is a **two-step paid fetch**: call it
without `confirmedByUser` for the quote, show the user `estimatedCredits`, and only on
approval call again with `confirmedByUser: true`, the `quoteToken` echoed verbatim, and
`maxCredits` set to exactly what they approved. Once the run settles, read them back with
`includeComments: true` on the discussion read.

**Step 1G — Paid presence (P2).** The boosted/organic split from 1B is the competitive
read. If the team has a connected ad account, `list_ad_accounts` then
`get_creative_leaderboard({ accountIds, range, sortBy: 'spend', includeMedia: true })`
gives the brand's own paid performance with inline creative media. Omit the block entirely
when there is no connected account rather than filling it with organic numbers.

**Verify the data pull.** Before proceeding, confirm you have:
- 20+ brand items in the window with engagement and lift data
- Label distributions from `get_table_data` on dimensions that exist in this scope
- At least 3 brands clearing the reliability floor
- Thumbnail URLs for every post that will appear on a card
- The coverage lists from `get_project`

If something critical is missing, tell the user what's unavailable and adjust the affected
sections — use "Insufficient data" notes rather than fabricating.

### Phase 1.5 — Download Thumbnails (MANDATORY)

This step produces the real thumbnail images for the report. Do not skip it.

From the Phase 1D data, collect all `thumbnail` URLs you need:
- 6 scoreboard posts (P1) + 1 spotlight post (P1) = 7 images
- 5 trend example posts (P3) + 3 coaching posts (P3) = 8 images
- Total: up to 15 images

> **Why this skill ships its own thumbnail script (instead of using
> `content-intelligence:thumbnails`):** the PDF assembly step embeds images
> inline as base64 data URIs in `@page`-bounded CSS so WeasyPrint can render
> them without re-fetching at print time. The bundled script resizes to a
> uniform 150×188px and encodes at JPEG quality 60 specifically to fit the
> per-page file-size budget enforced by `qa_check.py`. Use this script for the
> standard 3-page brief. **If it fails for more than half of the URLs (Python
> `requests` can be blocked in some sandboxes the same way `curl` is),
> fall back to `content-intelligence:thumbnails` for the remaining URLs** and
> manually base64-encode and resize the returned images before stitching them
> into `thumbnails.json` in the same format the renderer expects.

**Run the bundled download script:**

```bash
python3 {skill_path}/scripts/download_thumbnails.py \
  --urls "URL1" "URL2" "URL3" ... \
  --output {output_dir}/thumbnails.json
```

Pass ALL thumbnail URLs as arguments. The script:
1. Installs Pillow and requests if needed
2. Downloads each image
3. Resizes to 150x188px (fits all containers — scoreboard, spotlight, trend, coaching)
4. Encodes as JPEG quality 60 → base64 data URI
5. Each resized image is ~5-15KB (vs. 500KB-1MB for full resolution)
6. Writes a JSON file mapping each URL to its `data:image/jpeg;base64,...` string
7. Retries failed downloads once before giving up on that specific image

After the script finishes, read `thumbnails.json`. It contains:
```json
{
  "https://example.com/post1/thumbnail.jpg": "data:image/jpeg;base64,/9j/4AAQ...",
  "https://example.com/post2/thumbnail.jpg": "data:image/jpeg;base64,/9j/4BBR...",
  "https://example.com/post3/thumbnail.jpg": null
}
```

A `null` value means that specific image couldn't be downloaded after retries. For any
`null` entries, swap that post out for the next-ranked post from Phase 1C that does have
a working thumbnail, and re-hydrate it through `analyze` by id. Every card in the final
report must have a real image.

**Sandbox-failure fallback:** if more than half of the URLs come back `null`
across the entire batch (likely indicates outbound HTTP is blocked, not
per-asset failures), invoke `content-intelligence:thumbnails` for the still-
unresolved URLs, base64-encode and resize the returned images to match the
150×188px / quality 60 JPEG format, and merge them into `thumbnails.json`
manually before continuing to Phase 2. Do not continue with a half-empty
`thumbnails.json` — `qa_check.py` will FAIL the run on missing images
(see Phase 6).

### Phase 2 — Build Page 1 (Visual Scoreboard + Intel Strip)

Read these files for detailed instructions:
- `references/P1_prompt.txt` — step-by-step analysis logic
- `references/P1_output_schema.yaml` — field names and example values
- `references/P1_render_package.html` — HTML/CSS template

**Build the HTML directly in this thread.** Use the data from Phase 1 to:

1. Compute stat pills (total_posts, brand_count, top_engagement, leader_vs_you)
2. Build scoreboard: 6 unique brands from the outlier ranking, with hooks/labels
3. Build spotlight: primary brand's top post with gap-to-leader math
4. Compute insight bar text using the 3-tier threshold logic
5. Build intel strip: winning hook, creative momentum, AI brief
6. **Insert thumbnail images**: For each scoreboard card and the spotlight, look up
   the post's thumbnail URL in `thumbnails.json` and insert the base64 data URI into
   the `<img src="...">` tag. Every card must have a real image.
7. **For the comment area**: use the first 80 characters of the post's `headline` as a
   preview, unless comments for that source are already in the pool from Phase 1F.
8. Substitute all values into the render template
9. Save as `P1_complete.html` in the outputs directory

**Verify P1 before moving on:**
- File size between 30KB and 200KB (under 30KB means you forgot the thumbnails)
- No `{{placeholder}}` tokens remaining
- All engagement numbers are real (from your data pull, not the schema examples)
- Every lift multiple printed alongside its source baseline
- All `<img src="data:image/jpeg;base64,...">` tags contain real base64 data

### Phase 3 — Build Page 2 (Market Signals)

Read these files:
- `references/P2_prompt.txt`
- `references/P2_output_schema.yaml`
- `references/P2_render_package.html`

Build the HTML directly:

1. **News headlines**: Use web search for 4-6 industry news items. Classify each as
   Threat / Your Brand / Watch / Opportunity. Write "So What" strategic implications.
2. **Community intelligence**: From Phase 1F, select the top 4 strategically relevant
   threads. Extract quotes, sources, strategic implications.
3. **Hook performance chart**: From Phase 1E, compute bar widths and signal badges
4. **Hook × format combos**: From the composite table, top 4 by median engagement
5. **Brand leaderboard**: From Phase 1B `rows` (never `directionalRows`), top 8 brands
6. **Paid presence**: From the boosted/organic split in 1B, plus the ad-account
   leaderboard from 1G when one is connected
7. **Action board**: Synthesize 3 cards (Defend / Attack / Watch) from all intelligence
8. Substitute into render template
9. Save as `P2_complete.html`

**Verify P2:** File size < 50KB, no placeholders, real data throughout.

### Phase 4 — Build Page 3 (Social Trends + Coaching)

Read these files:
- `references/P3_prompt.txt`
- `references/P3_output_schema.yaml`
- `references/P3_render_package.html`

Build the HTML directly:

1. **Creative profile**: From Phase 1E `focalVsRest`, extract the primary brand's dominant
   hook/format and the dimensions where its `useRate` is zero but the category's isn't
2. **5 trends**: From the Phase 1C ranking, group posts by creative pattern. Select 5
   trends the primary brand hasn't tested. Each needs proof, description, brand-specific
   play, and 3 source links using real `url` values.
3. **3 coaching posts**: From the primary brand's own ranked posts, select 3 with
   optimization potential. Write specific data-backed tweaks with signal badges.
4. **Methodology box**: how the analysis was done, and the coverage window it rests on
5. **Insert thumbnail images**: For each trend card and coaching card, look up the post's
   thumbnail URL in `thumbnails.json` and insert the base64 data URI. Every card must
   have a real image.
6. Substitute into render template, replacing `{{primary_brand}}` everywhere
7. Save as `P3_complete.html`

**Verify P3:** File size between 30KB and 200KB, no placeholders, all URLs real, all
`<img>` tags contain real base64 data.

### Phase 5 — Assemble PDF

1. **Verify all 3 HTML files exist and pass size checks**
2. **Install WeasyPrint** if needed:
   ```bash
   pip install weasyprint pypdf --break-system-packages
   ```
3. **Run the assembly script**:
   ```bash
   python3 {skill_path}/scripts/assemble_pdf.py \
     --pages P1_complete.html P2_complete.html P3_complete.html \
     --output weekly_brief_{primary_brand}_{week_start}.pdf \
     --working-dir {output_dir}
   ```

### Phase 6 — QA Check

Run the QA validation:
```bash
python3 {skill_path}/scripts/qa_check.py \
  --pages P1_complete.html P2_complete.html P3_complete.html \
  --working-dir {output_dir}
```

The QA script checks:
- File sizes are within budget (30KB-200KB for P1/P3, under 50KB for P2)
- No leftover `{{placeholder}}` tokens
- Real base64 images present (P1 needs 7, P3 needs 8)
- Real URLs in all links
- Correct page CSS dimensions

Fix any FAIL-level issues before delivering.

### Phase 7 — Deliver

Present the final PDF with a brief summary:
- Project and primary brand
- Date range covered
- One key highlight from each page
- **The coverage note**: which tracked sources are current through the window, and which
  are covered only through an earlier date or not yet acquired — by name. If the user
  wants those closed, that's a `pull_data` quote away, and `confirm_pull` charges.

## Reference Files

| File | Purpose | When to read |
|------|---------|-------------|
| `references/P1_prompt.txt` | Step-by-step data pipeline for Page 1 | Before building P1 |
| `references/P1_output_schema.yaml` | Field names + example values for P1 | Before building P1 |
| `references/P1_render_package.html` | HTML/CSS template for P1 | While building P1 |
| `references/P2_prompt.txt` | Step-by-step data pipeline for Page 2 | Before building P2 |
| `references/P2_output_schema.yaml` | Field names + example values for P2 | Before building P2 |
| `references/P2_render_package.html` | HTML/CSS template for P2 | While building P2 |
| `references/P3_prompt.txt` | Step-by-step data pipeline for Page 3 | Before building P3 |
| `references/P3_output_schema.yaml` | Field names + example values for P3 | Before building P3 |
| `references/P3_render_package.html` | HTML/CSS template for P3 | While building P3 |

**Important — DO NOT COPY ANYTHING FROM THE EXAMPLE SCHEMAS VERBATIM.** The
structural fields at the top of each YAML (`project_id`, `project_name`,
`primary_brand`) have been deliberately replaced with `EXAMPLE_*` placeholders
so it is syntactically obvious when they leak. The *prose* in the example
outputs (headlines, hooks, "so what" lines, coaching narratives) still uses real
brand names like Glossier, Rhode, MAC, and Fenty — those are kept for
pedagogical value to show what good output prose reads like, but every word of
that prose is fabricated. Pull all values from the live project scope; never
copy a sentence, headline, quote, or number from a schema into a real brief.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/download_thumbnails.py` | Downloads thumbnail images, resizes to 150x188px, base64-encodes, outputs JSON |
| `scripts/assemble_pdf.py` | Renders 3 HTML pages via WeasyPrint, merges into one PDF |
| `scripts/qa_check.py` | Validates completed HTML: real images present, no placeholders, real links, correct CSS |

## Adology Tools Used

- `whoami`, `list_portfolios`, `list_projects` — orient
- `get_project` — the scope and its per-source coverage state
- `create_project` / `update_project_scope` — fix the scope this brief is about
- `list_labels` / `get_table_data` — the label vocabulary, then the pivots on it
- `aggregate` — time series, brand leaderboard, boosted/organic split
- `query_items` — the window's ranked outliers by lift
- `analyze` — by-id hydration for thumbnails, urls, and creative fields; audience voice
- `pull_data` / `check_pull` / `confirm_pull` — close a coverage gap (`confirm_pull` charges)
- `fetch_comments` — bring post comments into the pool (two-step, charges)
- `list_ad_accounts` / `get_creative_leaderboard` — the brand's own paid performance

## External Tools Used

- **Web Search** — P2 news headlines (industry news for the competitive set)
- **WeasyPrint** — HTML-to-PDF rendering (installed via pip if needed)

## Design System — Energy V4

- Background: `#f0ead6` (warm cream)
- Primary dark: `#1a1a1a`
- Forest green: `#1b4332`
- Olive accent: `#6b8c1a`
- Lime highlight: `#c8e64a`
- Sage text: `#c5d5b5`, `#8fbc8f`
- Font: Helvetica Neue / Helvetica / Arial
- Page: 8.5in x 11in portrait, no margins (full bleed)

## File Size Budget

| File | Min Size | Max Size | What it means |
|------|----------|----------|---------------|
| P1_complete.html | 30KB | 200KB | Under 30KB = missing thumbnails. Over 200KB = full-res images embedded. |
| P2_complete.html | 5KB | 50KB | No images on P2. |
| P3_complete.html | 30KB | 200KB | Under 30KB = missing thumbnails. Over 200KB = full-res images embedded. |
| Final PDF | 100KB | 1MB | WeasyPrint with resized thumbnails should produce ~200-500KB. |

## Data Integrity Rules

- Every number comes from an actual Adology tool response (no fabrication)
- Engagement numbers: use raw values for computation, formatted ("187K") for display
- A lift multiple always appears with the baseline it was computed against
  (`likesMultiple` next to `sourceMedianLikes`) — a bare "5.2×" is not a finding
- Rank from an aggregate's `rows`; `directionalRows` entries appear only as texture,
  with their `n` stated
- URLs must be real permalinks from the item data
- Label dimensions and values come from the scope's own taxonomy, discovered with
  `list_labels` — never assumed
- If a field can't be computed from available data, use "N/A" — never invent data
- Boosted posts: state whether a number includes them or excludes them
- Week dating: `week_start` = Monday, `week_end` = Sunday. If the user gives a single
  date, compute the full Monday–Sunday range containing that date.
- Replace `{{primary_brand}}` everywhere with the actual brand name
- Every thumbnail `<img>` tag must contain a real base64 data URI from a real downloaded image
- The coverage note ships with the brief, naming stale and unacquired sources
