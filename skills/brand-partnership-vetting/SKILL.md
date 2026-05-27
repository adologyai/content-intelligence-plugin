---
name: brand-partnership-vetting
description: >
  Vet, score, and shortlist brand co-marketing partners using content intelligence.
  Produces an editorial HTML report with executive summary, competitor partnership
  matrix, ranked shortlist, scorecards with reference thumbnails, adapted partnership
  briefs with positioning callouts, and a creator activation map. Use whenever the
  user mentions brand partnerships, co-marketing, partner shortlists, or
  brand-to-brand collaborations — even without explicit "vetting" language. Trigger
  on "vet brand partners", "brand partnership vetting", "score brands as partners",
  "find brand partners", "co-marketing partners", "is this brand a good partner",
  "partnership shortlist", "partnership scorecard", "brand partnership audit",
  "brand-to-brand partnerships", "who should we partner with". Also trigger when
  someone pastes brand names for evaluation as partners, or describes a focal brand
  and wants partnership candidates. Partnership counterpart to influencer-vetting.
---

# Brand Partnership Vetting & Selection

Self-contained skill. Everything you need — methodology, full HTML production
template with CSS, thumbnail download script, section-by-section guidance — is in
this file.

## What This Skill Does

Takes a partnership brief, sources or evaluates candidate partner brands, scores them
on observable content signals across seven weighted dimensions, and produces ranked
scorecards with adapted partnership briefs and positioning implications for top
picks. Final deliverable is an editorial HTML report a CMO or BD lead can print and
circulate.

## What You Can and Cannot Assess

**Content intelligence shows you:** brand voice and emotional register, existing
partnership behavior, audience lifestyle signals, cultural currency, competitor
precedent when triangulating against the focal brand's category peers.

**Content intelligence cannot tell you:** verified audience demographics, partnership
pricing or commercial terms, partnership-team responsiveness, past partnership
performance or conversion lift, active pipeline partnerships not yet in market, legal
or compliance conflicts, whether content overlap translates to purchase behavior.

This is why every report ends with a "Verify Externally" checklist — flagging
exactly what the user must check through other means.

## Phase 1: Partnership Brief Intake

Partner-fit is entirely relative to the brief. Don't proceed without these inputs.

**Required:** focal brand name, partnership goal, target audience (specific, not
"Gen Z"), focal brand voice posture.

**Strongly recommended:** use cases to amplify, partner archetypes of interest (earn
money / spend money / manage habits / relieve bill stress / aspiration unlock /
cultural moment), competitive context, partnership budget tier, number of picks.

**Optional but valuable:** existing partnerships to avoid, must-haves, dealbreakers,
internal stakeholder for the deliverable.

If the user just drops brand names without a brief, ask for the brief. Be friendly:
"Before I vet these, I need to understand the partnership strategy so I can score
them against something real."

## Phase 2: Candidate Sourcing

Two paths.

**Path A — User provides a list.** Proceed directly to Phase 3.

**Path B — Discovery.** Three steps:
1. Audit the focal brand's competitive set first. Pull existing partnership content
   from 2–3 direct competitors to see what lanes are occupied. Partnership recs are
   largely a function of where competitors are NOT.
2. Generate a longlist organized by partner archetype (4–6 brands per archetype,
   20–30 candidates total). Weight selection toward brands the audience already uses
   and trusts, brands with visible partnership behavior, and brands no competitor
   has partnered with yet.
3. Sanity-check with the user. "Here are 20 candidates organized by archetype. Any
   to drop, any to add?" Don't block on approval — Phase 3 is efficient at scale.

## Phase 3: Content Intelligence Analysis

Two-pass model. First-pass at consistent depth across all candidates; deep-dive on
specific brands by request.

### First Pass (default — all candidates, ~6–8 posts each)

1. `batch_add_feeds` to add all candidate brands + 2–3 competitors as feeds.
2. `trigger_fetch` to collect content.
3. For each candidate, run `analyze` with:
   ```
   distribution: "top"
   limit: 6-8
   feedNames: ["BrandName"]
   fields: [
     "adDescription", "mainMessage", "brandPositioning",
     "targetAudienceLifestyle", "creativeConcept", "uniqueSellingProposition",
     "oneLineInsight", "emotionalStrategy", "thumbnail", "url"
   ]
   ```
4. Pull the focal brand at the same depth as a baseline.
5. Pull each direct competitor for the Precedent dimension, focusing on partnership
   content.

`adDescription` is the most important field — it's a comprehensive AI-written
description of each post including visual + narrative + creative choice. Combined
with `mainMessage`, `brandPositioning`, `targetAudienceLifestyle`, and
`emotionalStrategy`, it gives enough signal to score every dimension.

### Deep Dive (on request)

When the user says "go deeper on [brand]": pull 30–50 posts via `analyze` with
higher `limit`, use `get_table_data` for label distributions, `get_item_detail` for
top posts with full transcripts, `search_items` for partnership-specific content.
Re-score with higher confidence.

### Empty Feeds

Some brand handles don't resolve cleanly to active accounts (e.g., `dave` matches
a person, not Dave the banking app; `step` matches an unrelated account). If a feed
comes back empty, use `discover_brands` to verify, or pass exact known handles
(`davebanking`, `stepmobile`, `acorns_app`). Re-add and re-trigger fetch on those
feeds only.

## Phase 4: Scoring on Seven Dimensions

Each candidate scored across these seven dimensions. Weights sum to 100%.

**Voice & Values Fit (20%)** — Does the brand's voice and values match the focal
brand? Read the candidate's content for voice fingerprint, then compare directly to
the focal brand's content. Translation cost matters: how much would the focal brand
have to bend to make co-branded content land naturally?

