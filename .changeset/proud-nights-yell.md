---
"content-intelligence": patch
---

Addresses code-review feedback on the v0.2.0 skills (brand-partnership-vetting, tone-of-voice, weekly-brief).

### Fixed

- **`tone-of-voice`** — Replaced references to the non-existent `anthropic-skills:adology-thumbnails` skill with the actual `content-intelligence:thumbnails` skill in `SKILL.md`, `references/thumbnail_handling.md`, and `references/output_formats.md`. Deliverables that need thumbnails now point to a real skill instead of failing silently.
- **`brand-partnership-vetting`** — Swapped the inline `curl` + `ffmpeg` bash script for an invocation of `content-intelligence:thumbnails`, matching the convention used by `audience-deep-dive` / `influencer-vetting` / `creative-toolkit`. Removes the implicit `ffmpeg` dependency and the sandbox-CDN-fetch risk.
- **`weekly-brief`** — Documented why the skill ships its own `download_thumbnails.py` and added an explicit fallback to `content-intelligence:thumbnails` when the bundled script can't resolve more than half of the URLs (likely sandbox HTTP block). Added a "Path Conventions" subsection explaining the `{skill_path}` and `{output_dir}` placeholders.
- **`weekly-brief/scripts/qa_check.py`** — Promoted missing-thumbnail count from `WARN` to `FAIL` so a PDF missing required images no longer passes QA. Tightened the engagement-metric regex so plain integers (font sizes, years, structural digits) no longer match. Anchored page-key extraction to `^P[1-3]_` so `Pickle1.html` / `Project1.html` don't inherit `P1`'s budgets.
- **`weekly-brief/scripts/assemble_pdf.py`** — Replaced deprecated `PdfMerger` with `PdfWriter` for pypdf ≥ 5.0 compatibility. Removed the unused outer module variables left over from the dual-import pattern.
- **`weekly-brief/scripts/download_thumbnails.py`** — Hoisted `requests` and `PIL.Image` to module scope after `ensure_packages()` instead of re-importing on every call.
- **`weekly-brief/references/P{1,2,3}_output_schema.yaml` + `P{1,2,3}_prompt.txt`** — Anonymized structural `ks_id` / `ks_name` / `primary_brand` fields with `EXAMPLE_*` placeholders so leakage is syntactically obvious. Strengthened the "DO NOT COPY VERBATIM" banner. Prose examples retain real brand names for pedagogical value.

### Added

- **`brand-partnership-vetting/assets/report_template.html`** — Extracted the 428-line inline HTML/CSS skeleton from `SKILL.md` into a standalone template asset. `SKILL.md` now points to it and keeps the inline version collapsed in a `<details>` block for offline access.
