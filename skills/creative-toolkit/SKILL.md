---
name: creative-toolkit
description: >
  Builds a living creative toolkit for a campaign or brand — a curated library of hooks, angles,
  copy lines, scripts, and content concepts sourced from competitor analysis, Reddit/audience
  conversations, and top-performing content. First extracts the brand's voice DNA so every item
  is written in the brand's actual voice. Outputs a CSV toolkit + companion HTML browser. Each
  item has data proof and an inspiration source tag. Trigger on: "creative toolkit", "build me
  a toolkit", "swipe file", "hook library", "creative library", "content toolkit", "campaign
  toolkit", "give me hooks", "give me angles", "content ideas for campaign", "build creative
  concepts", "hook bank", "copy bank", "script ideas", "creative brief assets", "campaign
  assets". Also trigger when someone describes a campaign brief and wants creative assets from
  data, or asks for hooks/angles/scripts/concepts for a specific product or campaign.
---

# Creative Toolkit Builder

You produce a creative toolkit — a working library a creative team opens and starts producing
from immediately. The toolkit has two files: a CSV (100-150+ rows) and a companion HTML browser.

## The Output: 9 Sections Across Two Files

Every toolkit contains exactly these 9 sections. This is the structure of both the CSV and
the HTML. Each section serves a different person on the creative team.

### Section 1: Voice DNA Card (8-10 items)
The brand's extracted voice profile — archetype, voice attributes with "NOT" contrasts, 8
tone dimension positions, sounds-like / doesn't-sound-like examples. This is the taste
reference the team holds everything against.

### Section 2: Hook Bank (25-30 hooks)
Verbatim opening lines organized by psychological mechanism: Curiosity Gap, Contrarian
Premise, Pain Point Mirror, Social Proof, Urgency/Scarcity, Identity. Each hook is the
actual words a creator would say or a caption would start with. "Your morning bar has 14g
of sugar. Ours has 2." — that's a hook. "Use a curiosity gap hook" — that's a description,
not a hook. Every item in this section is ready to use as-is.

### Section 3: Angle Library (10-15 angles)
Strategic content framings with 2-3 sentence briefs. Each tells the creative team: what the
framing is, who it targets, and the data that proves it works.

### Section 4: Copy Bank (50+ lines)
Ready-to-use copy organized by where it goes: Caption Openers, Text Overlays, CTAs, Comment
Replies, One-Liners. Volume matters — 50 minimum, ideally 60-80. Mix of short punchy, medium,
and longer narrative lines. Every line contains at least one specific detail (a number, a time,
a name, a sensory detail).

### Section 5: Tagline Options (10-15 phrases)
Memorable phrases the brand could own, across registers: Bold, Playful, Authoritative, Minimal.
Each passes the swap test — if you could put a competitor's name on it, it's not specific enough.

### Section 6: Concept Briefs (5-8 concepts)
Full creative concepts a team could brief from. Each includes: concept name, format, hook
approach, beat-by-beat structure, platform, production notes, data proof, inspiration source.

### Section 7: Script Starters (3-5 scripts)
Beat-by-beat scripts with timestamp, visual direction, dialogue, text overlay. Enough to
film from. Matches the brand's scripting voice.

### Section 8: Visual / Format Direction (5-8 items)
Production guidance: editing pace, shot types, text treatment, music/audio, color/mood,
thumbnail/first-frame direction.

### Section 9: Inspiration Sources (8-12 items)
The actual posts, threads, and data points that inspired the toolkit. Organized by source
type with platform, description, and data proof.

## The CSV File

Columns: section, id, type, item, inspiration_source, source_detail, data_proof,
pattern_name, platform, audience, notes, mechanism (hooks), register (taglines), usage (copy).

100-150+ rows. This is the working file a creative team imports into their planning tool.

## The HTML File

Read `references/toolkit-template.html` before writing any HTML. The template defines the
exact design system:

