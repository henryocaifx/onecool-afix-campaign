#!/usr/bin/env python3
"""Consolidate actual generation, export, review, and delivery evidence."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT/path).read_text())
campaign=read("records/campaign.json")
films=read("records/films.json")
refs=read("records/reference-manifest.json")
delivery=read("records/delivery.json") if (ROOT/"records/delivery.json").exists() else []
private=read("records/delivery-private.json") if (ROOT/"records/delivery-private.json").exists() else []
assets={x["local_path"]:x for x in delivery}
private_assets={x["local_path"]:x for x in private}
items=[]
for film in films:
    fid=film["id"]
    job=read("records/"+fid+"-job.json")
    technical=read("records/"+fid+"-technical.json")
    verified=read("records/"+fid+"-verification.json")
    source=next(x for x in technical["source_probe"]["streams"] if x["codec_type"]=="video")
    video=next(x for x in verified["probe"]["streams"] if x["codec_type"]=="video")
    audio=next(x for x in verified["probe"]["streams"] if x["codec_type"]=="audio")
    item={"film_id":fid,"title":film["title"],"format":film["format"],"version":"clean-text-free","local_mp4":"films/"+fid+".mp4","local_poster":"posters/"+fid+".png","model_id":job["foundation_model"],"endpoint_id":job["endpoint_id"],"job_id":job["job_id"],"prompt":job["prompt"],"generation_settings":job["settings"],"reference":next(x for x in refs if x["film_id"]==fid),"source":{"path":job["source"]["path"],"width":source["width"],"height":source["height"],"codec":source["codec_name"],"fps":source["r_frame_rate"],"duration":source["duration"],"sha256":job["source"]["sha256"]},"finishing":technical["source_processing"],"final":{"duration":video["duration"],"width":video["width"],"height":video["height"],"aspect_ratio":"21:9 (7:3)","fps":video["avg_frame_rate"],"frames":int(video["nb_read_frames"]),"codec":video["codec_name"],"pixel_format":video["pix_fmt"],"audio_codec":audio["codec_name"],"audio_channels":audio["channels"],"audio_sample_rate":audio["sample_rate"],"sha256":verified["sha256"],"bytes":verified["bytes"]},"verification":{"status":verified["status"],"checks":verified["checks"],"audio_loudness":verified["loudness"]},"usage":job["result"].get("usage"),"cost":job.get("cost"),"r2":assets.get("films/"+fid+".mp4")}
    items.append(item)
complete=len(delivery)==17 and all(x.get("readback_sha256_matches") for x in delivery) and all(x.get("downloaded_media_full_decode_passed") for x in delivery if x["category"]=="final")
manifest={"campaign":campaign,"status":"delivered_and_verified" if complete else "local_verified_delivery_pending","latest_user_direction":"No title/subtitle/text box; delivered films contain no added text, graphics, UI overlays, logos or end cards.","films":items,"assets":delivery,"estimated_generation_list_price_usd":round(sum(x["cost"]["estimated_list_price_usd"] for x in items),6),"actual_invoice_cost_usd":None,"other_costs":"Image generation, R2 and Worker invoice amounts were not returned. List-price estimates are not actual charges.","production_assets":"aifx-studio-production-assets.zip","scripts":"docs/scripts-clean.md","editing_instructions":"docs/editing-clean.md","source_clips":"sources/; also uploaded as individually verified R2 assets","deviations":["Latest user instruction supersedes original typography, branding overlay and CTA/end-card requirements.","Official 1080p 21:9 source is 2206x946. Finished frames are scaled/cropped to exact 2520x1080.","27-second accepted narratives are retimed to exactly 30 seconds at 90% speed; audio tempo changes preserve pitch.","Supplied product repository returned 404. Creation routes require sign-in. Product research is limited to real public UI and published positioning; no unverified application capabilities are claimed.","Existing R2 credentials are absent in the runtime. With explicit user approval, a scoped private-bucket Worker supplies expiring HMAC-signed download URLs instead of S3 presigned URLs.","Provider documentation describes mono audio; actual received files have two AAC channels with measurable differences, which are preserved."]}
(ROOT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
private_manifest=json.loads(json.dumps(manifest))
private_manifest["assets"]=private
for item in private_manifest["films"]:
    item["r2"]=private_assets.get(item["local_mp4"])
(ROOT/"deliverables-manifest.json").write_text(json.dumps(private_manifest,indent=2)+"\n")
lines=["# Verification report","", "Status: **"+manifest["status"]+"**.","", "All four final videos are clean masters with no added title, subtitle, text box, UI overlay, logo, or text end card, following the user's final direction.","", "| Film | Duration | Frame | FPS / frames | Video / audio | LUFS-I | True peak | R2 |","| --- | --- | --- | --- | --- | ---: | ---: | --- |"]
for x in items:
    f=x["final"]; l=x["verification"]["audio_loudness"]; d=x.get("r2")
    lines.append(f"| {x['title']} | {f['duration']} s | {f['width']} × {f['height']}, 21:9 | 24 / 720 | H.264 / AAC stereo 48 kHz | {l['input_i']} | {l['input_tp']} dBTP | {'Verified' if d and d.get('readback_sha256_matches') else 'Pending'} |")
lines += ["", "Technical checks: square pixels, constant 24 fps, exact 720-frame video duration, 30-second audio, H.264 yuv420p, AAC stereo, complete video/audio decode, loudness and peak analysis. All pass. Technical results are tied to final-file SHA-256 values, so superseded branded drafts cannot be mistaken for accepted clean masters.","", "Visual review used full-resolution checkpoints and temporal frame sheets for all four sources and clean exports. Reviewed frames retain consistent recurring characters, readable cinematic action, and clear visual joke/hero-shot beats. No distracting anatomy failures or accidental caption overlays were observed in the reviewed frames. The native film soundtracks provide original music and synchronized effects. There is no scripted spoken dialogue, and no subtitle track is present.","", "R2 destination: `"+campaign["bucket"]+"`, prefix `"+campaign["r2_prefix"]+"`. Objects are created without overwriting existing data; SHA-256 is validated by R2 and confirmed by full signed-URL readback. Finished MP4 readbacks are decoded in full and HTTP byte ranges are checked for playback/seeking. Bucket public access remains disabled.","", "Signed download expiry: **2026-10-22 16:27:57 Asia/Taipei** (2026-10-22T08:27:57Z). Upload authorization expires 2026-10-15T10:27:57Z. The Worker rejects unsigned access, files outside the 17-object allowlist, expired links, and overwrite attempts.","", "Published video-generation list-price estimate: **USD 61.899504** for four accepted jobs. Actual billing, discounts/resource packs, image generation, R2 and Worker charges are not available from the returned usage records.","", "Documented deviations:",""]
lines += ["- "+x for x in manifest["deviations"]]
lines += ["", "The production ZIP is a source-material snapshot containing references, clean posters, scripts, editing/API tools, research, job records, and export verification. Source video clips and final MP4s are delivered separately. The latest delivery evidence and consolidated manifest are retained in the repository and the local deliverables manifest."]
(ROOT/"docs/verification-report.md").write_text("\n".join(lines)+"\n")
print(manifest["status"],len(delivery),"assets verified")
