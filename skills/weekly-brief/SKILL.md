---
name: weekly-brief
description: >
  Build a 3-page Adology Weekly Competitive Intelligence Brief (PDF) from a knowledge set.
  Produces Page 1 (Visual Scoreboard + Intel Strip), Page 2 (Market Signals), and
  Page 3 (Social Trends + Coaching) — each built independently, then assembled into
  a single QA'd PDF with real thumbnails. Use this skill whenever the user says
  "weekly brief", "competitive brief", "run the brief", "weekly report",
  "competitive recap", "generate the report", "build the brief", or references
  the 3-page Adology report. Also trigger when the user asks for a competitive
  intelligence PDF, a weekly scoreboard, or says "brief me on [knowledge set]".
  Trigger liberally — if it sounds like they want a multi-page competitive
  analysis document from Adology data, this is the skill.
---

# Weekly Competitive Intelligence Brief

Build a polished 3-page PDF competitive intelligence report from an Adology knowledge set.
Each page is a self-contained "slide" with its own data pipeline, rendered as HTML via
WeasyPrint, then merged into a single PDF. Every page includes real post thumbnails.

## Architecture Rules

**DO NOT use subagents.** Build all 3 pages yourself, sequentially, in the main thread.
Subagents caused cascading failures in production — they made unchecked decisions,
crashed the sandbox disk, and couldn't be course-corrected.

**Thumbnails are MANDATORY.** Every scoreboard card, spotlight, trend card, and coaching
card must have a real thumbnail image from the actual post. The skill includes a bundled
script (`scripts/download_thumbnails.py`) that handles downloading, resizing, and
base64-encoding. You run this script — it produces a JSON file mapping post URLs to
small base64 data URIs. Then you insert those data URIs into the HTML `<img>` tags.
There is no alternative to this. Do not skip thumbnails. Do not use CSS placeholders.
Do not use colored rectangles with initials. Download the real images.

## Path Conventions

This skill's shell examples use two literal placeholders that you must substitute
before running any command:

- `{skill_path}` — the absolute path to this skill's directory (the directory
  containing this `SKILL.md`). At runtime this resolves to something like
  `/Users/<you>/.../skills/weekly-brief`. Use it to invoke bundled scripts under
  `scripts/` and to read reference files under `references/`.
- `{output_dir}` — the working/output directory for this brief's HTML, JSON,
  and final PDF artifacts. Pick a fresh directory per run (e.g.
  `outputs/<ks_name>-<week_end>/`) and substitute it consistently across the
  whole workflow.

If you see either placeholder in a command, **replace it with the actual path
before executing**. Do not pass the literal string `{skill_path}` to a shell.

## Overview

The brief has three pages:

- **Page 1 — Visual Scoreboard + Intel Strip**: Top 6 posts across brands (scoreboard
  grid with real thumbnails), primary brand spotlight, stat pills, insight bar, and a
  3-column intel strip with hook/creative/AI analysis.
- **Page 2 — Market Signals**: Industry news headlines with strategic signals, Reddit
  community intelligence, hook performance charts, brand engagement leaderboard, Meta
  Ad Library paid activity, and a 3-card action board (Defend / Attack / Watch).
- **Page 3 — Social Trends + Coaching**: 5 trend cards (with real thumbnails and source
  links), plus 3 coaching cards with real thumbnails showing how to optimize existing
  primary brand posts with specific data-backed tweaks.

## Workflow

### Phase 0 — Identify & Prepare Knowledge Set

1. **Ask for inputs** (if not already provided):
   - `primary_brand` — the brand being briefed (e.g. "WellWithAll")
   - `ks_name` — knowledge set name (e.g. "WellWithAll Energy")
   - `week_start` / `week_end` — the Monday–Sunday window (default: last full week)

2. **Find the knowledge set**: Call `list_knowledge_sets` and match by name. If not
   found, use the `brand-builder` skill to create one.

3. **Refresh if needed**: Call `trigger_fetch` on the knowledge set to ensure data is
   current. Check `get_workflow_status` — if a fetch is running, wait for it to complete.

