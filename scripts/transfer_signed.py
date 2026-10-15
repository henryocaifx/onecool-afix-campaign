#!/usr/bin/env python3
"""Transfer using exact-file signed URLs; no Cloudflare/R2 credentials needed.

Tickets are produced by the connected Cloudflare tool in memory and saved only
to records/transfer-private.json, which is excluded from Git and asset packages.
Never print the signed URLs in logs. The final delivery record intentionally
contains user download URLs, while the public record contains object metadata.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request
import urllib.error

ROOT=Path(__file__).resolve().parents[1]
(ROOT/"tmp").mkdir(exist_ok=True)
state=json.loads((ROOT/"records/transfer-private.json").read_text())
completed=[]
for ticket in state["tickets"]:
    path=ROOT/ticket["local_path"]
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    if digest!=ticket["sha256"] or path.stat().st_size!=ticket["bytes"]:
        raise RuntimeError("Local file changed after signing: "+ticket["local_path"])
    # Check an existing same-key object before attempting any upload. PUT also
    # uses an R2 atomic create-only precondition, so races cannot overwrite it.
    head_request=urllib.request.Request(ticket["download_url"],method="HEAD")
    exists=False
    try:
        with urllib.request.urlopen(head_request,timeout=60) as r:
            exists=True
            assert r.headers["X-Content-SHA256"]==digest
    except urllib.error.HTTPError as e:
        if e.code!=404:
            raise RuntimeError(f"Signed HEAD failed ({e.code}) for {ticket['key']}") from None
    if not exists:
        with path.open("rb") as body:
            req=urllib.request.Request(ticket["upload_url"],data=body,method="PUT",headers={"Content-Type":ticket["content_type"],"Content-Length":str(ticket["bytes"])})
            try:
                with urllib.request.urlopen(req,timeout=240) as r:
                    upload=json.load(r)
            except urllib.error.HTTPError as e:
                raise RuntimeError(f"Signed upload failed ({e.code}) for {ticket['key']}") from None
        assert upload["sha256"]==digest and upload["size"]==ticket["bytes"]
    with urllib.request.urlopen(head_request,timeout=60) as r:
        assert int(r.headers["Content-Length"])==ticket["bytes"]
        assert r.headers["Content-Type"].split(";")[0]==ticket["content_type"]
        etag=r.headers.get("ETag")
    downloaded=ROOT/"tmp"/(path.name+".r2-readback")
    h=hashlib.sha256()
    with urllib.request.urlopen(ticket["download_url"],timeout=240) as r, downloaded.open("wb") as dest:
        for chunk in iter(lambda:r.read(1024*1024),b""):
            h.update(chunk); dest.write(chunk)
    assert h.hexdigest()==digest, "R2 readback SHA-256 mismatch"
    decode=None
    if ticket["category"]=="final":
        subprocess.run(["ffmpeg","-v","error","-i",str(downloaded),"-f","null","-"],check=True)
        decode=True
        # Validate HTTP byte ranges for playback/seek support via the same URL.
        range_req=urllib.request.Request(ticket["download_url"],headers={"Range":"bytes=0-1023"})
        with urllib.request.urlopen(range_req,timeout=60) as r:
            assert r.status==206 and r.headers["Content-Range"].startswith("bytes 0-1023/")
            assert r.read()==path.read_bytes()[:1024]
    downloaded.unlink()
    row={k:v for k,v in ticket.items() if k!="upload_url"}
    row.update(bucket=state["bucket"],etag=etag,readback_sha256_matches=True,downloaded_media_full_decode_passed=decode,range_playback_verified=decode,download_expires_at_utc=state["download_expires_at_utc"],status="uploaded_and_verified")
    completed.append(row)
    (ROOT/"records/delivery-private.json").write_text(json.dumps(completed,indent=2)+"\n")
    public=[{k:v for k,v in row.items() if k!="download_url"} for row in completed]
    (ROOT/"records/delivery.json").write_text(json.dumps(public,indent=2)+"\n")
    print(ticket["category"],ticket["key"],"uploaded and readback verified",flush=True)
print("All signed transfers verified.")
