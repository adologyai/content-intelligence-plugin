# Review Action Plan — initial-build

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. If that skill is unavailable, work through each task sequentially.

**Branch:** initial-build
**Date:** 2026-04-30
**Sources:** PR comments + automated code review

---

## Critical (Must Fix)

None.

---

## Major (Should Fix)

### Task 1: Replace nonexistent `--plugin-dir` flag with the real `/plugin` marketplace flow

**Source:** Code review
**Severity:** Major
**Files:** /Users/haldunanil/Development/adology/marketing-skills/docs/installation-claude-code.md:32, /Users/haldunanil/Development/adology/marketing-skills/docs/installation-claude-code.md:40, /Users/haldunanil/Development/adology/marketing-skills/README.md:52
**Issue:** The docs and README instruct users to run `claude --plugin-dir ./` and `claude --plugin-dir ~/.claude/plugins/...`, but Claude Code has no `--plugin-dir` CLI flag. Users copy-pasting these commands will hit "unknown option" and conclude the install path is broken.
**Steps:**

1. Open `/Users/haldunanil/Development/adology/marketing-skills/docs/installation-claude-code.md`.
2. Replace the Option 2 and Option 3 instructions (around lines 32 and 40) with the real flow:
   ```
   claude
   /plugin marketplace add /absolute/path/to/marketing-skills
   /plugin install content-intelligence@adology-marketplace
   ```
3. Open `/Users/haldunanil/Development/adology/marketing-skills/README.md`.
4. Update the quickstart at line 52 to use the same `/plugin marketplace add` + `/plugin install` flow instead of `--plugin-dir`.
5. Re-read both files end-to-end to confirm no other reference to `--plugin-dir` remains.

---

### Task 2: Reconcile `/export` slash command with `/analyze` and `/compare` follow-up suggestions

**Source:** Code review
**Severity:** Major
**Files:** /Users/haldunanil/Development/adology/marketing-skills/commands/export.md, /Users/haldunanil/Development/adology/marketing-skills/commands/analyze.md:57, /Users/haldunanil/Development/adology/marketing-skills/commands/compare.md:65
**Issue:** `/export` has no `argument-hint`, takes no argument, and the body just tells the user to go to the web UI — yet `/analyze` and `/compare` advertise it as `/export csv`. The frontmatter description "Export knowledge set data" is also misleading because the command does not actually export anything.
**Steps:**

1. Open `/Users/haldunanil/Development/adology/marketing-skills/commands/export.md`.
2. Decide the resolution path:
   - Option A — keep the redirect-only behavior: rewrite the frontmatter `description` to "Get a link to export your knowledge set in the Adology web UI" and remove any expectation of an argument.
   - Option B — make `/export` do something useful (e.g. emit a CSV link or invoke an export tool) and add an `argument-hint` like `[csv|json]`.
3. Open `/Users/haldunanil/Development/adology/marketing-skills/commands/analyze.md`. At line 57, drop the "Try `/export csv`" suggestion (or update it to match whichever resolution was chosen in step 2).
4. Open `/Users/haldunanil/Development/adology/marketing-skills/commands/compare.md`. At line 65, apply the same fix as analyze.md.
5. Re-read all three files to confirm the cross-references are internally consistent.

---

### Task 3: Clarify the MCP URL vs token relationship in `installation-claude-code.md`

**Source:** Code review
**Severity:** Major
**Files:** /Users/haldunanil/Development/adology/marketing-skills/docs/installation-claude-code.md:54, /Users/haldunanil/Development/adology/marketing-skills/.mcp.json
**Issue:** The doc note at line 54 says the MCP URL is hardcoded in `.mcp.json`, but the surrounding text discusses `${ADOLOGY_API_TOKEN}`, which `.mcp.json` only uses for the bearer token — not the URL. The juxtaposition is confusing for first-time installers.
**Steps:**

1. Open `/Users/haldunanil/Development/adology/marketing-skills/docs/installation-claude-code.md`.
2. At line 54, rewrite the note so the relationship is explicit, e.g.: "The MCP server URL is fixed in `.mcp.json`; the bearer token is interpolated from `$ADOLOGY_API_TOKEN` at runtime."
3. Cross-check `.mcp.json` to ensure the wording matches the actual values (URL hardcoded, token via env var).

---

## Minor (Nice to Have)

### Task 4: Stop shipping `SUBMISSION_CHECKLIST.md` operational TODOs in the bundle

**Source:** Code review
**Severity:** Minor
**Files:** /Users/haldunanil/Development/adology/marketing-skills/SUBMISSION_CHECKLIST.md (lines 43-46, 51, 86-87), /Users/haldunanil/Development/adology/marketing-skills/scripts/export-plugin.sh
**Issue:** The shipped bundle currently includes unchecked external-commitment TODOs (Privacy Policy URL resolves, Terms of Service URL resolves, Reviewer Template workspace built). A directory reviewer opening the zip will see unchecked compliance boxes.
**Steps:**

1. Pick one of:
   - Option A — Add `--exclude='SUBMISSION_CHECKLIST.md'` to the `rsync` invocation in `scripts/export-plugin.sh` so the file is omitted from the bundle.
   - Option B — Move the unchecked external-commitment items (lines 43-46, 51, 86-87) from `SUBMISSION_CHECKLIST.md` into an internal-only doc (e.g. `internal/release-todos.md`) and ensure the new path is excluded from the bundle.
2. If Option A: update `scripts/export-plugin.sh` near the existing exclusion list.
3. If Option B: create the new internal doc and verify it does not get rsynced into the bundle.
4. Re-run `./scripts/export-plugin.sh` and unzip the artifact to confirm the file is no longer present (or that all remaining checklist items are appropriate to ship).