**Audience Overlap (15%)** — Does the audience plausibly overlap with the focal
brand's user? Read `targetAudienceLifestyle`, comment texture, engagement patterns.
Be honest — lifestyle labels are directional; demographic verification requires
third-party panels.

**Utility Fit (20%)** — Does the brand solve a money-adjacent (or category-adjacent)
problem the focal audience has? Map to one of the partner archetypes. The strongest
candidates hit two utility frames at once (e.g., DoorDash hits both *earn* and
*spend* for a fintech).

**Cultural Currency (10%)** — Is the brand having a cultural moment? Look at
`likesMultiple`, `isOutlier`, viral content frequency, cultural-reference density.

**Activation Readiness (10%)** — How partnership-prone is the brand? Volume and
variety of past co-marketing, quality of existing partnership creative,
infrastructure (Walmart Connect, custom card programs, creator pipelines).

**Precedent & White Space (10%)** — Has any direct competitor of the focal brand
already partnered in this category? If yes, what's the lesson and why follow rather
than lead elsewhere? If no, is the white space real or a category warning?

**Strategic Asymmetry (15%)** — Is the value-exchange roughly balanced? Symmetric
is best. Asymmetric in the partner's favor (they don't need this) makes the
partnership hard to land. Asymmetric in the focal brand's favor sounds great but
partners disengage. Name the value exchange explicitly.

**Overall Score** = 0.20·Voice + 0.15·Audience + 0.20·Utility + 0.10·Currency +
0.10·Readiness + 0.10·Precedent + 0.15·Asymmetry.

**Tier thresholds:** 78+ pursue (Tier 1), 62–77 pilot (Tier 2), 48–61 watchlist
(Tier 3), <48 pass.

**Confidence chip per scorecard:** High (200+ posts in feed, 6+ scored), Medium
(50–200 posts), Low (<50 posts, treat as preliminary).

**Brand Safety** is treated as a red-flag callout, not a scored dimension. Flag
explicitly: voice mismatch severe, audience mismatch severe, lane already occupied
by a competitor, recent controversy, asymmetric value to a problematic degree.

## Phase 5: Adapted Partnership Briefs (Tier 1 Only)

For each Tier 1 candidate, produce a brief with these sections:

1. **Pitch line** — One sentence describing the partnership concept.
2. **Positioning implication** — *Critical and unique to brand-partnership work.*
   Each Tier 1 partnership reshapes the focal brand's identity differently. Name
   the tradeoff: "If this lands, [focal] becomes [X]. Risk: [Y]. Best for a
   strategy that [Z]." Picking one is a positioning choice, not just a partnership
   choice.
3. **Recommended archetype** — Embedded utility, content franchise, brand-narrative,
   celebrity-led activation, etc.
4. **First activation** — Specific first thing to launch.
5. **Messaging angles in focal brand voice** — 3–4 lines that sound like the focal
   brand, not the partner.
6. **Non-negotiables** — FTC, compliance, exclusivity, brand standards.
7. **BD-side pitch target** — Which team, which department, what's the right
   inroad.
8. **Why this wins** — 3 bullets summarizing scoring + time-to-launch estimate.

## Phase 6: Creator Activation Map (Optional)

If the knowledge set has fintok / vertical-relevant creator feeds, add a Creator
Activation Map to the report. Map each creator to one Tier 1 partnership with a
casting rationale. Turns the report from "here are some ideas" into "here are some
ideas and here's the creator who activates each one."

---

## Output: Full HTML Production

The deliverable is an editorial HTML report saved to
`outputs/<focal>_partnership_vetting_report.html`. Visual style: warm cream
background, white surfaces, single accent color from the focal brand's identity,
three-tier color system, editorial sans-serif typography.

**Accent color selection.** Pick from the focal brand's primary palette:
- Fintech green (`#1B7B3F`) for MoneyLion-style pragmatic financial brands
- Saturated red (`#c8102e`) for Neutrogena-style health/beauty brands
- Saturated blue (`#0066cc`) for tech/SaaS brands
- Default: deep, saturated, single-tone color from the focal brand's primary
  palette. Avoid neon, gradients, or multi-tone systems.

### Full HTML Skeleton

