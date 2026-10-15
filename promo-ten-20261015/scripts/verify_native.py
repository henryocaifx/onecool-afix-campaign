#!/usr/bin/env python3
"""Read-only verification and frame extraction; never alter a provider MP4."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
(ROOT/"review").mkdir(exist_ok=True)
(ROOT/"posters").mkdir(exist_ok=True)
rows=[]
for film in json.loads((ROOT/"records/films.json").read_text()):
    fid=film["id"]; path=ROOT/"sources"/(fid+".mp4")
    job_path=ROOT/"records"/(fid+"-job.json")
    if not path.exists() or not job_path.exists():
        continue
    job=json.loads(job_path.read_text()); digest=hashlib.sha256(path.read_bytes()).hexdigest()
    cached=ROOT/"records"/(fid+"-native-verification.json")
    if cached.exists():
        old=json.loads(cached.read_text())
        if old.get("sha256")==digest and old.get("status")=="passed":
            rows.append(old);print(fid,"verified unchanged native file",flush=True);continue
    probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-count_frames","-show_format","-show_streams","-of","json",str(path)]))
    video=next(s for s in probe["streams"] if s["codec_type"]=="video")
    audio=next(s for s in probe["streams"] if s["codec_type"]=="audio")
    run=subprocess.run(["ffmpeg","-hide_banner","-v","info","-i",str(path),"-map","0:v:0","-map","0:a:0","-af","loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json","-f","null","-"],capture_output=True,text=True)
    m=re.search(r'\{\s*"input_i".*?\}',run.stderr,re.S); loudness=json.loads(m.group()) if m else None
    checks={"unchanged_provider_sha256":digest==job.get("source",{}).get("sha256"),"requested_native_30_seconds":job["settings"]["duration"]==30,"native_duration_near_30":29.5<=float(video["duration"])<=30.5,"native_1080p_ultrawide":(video["width"],video["height"])==(2206,946),"native_24_fps":video.get("r_frame_rate")=="24/1","soundtrack_present":audio.get("channels",0)>=1,"no_subtitle_track":not any(s["codec_type"]=="subtitle" for s in probe["streams"]),"full_video_audio_decode":run.returncode==0,"r2_single_request_size":path.stat().st_size<99*1024*1024}
    result={"film_id":fid,"status":"passed" if all(checks.values()) else "needs_attention","checks":checks,"sha256":digest,"bytes":path.stat().st_size,"no_transcode_or_post_edit":True,"native_video_codec":video["codec_name"],"native_pixel_format":video.get("pix_fmt"),"native_video_duration":video["duration"],"native_container_duration":probe["format"]["duration"],"native_audio_duration":audio.get("duration"),"native_dimensions":[video["width"],video["height"]],"native_fps":video["r_frame_rate"],"native_frames":video.get("nb_read_frames"),"native_audio_codec":audio["codec_name"],"native_audio_channels":audio.get("channels"),"loudness_analysis_only":loudness,"probe":probe}
    cached.write_text(json.dumps(result,indent=2)+"\n");rows.append(result)
    def frame(args):subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",*args],check=True)
    frame(["-i",str(path),"-vf","fps=1,scale=630:-1,tile=3x11:padding=5:margin=5:color=black","-frames:v","1",str(ROOT/"review"/(fid+"-sheet.png"))])
    for sec in [1,4,10,16,23,28]:frame(["-ss",str(sec),"-i",str(path),"-frames:v","1",str(ROOT/"review"/f"{fid}-{sec:02}.png")])
    frame(["-ss","23.5","-i",str(path),"-frames:v","1",str(ROOT/"posters"/(fid+".png"))])
    assert hashlib.sha256(path.read_bytes()).hexdigest()==digest
    print(fid,result["status"],video["codec_name"],video["duration"],flush=True)
(ROOT/"records/native-verification.json").write_text(json.dumps(rows,indent=2)+"\n")
