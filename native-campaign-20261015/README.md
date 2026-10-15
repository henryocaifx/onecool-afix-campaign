# ONECOOL AIFX · Four New Worlds

Four additional human-led native Seedance 2.5 films: two complete stories and two Hollywood-style trailers. No animals, no title/subtitle/text boxes, and an authentic ONECOOL AIFX equipment-case logo reference. Video files are uploaded exactly as returned by Seedance, without transcoding or post-editing.

| Film | Format |
| --- | --- |
| 05 — The Rooftop Cinema | Storytelling short |
| 06 — The Gravity Laundrette | Storytelling short |
| 07 — The Ninth Platform | Movie trailer |
| 08 — The Glass Tide | Movie trailer |

See `docs/scripts.md` for exact 30-second requested scripts, `records/films.json` for full API prompts/settings, `records/reference-prompts.json` for image prompts, and `docs/native-delivery.md` for the no-edit delivery specification. Native videos live in `sources/` and are delivered through R2 rather than Git objects.

From the repository root:

```sh
python scripts/byteplus_jobs.py submit --project-root native-campaign-20261015
python scripts/byteplus_jobs.py poll --project-root native-campaign-20261015
python native-campaign-20261015/scripts/verify_native.py
```

Do not delete or reset submission ledgers to force a retry. Signed transfer URLs and credentials are excluded from commits. The original four-film campaign and its download service are preserved.

All four native MP4s are uploaded and readback verified in R2. See `manifest.json` and `docs/verification-report.md`; local signed links are in ignored `deliverables-manifest.json`. The laundrette includes a brief native logo-only closing shot, preserved without editing.