---

### Task 5: Exclude `.gitignore` from the exported zip

**Source:** Code review
**Severity:** Minor
**Files:** /Users/haldunanil/Development/adology/marketing-skills/scripts/export-plugin.sh:75
**Issue:** The zip artifact contains `.gitignore` (54 bytes). It is harmless but it is a development-time file and should not ship in the marketplace bundle.
**Steps:**

1. Open `/Users/haldunanil/Development/adology/marketing-skills/scripts/export-plugin.sh`.
2. Around line 75, add `--exclude='.gitignore'` to the `rsync` exclusion list.
3. Re-run `./scripts/export-plugin.sh` and inspect the resulting zip to confirm `.gitignore` is gone.

---

### Task 6: Document the dual auth flow (env-var token vs OAuth) in `installation-claude-code.md`

**Source:** Code review
**Severity:** Minor
**Files:** /Users/haldunanil/Development/adology/marketing-skills/docs/installation-claude-code.md:48, /Users/haldunanil/Development/adology/marketing-skills/.claude-plugin/plugin.json:51-56
**Issue:** The Claude Code install doc documents `ADOLOGY_API_TOKEN` while `plugin.json` declares `auth.required: true, type: oauth2.1, provider: stytch`. The two flows are legitimate but neither doc nor README tells a Claude Code user when each applies.
**Steps:**

1. Open `/Users/haldunanil/Development/adology/marketing-skills/docs/installation-claude-code.md`.
2. Near line 48, add a one-sentence explanation along the lines of: "Use the `ADOLOGY_API_TOKEN` environment variable if you already have a long-lived token; otherwise the marketplace install will trigger the OAuth 2.1 flow on first request."
3. Re-read the section to confirm the dual flow reads naturally to a first-time installer.

---

### Task 7: Verify the `plugin-v0.1.0` git tag exists before submission

**Source:** Code review
**Severity:** Minor
**Files:** /Users/haldunanil/Development/adology/marketing-skills/SUBMISSION.md:104, /Users/haldunanil/Development/adology/marketing-skills/.github/workflows/release.yml:76
**Issue:** `SUBMISSION.md` claims the release tag is `plugin-v0.1.0` and the release workflow does cut tags as `plugin-v$VERSION`, but the visible release commit is `chore(release): v0.1.0 — initial release` and there is no proof on this branch that the tag actually exists.
**Steps:**

1. Run `git tag -l 'plugin-v*'` to confirm the tag exists.
2. If it is missing, either (a) cut the tag manually with `git tag plugin-v0.1.0 <release-sha>` and push it, or (b) update `SUBMISSION.md:104` to reference the actual tag that was cut.
3. Re-read `SUBMISSION.md` to confirm the tag reference is accurate.

---

### Task 8: Trim or split the oversized `creative-patterns.md` reference if a bundle size budget exists

**Source:** Code review
**Severity:** Minor
**Files:** /Users/haldunanil/Development/adology/marketing-skills/creative-toolkit/references/creative-patterns.md, /Users/haldunanil/Development/adology/marketing-skills/creative-toolkit/references/toolkit-template.html, /Users/haldunanil/Development/adology/marketing-skills/influencer-vetting/SKILL.md
**Issue:** `creative-patterns.md` is 62KB, `toolkit-template.html` is 25KB, and `influencer-vetting/SKILL.md` is 28KB. Together with other references the bundle is ~370KB extracted. Not a blocker, but if the marketplace has a soft size budget, `creative-patterns.md` is the obvious candidate to split or trim.
**Steps:**

1. Confirm whether the directory enforces a bundle size budget (check `SUBMISSION.md` and any marketplace policy URLs already linked from `plugin.json`).
2. If a budget exists and the bundle exceeds it, split `creative-patterns.md` into smaller topic-scoped reference files under `creative-toolkit/references/` and update any cross-links inside `creative-toolkit/SKILL.md` accordingly.
3. If no budget exists, no action — note the finding for a future cleanup.

---

### Task 9: Fix the misleading "Re-create the staging root" comment in `export-plugin.sh`

**Source:** Code review
**Severity:** Minor
**Files:** /Users/haldunanil/Development/adology/marketing-skills/scripts/export-plugin.sh:86
**Issue:** The comment at line 86 says "Re-create the staging root if the empty-dir prune removed it," but the body only prints an error and exits — it does not re-create anything. The comment is misleading.
**Steps:**

1. Open `/Users/haldunanil/Development/adology/marketing-skills/scripts/export-plugin.sh`.
2. At line 86, pick one:
   - Option A — change the comment to "Defensive guard: bail if the prune unexpectedly removed the staging root" so it matches the existing `if [ ! -d "$STAGE" ]; then echo ...; exit ...; fi` body.
   - Option B — change the body to actually `mkdir -p "$STAGE"` so it matches the original comment.
3. Re-run `./scripts/export-plugin.sh` to confirm the script still completes cleanly.

---

## Validation

After applying the changes above, run:

```bash
npm test
./scripts/export-plugin.sh
```

Then `unzip -l` the resulting artifact and confirm:

- No `.gitignore` in the zip (Task 5).
- `SUBMISSION_CHECKLIST.md` either absent or free of unchecked external-commitment TODOs (Task 4).
- The `/plugin marketplace add` and `/plugin install` instructions in `docs/installation-claude-code.md` and `README.md` are copy-paste-correct (Task 1).

Optionally run `npm run check` as a final full-suite gate before resubmitting.

---

## Summary

- **Critical:** 0 items
- **Major:** 3 items
- **Minor:** 6 items
- **Total:** 9 items
