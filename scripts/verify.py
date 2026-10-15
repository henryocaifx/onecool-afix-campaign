#!/usr/bin/env python3
"""Probe, fully decode, and measure each completed campaign film."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
results = []
for film in json.loads((ROOT/"records/films.json").read_text()):
    fid = film["id"]
    path = ROOT/"films"/(fid+".mp4")
    if not path.exists():
        results.append({"film_id":fid,"status":"missing"})
        continue
    data=json.loads(subprocess.check_output(["ffprobe","-v","error","-count_frames","-show_streams","-show_format","-of","json",str(path)]))
    v=next(x for x in data["streams"] if x["codec_type"]=="video")
    a=next(x for x in data["streams"] if x["codec_type"]=="audio")
    # This decodes both streams completely while analyzing loudness and peaks.
    run=subprocess.run(["ffmpeg","-hide_banner","-v","info","-i",str(path),"-map","0:v:0","-map","0:a:0","-af","loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json","-f","null","-"],capture_output=True,text=True)
    log=run.stderr
    m=re.search(r'\{\s*"input_i".*?\}',log,re.S)
    loudness=json.loads(m.group()) if m else None
    errors=[line for line in log.splitlines() if any(k in line.lower() for k in ["error while", "invalid data", "corrupt decoded", "failed to", "non monotonically"])]
    checks={
        "container_duration_30":abs(float(data["format"]["duration"])-30)<.001,
        "video_duration_30":abs(float(v["duration"])-30)<.001,
        "dimensions_2520x1080":(v["width"],v["height"])==(2520,1080),
        "square_pixels":v.get("sample_aspect_ratio")=="1:1",
        "aspect_21_9":v["width"]*3==v["height"]*7,
        "fps_24":v.get("r_frame_rate")=="24/1" and v.get("avg_frame_rate")=="24/1",
        "frames_720":int(v.get("nb_read_frames",0))==720,
        "h264_yuv420p":v.get("codec_name")=="h264" and v.get("pix_fmt")=="yuv420p",
        "aac_stereo_48k":a.get("codec_name")=="aac" and a.get("channels")==2 and a.get("sample_rate")=="48000",
        "audio_duration_30":abs(float(a["duration"])-30)<.025,
        "full_decode":run.returncode==0 and not errors,
        "audio_below_clipping":bool(loudness and float(loudness["input_tp"])<0),
        "integrated_loudness_near_target":bool(loudness and -18<=float(loudness["input_i"])<=-14),
    }
    result={"film_id":fid,"status":"passed" if all(checks.values()) else "needs_attention","checks":checks,"loudness":loudness,"decode_errors":errors,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"bytes":path.stat().st_size,"probe":data}
    (ROOT/"records"/(fid+"-verification.json")).write_text(json.dumps(result,indent=2)+"\n")
    results.append({k:v for k,v in result.items() if k!="probe"})
    print(fid,result["status"],{k:v for k,v in checks.items() if not v},flush=True)
(ROOT/"records/technical-verification.json").write_text(json.dumps(results,indent=2)+"\n")
if any(x["status"]!="passed" for x in results):
    raise SystemExit(1)
