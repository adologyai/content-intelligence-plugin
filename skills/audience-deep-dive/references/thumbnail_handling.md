# Thumbnail handling for Adology / web visuals

When producing any deliverable that needs thumbnails (decks, reports, HTML canvases with example creative), **use the `content-intelligence:thumbnails` skill**. It exists specifically to solve a sandbox limitation where bash can't fetch images from external CDNs — without the workaround, thumbnails silently fail and you ship broken image tags.

**Rule of thumb:** before embedding *any* external image in a .docx, .pptx, .html, or .md deliverable, invoke the adology-thumbnails skill to get the correct fetch method. Don't try to `curl` or `wget` the image directly.

If thumbnails can't be fetched for any reason, fall back to:
- Text description of the visual (e.g., "Ad shows smiling grey-haired couple on a beach, bright color palette, tagline 'Your next chapter'").
- Direct link to the source so the reader can view it.

Never ship a broken `<img>` tag.
