#!/usr/bin/env python3
"""Package production assets and enumerate exact-file R2 transfer candidates."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
campaign=json.loads((ROOT/"records/campaign.json").read_text())
prefix=campaign["r2_prefix"]
films=json.loads((ROOT/"records/films.json").read_text())
bundle=ROOT/"aifx-studio-production-assets.zip"
with zipfile.ZipFile(bundle,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for folder in ["docs","scripts","records","assets/references","assets/captures","posters","research"]:
        for path in sorted((ROOT/folder).rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts or "private" in path.name or path.suffix in [".pyc",".tmp"] or "delivery" in path.name:
                continue
            z.write(path,path.relative_to(ROOT))
    for name in ["README.md","requirements.txt"]:
        z.write(ROOT/name,name)
files=[]
def add(path,category,key=None):
    p=ROOT/path
    size=p.stat().st_size
    if size>99*1024*1024:
        raise RuntimeError("File exceeds this delivery bridge's per-request limit: "+path)
    files.append({"local_path":path,"category":category,"key":prefix+(key or path),"bytes":size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"content_type":"video/mp4" if p.suffix==".mp4" else "image/png" if p.suffix==".png" else "application/zip"})
for film in films:
    fid=film["id"]
    technical=json.loads((ROOT/"records"/(fid+"-technical.json")).read_text())
    if technical.get("version")!="clean-text-free":
        raise RuntimeError("Only clean masters may be packaged: "+fid)
    add("films/"+fid+".mp4","final",fid+".mp4")
for film in films:
    add("sources/"+film["id"]+".mp4","source")
for film in films:
    add("posters/"+film["id"]+".png","poster")
for film in films:
    add(film["reference"],"reference")
add(bundle.name,"production_assets",bundle.name)
data={"campaign":campaign,"files":files}
(ROOT/"records/transfer-index.json").write_text(json.dumps(data,indent=2)+"\n")
print(json.dumps(data))