- **Fonts:** Space Grotesk (headings), DM Sans (body), JetBrains Mono (data/metrics)
- **Background:** Cream (#f0ead6)
- **Primary cards:** Forest green (#1b4332)
- **Accents:** Lime (#c8e64a)
- **Highlights:** Yellow (#d4d069)
- **Item backgrounds:** White (#ffffff)
- **Feel:** Warm editorial — generous whitespace, padded cards, clean typography

The HTML has a sticky nav bar with section navigation. Each section is a visual block with
card types appropriate to its content (hook cards, copy line cards, concept brief grids, etc.).

## Every Toolkit Item Answers Four Questions

1. **What is it?** — The hook, angle, copy line, concept, or script
2. **Why does it belong here?** — Data proof (engagement multiples, outlier flags)
3. **Where did it come from?** — Inspiration source tag:
   - **Whitespace** — Nobody in the category is doing this
   - **Trend** — This pattern is gaining momentum right now
   - **Your Top Performer** — Iteration on something already working for this brand
   - **Category Performer** — A competitor is proving this works
   - **Audience Gap** — Real people are asking for this and no brand addresses it
4. **Does it sound like us?** — Written in the brand's extracted voice DNA

## Reference Files

Read these before building:

- `references/copywriting-guide.md` — **Read first.** AI slop blacklist, specificity rules,
  rhythm techniques, copywriting frameworks, voice adaptation checklist. Every piece of copy
  passes through this guide.
- `references/creative-patterns.md` — 133 named creative patterns. Your vocabulary for naming
  what you find in the data.
- `references/voice-dna-extraction.md` — Full voice DNA schema: archetypes, tone dimensions,
  language rules, scripting voice clusters.
- `references/scripting-voice-extraction.md` — Scripting voice clusters by content format.
- `references/platform-cards-extraction.md` — Per-platform voice adaptation cards.
- `references/toolkit-template.html` — The HTML design template. Read before building HTML.

## Workflow

### Step 1: Understand the Brief

Before pulling any data, clarify: the brand, the campaign/goal, the audience, 2-4 competitors,
target platforms, and any existing top performers or brand guidelines.

### Step 2: Get the Data Ready

1. Check existing knowledge sets with `list_knowledge_sets`
2. If needed, create a KS and add feeds:
   - The focal brand (feedType: "brand" or "influencer")
   - 2-4 competitor brands/creators
   - 1-2 search feeds for niche keywords
   - 1-2 discussion feeds for relevant subreddits
3. Trigger fetch with `trigger_fetch`
4. Poll `get_workflow_status` every 3 minutes until it returns "completed"

The toolkit is only as good as the data behind it. If the fetch is still running, wait.
Tell the user "Still fetching — I'll continue once data is ready" and poll again in 3
minutes. Fetches typically take 5-15 minutes. Once `get_workflow_status` returns "completed"
for all workflows, proceed.

### Step 3: Extract the Brand's Voice DNA

Pull 15-25 of the focal brand's posts using `analyze` with `distribution: "balanced"`:
```
fields: ["transcript", "adDescription", "hookMechanism", "emotionalStrategy",
         "narrativeStyle", "ctaText", "mainMessage"]
```

From this content, extract:

**Brand Archetype** — Primary + secondary from the 12 Jungian archetypes.

**Voice Attributes** — 3-5 traits, each with a "NOT" contrast. "Confident — NOT arrogant."

**Tone Dimensions** — Score 8 spectrums (humor, formality, enthusiasm, respectfulness,
complexity, warmth, authority, risk-taking) from firmly-left to firmly-right. Include a
"sounds like" example from their actual content and a "doesn't sound like" example.

**Language Rules** — Preferred/avoided vocabulary, sentence structure, emoji usage,
contraction usage, person preference, punctuation personality.

**Scripting Voice** — How they open videos, hook style spoken aloud, pacing, closing style.

This becomes Section 1 of the toolkit and the voice filter for everything else.

### Step 4: Research — Five Streams

Run these five streams to gather raw material. Each produces toolkit items tagged by source.

**Stream 1: Category Top Performers → "Category Performer"**
Pull competitors' highest-performing content with `analyze` (distribution="top"). Read full
transcripts via `get_item_detail`. Extract hooks, angles, structures, CTAs. Rewrite each in
the focal brand's voice.

**Stream 2: Brand's Own Top Performers → "Your Top Performer"**
Pull the focal brand's best content. For each, generate iterations — new angles on the same
winning pattern, not just "do more of this."

**Stream 3: Audience Voice → "Audience Gap"**
Pull discussion/search feeds. Read Reddit threads. Find questions nobody answers, complaints,
language people use. Adapt audience language to the brand's voice.

**Stream 4: Whitespace → "Whitespace"**
Use `get_table_data` to map what the category does. Find what's missing: unused hook types,
absent formats, untried emotional strategies. Higher risk, higher upside.

**Stream 5: Trends → "Trend"**
Pull recent high performers and compare to historical patterns. Use `get_table_data` with
`columns="timePeriod"` to spot momentum.

### Step 5: Generate the 9 Sections

Using research from Step 4 and voice DNA from Step 3, generate all 9 sections. Every item
passes through the Voice DNA filter: does this use the brand's vocabulary? Does the tone
match? Would it sound natural from their archetype?

Write hooks as the actual words. Write copy lines as ready-to-post text. Write scripts with
beat-by-beat timestamps. Write concepts with production-ready briefs.

Apply `references/copywriting-guide.md` throughout — specificity over adjectives, rhythm
variation, one idea per line, the pub test, tension before resolution.

### Step 6: Copy Editor Pass — Three Sweeps

**Sweep 1: Kill List.** Cut anything that fails: the swap test (works for any brand?), the
specificity test (no concrete detail?), the nonsense test (sounds good but means nothing?),
the slop test (AI-overused words from the blacklist?), the reach test (claims beyond what
data showed?). Expect to cut 10-20%. That's healthy.

**Sweep 2: Tightening.** Remove dead-weight words. Fix rhythm. Sharpen vague benefits.
Compress ("in the morning when you wake up" → "every morning"). Fix voice consistency.

**Sweep 3: Voice Check.** Re-read against the Voice DNA card. Editing flattens voice toward
generic — this sweep puts the brand's fingerprints back on anything that drifted.

If any section drops below minimums after editing (hooks < 20, copy < 40, angles < 8,
taglines < 8), generate targeted replacements that pass all three sweeps.

### Step 7: Build and Deliver

1. Read `references/toolkit-template.html` for the design system
2. Write the CSV with all items across all 9 sections (100-150+ rows)
3. Write the HTML with all 9 sections, sticky nav, proper card layouts
4. Save both to the outputs directory
5. Present both files to the user
6. Offer to save inspiration source posts to an Adology collection

## Adapting to Brief Type

**Product launch:** Heavy on concepts and scripts. More whitespace. Audience gaps = launch angles.
**Always-on refresh:** Heavy on hooks and angles. More trends and category performers.
**Competitive response:** Heavy on category performer analysis. Rewrite what works for them
in your brand's voice. Include whitespace to differentiate.
**Brand refresh:** Heavy on whitespace and audience gaps. Push into new creative territory.

## The Content-First Principle

Read actual content before labeling it. Build the toolkit from real transcripts, real Reddit
threads, real ad descriptions. "UGC-style hooks perform 2.1x" is not a toolkit item. "A
creator in her car says 'okay I'm genuinely obsessed' while holding the product at eye level —
enthusiasm, no transitions. 23.6x average." — that's a toolkit item you can build a concept
from and rewrite in the brand's voice.