Copy this skeleton, swap the accent color, and fill in the section content. Save
to `outputs/<focal>_partnership_vetting_report.html`.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>[Focal Brand] — Brand Partnership Vetting Report</title>
<style>
  :root {
    --bg: #faf8f5;
    --surface: #ffffff;
    --ink: #1a1a1a;
    --ink-dim: #4a4a4a;
    --ink-faint: #858585;
    --accent: #1B7B3F;        /* CHANGE — focal brand accent */
    --accent-ink: #0F4D27;    /* darker shade of accent */
    --accent-soft: #e8f3ec;   /* tinted bg for callouts */
    --line: #e8e4df;
    --line-soft: #f1ede7;
    --t1: #0e7a4f;
    --t1-bg: #e6f5ee;
    --t2: #8a6700;
    --t2-bg: #fdf3d4;
    --t3: #7b3ba3;
    --t3-bg: #f3e9fa;
    --warn: #b54400;
    --warn-bg: #fff1e6;
    --info-bg: #eef4f9;
    --info-ink: #2a4d6a;
    --good-bg: #ecf5ef;
  }
  * { box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Helvetica Neue", sans-serif;
    background: var(--bg);
    color: var(--ink);
    margin: 0;
    line-height: 1.55;
    font-size: 15px;
  }
  .wrap { max-width: 1160px; margin: 0 auto; padding: 56px 32px 96px; }
  header.hero { border-bottom: 1px solid var(--line); padding-bottom: 40px; margin-bottom: 48px; }
  .kicker { font-size: 12px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--accent); font-weight: 700; margin-bottom: 10px; }
  h1 { font-size: 44px; line-height: 1.08; margin: 0 0 16px; font-weight: 800; letter-spacing: -0.02em; }
  h1 span { color: var(--accent); }
  .subtitle { font-size: 17px; color: var(--ink-dim); max-width: 760px; }
  .meta-strip { margin-top: 24px; display: flex; flex-wrap: wrap; gap: 10px 24px; font-size: 13px; color: var(--ink-faint); }
  .meta-strip strong { color: var(--ink); }
  h2 { font-size: 26px; font-weight: 800; margin: 64px 0 8px; letter-spacing: -0.01em; }
  h2 + .section-sub { color: var(--ink-dim); font-size: 15px; margin-bottom: 24px; max-width: 820px; }
  h3 { font-size: 20px; font-weight: 700; margin: 0; letter-spacing: -0.005em; }
  h4 { font-size: 18px; margin: 0 0 16px; font-weight: 700; }
  h5 { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--ink-faint); margin: 16px 0 8px; }

  /* Executive summary */
  .exec { background: var(--accent-soft); border-left: 4px solid var(--accent); border-radius: 6px 12px 12px 6px; padding: 28px 32px; margin-bottom: 40px; }
  .exec h4 { color: var(--accent-ink); font-size: 13px; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 14px; }
  .exec-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 24px; margin-top: 16px; }
  .exec-grid h5 { color: var(--accent-ink); margin-top: 0; }
  .exec-grid p { font-size: 14px; color: var(--ink-dim); margin: 0 0 6px; line-height: 1.55; }
  .exec-grid strong { color: var(--ink); font-weight: 600; }

  /* Brief summary */
  .brief-summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 18px; margin-bottom: 32px; }
  .brief-cell { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 16px 18px; }
  .brief-cell .label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--ink-faint); margin-bottom: 6px; }
  .brief-cell .val { font-size: 15px; color: var(--ink); font-weight: 600; }

  /* Methodology */
  .method { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 28px; margin-bottom: 32px; }
  .method-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; margin-top: 16px; }
  .weight-row { display: flex; align-items: center; gap: 12px; padding: 10px 0; border-bottom: 1px solid var(--line-soft); }
  .weight-row:last-child { border: none; }
  .weight-chip { background: var(--accent); color: white; font-weight: 700; font-size: 13px; padding: 4px 10px; border-radius: 99px; min-width: 48px; text-align: center; }
  .weight-label strong { display: block; font-size: 14px; }
  .weight-label span { font-size: 13px; color: var(--ink-dim); }

  /* Competitor matrix */
  .comp-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }
  .comp-card { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 24px; }
  .comp-card h4 { margin-bottom: 6px; }
  .comp-card .comp-pos { font-size: 13px; color: var(--ink-dim); margin-bottom: 16px; line-height: 1.5; }
  .comp-thumbs { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 14px; }
  .comp-thumb { position: relative; aspect-ratio: 4 / 5; border-radius: 6px; overflow: hidden; background: #f0ebe4; border: 1px solid var(--line-soft); }
  .comp-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .comp-thumb .cap { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.85), rgba(0,0,0,0)); color: white; padding: 16px 8px 8px; font-size: 11px; line-height: 1.3; font-weight: 600; }
  .comp-claim { font-size: 12.5px; color: var(--ink-dim); border-top: 1px solid var(--line-soft); padding-top: 10px; }
  .comp-claim strong { color: var(--ink); display: block; font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; }
  .ml-lane { background: var(--accent-soft); border: 1px solid var(--accent); border-radius: 10px; padding: 20px 24px; margin-top: 20px; }
  .ml-lane h5 { color: var(--accent-ink); margin-top: 0; }
  .ml-lane p { font-size: 14px; color: var(--ink-dim); margin: 0; line-height: 1.55; }
  .ml-lane strong { color: var(--ink); }

  /* Ranked table */
  .table-wrap { overflow-x: auto; border: 1px solid var(--line); border-radius: 10px; background: var(--surface); }
  table.ranks { width: 100%; border-collapse: collapse; font-size: 14px; }
  table.ranks th { background: #f7f3ee; padding: 12px 14px; text-align: left; font-weight: 700; color: var(--ink); border-bottom: 1px solid var(--line); font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em; }
  table.ranks td { padding: 12px 14px; border-bottom: 1px solid var(--line-soft); }
  table.ranks tr:last-child td { border-bottom: none; }
  table.ranks td.right { text-align: right; font-variant-numeric: tabular-nums; }
  table.ranks td.score { font-weight: 700; color: var(--accent); }

  /* Badges */
  .badge { display: inline-block; padding: 3px 10px; border-radius: 99px; font-size: 11px; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; }
  .badge.t1 { background: var(--t1-bg); color: var(--t1); }
  .badge.t2 { background: var(--t2-bg); color: var(--t2); }
  .badge.t3 { background: var(--t3-bg); color: var(--t3); }
  .badge.conf-h { background: var(--good-bg); color: var(--t1); }
  .badge.conf-m { background: var(--t2-bg); color: var(--t2); }
  .badge.conf-l { background: var(--warn-bg); color: var(--warn); }

  /* Scorecards */
  .creator-card { background: var(--surface); border: 1px solid var(--line); border-left: 4px solid var(--line); border-radius: 10px; padding: 28px; margin-bottom: 24px; }
  .creator-card.t1 { border-left-color: var(--t1); }
  .creator-card.t2 { border-left-color: var(--t2); }
  .creator-card.t3 { border-left-color: var(--t3); }
  .creator-head { display: flex; justify-content: space-between; align-items: flex-start; gap: 24px; margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid var(--line-soft); }
  .creator-meta { margin-top: 8px; display: flex; gap: 16px; align-items: center; flex-wrap: wrap; font-size: 13px; color: var(--ink-dim); }
  .overall { text-align: right; flex-shrink: 0; }
  .overall-num { font-size: 42px; font-weight: 800; color: var(--accent); line-height: 1; font-variant-numeric: tabular-nums; }
  .overall-label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.12em; color: var(--ink-faint); margin-top: 4px; }

  .stat-strip { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 8px; margin-bottom: 18px; }
  .stat-cell { background: #fbf9f6; border: 1px solid var(--line-soft); border-radius: 6px; padding: 10px 12px; }
  .stat-cell .stat-label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--ink-faint); margin-bottom: 3px; }
  .stat-cell .stat-val { font-size: 13px; color: var(--ink); font-weight: 600; }

  .voice-fingerprint { background: var(--accent-soft); border-left: 3px solid var(--accent); border-radius: 4px 8px 8px 4px; padding: 14px 18px; margin-bottom: 18px; font-size: 14px; color: var(--ink-dim); }
  .voice-fingerprint strong { display: block; font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--accent-ink); margin-bottom: 6px; }

  .dim-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; }
  .dim { background: #fbf9f6; border: 1px solid var(--line-soft); border-radius: 8px; padding: 14px 16px; }
  .dim-head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 6px; }
  .dim-label { font-size: 13px; font-weight: 700; }
  .wt { color: var(--ink-faint); font-weight: 500; font-size: 11px; margin-left: 4px; }
  .dim-score { font-size: 22px; font-weight: 800; color: var(--accent); font-variant-numeric: tabular-nums; }
  .dim-score .out { font-size: 12px; color: var(--ink-faint); font-weight: 500; }
  .dim-just { font-size: 13px; color: var(--ink-dim); line-height: 1.5; }

  /* Evidence cards */
  .evidence-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-top: 18px; }
  .evidence-card { background: white; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; }
  .evidence-card .thumb { width: 100%; aspect-ratio: 4 / 5; object-fit: cover; display: block; background: #f0ebe4; }
  .evidence-body { padding: 10px 12px 12px; flex: 1; display: flex; flex-direction: column; gap: 8px; }
  .evidence-tag { font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--accent); font-weight: 700; }
  .evidence-note { font-size: 12px; line-height: 1.4; color: var(--ink-dim); flex: 1; }
  .evidence-link a { font-size: 11px; color: var(--accent); text-decoration: none; font-weight: 600; }
  .evidence-link a:hover { text-decoration: underline; }

  /* Red flags */
  .redflag { margin-top: 18px; background: var(--warn-bg); border: 1px solid #f2d4b8; border-radius: 8px; padding: 12px 16px; color: var(--warn); font-size: 14px; }
  .redflag strong { display: block; font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }
  .redflag ul { margin: 0; padding-left: 18px; }
  .redflag li { margin-bottom: 4px; }

  /* Brief cards */
  .brief-card { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 28px; margin-bottom: 20px; }
  .brief-card h3 { color: var(--accent-ink); margin-bottom: 4px; }
  .brief-card .pitch-line { color: var(--ink-dim); font-size: 14px; margin-bottom: 18px; }
  .position-callout { background: var(--info-bg); border-left: 3px solid var(--info-ink); border-radius: 4px 8px 8px 4px; padding: 14px 18px; margin-bottom: 18px; font-size: 14px; color: var(--ink-dim); }
  .position-callout strong { color: var(--info-ink); display: block; font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }
  .position-callout em { color: var(--ink); font-style: normal; font-weight: 600; }
  .brief-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; }
  .brief-col h5 { margin-top: 0; }
  .brief-col ul { margin: 0 0 12px; padding-left: 18px; font-size: 13.5px; color: var(--ink-dim); }
  .brief-col li { margin-bottom: 5px; }
  .kv { margin-bottom: 6px; font-size: 13.5px; }
  .kv > span:first-child { font-weight: 600; color: var(--ink); }
  .kv > span:last-child { color: var(--ink-dim); }

  /* Creator activation map */
  .creator-map { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-bottom: 24px; }
  .creator-row { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 18px 20px; }
  .creator-row h4 { font-size: 15px; margin-bottom: 4px; }
  .creator-row .creator-handle { font-size: 12px; color: var(--ink-faint); margin-bottom: 12px; }
  .creator-row .activates { font-size: 13px; color: var(--ink-dim); line-height: 1.55; }
  .creator-row .activates strong { color: var(--accent-ink); }
  .creator-row .stats { font-size: 11px; color: var(--ink-faint); margin-top: 10px; padding-top: 8px; border-top: 1px solid var(--line-soft); }

  /* Checklist */
  .checklist { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 28px; margin-bottom: 24px; }
  .checklist ul { list-style: none; padding: 0; margin: 0; }
  .checklist li { padding: 12px 0; border-bottom: 1px solid var(--line-soft); display: flex; gap: 12px; align-items: flex-start; }
  .checklist li:last-child { border: none; }
  .checklist .box { width: 18px; height: 18px; border: 2px solid var(--accent); border-radius: 4px; margin-top: 3px; flex-shrink: 0; }
  .checklist strong { display: block; margin-bottom: 2px; }
  .checklist span { color: var(--ink-dim); font-size: 13.5px; }

  /* Disclosures */
  .disclosures { background: #fff9f5; border: 1px solid #f1dcc7; border-radius: 10px; padding: 20px 24px; font-size: 13.5px; color: var(--ink-dim); margin: 24px 0; }
  .disclosures h4 { color: var(--warn); margin-bottom: 8px; font-size: 13px; text-transform: uppercase; letter-spacing: 0.08em; }

  footer { margin-top: 72px; padding-top: 24px; border-top: 1px solid var(--line); font-size: 12px; color: var(--ink-faint); }

  @media print { body { background: white; } .creator-card, .brief-card, .method, .checklist, .comp-card, .exec { break-inside: avoid; } }
  @media (max-width: 760px) { .comp-grid { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<div class="wrap">

  <!-- HERO -->
  <header class="hero">
    <div class="kicker">Adology Brand Partnership Vetting</div>
    <h1>[Focal Brand] <span>Co-Marketing Partner</span><br>Shortlist &amp; Scorecard</h1>
    <div class="subtitle">[1-2 sentence description of the report]</div>
    <div class="meta-strip">
      <div><strong>Prepared for:</strong> [team]</div>
      <div><strong>Data source:</strong> Adology content intelligence (N candidates, M competitors, K creators)</div>
      <div><strong>Date:</strong> [Month Year]</div>
      <div><strong>Brands scored:</strong> [N]</div>
    </div>
  </header>

  <!-- EXEC SUMMARY -->
  <h2 style="margin-top:0">Executive Summary</h2>
  <div class="section-sub">If you read nothing else.</div>
  <div class="exec">
    <h4>The bottom line</h4>
    <div class="exec-grid">
      <div><h5>The thesis</h5><p>[1 paragraph naming the strategic insight]</p></div>
      <div><h5>The picks</h5><p>[Tier 1 brands with one-line rationales]</p></div>
      <div><h5>The positioning choice</h5><p>[How each Tier 1 reshapes the focal brand. End with: "Pick one — they're not additive."]</p></div>
      <div><h5>What to do this quarter</h5><p>[Sequenced first move with time-to-launch estimates]</p></div>
    </div>
  </div>

  <!-- PARTNERSHIP BRIEF -->
  <h2>Partnership Brief</h2>
  <div class="section-sub">All scoring decisions are relative to this brief.</div>
  <div class="brief-summary">
    <div class="brief-cell"><div class="label">Brand</div><div class="val">[Focal]</div></div>
    <div class="brief-cell"><div class="label">Goal</div><div class="val">[Goal]</div></div>
    <div class="brief-cell"><div class="label">Audience</div><div class="val">[Audience]</div></div>
    <div class="brief-cell"><div class="label">Voice posture</div><div class="val">[Voice]</div></div>
    <div class="brief-cell"><div class="label">Use cases to amplify</div><div class="val">[Use cases]</div></div>
    <div class="brief-cell"><div class="label">Partner archetypes</div><div class="val">[Archetypes]</div></div>
    <div class="brief-cell"><div class="label">Competitive context</div><div class="val">[What competitors own]</div></div>
    <div class="brief-cell"><div class="label">Target picks</div><div class="val">[N to pursue, M to pilot]</div></div>
  </div>

  <!-- COMPETITOR MATRIX -->
  <h2>What Competitors Are Doing</h2>
  <div class="section-sub">Inventory of [Competitor 1] and [Competitor 2]'s recent partnership content. The clearer the lanes they own, the cleaner the white space [focal] can claim.</div>
  <div class="comp-grid">
    <div class="comp-card">
      <h4>[Competitor 1] — [positioning summary]</h4>
      <div class="comp-pos">[1-2 sentence positioning read]</div>
      <div class="comp-thumbs">
        <div class="comp-thumb"><img src="thumbs/comp1_a.jpg" alt="..."><div class="cap">[caption]</div></div>
        <div class="comp-thumb"><img src="thumbs/comp1_b.jpg" alt="..."><div class="cap">[caption]</div></div>
        <div class="comp-thumb"><img src="thumbs/comp1_c.jpg" alt="..."><div class="cap">[caption]</div></div>
        <div class="comp-thumb"><img src="thumbs/comp1_d.jpg" alt="..."><div class="cap">[caption]</div></div>
      </div>
      <div class="comp-claim"><strong>Lanes they own</strong>[Category 1] · [Category 2] · [Category 3]</div>
    </div>
    <div class="comp-card">
      <h4>[Competitor 2] — [positioning summary]</h4>
      <!-- same structure -->
    </div>
  </div>
  <div class="ml-lane">
    <h5>The lane [focal] can claim</h5>
    <p>[Strategic argument: neither competitor has touched X. The fight isn't over Y. It's over Z. Tie back to the focal brand's voice and what it can credibly own.]</p>
  </div>

  <!-- METHODOLOGY -->
  <h2>Methodology</h2>
  <div class="section-sub">Seven-dimensional weighted scoring, transparent weights, every score backed by post evidence. Brand Safety is a red-flag callout, not a scored dimension.</div>
  <div class="method">
    <div class="method-grid">
      <div>
        <h5>Scoring weights (sum to 100%)</h5>
        <div class="weight-row"><div class="weight-chip">20%</div><div class="weight-label"><strong>Voice &amp; Values Fit</strong><span>Brand voice and emotional register vs. focal</span></div></div>
        <div class="weight-row"><div class="weight-chip">15%</div><div class="weight-label"><strong>Audience Overlap</strong><span>Plausible user-base overlap</span></div></div>
        <div class="weight-row"><div class="weight-chip">20%</div><div class="weight-label"><strong>Utility Fit</strong><span>Solves a real category-adjacent problem</span></div></div>
        <div class="weight-row"><div class="weight-chip">10%</div><div class="weight-label"><strong>Cultural Currency</strong><span>Brand momentum and cultural relevance</span></div></div>
        <div class="weight-row"><div class="weight-chip">10%</div><div class="weight-label"><strong>Activation Readiness</strong><span>How partnership-prone the brand is</span></div></div>
        <div class="weight-row"><div class="weight-chip">10%</div><div class="weight-label"><strong>Precedent &amp; White Space</strong><span>Competitor track record in the category</span></div></div>
        <div class="weight-row"><div class="weight-chip">15%</div><div class="weight-label"><strong>Strategic Asymmetry</strong><span>Value-exchange balance and halo direction</span></div></div>
      </div>
      <div>
        <h5>Tier thresholds</h5>
        <div class="kv"><span>78+ </span><span>Pursue now (Tier 1)</span></div>
        <div class="kv"><span>62 – 77</span><span>Pilot or test (Tier 2)</span></div>
        <div class="kv"><span>48 – 61</span><span>Watchlist with caveats (Tier 3)</span></div>
        <div class="kv"><span>Below 48</span><span>Pass for this strategy</span></div>
        <h5 style="margin-top:24px">Confidence calibration</h5>
        <ul style="font-size:13.5px;color:var(--ink-dim);padding-left:18px;margin:0">
          <li><strong>High:</strong> 200+ posts in feed, 6+ scored items pulled</li>
          <li><strong>Medium:</strong> 50–200 posts, directional signal</li>
          <li><strong>Low:</strong> &lt;50 posts, treat as preliminary</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- RANKED SHORTLIST -->
  <h2>Ranked Shortlist</h2>
  <div class="section-sub">All candidates ranked by overall score. Confidence chip indicates how much weight to put on the score given sample density.</div>
  <div class="table-wrap">
    <table class="ranks">
      <thead><tr><th>#</th><th>Brand</th><th>Tier</th><th>Confidence</th><th>Archetype</th><th class="right">Voice</th><th class="right">Aud.</th><th class="right">Utility</th><th class="right">Currency</th><th class="right">Ready</th><th class="right">Prec.</th><th class="right">Asym.</th><th class="right">Overall</th></tr></thead>
      <tbody>
        <tr><td>1</td><td><strong>[Brand]</strong></td><td><span class="badge t1">Tier 1</span></td><td><span class="badge conf-h">High</span></td><td>[archetype]</td><td class="right">XX</td><td class="right">XX</td><td class="right">XX</td><td class="right">XX</td><td class="right">XX</td><td class="right">XX</td><td class="right">XX</td><td class="right score">XX</td></tr>
        <!-- repeat per brand -->
      </tbody>
    </table>
  </div>

  <!-- SCORECARDS -->
  <h2>Scorecards</h2>
  <div class="section-sub">One scorecard per brand, ordered by overall score. Tier 1 cards include real reference thumbnails on each evidence card.</div>

  <!-- TIER 1 SCORECARD TEMPLATE -->
  <div class="creator-card t1">
    <div class="creator-head">
      <div>
        <h3>1. [Brand] <span class="badge t1" style="margin-left:8px">Tier 1 — Pursue now</span> <span class="badge conf-h" style="margin-left:6px">High confidence</span></h3>
        <div class="creator-meta">
          <span><strong>Archetype:</strong> [archetype]</span>
          <span><strong>Platforms:</strong> [platforms]</span>
          <span><strong>Posts in feed:</strong> [N]</span>
          <span><strong>Items scored:</strong> [M]</span>
        </div>
      </div>
      <div class="overall"><div class="overall-num">XX</div><div class="overall-label">Overall</div></div>
    </div>
    <div class="stat-strip">
      <div class="stat-cell"><div class="stat-label">Content volume</div><div class="stat-val">[N items]</div></div>
      <div class="stat-cell"><div class="stat-label">Top platform</div><div class="stat-val">[platform]</div></div>
      <div class="stat-cell"><div class="stat-label">Audience lifestyle</div><div class="stat-val">[lifestyle]</div></div>
      <div class="stat-cell"><div class="stat-label">Past fintech tie</div><div class="stat-val">[Yes/No/details]</div></div>
      <div class="stat-cell"><div class="stat-label">Voice similarity to [focal]</div><div class="stat-val">[High/Mid/Low]</div></div>
      <div class="stat-cell"><div class="stat-label">Most recent post</div><div class="stat-val">[date]</div></div>
    </div>
    <div class="voice-fingerprint">
      <strong>Voice fingerprint vs. [focal]</strong>
      [2-3 sentences comparing the candidate's voice to the focal brand's. Cite specific posts. End with the bridge or the gap.]
    </div>
    <div class="dim-grid">
      <div class="dim"><div class="dim-head"><div class="dim-label">Voice &amp; Values Fit<span class="wt">20%</span></div><div class="dim-score">XX<span class="out">/100</span></div></div><div class="dim-just">[justification with evidence]</div></div>
      <div class="dim"><div class="dim-head"><div class="dim-label">Audience Overlap<span class="wt">15%</span></div><div class="dim-score">XX<span class="out">/100</span></div></div><div class="dim-just">[justification]</div></div>
      <div class="dim"><div class="dim-head"><div class="dim-label">Utility Fit<span class="wt">20%</span></div><div class="dim-score">XX<span class="out">/100</span></div></div><div class="dim-just">[justification]</div></div>
      <div class="dim"><div class="dim-head"><div class="dim-label">Cultural Currency<span class="wt">10%</span></div><div class="dim-score">XX<span class="out">/100</span></div></div><div class="dim-just">[justification]</div></div>
      <div class="dim"><div class="dim-head"><div class="dim-label">Activation Readiness<span class="wt">10%</span></div><div class="dim-score">XX<span class="out">/100</span></div></div><div class="dim-just">[justification]</div></div>
      <div class="dim"><div class="dim-head"><div class="dim-label">Precedent &amp; White Space<span class="wt">10%</span></div><div class="dim-score">XX<span class="out">/100</span></div></div><div class="dim-just">[justification]</div></div>
      <div class="dim"><div class="dim-head"><div class="dim-label">Strategic Asymmetry<span class="wt">15%</span></div><div class="dim-score">XX<span class="out">/100</span></div></div><div class="dim-just">[justification]</div></div>
    </div>
    <div class="evidence-row">
      <div class="evidence-card"><img class="thumb" src="thumbs/[brand]_a.jpg" alt="..."><div class="evidence-body"><div class="evidence-tag">Voice evidence</div><div class="evidence-note">[strategic note]</div><div class="evidence-link"><a href="[post_url]" target="_blank">View post →</a></div></div></div>
      <!-- 4 evidence cards total -->
    </div>
  </div>

  <!-- Tier 2 scorecards: same structure, no thumbnails. Tier 3: same plus .redflag block. -->

  <!-- ADAPTED BRIEFS -->
  <h2>Adapted Partnership Briefs — Top 3</h2>
  <div class="section-sub">Each Tier 1 brief includes a positioning implication callout. Picking one is a positioning choice, not just a partnership choice.</div>
  <div class="brief-card">
    <h3>[Partner] × [Focal] — [Concept Name]</h3>
    <div class="pitch-line">[One sentence describing the partnership concept]</div>
    <div class="position-callout">
      <strong>If this lands, [focal] becomes</strong>
      <em>[New brand identity]</em>. [Risk]. Best for a strategy that [Z].
    </div>
    <div class="brief-grid">
      <div class="brief-col">
        <h5>Recommended archetype</h5>
        <ul><li>[archetype detail]</li><li>[Tier 1 spec]</li><li>[Tier 2 spec]</li></ul>
        <h5>First activation</h5>
        <ul><li>[specific first launch]</li><li>[companion creator series]</li></ul>
      </div>
      <div class="brief-col">
        <h5>Messaging angles in [focal] voice</h5>
        <ul><li>[line 1]</li><li>[line 2]</li><li>[line 3]</li></ul>
        <h5>Non-negotiables</h5>
        <ul><li>[FTC]</li><li>[compliance]</li><li>[exclusivity]</li></ul>
      </div>
      <div class="brief-col">
        <h5>BD-side pitch target</h5>
        <ul><li>[team / department]</li><li>[product team if embedded utility]</li><li>[best inroad — agency or creator]</li></ul>
        <h5>Why this wins</h5>
        <ul><li>[reason 1]</li><li>[reason 2]</li><li>Time-to-launch: [estimate]</li></ul>
      </div>
    </div>
  </div>

  <!-- CREATOR ACTIVATION MAP -->
  <h2>Fintok Creator Activation Map</h2>
  <div class="section-sub">[Creator count] creators in the knowledge set. Each maps cleanly to one Tier 1 partnership.</div>
  <div class="creator-map">
    <div class="creator-row">
      <h4>[Creator name]</h4>
      <div class="creator-handle">@[handle] · [N] posts in feed</div>
      <div class="activates">Best for <strong>[Tier 1 brand]</strong>. [Casting rationale + specific creative concept]. Activation: [first deliverable].</div>
      <div class="stats">Most recent post: [date] · [prior brand work signals]</div>
    </div>
    <!-- repeat per creator -->
  </div>

  <!-- VERIFY EXTERNALLY -->
  <h2>Verify Externally Checklist</h2>
  <div class="section-sub">Content intelligence is one layer. Verify these through external means.</div>
  <div class="checklist">
    <ul>
      <li><div class="box"></div><div><strong>Audience demographics confirmation</strong><span>Run candidates through a third-party panel (Comscore, Resonate). Lifestyle labels are directional, not verified demographics.</span></div></li>
      <li><div class="box"></div><div><strong>Existing partnership exclusivities</strong><span>Confirm none of the Tier 1 brands have an active or pipeline partnership in the focal's category.</span></div></li>
      <li><div class="box"></div><div><strong>Proprietary card / payment-rail conflicts</strong><span>For fintech focals: check Target RedCard, Walmart Pay, or other card relationships before pitching.</span></div></li>
      <li><div class="box"></div><div><strong>Partnership-team responsiveness</strong><span>Two-week SLA on first conversation is the working benchmark.</span></div></li>
      <li><div class="box"></div><div><strong>Compliance review for embedded utility</strong><span>Any embedded payment / cash-flow integration requires legal review on money-movement licensing per state.</span></div></li>
      <li><div class="box"></div><div><strong>Co-marketing budget alignment</strong><span>Different partners operate on different commercial models (media-fee, rev-share, etc.). Align before the pitch.</span></div></li>
      <li><div class="box"></div><div><strong>Re-run scoring once missing feeds populate</strong><span>If any brand or competitor feeds were empty at scoring time, backfill and re-score before final BD decision.</span></div></li>
    </ul>
  </div>

  <div class="disclosures">
    <h4>Methodology disclosures</h4>
    [Honest disclosures about what content intelligence can and cannot show, sample biases, missing feeds, confidence caveats.]
  </div>

  <footer>
    Prepared by Adology Brand Marketing Mode · Knowledge set: [name] ([id]) · Generated [date]
  </footer>

</div>
</body>
</html>
```

### Section-by-Section Guidance

**Hero** — `h1` is 44px font-weight 800. Accent-colored span on the middle phrase
("Co-Marketing Partner"). Kicker 12px uppercase, accent color, 0.14em letter-spacing.

**Executive Summary** — Four columns, always in this order: thesis, picks,
positioning choice, what to do this quarter. The positioning-choice column ends with
"Pick one — they're not additive" because the user must understand that Tier 1
partnerships are a positioning choice, not just a partnership choice.

**Partnership Brief** — 8 cells. Use `repeat(auto-fit, minmax(200px, 1fr))` so it
reflows.

**Competitor matrix** — Two-column. 4 thumbnails per competitor (2x2 grid), captions
overlay the bottom of each thumbnail with a black gradient. After the two cards, the
"lane focal can claim" callout in accent-soft tinting names the white space directly.
This is one of the most important sections — the strategic case lives here.

**Methodology** — Two columns. Left: 7 dimensions with chips. Right: tier
thresholds + confidence calibration.

**Ranked shortlist** — Table with confidence chip column. All 7 dimension scores
visible, overall score in accent color, bold.

**Scorecards** — Tier 1 includes 4 evidence thumbnails per scorecard (real images
referenced via `thumbs/<name>.jpg`). Tier 2 same structure without thumbnails. Tier
3 includes a `.redflag` callout.

**Adapted briefs** — Tier 1 only. The positioning callout (info-blue tinted) is
unique to brand-partnership work — every Tier 1 partnership reshapes the focal
brand's identity differently. Name the tradeoff explicitly.

**Creator activation map** — Optional, only if creator feeds in KS. Map each
creator to one Tier 1 brand with the casting rationale.

**Verify externally** — White card with empty checkbox + bold title + dim
explanation. Customize the items based on the focal brand's category.

**Disclosures** — Warn-tinted box with small text. Be specific about which feeds
didn't populate and what that means for which dimension.

---

## Thumbnail Download Script

Reference thumbnails are pulled from Adology's scraper URLs and embedded as local
files referenced with relative paths (e.g. `thumbs/doordash_doormat.jpg`). For
Tier 1 scorecards (4 thumbs each = 12) plus competitor matrix (8 thumbs), you'll
download about 20 thumbnails per report.

**Workflow:**
1. Build a manifest file with one entry per line in `name|url` format.
2. Run the download script in parallel with `&` and `wait`.
3. Save thumbs to `outputs/thumbs/` and reference in HTML as `thumbs/<name>.jpg`.

**Inline bash script** (save this to a temp location, or paste inline):

```bash
#!/bin/bash
# Download thumbnails for the partnership vetting report.
# Usage: bash download_thumbnails.sh <manifest_file> <output_dir>
# Manifest format: one line per asset, "name.jpg|url"
# Auto-detects image vs video by URL suffix.

set +e
MANIFEST="$1"
OUTPUT_DIR="$2"
TMP_DIR="${TMPDIR:-/tmp}/thumb_dl_$$"

if [ -z "$MANIFEST" ] || [ -z "$OUTPUT_DIR" ]; then
  echo "usage: $0 <manifest_file> <output_dir>" >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR" "$TMP_DIR"

dl_image() {
  local name="$1"
  local url="$2"
  if curl -s -L --max-time 15 -o "$OUTPUT_DIR/$name" "$url"; then
    echo "OK image: $name"
  else
    echo "FAIL image: $name"
  fi
}

dl_video_frame() {
  local name="$1"
  local url="$2"
  local tmpf="$TMP_DIR/$name.mp4"
  if curl -s -L --max-time 20 -o "$tmpf" "$url" && \
     ffmpeg -y -i "$tmpf" -vframes 1 -q:v 3 "$OUTPUT_DIR/$name" -loglevel error 2>&1; then
    echo "OK video: $name"
  else
    echo "FAIL video: $name"
  fi
  rm -f "$tmpf"
}

while IFS='|' read -r name url; do
  [ -z "$name" ] && continue
  case "$name" in \#*) continue ;; esac
  case "$url" in
    *.mp4|*.mov|*.webm) dl_video_frame "$name" "$url" & ;;
    *.jpg|*.jpeg|*.png|*.gif|*.webp) dl_image "$name" "$url" & ;;
    *) dl_video_frame "$name" "$url" & ;;
  esac
done < "$MANIFEST"

wait
rm -rf "$TMP_DIR"
echo "---"
ls -la "$OUTPUT_DIR"
```

**Example manifest line:**
```
doordash_doormat.jpg|https://scrapes.example.com/path/to/asset.mp4
walmart_swim.jpg|https://scrapes.example.com/path/to/asset.jpg
```

Get the thumbnail URLs from the `thumbnail` field returned by `analyze` calls.
Image URLs end in `.jpg` / `.png`; video URLs end in `.mp4`. The script handles
both.

---

## Edge Cases

**Just vet one brand** — Scale down. One scorecard, one adapted brief if Tier 1.
Skip the ranked shortlist and competitor matrix.

**No brief yet** — Walk through Phase 1 inputs as a conversation. Then proceed.

**Score-only request** — Stop after Phase 4. Skip adapted briefs.

**Find AND vet** — Full pipeline. Phase 2 discovery → quick gut check → Phase 3
first-pass → present rankings → user picks deep-dives → Phase 4–6.

**Go deeper on [brand]** — Trigger deep-dive flow.

**Missing competitor data** — If competitor feeds haven't been ingested, flag in
disclosures and Verify Externally checklist. The Precedent dimension is the weakest
without competitor data.

**Limited data on a candidate** — Fewer than 20 posts → mark scorecard with low
confidence and note sample size in disclosures.

**Empty feeds** — Some brand handles don't resolve cleanly. Use `discover_brands`
or pass exact known handles. Re-add and re-trigger fetch on those feeds only.

---

## Tool Roles

**Web Search** — Sourcing. Find candidate brands when the user doesn't provide a
list, verify competitor partnerships not yet in the KS.

**Adology** — Studying. After candidates are sourced: `batch_add_feeds`,
`trigger_fetch`, `analyze` (per brand, full fields), `search_items` (partnership-
specific), `get_table_data` (deep-dive), `get_item_detail` (deep-dive transcripts).

**Bash + curl + ffmpeg** — Thumbnails. Use the inline download script above.

**Cowork outputs** — Deliverable. Save HTML to outputs folder, thumbs to
`outputs/thumbs/` referenced via relative paths.

---

## What This Skill Does NOT Do

- Does not measure partnership performance or commercial fit. Engagement ≠ ROI.
- Does not generate finished creative assets. Produces strategic thinking.
- Does not replace BD outreach, legal review, or commercial negotiation.
- Does not source partnership pricing — that requires direct outreach.
- Does not claim certainty. Illuminates, suggests, and questions.
