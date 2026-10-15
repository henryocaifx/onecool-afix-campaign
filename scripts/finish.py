#!/usr/bin/env python3
"""Reproducible FFmpeg finishing for the four accepted original source films."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def probe(path):
    return json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)]))


def finish(film):
    fid = film["id"]
    source = ROOT / "sources" / (fid + ".mp4")
    if not source.exists():
        print(fid, "source not downloaded; skipping", flush=True)
        return
    graphics = ROOT / "assets" / "graphics"
    out = ROOT / "films" / (fid + ".mp4")
    meta = probe(source)
    video = next(s for s in meta["streams"] if s["codec_type"] == "video")
    audio = next((s for s in meta["streams"] if s["codec_type"] == "audio"), None)
    if not audio:
        raise RuntimeError(fid + ": generated audio absent; soundtrack needs repair before release")
    args = ["ffmpeg", "-hide_banner", "-y", "-loglevel", "warning", "-threads", "4", "-i", str(source)]
    images = [graphics/(fid+"-bug.png"), graphics/(fid+"-product.png"), ROOT/"assets/captures/home.png", graphics/(fid+"-end.png")]
    for path in images:
        args += ["-loop", "1", "-framerate", "24", "-i", str(path)]
    args += ["-i", str(graphics/(fid+"-signature.wav"))]
    trailer = film["format"] == "movie trailer"
    if trailer:
        args += ["-loop", "1", "-framerate", "24", "-i", str(graphics/(fid+"-title.png"))]
    graph = [
        "[0:v]setpts=PTS-STARTPTS,fps=24,scale=2520:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=2520:1080,setsar=1,format=yuv420p,tpad=stop_mode=clone:stop_duration=4,trim=duration=30[v0]",
        "[1:v]format=rgba,fade=t=in:st=3:d=0.15:alpha=1,fade=t=out:st=5.3:d=0.2:alpha=1[bug]",
        "[v0][bug]overlay=0:0:enable='between(t,3,5.5)'[v1]",
        "[2:v]format=rgba,fade=t=in:st=24.25:d=0.2:alpha=1[product]",
        "[v1][product]overlay=0:0:enable='gte(t,24.25)*lt(t,27)'[v2]",
        "[3:v]crop=1920:650:0:0,scale=640:217:flags=lanczos,format=rgba,fade=t=in:st=24.25:d=0.2:alpha=1[ui]",
        "[v2][ui]overlay=132:750:enable='gte(t,24.25)*lt(t,27)'[v3]",
    ]
    if trailer:
        graph += ["[6:v]format=rgba,fade=t=in:st=23.15:d=0.2:alpha=1,fade=t=out:st=25.4:d=0.25:alpha=1[title]", "[v3][title]overlay=0:0:enable='gte(t,23.15)*lt(t,25.65)'[v4]"]
    else:
        graph += ["[v3]null[v4]"]
    graph += [
        "[v4][4:v]overlay=0:0:enable='gte(t,27)',trim=duration=30,fps=24[v]",
        "[0:a]asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,afade=t=out:st=26.35:d=0.65,apad,atrim=duration=30[original]",
        "[5:a]adelay=26700|26700,apad,atrim=duration=30[signature]",
        "[original][signature]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,atrim=duration=30[a]",
    ]
    args += ["-filter_complex_threads", "2", "-filter_complex", ";".join(graph), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "24", "-frames:v", "720", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", "-t", "30", "-movflags", "+faststart", "-metadata", "title="+film["title"]+" | AIFX Studio", "-metadata", "comment=Original Seedance 2.5 campaign film; authentic public AIFX Studio capture composited in edit", str(out)]
    (ROOT/"records"/(fid+"-edit-command.json")).write_text(json.dumps(args,indent=2)+"\n")
    print(fid, "rendering", flush=True)
    subprocess.run(args, check=True)
    result = {"source_probe": meta, "final_probe": probe(out), "source_processing": "Lanczos scale to cover 2520x1080, minimal centered crop, SAR 1:1; source audio channels preserved when stereo or promoted when mono, plus original stereo sonic motif; loudness normalization", "final_sha256": hashlib.sha256(out.read_bytes()).hexdigest(), "final_bytes": out.stat().st_size}
    (ROOT/"records"/(fid+"-technical.json")).write_text(json.dumps(result,indent=2)+"\n")
    print(fid, "finished", out.stat().st_size, flush=True)


if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("--film"); a=p.parse_args()
    for film in json.loads((ROOT/"records/films.json").read_text()):
        if not a.film or a.film == film["id"]:
            finish(film)
