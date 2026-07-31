---
name: influencer-vetting
description: >
  Vet, score, and select influencer/creator partners for brand campaigns using content
  intelligence. Covers the full pipeline: campaign brief intake, creator sourcing (web
  search + handle resolution), deep content analysis in an Adology project, evidence-based
  scoring, and personalized brief adaptation for top picks. Use this skill whenever the user
  wants to vet creators, evaluate influencers, find partnership candidates, score creator-brand
  fit, build a creator shortlist, adapt a brief for specific creators, or assess whether a
  creator is right for a campaign. Trigger on: "vet creators", "influencer vetting", "score
  these creators", "find influencers", "creator partnerships", "is this creator a good fit",
  "adapt brief for creator", "creator shortlist", "influencer scorecard", "partnership
  candidates", "vet these handles", "creator analysis", "influencer audit". Also trigger
  when someone pastes a list of social handles and wants them evaluated, or when they describe
  a campaign and want creator recommendations.
---

# Influencer Vetting & Selection

## What This Skill Does

Takes a campaign brief from the user, sources or evaluates creator candidates, scores them
on observable content signals, and produces ranked scorecards with adapted briefs for top
picks. The scoring is transparent — the user sees every weight and every piece of evidence
that drove each score.

The core insight: most influencer vetting is either pure vibes or pure metrics. This skill
does neither. It reads a creator's actual content — the way they tell stories, the hooks
they use, the emotional register they operate in, how they integrate products, what their
audience conversations look like — and assesses fit against the specific campaign, not
against generic benchmarks.

## What You Can and Cannot Assess

This is the foundation. Be honest about it throughout.

**What content intelligence shows you:**
- How a creator communicates — their hooks, narrative style, emotional tone, production
  approach, storytelling patterns
- What topics and themes they consistently cover
- How they integrate products and brands into content (naturally vs. forced)
- Creative range — do they have one trick or many?
- Posting consistency and content volume
- Engagement lift against the creator's own baseline as a proxy for audience quality
  (not audience identity)
- What their audience says back in comments — the texture of the community
- How their content compares to the broader landscape in their category

**What you cannot assess from content alone:**
- True audience demographics (age, gender, location, income)
- Fake follower percentages or bot activity
- Conversion rates from past partnerships
- Pricing and rate cards
- Professionalism, responsiveness, contract reliability
- Whether high engagement translates to purchase behavior

**What this means for output:**
Every scorecard includes a "Verify Externally" section that flags exactly what the user
needs to check through other means — audience quality tools (HypeAuditor, etc.), pricing
negotiations, reference checks with past brand partners. Don't pretend the analysis is
complete. It's the content intelligence layer — the deepest, hardest-to-get layer — but
it's one layer.

## Phase 1: Campaign Brief Intake

No analysis without context. Creator fit is entirely relative to the campaign. A creator
who's perfect for awareness is wrong for conversion. A creator who's great for Gen Z
lifestyle is wrong for B2B decision-makers.

**Before doing anything, get these from the user:**

**Required:**
- **Brand name** — Who is this for?
- **Campaign goal** — What does success look like? (Awareness, consideration, conversion,
  content library, community building)
- **Target audience** — Who are we trying to reach? Be specific — not just "millennials"
  but "health-conscious women 25-35 who are curious about functional beverages but skeptical
  of wellness hype"
- **Platform focus** — Where does this need to live? (TikTok, Instagram, YouTube, LinkedIn,
  multi-platform)

**Strongly recommended:**
- **Content format needs** — What kind of content? (Short-form video, long-form review,
  lifestyle integration, educational, UGC-style, polished production)
- **Brand voice/positioning** — How does the brand talk? What's the vibe? (Premium,
  approachable, scientific, playful, rebellious, etc.)
- **Existing brief or key messages** — If they have a creative brief, campaign messaging,
  or key talking points, get them. This is what Phase 5 adapts.
- **Budget tier** — Not exact numbers, but: nano (<10K followers), micro (10K-100K),
  macro (100K-1M), mega (1M+)? This shapes who to source.
- **Category/vertical** — What space is this in? (Beauty, fitness, tech, food, finance, etc.)

