# Output formats — detailed templates

Each format renders the same content spine differently. Pick based on audience and use case. Default recommendation: **Canvas + Brief together**.

## Format 1 — Empathy Canvas (HTML one-pager)

**Use for:** Workshop walls, creative kickoffs, briefing sessions. The thing people tape up.

**Template:** `assets/empathy_canvas_template.html` — editable HTML. Open in a browser, or convert to PDF for printing.

**Layout (v3.1 — no numbered boxes).** Two bands stacked:

### Band 1 — The foundation (who + need)
A two-column strip at the top that defines the person before anything else:
- **Who we're empathising with** — the sharp audience definition from step 1 (role, life stage, situation, role in the decision).
- **What they need to do** — the three jobs-to-be-done (functional / emotional / social) + what success looks like, from step 2.

These two are the foundation. Everything in the empathy map below should be read *through* them.

### Band 2 — The empathy map (inputs → synthesis)
Underneath, a classical empathy map arranged so the centre reads visibly as the synthesis of the four inputs around it:
- **What they see** (top-left) — split explicitly into two sub-sections inside the same panel:
  - *From our brand* — how our specific brand shows up in their world (advertising, social, events, retail, website, open days).
  - *From the wider category* — the category context our brand lives inside (competitor codes, conventions, dominant tropes, category news).
  The brand always lives *inside* the category. Showing them side-by-side forces the strategist to see our brand in its true context, and surfaces the gaps between our behaviour and category norms.
  For category-level briefs with no single focal brand: replace "From our brand" with "From specific operators" and list the shortlist (2–4 named operators) there, then use the category sub-section for category-wide patterns.
- **What they hear** (top-right) — friends, family, peers, authorities, the grapevine (step 5).
- **What they say** (bottom-left) — verbatim language, pulled with quotation marks (step 6).
- **What they do** (bottom-right) — observable behaviour, journey, moments of truth (step 7 + step 9).
- **What they think & feel** (centre, tinted, larger) — the System 1 decoder, pains, gains, cultural tension (step 4 + step 8). This is the strategist's read on what the four inputs *add up to*. Treat it as the synthesis — not another co-equal box.

The template draws a hairline cross behind the centre panel to reinforce the visual logic: inputs flow in, synthesis lands in the middle.

**Header band:** Audience one-liner, Goal (= business goal for this audience), For / Date / Strategist meta.

**Footer band:** The three **Killer Insights** (step 11) as prose-form highlighted blocks, each with an Implication line. Below that, a numbered **Sources** block — every superscript in the canvas resolves to a numbered entry here.

## Format 2 — Insight Brief (2-page markdown)

**Use for:** Exec consumption, inbox distribution, appendix to a bigger doc.

**Template:** `assets/insight_brief_template.md`

**Structure:**
- Audience in one sentence
- The three killer insights (bolded, boxed)
- Jobs-to-be-Done (three bullets)
- Cultural tension (one paragraph)
- Counter-narrative / reframe (one paragraph)
- So-what for marketing (four lines: positioning / messaging / channel / creative)
- Gaps & validation (three bullets)

**Length discipline:** two pages maximum. If it's longer, it's a report, not a brief.

## Format 3 — Deep Dive Deck (.pptx)

**Use for:** Stakeholder walkthroughs, internal briefings, agency handoffs.

**Slide sequence:**
1. Title + audience definition
2. Why this audience (business context, strategic importance)
3. Three killer insights (1 slide, highlighted)
4. Jobs-to-be-Done (functional / emotional / social)
5. Brand experience vs. Category experience (two-column slide)
6. Category codes & cultural tension (include visual examples / thumbnails)
7. What they hear
8. What they say (with verbatim quotes pulled from Adology / reddit / reviews)
9. What they do (journey snapshot + moments of truth)
10. Thoughts & feelings (System 1 decoder — one slide per killer insight explaining the heuristic)
11. Counter-narrative / reframe
12. So-what for marketing (4-quadrant: positioning / messaging / channel / creative)
13. Gaps & validation plan
14. Appendix — supporting data, additional insights, sources

**Visual:** use thumbnails heavily — Adology ad creatives, social posts, reddit threads. See `thumbnail_handling.md`. Use `anthropic-skills:pptx` skill for building.

## Format 4 — Full Written Report (.docx)

**Use for:** Strategy doc of record, agency deliverable, reference for multiple teams over time.

**Structure (use as h1/h2 headings):**

1. **Executive summary** — audience definition, three killer insights, key recommendations. One page.
2. **Audience definition & context** — who, situation, business importance.
3. **Jobs-to-be-Done** — all three, with worked rationale.
4. **Brand and category experience** — side-by-side analysis with visuals.
5. **Category codes & cultural tension** — what the category does visually/verbally, and the unspoken tension.
6. **What they hear / say / do** — with quotes, citations, and thumbnails.
7. **Thoughts & feelings — the System 1 decoder** — heuristics named, pains and gains detailed, confidence-tagged.
8. **Moments of truth** — the 3–5 intervention points.
9. **Counter-narrative / reframe** — conventional wisdom vs. our view.
10. **Implications for marketing** — positioning, messaging, channel, creative.
11. **Gaps in knowledge & validation plan** — named gaps with the cheapest route to fill each.
12. **Appendix** — full source list, additional insights, methodology note.

Use `anthropic-skills:docx` skill for building. Include thumbnails per `thumbnail_handling.md`.

## Common rendering rules — all formats

- **Highlight the 3 killer insights** visually — callout box, colored background, or dedicated slide/section.
- **Cite [Observed] claims** — Adology item ID, reddit URL, article link, interview quote.
- **Tag every claim** with [Observed] / [Inferred] / [Hypothesis].
- **Use verbatim language** from the audience where you've captured it — quote them.
- **Never pad.** If a section has nothing strategically meaningful, say so or cut it.
