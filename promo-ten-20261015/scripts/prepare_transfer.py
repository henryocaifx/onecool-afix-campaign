#!/usr/bin/env python3
"""Index only the unmodified provider MP4s for exact-file R2 delivery."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
campaign=json.loads((ROOT/"records/campaign.json").read_text())
files=[]
for film in json.loads((ROOT/"records/films.json").read_text()):
    fid=film["id"];p=ROOT/"sources"/(fid+".mp4")
    verification=json.loads((ROOT/"records"/(fid+"-native-verification.json")).read_text())
    if verification["status"]!="passed":raise RuntimeError("Native file has not passed: "+fid)
    digest=hashlib.sha256(p.read_bytes()).hexdigest()
    assert digest==verification["sha256"]
    files.append({"local_path":str(p.relative_to(ROOT)),"category":"final","key":campaign["r2_prefix"]+p.name,"bytes":p.stat().st_size,"sha256":digest,"content_type":"video/mp4"})
index={"campaign":campaign,"files":files}
(ROOT/"records/transfer-index.json").write_text(json.dumps(index,indent=2)+"\n")
print(json.dumps({"files":len(files),"bytes":sum(x["bytes"] for x in files),"prefix":campaign["r2_prefix"]}))
