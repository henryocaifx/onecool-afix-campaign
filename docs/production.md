# Production specification

## Verified provider configuration

Official documentation retrieved on 2026-10-15:

- https://ai.byteplus.com/ark/region:ap-southeast-1/docs/seedance-2-5.md
- https://ai.byteplus.com/ark/region:ap-southeast-1/docs/create-video-generation-task-api.md
- https://ai.byteplus.com/ark/region:ap-southeast-1/docs/base-url-and-authentication.md
- https://ai.byteplus.com/ark/region:ap-southeast-1/docs/model-pricing.md

The configured endpoint was read with the official BytePlus SDK. It reports foundation model `dreamina-seedance-2-5`, version `260628`, status `Running`. Full non-secret model metadata is retained in `records/endpoint.json`. AK/SK exchanged for an endpoint-scoped temporary token held only in memory; listing generation tasks returned HTTP 200. No generation is included in this preflight check.

Data-plane base URL: `https://ark.ap-southeast.bytepluses.com/api/v3`. Submit `POST /contents/generations/tasks`; poll `GET /contents/generations/tasks/{id}`. The actual configured endpoint ID is used as `model` when authenticating with scoped access-key credentials.

Current documentation supports 4–30-second generation, 480p/720p/1080p outputs, 21:9, synchronized generated audio, and omni reference images. A single request can carry up to 30 images, with a combined omni-asset limit of 50. Images may be supplied as HTTPS URLs, supported asset IDs, or base64 data URLs; request body limit 64 MB, single image under 30 MB, width/height 300–6000, aspect ratio 0.4–2.5. Use one clean reference image per film, submitted in a documented base64 data URL as `image_url` with `role: reference_image`. No contact sheets are sent to the API.

1080p at 21:9 is documented as **2206 × 946**, not 2520 × 1080. Finishing will scale with Lanczos and perform the minimal centered crop needed for exact 7:3 output; record actual source dimensions. Generated 1080p MP4 uses HEVC; finals will be re-encoded to H.264 yuv420p for broad playback support. Generated audio is mono; finishing will create an AAC stereo mix and document the mono source.

Published online list price for 1080p generation without input video: **USD 11.70 per million output tokens**. Retain returned usage and calculate a list-price estimate. This is not an actual invoice, and account discounts/resource-pack offsets may differ. Failed preflight is not a generation charge. Do not invent unavailable actual billing information.

## Editorial approach

Four separate 27-second, multi-shot source sequences maintain character and soundtrack continuity. The edit integrates authentic UI at a planned product beat, composites accurate titles, and adds an approximately three-second closing card. Source sequence timing is reviewed and adjusted if the model diverges from the script.

Final technical target: 30.000 seconds; 2520 × 1080; SAR 1:1; DAR 7:3 (21:9); 24 fps constant; 720 video frames; H.264 video; AAC stereo, 48 kHz; fast-start MP4. Music and effects are original model-generated audio plus any original procedural finishing accents, with no commercial music or existing character references.

## Delivery and security

No Cloudflare/R2 environment credentials are present in the current runtime. A connected Cloudflare account is available; its initial bucket listing contains `ariel` and `reaching-god`, but not `aifx-studio-campaign`. Upload route and target bucket availability remain unresolved. Do not modify any existing bucket or access settings. Create only the specifically requested destination if supported and needed for delivery. Use a unique `campaigns/<UTC timestamp>/` prefix. Do not commit presigned URLs into Git.

Generation submission is sequential and recorded immediately. Re-running a command must reuse saved job IDs rather than submit duplicates. No automatic retries on task creation. Polling may be resumed safely. Returned provider URLs are temporary and are downloaded promptly, then removed from publishable records.

## Acceptance checks

Inspect representative/full-resolution frames, the complete temporal sequence, and audio. Check script structure and memorable character beats. Probe each final with ffprobe, decode all frames/audio, measure loudness/peaks, and verify exact frame count. For R2: preserve object keys, MIME type, byte count, SHA-256, download/playback probe, and URL expiration when applicable. A missing check is recorded as incomplete rather than passed.
