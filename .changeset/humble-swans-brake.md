---
"content-intelligence": minor
---

Adds three new strategist-grade skills that turn raw Adology data into finished deliverables.

### Added

- **`brand-partnership-vetting`** — Vets, scores, and shortlists brand co-marketing partners. Produces an editorial HTML report with executive summary, competitor partnership matrix, ranked shortlist, scorecards with reference thumbnails, adapted partnership briefs with positioning callouts, and a creator activation map. Trigger on "vet partners", "co-marketing", "brand collab", "partnership shortlist".
- **`tone-of-voice`** — Builds a distinctive, actionable tone of voice grounded in Jungian archetypes, audited from Adology data, pressure-tested against competitors, plotted on a tone spectrum, and rendered as a "this, not that" guide with reworked real brand copy. Screens out UGC and creator content so the audit reads brand voice, not advocate voice. Trigger on "tone of voice", "ToV", "voice guidelines", "verbal identity", "brand personality", "we sound generic".
- **`weekly-brief`** — Generates a 3-page Adology Weekly Competitive Intelligence Brief (PDF) from a knowledge set. Page 1 (Visual Scoreboard + Intel Strip), Page 2 (Market Signals), and Page 3 (Social Trends + Coaching) are built independently with their own prompts and schemas, then QA'd and assembled into a single PDF with real thumbnails. Includes `assemble_pdf.py`, `download_thumbnails.py`, and `qa_check.py` helper scripts plus per-page render packages.
