# AIFX Studio · Make room for your imagination

Four completed original 30-second campaign films, commissioned in the attached brief. All four clean MP4s are uploaded and verified in the private `aifx-studio-campaign` R2 bucket, together with source clips, reference images, poster frames and the production-assets ZIP (17 objects total).

**Latest direction:** Final videos are clean cinematic masters with no added title, subtitle, text box, UI overlay, logo, or text end card. This supersedes the original campaign end-card requirement. The complete 27-second narrative source is retimed to exactly 30 seconds, with synchronized pitch-preserving audio adjustment. See `docs/editing-clean.md` for the final edit; earlier branding materials are retained only as development history.

| Film | Format | Creative identity |
| --- | --- | --- |
| 01 — The Little Idea That Escaped | Storytelling short | Handmade amber-and-teal adventure |
| 02 — Deadline: Impossible | Storytelling short | Fast, colorful studio comedy |
| 03 — The Last Spark | Movie trailer | Monumental monochrome-to-color science fantasy |
| 04 — The Imagination Heist | Movie trailer | Magenta-and-cyan caper with a comic sting |

See [the final scripts](docs/scripts-clean.md), [product research](docs/product-research.md), and [verification report](docs/verification-report.md). Assets, generation records, source clips, exports, and delivery records remain separate. Large final/source videos are delivered through R2 rather than regular Git objects. Never commit credentials, temporary access tokens, or signed provider result URLs.

Milestone commits are pushed to `main` in `henryocaifx/onecool-afix-campaign`, as requested.

The additional human-led, unedited native Seedance batch is tracked in [Four New Worlds](native-campaign-20261015/README.md). Its source files, records and R2 prefix remain separate from the original four films.

Delivery prefix: `campaigns/20261015T075922Z-7d16e228/`. Every final is 2520 × 1080, exact 21:9, 24 fps / 720 frames, H.264 yuv420p with 48 kHz AAC stereo. Signed URLs are in the local `deliverables-manifest.json`; they expire **2026-10-22 16:27:57 Asia/Taipei**. The committed `manifest.json` retains public object keys, hashes, prompts, settings, usage and verification evidence without publishing signed access URLs.