4. **Validate the KS has enough data**: Call `get_table_data` with `rows = "brand"` and
   `feedTypes = ["brand"]`. Need at least 3 brands and 20+ posts. If insufficient,
   tell the user and suggest adding more brands.

### Phase 1 — Pull Shared Data (One Pass)

Before building any pages, pull the core data that multiple pages need. This avoids
redundant API calls and ensures consistency across pages.

**Step 1A — Top Posts (used by P1 + P3)**
Call `search_items` with:
  - `knowledgeSetId` = ks_id
  - `sortBy` = "engagement"
  - `limit` = 50
  - `feedTypes` = ["brand"]
  - Request fields: hookMechanism, creativeConcept, oneLineInsight, mediaType, thumbnail, url
  - Request labelFields: Hook, Creative

Store the full response. You'll extract:
- Top 6 unique-brand posts (excluding primary_brand) → P1 scoreboard
- Primary brand's top post → P1 spotlight
- Top 50 posts grouped by pattern → P3 trends
- Primary brand's top 10 → P3 coaching

**IMPORTANT**: Make sure the response includes `thumbnail` URLs for each post. You will
need these in Phase 1.5 to download real images.

**Step 1B — Aggregate Stats (used by P1 + P2)**
Call `get_table_data` with:
  - `rows` = "brand", `feedTypes` = ["brand"]  → total_posts, brand_count, median engagement
  - `rows` = "platform", `feedTypes` = ["brand"]  → platform_count

Call `search_items` with `feedTypes` = ["search","discussion"], `limit` = 1 to get
total organic mention count from the response metadata.

**Step 1C — Label Performance (used by P1 + P2 + P3)**
Call `get_table_data` with:
  - `rows` = "Hook"
  - `columns` = "focalVsRest"
  - `focalBrand` = primary_brand
  - `feedTypes` = ["brand"]
  - `metrics` = ["count", "medianLikes", "useRate"]
  - `topN` = 15

Store the full response. You'll extract:
- Hook multipliers → P1 insight bar + intel strip
- Per-brand hook performance → P2 charts
- Primary brand gaps → P3 trend selection

Also call with `rows` = "Creative" to get format data.

**Step 1D — Paid Activity (used by P2)**
Call `search_items` with:
  - `feedTypes` = ["adLibrary"]
  - `sortBy` = "date"
  - `limit` = 50

**Step 1E — Community Intelligence (used by P2)**
Call `search_items` with:
  - `feedTypes` = ["discussion"]
  - `sortBy` = "engagement"
  - `limit` = 20

**Verify the data pull.** Before proceeding, confirm you have:
- 20+ brand posts with engagement data and thumbnail URLs
- Label/hook distributions from get_table_data
- At least 3 brands in the aggregation
- Discussion feed results (even if sparse)

If any critical data is missing, tell the user what's unavailable and adjust the
affected page sections (use "Insufficient data" notes rather than fabricating).

### Phase 1.5 — Download Thumbnails (MANDATORY)

This step produces the real thumbnail images for the report. Do not skip it.

From the Phase 1A data, collect all thumbnail URLs you need:
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

A `null` value means that specific image couldn't be downloaded after retries. For
any `null` entries, go back to the Adology data and try an alternative thumbnail URL
from the same post (some posts have multiple image URLs). If there truly is no image
available for a post, swap that post out for the next-highest-engagement post that
does have a thumbnail. Every card in the final report must have a real image.

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

1. Compute stat pills (total_posts, organic_mentions, top_engagement, leader_vs_you)
2. Build scoreboard: deduplicate to 6 unique brands, extract hooks/labels
3. Build spotlight: primary brand's top post with gap-to-leader math
4. Compute insight bar text using the 3-tier threshold logic
5. Build intel strip: winning hook, creative momentum, AI brief
6. **Insert thumbnail images**: For each scoreboard card and the spotlight, look up
   the post's thumbnail URL in `thumbnails.json` and insert the base64 data URI into
   the `<img src="...">` tag. Every card must have a real image.
