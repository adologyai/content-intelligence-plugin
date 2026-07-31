---
name: thumbnails
description: >
  Work with Adology thumbnails — the poster frame on every item. Covers getting thumbnail
  URLs, reading what's in the frame for visual/creative analysis, and embedding the images
  reliably in generated documents (HTML, PDF, slides). Use whenever a deliverable carries
  visual citations from Adology items — empathy canvases, insight briefs, scorecards,
  creative toolkits, audit reports, decks — or when the question is about the first frame
  itself: thumbnail style, hook visuals, what an image-led post looks like versus a video.
  Triggers on: "embed thumbnail", "include thumbnails", "show thumbnail", "first frame",
  "thumbnail analysis", or whenever any other skill produces a document with visual
  citations from Adology.
---

# Thumbnails

Every item Adology returns from `analyze` carries a `thumbnail` in its base set — a poster
image, so a video item resolves to a still frame rather than a video file. Alongside it is
`url`, the post's own permalink. Those two fields are the whole visual citation.

An item with no stored asset comes back with an empty `thumbnail`. That's a real state, not
an error: drop the item, or swap it for the next candidate, rather than rendering a broken
image or inventing a placeholder.

## Getting thumbnail URLs

Thumbnails ride on `analyze`. Two shapes cover almost everything:

- **You already know which posts you want** — `analyze({ projectId, itemIds: [...] })`. The
  by-id deep dive returns each item's full creative read plus `url` and `thumbnail`. This is
  the hydration step after any ranking: rank with `query_items` (which carries lift multiples,
  `isOutlier`, and `externalUrl`), collect the `itemId` values, then hydrate them here for the
  images and creative fields.
- **You want a set that matches a description** — `analyze({ projectId, query, distribution })`
  with `distribution: 'top'` for the highest-engagement items per feed, `'recent'` for newest,
  or `'exhaustive'` with `sortBy` for a deterministic ranked page you can page through.

Add `mediaTypeFilter: 'image'` or `'video'` to keep the set to one media class — worth doing
whenever the question is about the frame itself, since a video's poster and a still image are
different creative artifacts even though both arrive as a `thumbnail`.

## Reading what's in the frame

For visual and first-frame analysis, ask `analyze` for the fields that describe the image
rather than the copy: `visualDescription`, `visualConcept`, `productDisplayStyle`,
`productionStyle`, `creativeExecution`, and `narrativeFormat`. Pair those with
`mediaTypeFilter` so you're comparing like with like.

To quantify a visual pattern instead of reading individual frames, pivot on the scope's
visual label dimensions. Discover which dimensions exist first — `list_labels({ projectId })`,
or `get_table_data({ projectId, listDimensions: true })` — then pivot:
`get_table_data({ projectId, rows: ['<visual dimension>'], columns: 'focalVsRest', focalBrand,
metrics: ['count','useRate','medianLikes'], mediaTypes: ['video'] })`. Assumed dimension names
produce empty tables, so always take them from the discovery call.

**Every data claim comes from the tools.** You may look at a downloaded image to write a
caption about what it shows, but counts, rates, engagement, lift, and label distributions come
from `analyze`, `get_table_data`, or `aggregate` — never from eyeballing a grid of pictures.

## Embedding thumbnails in a deliverable

Invoke this skill **before** producing any deliverable that includes a visual citation. The
deliverable types that need it:

- Empathy canvases (HTML one-pagers from `audience-deep-dive`)
- Insight briefs (markdown with image embeds)
- Influencer scorecards (HTML reports from `influencer-vetting`)
- Creative toolkit HTML companion files (from `creative-toolkit`)
- Coaching reports (from `influencer-coach`)
- Any audit deck or report that cites specific posts

A naive `<img src="https://...">` reference to a thumbnail URL can silently fail to render in
generated HTML/PDF: the URL is reachable, but the runtime fetch breaks during document
generation. Inline the bytes instead.

### Base64 inlining

1. Fetch the thumbnail URL into memory.
2. Convert the bytes to a base64 data URI: `data:image/jpeg;base64,<encoded>`.
3. Use the data URI as the `src` of the `<img>` tag.

This makes the document self-contained — the recipient can open it offline, with no network
access and no Adology session.

### Reference implementation (Python, sandbox-safe)

```python
import base64, mimetypes, urllib.request

def to_data_uri(url: str, timeout: int = 10) -> str:
    with urllib.request.urlopen(url, timeout=timeout) as r:
        data = r.read()
        mime = r.headers.get("Content-Type") or mimetypes.guess_type(url)[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"
```

Use Python's `urllib.request` (or an equivalent library call) rather than shell `curl`/`wget` —
the shell fetch is the exact failure mode this skill exists to work around.

*Edge case: if the deliverable will only be viewed inside the Adology workbench, where the page
already holds an Adology session, the bare URL works. Rare for plugin users — when in doubt,
always inline.*

## Workflow inside a host skill

When another skill (e.g. `audience-deep-dive`) is producing a deliverable with thumbnails:

1. Identify the items that will appear, and hydrate them through `analyze` for `url` +
   `thumbnail`.
2. Fetch and base64-encode each thumbnail.
3. Substitute the data URIs into the document template, keeping each item's `url` as the link
   target.
4. Render the final document.

The host skill invokes `content-intelligence:thumbnails` and applies the substitution as part
of its own rendering step; there is no shared utility script.

## Common pitfalls

- **Don't fetch sequentially.** If the document has 20 thumbnails, fetch them in parallel.
- **Don't lose the mapping.** Keep an explicit URL → data-URI map so each image lands in the
  right document position.
- **Handle the empty `thumbnail`.** Swap in the next-ranked item rather than shipping a gap.
- **Set a sensible timeout** on the fetch. If a fetch is slow, fail loudly (preserving the
  original URL) rather than producing a broken document.
- **Caption from your own reading, not from the item text.** Restating `visualDescription`
  under an image the reader can already see adds nothing.
