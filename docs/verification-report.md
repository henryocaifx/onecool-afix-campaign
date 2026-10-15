# Verification report

Status: **delivered_and_verified**.

All four final videos are clean masters with no added title, subtitle, text box, UI overlay, logo, or text end card, following the user's final direction.

| Film | Duration | Frame | FPS / frames | Video / audio | LUFS-I | True peak | R2 |
| --- | --- | --- | --- | --- | ---: | ---: | --- |
| The Little Idea That Escaped | 30.000000 s | 2520 × 1080, 21:9 | 24 / 720 | H.264 / AAC stereo 48 kHz | -15.27 | -1.30 dBTP | Verified |
| Deadline: Impossible | 30.000000 s | 2520 × 1080, 21:9 | 24 / 720 | H.264 / AAC stereo 48 kHz | -16.19 | -1.44 dBTP | Verified |
| The Last Spark | 30.000000 s | 2520 × 1080, 21:9 | 24 / 720 | H.264 / AAC stereo 48 kHz | -17.22 | -1.40 dBTP | Verified |
| The Imagination Heist | 30.000000 s | 2520 × 1080, 21:9 | 24 / 720 | H.264 / AAC stereo 48 kHz | -16.55 | -1.43 dBTP | Verified |

Technical checks: square pixels, constant 24 fps, exact 720-frame video duration, 30-second audio, H.264 yuv420p, AAC stereo, complete video/audio decode, loudness and peak analysis. All pass. Technical results are tied to final-file SHA-256 values, so superseded branded drafts cannot be mistaken for accepted clean masters.

Visual review used full-resolution checkpoints and temporal frame sheets for all four sources and clean exports. Reviewed frames retain consistent recurring characters, readable cinematic action, and clear visual joke/hero-shot beats. No distracting anatomy failures or accidental caption overlays were observed in the reviewed frames. The native film soundtracks provide original music and synchronized effects. There is no scripted spoken dialogue, and no subtitle track is present.

R2 destination: `aifx-studio-campaign`, prefix `campaigns/20261015T075922Z-7d16e228/`. Objects are created without overwriting existing data; SHA-256 is validated by R2 and confirmed by full signed-URL readback. Finished MP4 readbacks are decoded in full and HTTP byte ranges are checked for playback/seeking. Bucket public access remains disabled.

Signed download expiry: **2026-10-22 16:27:57 Asia/Taipei** (2026-10-22T08:27:57Z). Upload authorization expires 2026-10-15T10:27:57Z. The Worker rejects unsigned access, files outside the 17-object allowlist, expired links, and overwrite attempts.

Published video-generation list-price estimate: **USD 61.899504** for four accepted jobs. Actual billing, discounts/resource packs, image generation, R2 and Worker charges are not available from the returned usage records.

Documented deviations:

- Latest user instruction supersedes original typography, branding overlay and CTA/end-card requirements.
- Official 1080p 21:9 source is 2206x946. Finished frames are scaled/cropped to exact 2520x1080.
- 27-second accepted narratives are retimed to exactly 30 seconds at 90% speed; audio tempo changes preserve pitch.
- Supplied product repository returned 404. Creation routes require sign-in. Product research is limited to real public UI and published positioning; no unverified application capabilities are claimed.
- Existing R2 credentials are absent in the runtime. With explicit user approval, a scoped private-bucket Worker supplies expiring HMAC-signed download URLs instead of S3 presigned URLs.
- Provider documentation describes mono audio; actual received files have two AAC channels with measurable differences, which are preserved.

The production ZIP is a source-material snapshot containing references, clean posters, scripts, editing/API tools, research, job records, and export verification. Source video clips and final MP4s are delivered separately. The latest delivery evidence and consolidated manifest are retained in the repository and the local deliverables manifest.
