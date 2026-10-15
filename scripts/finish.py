#!/usr/bin/env python3
"""Clean, text-free 30-second exports reflecting the user's final direction."""
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
    out = ROOT / "films" / (fid + ".mp4")
    render_out = ROOT / "films" / (fid + ".rendering.mp4")
    meta = probe(source)
    video = next(s for s in meta["streams"] if s["codec_type"] == "video")
    audio = next((s for s in meta["streams"] if s["codec_type"] == "audio"), None)
    if not audio:
        raise RuntimeError(fid + ": generated audio absent; soundtrack needs repair before release")
    args = ["ffmpeg", "-hide_banner", "-y", "-loglevel", "warning", "-threads", "4", "-i", str(source)]
    # Use all 27 seconds of narrative at 90% speed to fill 30 seconds. Keep
    # source pixels and character motion intact; no generated in-between frames.
    graph = [
        "[0:v]trim=duration=27,setpts=(PTS-STARTPTS)/0.9,fps=24,scale=2520:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=2520:1080,setsar=1,format=yuv420p,tpad=stop_mode=clone:stop_duration=0.15,trim=duration=30[v]",
        "[0:a]atrim=duration=27,asetpts=PTS-STARTPTS,atempo=0.9,aresample=48000,aformat=channel_layouts=stereo,apad,atrim=duration=30,afade=t=in:st=0:d=0.02,afade=t=out:st=29.8:d=0.2,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,atrim=duration=30[a]",
    ]
    args += ["-filter_complex_threads", "2", "-filter_complex", ";".join(graph), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-threads", "2", "-pix_fmt", "yuv420p", "-r", "24", "-frames:v", "720", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", "-t", "30", "-movflags", "+faststart", "-metadata", "title="+film["title"]+" | AIFX Studio", "-metadata", "comment=Original Seedance 2.5 campaign film; clean master without added text, titles, subtitles or graphics", str(render_out)]
    (ROOT/"records"/(fid+"-edit-command.json")).write_text(json.dumps(args,indent=2)+"\n")
    print(fid, "rendering", flush=True)
    subprocess.run(args, check=True)
    render_out.replace(out)
    result = {"source_probe": meta, "final_probe": probe(out), "version":"clean-text-free", "source_processing": "First 27 seconds retimed to 30 seconds at 90% speed with pitch-preserving audio tempo adjustment; Lanczos scale to cover 2520x1080, minimal centered crop, SAR 1:1; stereo source channels preserved; loudness normalization. No added text, titles, subtitles, UI, boxes, logos or end cards.", "final_sha256": hashlib.sha256(out.read_bytes()).hexdigest(), "final_bytes": out.stat().st_size}
    (ROOT/"records"/(fid+"-technical.json")).write_text(json.dumps(result,indent=2)+"\n")
    print(fid, "finished", out.stat().st_size, flush=True)


if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("--film"); a=p.parse_args()
    for film in json.loads((ROOT/"records/films.json").read_text()):
        if not a.film or a.film == film["id"]:
            finish(film)