**Optional but valuable:**
- **Competitors to avoid** — Creators who've recently worked with these brands are flagged
- **Must-haves or dealbreakers** — Anything specific? (Must be based in US, must do
  long-form, can't have worked with Brand X in last 6 months)
- **Number of creators needed** — How many final picks?

**If the user just drops handles without a brief**, ask for the brief. You can't score
fit without knowing what they're fitting against. Be friendly about it: "Before I vet
these, I need to understand the campaign so I can score them against something real.
What's the goal, who's the audience, and what kind of content do you need?"

## Phase 2: Creator Sourcing

Two entry paths. The user either gives you a list to vet, or asks you to find candidates.

### Path A: User Provides a List

The user drops handles (e.g., "@creator1, @creator2, @creator3"). Proceed directly to
Phase 3 with their list.

### Path B: Discovery Mode

When the user wants you to find candidates, use **web search at scale** as the sourcing
engine. The goal is a longlist of **30-50 candidates** — cast a wide net, then let the
content analysis narrow it down.

**1. Web search at scale (run in parallel)**
Launch 4-6 parallel web search agents simultaneously, each targeting a different angle:
- "[category] influencers [platform] 2026"
- "best [niche] creators on [platform]"
- "[brand vertical] content creators to watch"
- "[category] TikTok/Instagram/YouTube creators brand partnerships"
- "corporate/office/workplace [platform] creators" (for B2B campaigns)
- Adjacent category searches (e.g., for fintech: corporate humor, accounting, entrepreneurship)
- Competitor brand partnership searches (who has worked with similar brands?)

Each parallel agent should return 10-15 candidates with handles. The model's training data
also contains substantial knowledge about prominent creators across categories — use it.
Think about who you know in the space. The goal is raw volume: 30-50 names with handles
before analysis begins.

**2. Resolve names to real handles**
A name without a verified handle is a dead end — the wrong handle silently tracks the
wrong account. `lookup_brands` resolves a name against Adology's central directory and
returns the platform handles it holds (Instagram / TikTok / YouTube / X / LinkedIn),
already normalized to the shape the tracking tools accept. It's free and read-only. For
creators the directory doesn't carry, confirm the handle from the web-search result
itself before tracking it.

**3. What the portfolio already tracks**
Read the current tracked universe with `read_portfolio_context` — influencers already on
the list are candidates you can analyze immediately, often without spending anything.

**Discovery output:** A longlist of 30-50 candidates with handles and platforms. Present
this to the user for a quick gut check before proceeding — they might immediately cut
some based on context you don't have. But don't block on approval; the first-pass analysis
(Phase 3) is designed to handle large lists efficiently.

## Phase 3: Content Intelligence Analysis

This is where the real value lives. For each candidate creator, you're reading their
content the way a strategist reads a brand — not counting metrics, but understanding
how they communicate and whether that communication fits the campaign.

### Set Up the Working Scope

Orient first: `whoami` → `list_portfolios` → `list_projects({ portfolioId })`. Reuse a
project that already covers this campaign's space, or `create_project` for a fresh one
("Creator Vetting: [Campaign]"). `get_project` shows exactly what a project currently
covers — read it before you analyze, so you know whether the creators you care about are
in scope.

Track the candidates on the portfolio with `author_portfolio_context`, one item per
creator with `kind: "influencer"` and a handles object keyed by platform:

```
upsertItems: [
  { id: "fitcoachjess", kind: "influencer", name: "Fit Coach Jess",
    handles: { tiktok: "fitcoachjess", instagram: "fitcoachjess" } }
]
```

Then bring their content in with `pull_data({ projectId, candidates: [{ kind: "influencer",
handleOrTerm: "fitcoachjess", platform: "tiktok" }, …], dateRangeDays: 90, limit: 50 })`.

**`pull_data` costs nothing — it plans.** It splits your candidates into `readyNow`
(the pool's coverage is already current; those sources are attached to the project for
free, right now) and a gap that has to be fetched, and it quotes that gap as
`estimatedCostCredits` with a `previewId`. Show the user both halves and the credit
number, in plain language: "22 of your 40 creators are already covered and ready to
analyze. The other 18 cost N credits to fetch. Want me to pull them?"

**Only `confirm_pull({ previewId, projectId })` spends.** Call it only after the user
says yes to that number. It returns a `runId` and streams in over the next minute or
two — you don't wait for it. Analyze the ready sources meanwhile and use
`check_pull({ runId })` when you want to report progress.

If the user declines the fetch, say plainly which candidates you can score and which
you can't, and score only the covered ones.

### Two-Pass Analysis Model

**The default is a first-pass vet across ALL candidates.** Don't deep-dive on a few
creators and ignore the rest. Vet everyone at a consistent depth first, then let the
user decide who deserves a deeper look.

#### First Pass (default — all candidates, ~10 posts each)

`analyze` is the primary tool. Run it against the project with
`feedTypes: ["influencer"]` so brand accounts don't crowd the sample:

1. **A balanced read across every creator** — `distribution: "balanced"` gives equal
   per-feed representation, which is exactly what a fair first pass needs. Set `limit`
   to the page size you want (max 80); read `itemsReturned`, `hasMore`, and `nextOffset`
   and loop with `offset: nextOffset` until you've covered everyone.
2. **Their best work** — `distribution: "top"` (tune with `sortMetric`) shows what each
   creator does when it lands, including how they handle brand integrations.
3. **Sponsored content specifically** — `search_all({ projectId, query: "sponsored
   partnership ad" })` or `analyze({ mode: "semantic", query: "sponsored brand
   partnership disclosure" })` surfaces how they've handled past deals.
4. **Their outliers** — `outlierFilter: { metric: "likes", multipleGreaterThan: 3 }`
   keeps only the posts that beat the creator's own baseline. This is the fastest read
   on what actually works for them.

Narrow to one creator at any point with `feedNames: ["Fit Coach Jess"]`.

**Tell the user this is a first pass.** Say something like: "I'm doing a first-pass vet
across all [N] creators — analyzing ~10 posts each to score everyone at a consistent
depth. Once you see the rankings, let me know if you want me to go deeper on any
specific creators."

**Request the FULL field set for every post, even on the first pass.** Ten posts is a
small sample — you need maximum signal from each one. Every item already carries the base
set (id, brand, feedType, platform, headline, likes, views, shares, comments, isOutlier,
outlierType, likesMultiple, createdAt, url, thumbnail); ask for the rest:

```
fields: [
  "hookMechanism", "hookCategory",
  "creativeConcept", "creativeExecution", "creativeRationale",
  "narrativeStyle", "narrativeFormat", "productionStyle",
  "emotionalStrategy", "emotionalTones", "emotionalMood",
  "mainMessage", "visualDescription", "visualConcept",
  "productBenefits", "productDescription", "productDisplayStyle",
  "brandPositioning", "competitiveContext", "strategyFunction",
  "uniqueSellingProposition", "problemStatement", "demandStyle",
  "oneLineInsight", "noteworthy",
  "targetAudienceAge", "targetAudienceGender", "targetAudienceLifestyle",
  "ctaText", "ctaFraming", "offerType", "offerDelivery",
  "transcript", "adDescription", "mediaType",
  "viewsMultiple", "commentsMultiple", "sharesMultiple",
  "sourceMedianLikes", "sourceMedianViews", "sourceItemCount"
]
```

The `transcript` and `adDescription` are the most important fields — they capture the
FULL content of every post. The transcript is the verbatim spoken words. The adDescription
is a comprehensive AI-written description of the entire post — visuals, scene progression,
camera work, text overlays, pacing, and narrative arc. Together they give you everything
you'd get from watching the post yourself.

The semantic fields (`hookMechanism`, `emotionalStrategy`, `narrativeStyle`, etc.) are the
interpretation layer built on top. The `hookMechanism` tells you how they capture attention.
The `emotionalStrategy` tells you what register they operate in. The `narrativeStyle` tells
you whether they're storytellers, educators, entertainers, or commentators. The
`productDisplayStyle` tells you how they integrate brands. Read these like a portfolio
review, not a data table.

The `sourceMedian*` fields are the denominators behind the `*Multiple` lift numbers.
Never cite a "4x" without the baseline it's 4x of.

**10 posts with full fields is enough to:** identify their dominant content style, read
their actual voice and vocabulary, spot brand integration patterns, assess engagement
consistency, and evaluate voice/aesthetic fit. It's NOT enough to catch rare content types
or build high-confidence engagement statistics — that's what the deep-dive is for.

#### Deep Dive (on request — specific creators, 30-50+ posts)

When the user says "go deeper on [creator]" or "I want more detail on [creator]":

1. Page the creator's full set: `analyze({ feedNames: ["Creator Name"], distribution:
   "exhaustive", sortBy: "likesMultiple" })` — the deterministic ranked page over
   everything that matches, with `totalEstimated` and `nextOffset` so you can walk it all.
2. Quantify their label patterns with `get_table_data` — `rows` set to the dimensions
   that matter (Hook, Creative, Production, Narrative, Emotion, CTA), `columns:
   "focalVsRest"` with `focalBrand` set to the creator, which shows where their choices
   diverge from everyone else in the project. Discover the available dimensions with
   `get_table_data({ projectId, listDimensions: true })` or `list_labels`.
3. Deep-dive individual posts with `analyze({ itemIds: [...] })` — full creative, labels,
   and performance for specific items.
4. Ask what structurally drives their performance with `get_creative_dna({ projectId,
   feedTypes: ["influencer"], feedNames: ["Creator Name"] })` — it returns which label
   combinations carry real lift once the marginal averages are controlled, plus emerging
   and fading patterns when you pass a date range.
5. Produce a richer scorecard with more evidence citations and higher confidence scores.

Don't dump label distributions into the scorecard. Labels are the scaffolding, not the
insight.

### Audience Voice (Optional, Costs Credits)

Comment texture is the strongest available read on whether an audience is real and
engaged. To get it for tracked TikTok/Instagram creators, run `fetch_comments`.

It is a two-step, consent-gated spend. Call it FIRST without `confirmedByUser` — it
returns a real quote (`estimatedCredits`, `quoteToken`, the sources it would cover) and
charges nothing. Relay that exact number; never guess one. Only after the user approves,
call again with `confirmedByUser: true`, the `quoteToken` echoed verbatim, `maxCredits`
set to exactly the amount they approved, and the identical `sources`/`maxComments`.

By default it targets every commentable source in the project's scope and charges for
all of them. To fetch comments for just two creators, narrow with `sources`, or pin the
project first with `update_project_scope({ projectId, replace: [...] })`.

The run is async. A couple of minutes later, read the landed comments with
`analyze({ projectId, feedTypes: ["discussion"], includeComments: true, platformFilter:
["tiktok"] })` — one call per platform. Without `includeComments: true` the default read
fences social comments out and returns nothing.

If the user doesn't want to spend on comments, say so in the scorecard and lean on
engagement consistency instead.

### What You're Reading For

For each creator, you're building a picture across five dimensions. These aren't
checkboxes — they're interpretive reads that require judgment.

#### Dimension 1: Content-Brand Fit (Weight: 35%)

The central question: *Does this creator's content world feel like a natural home for
this brand?*

Read their content semantically. Look at:
- **Voice alignment** — Does the way they talk (casual, authoritative, vulnerable, funny,
  educational) match how the brand talks or wants to be talked about?
- **Aesthetic alignment** — Does their visual world (production style, color palette, vibe)
  feel compatible with the brand's identity?
- **Value alignment** — Do the themes they consistently return to (wellness, hustle culture,
  sustainability, luxury, authenticity) resonate with what the brand stands for?
- **Audience-brand overlap** — Based on the content they make and the conversations in their
  comments, does their audience seem like people who would actually care about this product?
- **Natural integration potential** — Could you imagine this creator mentioning this product
  without it feeling forced? Or would it be a jarring departure from their usual content?

Evidence: cite specific posts, transcripts, or creative concepts that show the fit (or
the gap). "Their emotional register is aspirational-but-accessible — they show the polished
result but also the messy process. That maps well to [Brand]'s positioning of premium
products for real people, not influencer fantasyland."

#### Dimension 2: Creative Capability (Weight: 30%)

The question: *Can this creator actually execute the kind of content this campaign needs?*

- **Hook quality** — Do they know how to capture attention? What mechanisms do they use?
  (Pattern interrupt, curiosity gap, bold claim, question, cold open) Are the hooks varied
  or do they lean on one trick?
- **Storytelling range** — Can they do narrative arcs, or just flat product demos? Do they
  build tension, create emotional beats, land a payoff?
- **Format versatility** — Do they work across formats (short-form, long-form, carousel,
  Stories, live) or are they one-dimensional? Does the campaign need versatility?
- **Production consistency** — Not production *value* (lo-fi can be great), but consistency.
  Is there a recognizable quality level post to post, or is it wildly uneven?
- **Product integration skill** — Look at how they've handled past brand integrations.
  Is the product woven into the content naturally, or does the ad read feel like a jarring
  interruption? This is one of the most important signals for partnership success.

Evidence: cite specific posts that demonstrate capability (or concerns). "Three of their
last 10 posts use curiosity-gap hooks with strong payoff narratives — that's the format
this campaign needs. But their carousel content is noticeably weaker, so if the campaign
requires static posts, that's a risk."

#### Dimension 3: Audience Signal Quality (Weight: 20%)

The question: *Does this creator's audience seem real, engaged, and relevant?*

You can't see audience demographics from content data alone. But you can read proxies:

- **Comment quality** — Are comments specific and personal ("I tried this after your last
  video and it actually worked for my skin type"), or generic ("Love this!" "Fire 🔥")?
  Specific comments indicate real humans who actually watch and care.
- **Engagement consistency** — Steady lift across posts (`likesMultiple`, `viewsMultiple`
  clustering near 1x with occasional spikes) suggests a real audience. Wild swings may
  indicate algorithmic dependence or engagement manipulation.
- **Community feel** — Does the creator respond to comments? Do commenters talk to each
  other? A real community is a powerful distribution asset.
- **Posting consistency** — Regular posting cadence suggests a creator who takes this
  seriously and has built audience habits. Erratic posting suggests risk.
- **Growth trajectory** — If you can see it, is this creator growing, stable, or declining?
  A growing creator is building momentum; a declining one is a risk.

Be explicit about what you can't verify: "Engagement patterns look healthy — consistent
across posts with specific comments — but I can't verify audience authenticity or
demographics. Recommend running through HypeAuditor or similar before proceeding."

#### Dimension 4: Strategic Value (Weight: 15%)

The question: *Beyond basic fit, does this creator offer something strategically
interesting for the campaign?*

- **Competitive proximity** — Have they worked with or mentioned competitors? This cuts
  both ways: competitor association might mean their audience is pre-qualified, but recent
  exclusive work with a competitor is a dealbreaker.
- **Whitespace opportunity** — Is this creator in a space the brand hasn't been? Would
  partnering open up a new audience or category entry point?
- **Content repurposability** — Does this creator make content the brand could license and
  repurpose in paid media, on their own channels, or in retail? Some creators make
  inherently reusable content; others make content that only works in their context.
- **Growth trajectory** — A creator on the rise offers more long-term value than one
  who's peaked. Early partnerships with rising creators often yield the best ROI.

### Red Flags (Immediate Concerns)

During analysis, flag these explicitly. Any of these can downgrade a score or trigger a
"Proceed with caution" note:

- **Recent competitor integration** — Worked with a direct competitor in the last 90 days
- **Content inconsistency** — Dramatic shift in content style, topic, or quality recently
  (might indicate account management change or desperation)
- **Brand safety concerns** — Controversial topics, polarizing takes, anything that could
  create risk
- **Engagement anomalies** — Patterns that suggest purchased engagement or pod activity
- **Over-saturation** — So many brand deals that the audience has ad fatigue. If every
  other post is sponsored, the next sponsorship has diminished impact.
- **Audience mismatch signals** — Comments in unexpected languages, engagement from
  accounts that don't match the expected audience profile

## Phase 4: Scoring & Output

### The Scorecard

For each creator, produce a scorecard with transparent scoring.

**Overall Score** = (Content-Brand Fit × 0.35) + (Creative Capability × 0.30) +
(Audience Signal Quality × 0.20) + (Strategic Value × 0.15)

Each dimension is scored 0-100 with:
- The score itself
- A 1-2 sentence justification
- 1-3 specific post references as evidence

**Show the user the weights.** The default weights above reflect the research on what
predicts partnership success, but different campaigns may want different emphasis. Call
this out: "These are the default weights — Content-Brand Fit is heaviest because research
shows audience-brand alignment is the strongest predictor of partnership ROI. If this
campaign is more about creative capability (e.g., you need content for your own channels),
you might want to increase that weight. Want to adjust?"

### Tier Assignments

- **Tier 1 (80+):** Strong recommend. Proceed to brief adaptation.
- **Tier 2 (65-79):** Good candidate with caveats. Worth pursuing if caveats are addressed.
- **Tier 3 (50-64):** Conditional. Specific concerns that may or may not be dealbreakers.
- **Below 50:** Pass for this campaign. May be a fit for different objectives.

### Verify Externally Checklist

Every scorecard includes this section. It lists what the user needs to check through
other tools and processes before making a final decision:

- [ ] **Audience authenticity** — Run through HypeAuditor, Modash, or similar. Look for
  >70% real follower rate.
- [ ] **Audience demographics** — Confirm age, gender, location, income alignment with
  campaign target. Most platforms and third-party tools provide this.
- [ ] **Pricing** — Request rate card. Compare to category benchmarks for their tier.
- [ ] **Past partnership performance** — Ask for case studies or references from previous
  brand partners. What were the deliverables, timelines, and results?
- [ ] **Exclusivity and conflicts** — Confirm no active or pending partnerships with
  direct competitors.
- [ ] **Legal/compliance** — Verify FTC disclosure history. Check for past compliance issues.
- [ ] **Responsiveness** — Initial outreach response time is a signal of professionalism.
  If they don't reply within 5 business days, consider it a yellow flag.

## Phase 5: Brief Adaptation

For Tier 1 and Tier 2 creators, generate adapted briefs. This is where the content
intelligence pays off — you've studied how each creator communicates, so you can translate
the brand's message into their language.

### How Brief Adaptation Works

1. **Extract the creator's content DNA.** From the content analysis, identify:
   - Their dominant hooks (how they open)
   - Their narrative style (how they tell stories)
   - Their emotional register (how they make people feel)
   - Their product integration approach (how they handle brand mentions)
   - Their format strengths (what content types they do best)

2. **Map the brand's key messages to the creator's voice.** Take each key message from
   the campaign brief and rewrite it in a way that sounds like this creator, not like
   the brand's marketing team. Include:
   - A suggested hook approach based on what works for them
   - A suggested narrative arc based on their storytelling patterns
   - Tone guidance that matches their emotional register
   - Example: "Instead of 'Our product uses clinically-tested ingredients for maximum
     absorption,' this creator would say something like 'ok so I've been geeking out on
     the ingredient list because I'm that person — and the bioavailability thing is
     actually real, here's why that matters for your morning...'"

3. **Tier the brief based on creator size.** Research shows that over-briefing kills
   authenticity, especially for smaller creators:

   **Macro creators (100K+):** Detailed brief. Clear deliverables, specific key messages,
   visual guidelines, approval process, revision rounds. They expect structure and their
   audience expects polish.

   **Micro creators (10K-100K):** Balanced brief. Key messages and non-negotiables, but
   generous flexibility zones. "Here's what we need you to communicate. Here's how we
   think it might fit your style. But you know your audience better than we do — adapt
   as you see fit."

   **Nano creators (<10K):** Light brief. Product info, 2-3 talking points, FTC requirements,
   and trust. "Use the product. Share your honest take. Tag us. That's it."

### Adapted Brief Template

For each top creator, produce:

**Creator Profile Summary**
- Their content DNA in 3-4 sentences (hooks, style, emotional register, format strengths)
- Why they're a fit for this campaign specifically
- Reference posts: 2-3 of their posts that demonstrate the fit (with URLs/thumbnails)

**Adapted Key Messages**
- Each brand message rewritten in the creator's voice
- Suggested hook approach
- Suggested narrative arc
- Non-negotiables clearly separated from suggestions

**Recommended Deliverables**
- Format and platform recommendation based on their strengths
- Posting window recommendation (if relevant)
- Tracking elements (UTM parameters, promo codes, etc.)

**Non-Negotiables**
- FTC disclosure requirements (#ad in first line / first 5 seconds)
- Core messages that must be communicated (even if reworded)
- Brand safety guardrails
- Usage rights expectations

**Flexibility Zones**
- Exact wording — adapt to their voice
- Visual treatment — their aesthetic, not the brand's
- Story angle — their narrative approach
- Timing — when it feels natural in their content calendar
- Format details — length, transitions, music (their choices)

## Output Format

The final deliverable is an HTML report (rendered in browser or converted to PDF).

**Structure:**
1. **Campaign Brief Summary** — Recap of the brief for alignment
2. **Scoring Methodology** — Weights, dimensions, what was assessed vs. what needs
   external verification. Transparent.
3. **Ranked Creator Scorecards** — One per creator, ordered by overall score. Each includes:
   - Overall score and tier
   - Per-dimension scores with justifications and evidence
   - Red flags (if any)
   - Content thumbnails from their posts (real images, not placeholders)
4. **Adapted Briefs** — One per Tier 1/2 creator. Includes their content profile,
   adapted messages, and recommended deliverables.
5. **Verify Externally Checklist** — The full list of what needs checking through
   other means.

**Design:** Clean, editorial, scannable. Think Notion document, not PowerPoint deck.
Use the `content-intelligence:thumbnails` skill to embed post thumbnails so the file is
self-contained. Same aesthetic approach as the weekly brief — warm, professional, readable.

Offer to save the shortlist's reference posts with `save_to_collection({ projectId,
collectionName: "Creator Shortlist — [Campaign]", itemIds })` so the evidence stays
attached to the portfolio after the report ships.

## Handling Edge Cases

**"Just vet one creator"** — Scale the output down. One scorecard, one adapted brief
if they're a fit. No need for the full ranked report.

**"I don't have a brief yet"** — Help them build one. Walk through the required inputs
from Phase 1 as a conversation. Then proceed.

**"Score them but I don't need briefs"** — Stop after Phase 4. Skip brief adaptation.

**"I already have a brief, just adapt it for these creators"** — Skip Phases 2-4. Go
directly to Phase 5 brief adaptation. Still need to analyze their content to adapt
effectively.

**"Can you find creators AND vet them?"** — Full pipeline. Phase 2 discovery (30-50
candidates via web search) → quick gut check with user → Phase 3 first-pass (10 posts
each for all candidates) → present rankings → user picks who to deep-dive → Phase 3
deep-dive on selected creators → Phase 4-5 on the final set.

**"Go deeper on [creator]"** — After the first-pass rankings, the user can request a
deep-dive on specific creators. Page their full set, pull label distributions, run
`get_creative_dna`. Re-score with higher confidence.

**Limited data (first pass)** — The first pass uses ~10 posts per creator. This is
intentional — it's enough for a directional score but not enough for high confidence.
Note this explicitly on every first-pass scorecard: "First-pass score based on ~10 posts.
Confidence: directional. Request a deep-dive for higher-confidence assessment."

**Limited data (few posts available)** — If a creator has fewer than 5 posts in the
project, flag it: "Only [N] posts available. Score confidence: low. This creator may
be inactive, new, or have a very low posting cadence." Check `get_project` — the creator
may be tracked with coverage that ended a while ago, in which case a `pull_data` refresh
(quoted, user-approved) brings in newer activity.

**A creator the project doesn't track** — every read answers about the project's
scope. If a name comes back unresolved, that creator isn't tracked yet: add
them with `author_portfolio_context`, then `pull_data`. Never present an empty result
as "this creator has no good content."

## Tool Roles (Use the Right Tool for the Right Job)

**Web search — sourcing.** Finds candidate names and handles. Run 4-6 parallel search
agents for 30-50 candidates.

**`lookup_brands` — handle resolution.** Free, read-only. Turns a name into the real
platform handles before you track anything.

**Adology project tools — studying.** After candidates are sourced:
1. `whoami` / `list_portfolios` / `list_projects` / `get_project` — orient and see scope
2. `author_portfolio_context` — track the creators as `kind: "influencer"`
3. `pull_data` → (user approves the quote) → `confirm_pull` → `check_pull` — acquire content
4. `analyze` — the workhorse: balanced/top/recent sampling, `exhaustive` for ranked pages,
   `mode: "semantic"` for meaning-based recall, `itemIds` for per-post deep dives
5. `search_all` — keyword search across the project's scope
6. `get_table_data` / `list_labels` — quantify label patterns, `focalVsRest` per creator
7. `get_creative_dna` — what structurally drives a creator's performance
8. `aggregate` — volume, cadence, and platform mix over time
9. `fetch_comments` — audience voice, quoted and user-approved before it charges
10. `save_to_collection` — keep the evidence set

**`content-intelligence:thumbnails` — visuals.** Embeds post thumbnails in the report.

**WeasyPrint — output.** HTML-to-PDF conversion if PDF output is requested.
