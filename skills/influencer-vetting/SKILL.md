---
name: influencer-vetting
description: >
  Vet, score, and select influencer/creator partners for brand campaigns using content
  intelligence analysis. Covers the full pipeline: campaign brief intake, creator sourcing
  (web search + Adology content intelligence), deep content analysis, evidence-based scoring,
  and personalized brief adaptation for top picks. Use this skill whenever the user wants to
  vet creators, evaluate influencers, find partnership candidates, score creator-brand fit,
  build a creator shortlist, adapt a brief for specific creators, or assess whether a creator
  is right for a campaign. Trigger on: "vet creators", "influencer vetting", "score these
  creators", "find influencers", "creator partnerships", "is this creator a good fit",
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
- Engagement patterns as a proxy for audience quality (not audience identity)
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

When the user wants you to find candidates, use **web search at scale** as the primary
sourcing engine. The goal is a longlist of **30-50 candidates** — cast a wide net, then
let Adology's content intelligence narrow it down.

**IMPORTANT: Do NOT use Adology for sourcing.** Adology is for *studying* creators after
you've found them. Web search finds the candidates. Adology reads their content.

**1. Web search at scale (primary sourcing tool — run in parallel)**
Launch 4-6 parallel web search agents simultaneously, each targeting a different angle:
- "[category] influencers [platform] 2025 2026"
- "best [niche] creators on [platform]"
- "[brand vertical] content creators to watch"
- "[category] TikTok/Instagram/YouTube creators brand partnerships"
- "corporate/office/workplace [platform] creators" (for B2B campaigns)
- Adjacent category searches (e.g., for fintech: corporate humor, accounting, entrepreneurship)
- Competitor brand partnership searches (who has worked with similar brands?)

Each parallel agent should return 10-15 candidates with handles. Claude's training data
also contains substantial knowledge about prominent creators across categories — use it.
Think about who you know in the space. The goal is raw volume: 30-50 names with handles
before any Adology analysis begins.

**2. User's existing knowledge set (supplement only)**
If the user has an Adology knowledge set with influencer feeds already configured, pull
those names from the feed list — but this supplements web search, it doesn't replace it.

**Discovery output:** A longlist of 30-50 candidates with handles and platforms. Present
this to the user for a quick gut check before proceeding — they might immediately cut
some based on context you don't have. But don't block on approval; the first-pass analysis
(Phase 3) is designed to handle large lists efficiently with only 10 posts per creator.

## Phase 3: Content Intelligence Analysis

This is where the real value lives. For each candidate creator, you're reading their
content the way a strategist reads a brand — not counting metrics, but understanding
how they communicate and whether that communication fits the campaign.

### Two-Pass Analysis Model

**The default is a first-pass vet across ALL candidates.** Don't deep-dive on a few
creators and ignore the rest. Vet everyone at a consistent depth first, then let the
user decide who deserves a deeper look.

#### First Pass (default — all candidates, ~10 posts each)

1. **Add all 30-50 candidates as influencer feeds** in an Adology knowledge set.
   Use `batch_add_feeds` to add them all at once.

2. **Trigger a fetch** to collect their content.

3. **Analyze with a balanced distribution** pulling ~10 posts per creator. Use `analyze`
   with `distribution: "balanced"` and set `limit` to roughly (number_of_creators × 10).

4. **Also pull top-performing content** with `distribution: "top"` to see each creator's
   best work and any brand integrations.

5. **Also search specifically for sponsored content** using `search_items` with queries
   like "#ad sponsored brand partnership" to assess brand integration patterns.

**Tell the user this is a first pass.** Say something like: "I'm doing a first-pass vet
across all [N] creators — analyzing ~10 posts each to score everyone at a consistent
depth. Once you see the rankings, let me know if you want me to go deeper on any
specific creators (I can pull 30-50+ posts for a more thorough read)."

**CRITICAL: Request the FULL field set for every post, even on the first pass.** 10 posts
is a small sample — you need maximum signal from each one. Don't cut corners on fields
to save tokens. Every post gets the complete analysis:

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
  "transcript", "adDescription",
  "mediaType", "thumbnail", "url"
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

**10 posts with full fields is enough to:** identify their dominant content style, read
their actual voice and vocabulary, spot brand integration patterns, assess engagement
consistency, and evaluate voice/aesthetic fit. It's NOT enough to catch rare content types
or build high-confidence engagement statistics — that's what the deep-dive is for.

#### Deep Dive (on request — specific creators, 30-50+ posts)

When the user says "go deeper on [creator]" or "I want more detail on [creator]":

1. Pull 30-50 posts using `analyze` with `feedNames: ["Creator Name"]` and higher `limit`.
2. Pull label distributions via `get_table_data` for that creator specifically.
3. Use `get_item_detail` for their top 3-5 posts to get full transcripts and descriptions.
4. Search for all their sponsored content specifically.
5. Produce a richer scorecard with more evidence citations and higher confidence scores.

Don't dump label distributions into the scorecard. Labels are the scaffolding, not the
insight.

**If Adology is not available or the creator isn't tracked:**
Use web search to find and assess their content. You can evaluate content quality, brand
voice, and creative approach from what you observe directly — it's less structured but
still valuable.

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
- **Engagement consistency** — Steady engagement across posts suggests a real audience.
  Wild swings (some posts get 50 comments, others get 2) may indicate algorithmic
  dependence or engagement manipulation.
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
Thumbnails should be embedded (base64) so the file is self-contained. Use the same
aesthetic approach as the weekly brief — warm, professional, readable.

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
deep-dive on specific creators. Pull 30-50+ posts, full label distributions, and detailed
transcripts. Re-score with higher confidence.

**Limited data (first pass)** — The first pass uses ~10 posts per creator. This is
intentional — it's enough for a directional score but not enough for high confidence.
Note this explicitly on every first-pass scorecard: "First-pass score based on ~10 posts.
Confidence: directional. Request a deep-dive for higher-confidence assessment."

**Limited data (fetch returned few posts)** — If a creator has fewer than 5 posts in
the fetch, flag it: "Only [N] posts available. Score confidence: low. This creator may
be inactive, new, or have a very low posting cadence."

## Tool Roles (Important — Use the Right Tool for the Right Job)

### Web Search — SOURCING (finding candidates)
Web search is the **only** tool for sourcing creators. Run 4-6 parallel search agents
to find 30-50 candidates. Adology does NOT source creators.

### Adology — STUDYING (analyzing candidates' content)
Adology is the tool for studying creators AFTER web search has found them. The workflow:
1. `batch_add_feeds` — Add all sourced creators as influencer feeds in a knowledge set
2. `trigger_fetch` — Collect their content
3. `analyze` — First-pass analysis (~10 posts per creator, balanced distribution)
4. `analyze` (distribution: "top") — See each creator's best-performing content
5. `search_items` — Find sponsored/brand integration content specifically
6. `get_item_detail` — Deep dive on specific posts (deep-dive phase only)
7. `get_table_data` — Label distributions for specific creators (deep-dive phase only)

### WeasyPrint — OUTPUT
HTML-to-PDF conversion if PDF output is requested.
