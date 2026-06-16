# Review Action Plan — add-3-new-skills-2026-05-27

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. If that skill is unavailable, work through each task sequentially.

**Branch:** add-3-new-skills-2026-05-27
**Date:** 2026-05-27
**Sources:** PR comments (none — PR #2 has no reviewer feedback yet) + automated code review (Agent B)

**Repo note:** This is a Claude Code plugin repo (markdown skills + small Python helpers). There is no `npm run check` / JS test suite. Validate Python changes with `python3 -m py_compile <file>` and validate markdown/skill changes by re-reading the affected file.

---

## Critical (Must Fix)

### Task 1: Replace broken skill ID `anthropic-skills:adology-thumbnails` with `content-intelligence:thumbnails`

**Source:** Code review
**Severity:** Critical
**Files:**
- skills/tone-of-voice/SKILL.md:162
- skills/tone-of-voice/references/thumbnail_handling.md:3,5,17
- skills/tone-of-voice/references/output_formats.md:81,142

**Issue:** The `tone-of-voice` skill instructs the agent to invoke `anthropic-skills:adology-thumbnails`. No such skill exists in the marketplace or this plugin. The project convention (used by `audience-deep-dive/SKILL.md:196`) is `content-intelligence:thumbnails`. Without this fix, every `tone-of-voice` deliverable that needs visuals will fall back to naive `<img>` fetches that the sandbox silently breaks — shipping broken images.

**Steps:**

1. Run `grep -rn 'anthropic-skills:adology-thumbnails' skills/` to enumerate every occurrence.
2. Edit each occurrence and replace `anthropic-skills:adology-thumbnails` with `content-intelligence:thumbnails`. The expected files are `skills/tone-of-voice/SKILL.md`, `skills/tone-of-voice/references/thumbnail_handling.md`, and `skills/tone-of-voice/references/output_formats.md`.
3. Re-run `grep -rn 'anthropic-skills:adology-thumbnails' skills/` and confirm it returns nothing.
4. Re-read the affected files and confirm the surrounding sentences still parse correctly with the new skill ID.

---

## Major (Should Fix)

### Task 2: Clarify `brand-partnership-vetting`'s deviation from the thumbnail convention

**Source:** Code review
**Severity:** Major
**Files:** skills/brand-partnership-vetting/SKILL.md:695-775

**Issue:** This skill inlines its own bash script using `curl` + `ffmpeg` for thumbnail downloads instead of delegating to `content-intelligence:thumbnails`. Other skills (`influencer-vetting`, `audience-deep-dive`, `creative-toolkit`) all defer to the `thumbnails` skill. `ffmpeg` is not guaranteed in sandboxes, so video thumbnails will silently fail. Either the inline approach should be justified, or the skill should follow project convention.

**Steps:**

1. Open `skills/brand-partnership-vetting/SKILL.md` and locate the thumbnail-handling section around line 695.
2. Decide: (a) swap the inline curl+ffmpeg approach for an invocation of `content-intelligence:thumbnails`, OR (b) keep the inline script but add a paragraph that (i) explains why the inline approach is preferred here, (ii) calls out that `ffmpeg` may not be available, and (iii) instructs the agent to fall back to `content-intelligence:thumbnails` if the inline script fails for >50% of URLs or `ffmpeg` is missing.
3. Apply the chosen change.
4. Re-read the section in context to confirm the agent will know which path to take at runtime.

### Task 3: Document or replace `weekly-brief`'s custom thumbnail script

**Source:** Code review
**Severity:** Major
**Files:** skills/weekly-brief/SKILL.md:137-177, skills/weekly-brief/scripts/download_thumbnails.py

**Issue:** `weekly-brief` ships its own `scripts/download_thumbnails.py` (Python `requests` + Pillow) without acknowledging that the project convention is `content-intelligence:thumbnails`. If the sandbox blocks outbound HTTP the same way it blocks `curl`, this script will silently produce `null` values and ship a PDF with broken thumbnails — violating the skill's own "Thumbnails are MANDATORY" preamble (`SKILL.md:33`).

**Steps:**

1. Open `skills/weekly-brief/SKILL.md` and find the section that invokes `download_thumbnails.py`.
2. Add an explicit fallback path: if `download_thumbnails.py` resolves <50% of URLs to data URIs, the agent must invoke `content-intelligence:thumbnails` for the remaining URLs.
3. Add a one-sentence rationale explaining why this skill ships its own script (e.g., needs base64 inline data for `@page` CSS PDF rendering) and how it differs from `content-intelligence:thumbnails`.
4. Re-read the surrounding skill text and confirm the fallback rule is unambiguous.

### Task 4: Promote image-count mismatch from WARN to FAIL in `qa_check.py`

**Source:** Code review
**Severity:** Major
**Files:** skills/weekly-brief/scripts/qa_check.py:122-134, skills/weekly-brief/scripts/qa_check.py:289-294

**Issue:** `EXPECTED_IMAGES = {"P1": 7, "P2": 0, "P3": 8}` but `check_images` only sets `status = "WARN"` when fewer images are found than expected. The overall file status (lines 289-294) only flips to FAIL on placeholders / page-CSS / file-size issues. So a PDF missing thumbnails passes QA today, violating the skill's "Thumbnails are MANDATORY" contract.

**Steps:**

1. Open `skills/weekly-brief/scripts/qa_check.py`.
2. In `check_images` (around line 122), change the branch where `found_count < expected_count and expected_count > 0` to set `status = "FAIL"` instead of `"WARN"`.
3. Confirm (or add) the image-count failure to the `critical_issues` list around line 290 so the overall result reflects it.
4. Run `python3 -m py_compile skills/weekly-brief/scripts/qa_check.py` to confirm the file still parses.

### Task 5: Tighten the engagement-metric regex in `qa_check.py`

**Source:** Code review
**Severity:** Major
**Files:** skills/weekly-brief/scripts/qa_check.py:39

**Issue:** `ENGAGEMENT_PATTERN = r'\b\d+[KM]\b|\b\d{1,3}(?:,\d{3})*\b'` matches every bare 1–3 digit integer, including `2024`, font sizes like `11pt`, and `<th>1</th>`. The "engagement metrics" check will essentially never WARN because CSS/structure tokens always satisfy it.

**Steps:**

1. Open `skills/weekly-brief/scripts/qa_check.py` at line 39.
2. Change `ENGAGEMENT_PATTERN` to `r'\b\d+(?:\.\d+)?[KM]\b|\b\d{1,3}(?:,\d{3})+\b'` — requires either a K/M suffix or at least one comma group, so plain integers no longer match.
3. Run `python3 -m py_compile skills/weekly-brief/scripts/qa_check.py`.
4. (Optional sanity check) Run `python3 -c "import re; p=r'\b\d+(?:\.\d+)?[KM]\b|\b\d{1,3}(?:,\d{3})+\b'; print(re.findall(p, 'font: 11pt; views 12K; likes 1,234; year 2024'))"` and confirm it returns `['12K', '1,234']` and not `2024` or `11`.

### Task 6: Centralize and anchor page-key detection in `qa_check.py`

**Source:** Code review
**Severity:** Major
**Files:** skills/weekly-brief/scripts/qa_check.py:96-101, skills/weekly-brief/scripts/qa_check.py:220-230

**Issue:** Both `check_images` and `check_file_size` detect page-key with substring checks like `"P1" in filename`. A file named `Pickle1.html` or `Project1.html` would incorrectly receive P1's budget. Logic also differs slightly between the two call sites.

**Steps:**

1. Open `skills/weekly-brief/scripts/qa_check.py`.
2. Add a top-level helper, e.g.:
   ```python
   import re
   PAGE_KEY_RE = re.compile(r'^(P[123])_', re.IGNORECASE)
   def page_key_from(filename):
       m = PAGE_KEY_RE.search(filename)
       return m.group(1).upper() if m else None
   ```
3. Replace both `"P1" in filename` / `"P2" in filename` / `"P3" in filename` style checks in `check_images` and `check_file_size` with `key = page_key_from(filename)` and branch on `key`.
4. Run `python3 -m py_compile skills/weekly-brief/scripts/qa_check.py`.

### Task 7: Replace deprecated `PdfMerger` with `PdfWriter` in `assemble_pdf.py`

**Source:** Code review
**Severity:** Major
**Files:** skills/weekly-brief/scripts/assemble_pdf.py:134

**Issue:** `PdfMerger` is deprecated in pypdf ≥ 5.0; the recommended API is `PdfWriter().append(...)`. A future pypdf major may remove it.

**Steps:**

1. Open `skills/weekly-brief/scripts/assemble_pdf.py` near line 134.
2. Replace the `PdfMerger` import and usage with `PdfWriter`. Pattern:
   ```python
   from pypdf import PdfWriter
   writer = PdfWriter()
   for path in input_paths:
       writer.append(path)
   with open(output_path, 'wb') as f:
       writer.write(f)
   ```
3. Run `python3 -m py_compile skills/weekly-brief/scripts/assemble_pdf.py`.

---

## Minor (Nice to Have)

### Task 8: Tidy up the duplicate-import/unused-var pattern in `assemble_pdf.py`

**Source:** Code review
**Severity:** Minor
**Files:** skills/weekly-brief/scripts/assemble_pdf.py:64-86, skills/weekly-brief/scripts/assemble_pdf.py:116-149

**Issue:** Each function calls `import_with_fallback` separately and then re-imports the package inside a try block (e.g., `from weasyprint import HTML`). The outer module variable is unused after the None check. Cosmetic only.

**Steps:**

1. Open `skills/weekly-brief/scripts/assemble_pdf.py`.
2. Either use the returned module from `import_with_fallback` directly, or drop the outer variable and rely on the inner `from X import Y`.
3. Run `python3 -m py_compile skills/weekly-brief/scripts/assemble_pdf.py`.

### Task 9: Document the `{skill_path}` placeholder convention in `weekly-brief`

**Source:** Code review
**Severity:** Minor
**Files:** skills/weekly-brief/SKILL.md:148-152 (and similar `{skill_path}` references throughout)

**Issue:** `python3 {skill_path}/scripts/download_thumbnails.py` leaves `{skill_path}` as a literal placeholder. There's no section telling the agent what `{skill_path}` resolves to.

**Steps:**

1. Open `skills/weekly-brief/SKILL.md`.
2. Add a short subsection near the start (or in the "Conventions" / "How to read this" area) stating: `{skill_path}` = absolute path to this skill directory (i.e., the directory containing this SKILL.md). Substitute it before running any shell command.
3. Re-read the script-invocation examples in context to confirm the convention is now explicit.

### Task 10: Qualify references to `marketing:draft-content` / `marketing:content-creation` in `tone-of-voice`

**Source:** Code review
**Severity:** Minor
**Files:** skills/tone-of-voice/SKILL.md:32

**Issue:** The skill suggests redirecting to `marketing:draft-content` or `marketing:content-creation`, but neither skill exists in this plugin or the visible marketplace. An agent following the instruction may fabricate a tool call.

**Steps:**

1. Open `skills/tone-of-voice/SKILL.md` at line 32.
2. Qualify the redirect with "if a content-drafting skill is available" (or remove the named skill IDs and describe the capability in plain language).
3. Re-read the paragraph to confirm it no longer commits to specific skill IDs that don't exist.

### Task 11: Anonymize example brand names in `weekly-brief` schemas

**Source:** Code review
**Severity:** Minor
**Files:** skills/weekly-brief/references/P1_output_schema.yaml, skills/weekly-brief/references/P2_output_schema.yaml, skills/weekly-brief/references/P3_output_schema.yaml (and any prompt files that mirror them)

**Issue:** Schemas embed real brand names ("Glossier", "Rhode", "Beauty Brands"). The skill warns "Never copy example values from the schema into the output" (`SKILL.md:312`), but real brand names sometimes leak into outputs. Placeholders make leakage syntactically obvious.

**Steps:**

1. `grep -rn -E 'Glossier|Rhode|Beauty Brands' skills/weekly-brief/` to locate every example brand name.
2. Replace each occurrence with a generic placeholder (`EXAMPLE_BRAND_1`, `EXAMPLE_BRAND_2`, `EXAMPLE_KS_NAME`, etc.).
3. Re-run the grep and confirm no real brand names remain in example/schema files.

### Task 12: Consider extracting `brand-partnership-vetting`'s HTML skeleton to `assets/`

**Source:** Code review
**Severity:** Minor
**Files:** skills/brand-partnership-vetting/SKILL.md

**Issue:** The skill is a single 827-line file with all CSS inlined. Within precedent (matches `influencer-vetting`), but the largest skill on disk and may pressure context budgets when loaded.

**Steps:**

1. Open `skills/brand-partnership-vetting/SKILL.md` and locate the inline HTML/CSS skeleton.
2. Create `skills/brand-partnership-vetting/assets/report_template.html` containing the skeleton.
3. Replace the inline block in `SKILL.md` with a short reference: "Use the template at `assets/report_template.html` as the base structure."
4. Re-read both files to confirm the skill still tells the agent how to fill in placeholder slots in the template.

### Task 13: Refactor lazy-import pattern in `download_thumbnails.py` (cosmetic)

**Source:** Code review
**Severity:** Minor
**Files:** skills/weekly-brief/scripts/download_thumbnails.py

**Issue:** `requests`/`Pillow` are imported lazily inside `download_and_resize`. The `ensure_packages()` check at the top of `main()` does the right thing, but the dual import + lazy install pattern is unusual and hurts readability.

**Steps:**

1. Open `skills/weekly-brief/scripts/download_thumbnails.py`.
2. After `ensure_packages()` succeeds in `main()`, import `requests` and `PIL` at module scope (or pass the imported modules through to `download_and_resize`).
3. Remove the duplicate inner imports.
4. Run `python3 -m py_compile skills/weekly-brief/scripts/download_thumbnails.py`.

### Task 14: Optionally bundle `brand-partnership-vetting`'s inline bash as a script file

**Source:** Code review
**Severity:** Minor
**Files:** skills/brand-partnership-vetting/SKILL.md:707

**Issue:** The skill instructs "Inline bash script (save this to a temp location, or paste inline)". `weekly-brief` ships equivalents as real files under `scripts/`, which is cleaner.

**Steps:**

1. Decide whether Task 2 already supersedes this (if Task 2 swaps to `content-intelligence:thumbnails`, this task is moot).
2. If keeping the inline approach, move the bash to `skills/brand-partnership-vetting/scripts/download_thumbnails.sh` and have `SKILL.md` invoke it as `bash {skill_path}/scripts/download_thumbnails.sh <args>`.
3. `chmod +x` the new file.
4. Re-read `SKILL.md` to confirm the invocation is consistent with `weekly-brief`'s pattern.

---

## Summary

- **Critical:** 1 item
- **Major:** 6 items
- **Minor:** 7 items
- **Total:** 14 items
