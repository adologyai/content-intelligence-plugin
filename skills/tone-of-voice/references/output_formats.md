# Output formats — detailed templates

Each format renders the same content spine differently. Pick based on the user's stated use case. Default recommendation: **HTML one-pager + Word doc together**.

The content spine (regardless of format):

1. Personality in one sentence
2. Archetype rationale (primary + secondaries, with brand mission tie-in; note which angle was chosen from the step-2 options if relevant)
3. Tone spectrum plot
4. Voice principles (4–6, each with a this/not-that)
5. This, not that — applied to existing brand copy (4–6 reworked examples, drawn from real brand-authored content with source links)
6. **Voice across touchpoints** — Marketing vs. Service voice required; plus 1–2 additional touchpoints relevant to the brand (website, email, sales, package, organic social, etc.) with same-message-rendered-both-ways examples
7. Vocabulary lists (use / don't use)
8. Do/don't checklist

The audit appendix (in .docx and .pptx) must include:
- A note on **methodology**: total sample, brand-authored vs. excluded UGC / creator / no-copy content, dominant campaigns, campaign-bias check result
- Top-6 archetype table with counts, verbatim examples, and **thumbnails + source URLs** so the user can audit the classification
- A note on touchpoint coverage: what Adology saw, what was inferred from the website, what was inferred without direct evidence (and where validation is needed)

---

## Format 1 — HTML one-pager

**Use for:** Daily reference for the team. The thing writers bookmark. Easy to share via link or screenshot. Workshop walls.

**Layout (vertical, scrollable, designed to read like a strategist's poster):**

```
[Header band — full width]
  Brand name • "Voice Guide" • Date
  
[Section 1 — Personality]
  The one-sentence personality, set big (40–60pt). 
  Subtle background tint. This is the headline.
  
[Section 2 — Archetype rationale]
  Primary archetype name + icon/emoji
  Secondary archetype(s) name + icon/emoji
  3–4 sentences of rationale below, tying to mission and audience.
  
[Section 3 — Spectrum plot]
  8 horizontal bars, each showing position on a dimension.
  Each bar: label, anchor words at each end, marker showing position,
  one-line verbal cue underneath.
  
[Section 4 — Voice principles]
  4–6 principle cards, each with:
    - Principle (1 line, bold)
    - Why (1 line, light grey)
    - This / not that (two columns)
  
[Section 5 — Reworked examples]
  4–6 before/after pairs, each as a two-column block.
  Left column (light red tint): "Before — the old voice"
  Right column (light green tint): "After — in our voice"
  Brief annotation underneath each pair: what changed and why.
  
[Section 6 — Marketing voice vs. Service voice]
  Two-column comparison.
  Same scenario rendered both ways at the top.
  Below: a short rule for each context.
  
[Section 7 — Vocabulary]
  Two-column lists side by side.
  "Words we use" — green tick or dot
  "Words we don't" — grey, strikethrough optional
  
[Section 8 — Quick checklist]
  5–7 items, large checkboxes, easy to scan.
  Designed to be the last thing a writer checks before sending.
```

**Design principles:**
- Restrained palette — two accent colours plus neutrals. Let the writing be the visual.
- Typography matters. A sans-serif headline and a readable body face. Don't use the brand's actual fonts unless the user supplies them — use sensible defaults (Inter, Söhne, Söhne Buch, or system stack).
- Generous whitespace. A voice guide that looks crammed reads as not-thought-through.
- One screen scroll should reveal one major section — pacing matters.
- Self-contained HTML file (CSS embedded, no external dependencies) so the user can email it or save it locally.

**If Adology thumbnails are referenced** (in the "before" examples): embed as base64 inline to keep the file portable. See `thumbnail_handling.md`.

---

## Format 2 — Word document (.docx)

**Use for:** The brand book of record. Anything that needs to live in the company's central documentation, get printed, or be appendix'd to a brand bible.

**Use the `anthropic-skills:docx` skill to build it.**

**Section structure (use as H1/H2 headings):**

1. **Executive summary** — half a page. The personality sentence, the primary + secondary archetypes, the three biggest changes from current voice.

2. **The personality**
   - 2.1 One-sentence personality
   - 2.2 Primary archetype: what it means, why we chose it, mission tie-in
   - 2.3 Secondary archetype(s): same treatment
   - 2.4 What we considered and rejected (1 paragraph — useful when the user revisits this in 18 months)

3. **The competitive landscape**
   - 3.1 Where competitors sit archetypally (1 paragraph each, with example copy)
   - 3.2 Where we are distinctive
   - 3.3 Where we overlap and how we'll sharpen

4. **The tone spectrum**
   - One sub-section per dimension. Position, rationale, verbal cue, one this/not-that.
   - Include a single combined visualisation at the top of section 4.

5. **Voice principles**
   - 4–6 sub-sections, one per principle. Principle as the heading, then: what it means, why it matters, this/not-that examples (at least two per principle).

6. **Voice in practice — reworked copy**
   - One sub-section per reworked example. Show the original (with the Adology source link as a footnote), the revised version, and a short annotation of what changed.

7. **Marketing voice vs. Service voice**
   - 7.1 Where marketing voice has more latitude
   - 7.2 Where service voice dials back, and why
   - 7.3 The same message rendered both ways — at least two scenarios (e.g., a delay notification, an onboarding welcome)

8. **Vocabulary**
   - 8.1 Words we use (with brief gloss on each — *why* this word fits)
   - 8.2 Words we don't (with brief gloss — *why* it doesn't fit)

9. **The do/don't checklist**
   - The same 5–7 item checklist as the HTML one-pager. Easy to lift onto a slide or print.

10. **How to use this guide**
    - Who owns the voice (named role)
    - When to revisit (suggest annual review + after any major brand change)
    - What to do when in doubt — "ask: would the archetype say it this way?"

11. **Appendix**
    - 11.1 Audit summary — top-6 archetypes from current content with counts and examples
    - 11.2 Competitor archetype reads
    - 11.3 Methodology note — Adology sample size, date range, limitations

**Cover page:** Brand name + "Voice Guide" + version number + date. Keep it simple.

**Page setup:** Standard letter or A4 (ask user). Body 11pt, headings step up from there. Footer with page numbers.

**Thumbnails:** include Adology source thumbnails in the audit appendix at least. Use the `content-intelligence:thumbnails` skill — bash can't fetch them directly.

---

## Format 3 — Slide deck (.pptx)

**Use for:** Stakeholder walkthroughs, brand training sessions, agency handoffs.

**Use the `anthropic-skills:pptx` skill to build it.**

**Slide sequence:**

1. **Title.** Brand • Voice Guide • Date.

2. **What this is, and what it isn't.** 4 bullets. (E.g., "This is a guide for how we sound. It's not a positioning doc, it's not a content strategy, it's a writing reference.")

3. **The personality — one sentence.** Set big. Single slide.

4. **The archetype.** Primary + secondaries. Visual representation (icon or symbol per archetype). One-paragraph rationale on the slide, fuller rationale in the notes.

5. **Why this fits us.** Mission tie-in. Pull 1–2 sentences from the brand's website/About page if useful.

6. **What we considered and rejected.** Useful for pre-empting "why not X?" pushback.

7. **The competitive landscape.** Visual — quadrant or matrix showing where competitors sit and where we sit. Brief commentary.

8–9. **Distinctiveness watch-outs and how we'll handle them.** One slide for the most significant overlap with a competitor, one for how the secondaries differentiate us.

10. **The tone spectrum — the plot.** Visual: 8 horizontal bars showing position on each dimension. One slide.

11–13. **Three of the most important dimensions, in depth.** One slide each. Position, rationale, this/not-that. Choose the dimensions where the user-team relationship will most need this depth.

14. **The voice principles.** One slide listing all 4–6 principles in short form.

15–17. **Three principle deep-dives.** One slide each with this/not-that examples. (Cover the principles the team is most likely to get wrong.)

18–19. **Voice in practice — reworked copy.** 2 slides, each with one before/after example. Visual layout: left = before, right = after, annotation underneath.

20. **Marketing voice vs. Service voice.** Two-column slide with rules and one shared scenario rendered both ways.

21. **Vocabulary at a glance.** Two-column slide: words we use / words we don't.

22. **The do/don't checklist.** Final reference slide.

23. **How to use this guide.** Ownership, revisit cadence, the "would the archetype say it?" rule.

24. **Appendix divider.**

25–28. **Audit details.** Top-6 archetypes from current content, with thumbnails of representative Adology items.

29. **Methodology note.**

**Visual approach:**
- Restrained palette consistent with the brand if known; sensible defaults otherwise.
- Use thumbnails generously in the audit and competitive sections — visual evidence beats claims.
- Type hierarchy: one large headline per slide, body text capped at ~40 words per slide.

**Speaker notes:** Use them. The slides should be presentable but the notes should be where the rationale lives — a stakeholder reading the deck later (without you in the room) needs the why, not just the what.

---

## Common rendering rules — all formats

- **Use the brand's actual copy, not made-up examples.** This is the single most important thing. A guide that uses generic examples ("Brand X says…") is unconvincing; a guide that reworks the brand's own current copy is undeniable.
- **Cite Adology sources** for every "before" example used in the reworked copy section. A short footnote or link is enough.
- **Show the archetype, don't just name it.** Every claim about how the brand should sound needs a concrete verbal example.
- **Length discipline.** A great voice guide fits on 3–6 pages of document, one HTML scroll, or 20–25 slides. Longer than that and it won't be read.
- **Test before delivery.** Read the guide aloud. If a principle is hard to apply ("be authentic"), rewrite it as a behaviour ("use 'I' when speaking on behalf of the founder").

---

## Quick decision tree for format

- User wants one thing for the team to refer to daily → HTML one-pager
- User wants something for the brand book / agency handoff → Word doc
- User wants to present the work to leadership → Slide deck
- User wants both daily use and a doc of record → HTML + Word doc (default)
- User wants to use the guide to train writers in a session → Slide deck + HTML

When in doubt, ask the user. Don't pick for them.
