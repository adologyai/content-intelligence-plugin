# Skills Reference

The plugin bundles 11 skills. Each is a self-contained Claude workflow that
triggers on recognizable user phrases and runs to completion.

## Onboarding & foundational

| Skill                | Triggers                                                         |
| -------------------- | ---------------------------------------------------------------- |
| `getting-started`    | First-time user or "how do I use this", "walk me through"        |
| `brand-builder`      | "Build a knowledge set for [brand]", "track [brand] + competitors" |
| `data-explorer`      | "What data do you have", "show me the schema", "query items"    |

## Analysis & research

| Skill                          | Triggers                                                         |
| ------------------------------ | ---------------------------------------------------------------- |
| `research-analyst`             | "Do research on [topic]", "analyze across [brands]"              |
| `content-strategist`           | "What content strategy should we run", "content plan"            |
| `audience-deep-dive`           | "Audience deep dive", "persona for [segment]", "who is our customer" |

## Strategy & brand

| Skill                             | Triggers                                                      |
| --------------------------------- | ------------------------------------------------------------- |
| `brand-marketing-mode`            | "Brand marketing mode", "how should we market", "positioning" |

## Creative

| Skill                | Triggers                                                       |
| -------------------- | -------------------------------------------------------------- |
| `creative-toolkit`   | "Creative toolkit", "swipe file", "hook library", "give me angles" |

## Creator / influencer

| Skill                   | Triggers                                                     |
| ----------------------- | ------------------------------------------------------------ |
| `influencer-coach`      | "Coach my content", "why did my post flop", "analyze my account" |
| `influencer-vetting`    | "Vet creators", "score these influencers", "creator shortlist" |

## Utilities

| Skill          | Triggers                                                                        |
| -------------- | ------------------------------------------------------------------------------- |
| `thumbnails`   | Reliably embed Adology thumbnails in generated documents (workaround for sandbox img-fetch quirk). |

Each skill file (`skills/<name>/SKILL.md`) contains its full instructions,
trigger patterns, and any bundled reference material or templates.
