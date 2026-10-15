#!/usr/bin/env python3
"""Extract temporal review sheets, full-resolution checkpoints, and posters."""
import argparse
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
(ROOT/"tmp").mkdir(exist_ok=True)
(ROOT/"review").mkdir(exist_ok=True)


def run(args):
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",*args],check=True)


p=argparse.ArgumentParser(); p.add_argument("--final",action="store_true"); p.add_argument("--film"); a=p.parse_args()
for film in json.loads((ROOT/"records/films.json").read_text()):
    fid=film["id"]
    if a.film and a.film!=fid:
        continue
    path=ROOT/("films" if a.final else "sources")/(fid+".mp4")
    if not path.exists():
        continue
    tag="final" if a.final else "source"
    run(["-i",str(path),"-vf","fps=1,scale=630:-1,tile=3x10:padding=5:margin=5:color=black","-frames:v","1",str(ROOT/"review"/(fid+"-"+tag+"-sheet.png"))])
    for sec in ([1,4,10,14,19,22,25,28] if a.final else [1,4,10,14,19,22,25]):
        run(["-ss",str(sec),"-i",str(path),"-frames:v","1",str(ROOT/"review"/f"{fid}-{tag}-{sec:02}.png")])
    if a.final:
        title=ROOT/"tmp"/(fid+"-poster-title.txt"); title.write_text(film["title"])
        filters=f"drawbox=x=0:y=805:w=iw:h=275:color=black@0.65:t=fill,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:textfile='{title}':fontsize=100:fontcolor=white:x=105:y=850,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='AIFX STUDIO  /  ORIGINAL WORLDS':fontsize=27:fontcolor=0xddd6ee:x=110:y=1000"
        run(["-ss","21.5","-i",str(path),"-vf",filters,"-frames:v","1",str(ROOT/"posters"/(fid+".png"))])
    print(fid,tag,"review assets extracted",flush=True)
