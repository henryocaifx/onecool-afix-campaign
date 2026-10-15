# Native delivery verification

Status: **delivered_and_verified**.

The videos are the original Seedance MP4s. No transcoding or post-editing was applied.

| Film | Native video duration | Container duration | Dimensions | Codec / pixel format | FPS / frames | Provider SHA = R2 SHA |
| --- | --- | --- | --- | --- | --- | --- |
| The Snack-Sized Blockbuster | 30.041667 s | 30.080000 s | 2206 × 946 | hevc / yuv420p10le | 24/1 / 721 | Yes |
| The Paper Street Parade | 30.041667 s | 30.080000 s | 2206 × 946 | hevc / yuv420p10le | 24/1 / 721 | Yes |
| The Jelly Lens | 30.041667 s | 30.080000 s | 2206 × 946 | hevc / yuv420p10le | 24/1 / 721 | Yes |
| The Clay Set Catastrophe | 30.041667 s | 30.080000 s | 2206 × 946 | hevc / yuv420p10le | 24/1 / 721 | Yes |
| The Neon Lens Run | 30.041667 s | 30.080000 s | 2206 × 946 | hevc / yuv420p10le | 24/1 / 721 | Yes |
| The Ink and Silk Set | 30.041667 s | 30.080000 s | 2206 × 946 | hevc / yuv420p10le | 24/1 / 721 | Yes |
| The Popcorn Orbit | 30.041667 s | 30.080000 s | 2206 × 946 | hevc / yuv420p10le | 24/1 / 721 | Yes |
| The Desert Ribbon Rally | 30.041667 s | 30.080000 s | 2206 × 946 | hevc / yuv420p10le | 24/1 / 721 | Yes |
| The Museum of Maybe | 30.041667 s | 30.080000 s | 2206 × 946 | hevc / yuv420p10le | 24/1 / 721 | Yes |
| The Midnight Light Kitchen | 30.041667 s | 30.080000 s | 2206 × 946 | hevc / yuv420p10le | 24/1 / 721 | Yes |

Generation: Seedance 2.5, 30-second request, native 1080p preset, 21:9, native synchronized audio, no watermark. Casts include people and animated objects; human casts were optional. The authentic logo was provided as a separate reference for a physical equipment-case mark; no text overlay or logo overlay was added in editing.

Checks: full native video/audio decode, frame and codec probe, soundtrack/loudness analysis without changing audio, complete R2 signed-URL readback SHA-256, full decode of downloaded R2 video and byte-range playback. No subtitle tracks are present.

Native 1080p ultrawide is 2206 × 946 and may contain an extra frame/audio encoder tail beyond nominal 30 seconds. These native characteristics are intentionally preserved, following the user’s direct-upload instruction.

R2 bucket: `aifx-studio-campaign`; prefix: `campaigns/20261015T090200Z-promo-ten/`. Existing objects and first-batch links are preserved. Signed download URLs are in the local deliverables manifest and are omitted from Git.

Video-generation list-price estimate: USD 171.91652. Actual invoice costs, resource-pack/discount offsets, image generation and R2/Worker charges were not returned.

Signed download expiry UTC: 2026-10-22T09:28:08.000Z.

Three initial attempts returned no MP4 because of provider output checks: one video copyright flag and two audio copyright flags. The first concept was replaced with the original Jelly Lens treatment; the two audio-flagged concepts were regenerated with original Foley-only sound design and no music or melody. Failed ledgers are retained in `records/attempts/`. Their invoice costs were not returned. The estimate above covers the ten successful outputs only.

Visual observations and native variations are recorded in `records/visual-review.json`. Review used temporal sheets and selected full-resolution frames; it does not assert perfect generative continuity.

Final Cloudflare API inventory independently confirms all 31 objects across the three batches (17 original assets, four native films, ten native promos), with sizes and SHA-256 metadata matching each transfer index. Managed public R2 access remains disabled.