7. **For comments**: Try Apify. If unavailable, use the first 80 chars of the post
   caption as a preview in the comment area.
8. Substitute all values into the render template
9. Save as `P1_complete.html` in the outputs directory

**Verify P1 before moving on:**
- File size between 30KB and 200KB (under 30KB means you forgot the thumbnails)
- No `{{placeholder}}` tokens remaining
- All engagement numbers are real (from your data pull, not the schema examples)
- All `<img src="data:image/jpeg;base64,...">` tags contain real base64 data

### Phase 3 — Build Page 2 (Market Signals)

Read these files:
- `references/P2_prompt.txt`
- `references/P2_output_schema.yaml`
- `references/P2_render_package.html`

Build the HTML directly:

1. **News headlines**: Use web search for 4-6 industry news items. Classify each as
   Threat / Your Brand / Watch / Opportunity. Write "So What" strategic implications.
2. **Community intelligence**: From Phase 1E discussion data, select top 4 strategically
   relevant posts. Extract quotes, subreddit sources, strategic implications.
3. **Hook performance chart**: From Phase 1C labels, compute bar widths and signal badges
4. **Hook × format combos**: Cross-reference from label data, top 4 by median engagement
5. **Brand leaderboard**: From Phase 1B aggregation, top 8 brands by median engagement
6. **Paid activity**: From Phase 1D ad library data, top 5 brands by ad count
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

1. **Creative profile**: From Phase 1C, extract primary brand's dominant hook/format/gaps
2. **5 trends**: From Phase 1A top posts, group by creative pattern. Select 5 trends the
   primary brand hasn't tested. Each needs proof, description, brand-specific play, and
   3 source links with real URLs.
3. **3 coaching posts**: From primary brand's top 10, select 3 with optimization potential.
   Write specific data-backed tweaks with signal badges.
4. **Methodology box**: Summarize how the analysis was done
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
- Knowledge set and primary brand
- Date range covered
- One key highlight from each page
- Any data gaps noted

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
structural fields at the top of each YAML (`ks_id`, `ks_name`, `primary_brand`)
have been deliberately replaced with `EXAMPLE_*` placeholders so it is
syntactically obvious when they leak. The *prose* in the example outputs
(headlines, hooks, "so what" lines, coaching narratives) still uses real brand
names like Glossier, Rhode, MAC, and Fenty — those are kept for pedagogical
value to show what good output prose reads like, but every word of that prose
is fabricated. Pull all values from the actual knowledge set; never copy a
sentence, headline, quote, or number from a schema into a real brief.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/download_thumbnails.py` | Downloads thumbnail images, resizes to 150x188px, base64-encodes, outputs JSON |
| `scripts/assemble_pdf.py` | Renders 3 HTML pages via WeasyPrint, merges into one PDF |
| `scripts/qa_check.py` | Validates completed HTML: real images present, no placeholders, real links, correct CSS |

## Adology MCP Tools Used

- `list_knowledge_sets` — find the KS by name
- `get_knowledge_set` — get KS metadata
- `trigger_fetch` — refresh KS data
- `get_workflow_status` — check fetch progress
- `search_items` — pull posts sorted by engagement, filtered by brand/feedType
- `get_table_data` — label distributions, hook/format performance, multipliers

## External Tools Used

- **Apify MCP** (optional — if not connected, use post captions in comment areas):
  - `louisdeconinck/instagram-comments-scraper` — top comments for IG posts
  - `clockworks/tiktok-comments-scraper` — top comments for TikTok posts
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

- Every number must come from an actual Adology MCP response (no fabrication)
- Engagement numbers: use raw values for computation, formatted ("187K") for display
- URLs must be real permalinks from Adology item data
- Labels/hooks must be extracted from actual Adology label arrays
- If a field can't be computed from available data, use "N/A" — never invent data
- Week dating: `week_start` = Monday, `week_end` = Sunday. If user gives a single date,
  compute the full Monday–Sunday range containing that date.
- Replace `{{primary_brand}}` everywhere with the actual brand name
- Every thumbnail `<img>` tag must contain a real base64 data URI from a real downloaded image
