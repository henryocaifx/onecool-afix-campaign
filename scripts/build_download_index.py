#!/usr/bin/env python3
"""Create an ignored, human-readable download index; never commit signed links."""
import html
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'review';out.mkdir(exist_ok=True)
lines=['# ONECOOL AIFX · Native campaign films','', 'Original Seedance MP4s, delivered without transcoding or post-editing. Requested 30 seconds, 1080p, 21:9. Exact native timing, dimensions and codec are retained in each verification report.','']
cards=[]
for folder,label in [('native-campaign-20261015','Four New Worlds — two stories and two trailers'),('promo-ten-20261015','Ten Ways Into Wonder — ten campaign promos')]:
    batch=ROOT/folder;manifest=batch/'deliverables-manifest.json'
    if not manifest.exists():continue
    data=json.loads(manifest.read_text())
    lines+=['## '+label,'','| Film | Style | Original MP4 |','| --- | --- | --- |']
    for f in data['films']:
        delivery=f.get('r2') or {};url=delivery.get('download_url')
        if not url:continue
        lines.append('| '+f['title']+' | '+f['format']+' | [Watch / download]('+url+') |')
        poster=(batch/f['poster']).as_uri()
        cards.append('<article><video controls playsinline preload="none" poster="'+html.escape(poster,quote=True)+'" src="'+html.escape(url,quote=True)+'"></video><div><h2>'+html.escape(f['title'])+'</h2><p>'+html.escape(f['format'])+'</p><a href="'+html.escape(url,quote=True)+'">Open original MP4 ↗</a></div></article>')
    dates=sorted(set(x['download_expires_at_utc'] for x in data['delivery']))
    lines+=['','Signed link expiry: '+', '.join(dates)+'.','']
(out/'downloads.md').write_text('\n'.join(lines)+'\n')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ONECOOL AIFX · Campaign films</title><style>
*{box-sizing:border-box}body{margin:0;background:#101113;color:#f6f1df;font:16px/1.5 system-ui,sans-serif}header,main,footer{max-width:1450px;margin:auto;padding:32px}header{padding-top:64px}h1{font-size:clamp(32px,5vw,62px);line-height:1.05;margin:12px 0 24px;letter-spacing:-.04em}header small{color:#e4b94c;letter-spacing:.2em}header p,footer{color:#bcb9b1;max-width:850px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,470px),1fr));gap:26px}article{background:#1b1d20;border:1px solid #33363a;border-radius:12px;overflow:hidden}video{width:100%;display:block;aspect-ratio:21/9;background:#000}article div{padding:20px}h2{font-size:23px;margin:0 0 7px}article p{color:#bcb9b1;margin:0 0 15px}a{color:#f0c65b;text-underline-offset:4px}footer{font-size:14px;padding-bottom:60px}</style><header><small>ONECOOL AIFX</small><h1>Make room for wonder.</h1><p>Four cinematic stories and trailers, followed by ten playful campaign worlds. Watch the original Seedance films or open an MP4 to save it.</p></header><main>'''+''.join(cards)+'''</main><footer>Original native files · no transcoding or post-editing. The signed R2 links expire seven days after each batch’s delivery; exact dates are listed in downloads.md. Playback depends on native HEVC support.</footer></html>'''
(out/'campaign-films.html').write_text(page)
print('Created local private download index and gallery:',len(cards),'films. Signed links remain excluded from Git.')
