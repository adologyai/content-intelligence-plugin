---
name: export
description: Show how to export knowledge set data from the Adology web UI
---

`/export` does not run an export from inside Claude — bulk data export
(CSV, JSONL, text) lives in the Adology web UI. When the user invokes
`/export`, tell them:

- Open the Adology web UI, navigate to the Knowledge Set, and use the
  export button to download data in CSV, JSONL, or text.
- For sharing curated selections of content from inside Claude, use the
  `save_to_collection` MCP tool to organize items into a named
  collection. The response includes a shareable gallery URL that can be
  opened directly in the Adology app.

If the user expected `/export` to produce a CSV in the conversation,
clarify that the in-Claude path is `save_to_collection` + the returned
gallery URL; CSV/JSONL/text downloads remain in the web UI.
