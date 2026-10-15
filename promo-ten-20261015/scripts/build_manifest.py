#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
films=read('records/films.json'); campaign=read('records/campaign.json')
delivered=read('records/delivery.json') if (ROOT/'records/delivery.json').exists() else []
private=read('records/delivery-private.json') if (ROOT/'records/delivery-private.json').exists() else []
by_path={x['local_path']:x for x in delivered}; private_by_path={x['local_path']:x for x in private}
out=[]
for film in films:
    fid=film['id'];job=read('records/'+fid+'-job.json');v=read('records/'+fid+'-native-verification.json');p='sources/'+fid+'.mp4'
    out.append({'film_id':fid,'title':film['title'],'format':film['format'],'file':p,'poster':'posters/'+fid+'.png','generation':{'model':job['foundation_model'],'endpoint':job['endpoint_id'],'job_id':job['job_id'],'prompt':job['prompt'],'settings':job['settings'],'references':job['references'],'usage':job['result'].get('usage'),'cost':job.get('cost')},'native_output':{k:x for k,x in v.items() if k!='probe'},'r2':by_path.get(p)})
complete=len(delivered)==len(films) and all(x.get('readback_sha256_matches') and x.get('downloaded_media_full_decode_passed') for x in delivered)
visual=read('records/visual-review.json') if (ROOT/'records/visual-review.json').exists() else None
data={'campaign':campaign,'status':'delivered_and_verified' if complete else 'native_files_verified_delivery_pending','films':out,'visual_review':visual,'authentic_logo_source':read('records/brand-source.json'),'delivery':delivered,'estimated_generation_list_price_usd':round(sum(x['generation']['cost']['estimated_list_price_usd'] for x in out),6),'actual_invoice_cost_usd':None,'native_delivery':'Provider MP4 bytes uploaded unchanged; no transcoding, trimming, retiming, scaling, graphics or audio edits. Requested 30 seconds at nominal 1080p/21:9; exact native duration/codec/dimensions are retained.','original_campaign_preserved':True}
data['rejected_generation_attempts']=read('records/rejected-attempts.json') if (ROOT/'records/rejected-attempts.json').exists() else []
(ROOT/'manifest.json').write_text(json.dumps(data,indent=2)+'\n')
data['delivery']=private
for film in data['films']:film['r2']=private_by_path.get(film['file'])
(ROOT/'deliverables-manifest.json').write_text(json.dumps(data,indent=2)+'\n')
lines=['# Native delivery verification','', 'Status: **'+data['status']+'**.','', 'The videos are the original Seedance MP4s. No transcoding or post-editing was applied.','', '| Film | Native video duration | Container duration | Dimensions | Codec / pixel format | FPS / frames | Provider SHA = R2 SHA |','| --- | --- | --- | --- | --- | --- | --- |']
for f in out:
 v=f['native_output'];d=f.get('r2');lines.append(f"| {f['title']} | {v['native_video_duration']} s | {v['native_container_duration']} s | {v['native_dimensions'][0]} × {v['native_dimensions'][1]} | {v['native_video_codec']} / {v['native_pixel_format']} | {v['native_fps']} / {v['native_frames']} | {'Yes' if d and d.get('readback_sha256_matches') else 'Pending'} |")
lines+=['','Generation: Seedance 2.5, 30-second request, native 1080p preset, 21:9, native synchronized audio, no watermark. Casts include people and animated objects; human casts were optional. The authentic logo was provided as a separate reference for a physical equipment-case mark; no text overlay or logo overlay was added in editing.','', 'Checks: full native video/audio decode, frame and codec probe, soundtrack/loudness analysis without changing audio, complete R2 signed-URL readback SHA-256, full decode of downloaded R2 video and byte-range playback. No subtitle tracks are present.','', 'Native 1080p ultrawide is 2206 × 946 and may contain an extra frame/audio encoder tail beyond nominal 30 seconds. These native characteristics are intentionally preserved, following the user’s direct-upload instruction.','', 'R2 bucket: `'+campaign['bucket']+'`; prefix: `'+campaign['r2_prefix']+'`. Existing objects and first-batch links are preserved. Signed download URLs are in the local deliverables manifest and are omitted from Git.','', 'Video-generation list-price estimate: USD '+str(data['estimated_generation_list_price_usd'])+'. Actual invoice costs, resource-pack/discount offsets, image generation and R2/Worker charges were not returned.']
if delivered:lines+=['','Signed download expiry UTC: '+delivered[0]['download_expires_at_utc']+'.']
lines+=['','Three initial attempts returned no MP4 because of provider output checks: one video copyright flag and two audio copyright flags. The first concept was replaced with the original Jelly Lens treatment; the two audio-flagged concepts were regenerated with original Foley-only sound design and no music or melody. Failed ledgers are retained in `records/attempts/`. Their invoice costs were not returned. The estimate above covers the ten successful outputs only.','', 'Visual observations and native variations are recorded in `records/visual-review.json`. Review used temporal sheets and selected full-resolution frames; it does not assert perfect generative continuity.']
(ROOT/'docs/verification-report.md').write_text('\n'.join(lines)+'\n')
print(data['status'])
