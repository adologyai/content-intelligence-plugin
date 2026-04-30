---
name: thumbnails
description: >
  Reliably embed Adology thumbnail images in generated documents (HTML, PDF, slides).
  Use whenever a deliverable references thumbnails from Adology items — empathy canvases,
  insight briefs, scorecards, creative toolkits, audit reports, decks. Triggers on:
  "embed thumbnail", "include thumbnails", "show thumbnail", or whenever any other skill
  produces a document with visual citations from Adology.
---

# Thumbnail Embedding

This skill exists because the sandbox environment Claude runs in has a quirk: naive `<img src="https://...">` references to Adology-hosted thumbnails silently fail to render in produced HTML/PDF documents. The Adology thumbnail URL is reachable but the runtime fetch breaks during document generation.

## When to use

Invoke this skill **before** producing any deliverable that includes a visual citation from Adology data. The deliverable types that need this:

- Empathy canvases (HTML one-pagers from `audience-deep-dive`)
- Insight briefs (markdown with image embeds)
- Influencer scorecards (HTML reports from `influencer-vetting`)
- Creative toolkit HTML companion files (from `creative-toolkit`)
- Coaching reports (from `influencer-coach`)
- Any audit deck or report that cites specific posts

## The mechanism

For every Adology thumbnail you want to embed:

### Option 1: Base64 inlining (preferred for self-contained documents)

1. Fetch the thumbnail URL into memory.
2. Convert the bytes to a base64 data URI: `data:image/jpeg;base64,<encoded>`.
3. Use the data URI as the `src` of the `<img>` tag.

This makes the document self-contained — the recipient can open it offline without needing Adology auth or network access.

### Reference implementation (Python, sandbox-safe)

```python
import base64, mimetypes, urllib.request

def to_data_uri(url: str, timeout: int = 10) -> str:
    with urllib.request.urlopen(url, timeout=timeout) as r:
        data = r.read()
        mime = r.headers.get("Content-Type") or mimetypes.guess_type(url)[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"
```

Do **not** use bash `curl`/`wget` — those are the exact failure mode this skill exists to work around. Use Python's `urllib.request` (or equivalent) instead.

*Edge case: if the deliverable will only be viewed inside the Adology workbench (where the page already has Adology auth), you can skip the encoding and use the bare URL. Rare for plugin users — when in doubt, always inline.*

## Workflow inside a host skill

When another skill (e.g., `audience-deep-dive`) is producing a deliverable with thumbnails:

1. Identify all thumbnail URLs that will appear in the document.
2. For each URL, fetch and base64-encode (Option 1).
3. Substitute the data URIs into the document template.
4. Render the final document.

The host skill should invoke `content-intelligence:thumbnails` and follow this workflow inline. There is no shared utility script — each host skill applies the substitution as part of its rendering step.

## Why this is a separate skill

The thumbnail-handling mechanism is a workaround for a specific runtime constraint. Centralizing it as a skill keeps the workaround in one place. If the underlying constraint is ever fixed, only this skill needs to change.

## Common pitfalls

- **Don't fetch sequentially.** If the document has 20 thumbnails, fetch them in parallel.
- **Don't lose track of which URL maps to which document position.** Maintain a URL → data-URI mapping during the substitution.
- **Watch for non-image thumbnail URLs.** Some Adology items have video thumbnails — handle them as still-frame fetches the same way.
- **Set a sensible timeout** on the fetch. If Adology is slow, fail loudly (with the original URL preserved as a fallback) rather than producing a broken document.
