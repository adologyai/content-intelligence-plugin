# Thumbnail handling for Adology / web visuals

When producing any deliverable that needs thumbnails (decks, reports, HTML one-pagers with example creative), **use the `content-intelligence:thumbnails` skill**. It exists specifically to solve a sandbox limitation where bash can't fetch images from external CDNs — without the workaround, thumbnails silently fail and you ship broken image tags.

**Rule of thumb:** before embedding *any* external image in a .docx, .pptx, .html, or .md deliverable, invoke the `content-intelligence:thumbnails` skill to get the correct fetch method. Don't try to `curl` or `wget` the image directly.

**Where this skill needs thumbnails:**

1. **Audit appendix in the .docx** — top-6 archetype examples with one or two thumbnails per archetype to show what the brand currently looks like.
2. **Competitive landscape slides in the .pptx** — showing each competitor's representative content visually.
3. **Before/after reworked examples in the HTML or .docx** — the "before" is real Adology content; showing the thumbnail alongside the verbatim copy makes the comparison concrete.

If thumbnails can't be fetched for any reason, fall back to:
- Text description of the visual (e.g., "Ad shows founder addressing camera in kitchen, plain styling, intimate tone").
- Direct link to the source so the reader can view it.

Never ship a broken `<img>` tag.
