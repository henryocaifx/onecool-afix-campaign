#!/usr/bin/env python3
"""Upload verified finals to an existing R2 bucket with byte-for-byte readback.

Required secure environment: R2_ENDPOINT_URL, R2_ACCESS_KEY_ID,
R2_SECRET_ACCESS_KEY. Optional R2_SESSION_TOKEN and R2_PUBLIC_BASE_URL.
Install boto3 separately. Never provide credential values as CLI arguments.
Download URLs are retained only in the ignored private delivery record.
"""
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from urllib.parse import quote

ROOT=Path(__file__).resolve().parents[1]
(ROOT/"tmp").mkdir(exist_ok=True)
required=["R2_ENDPOINT_URL","R2_ACCESS_KEY_ID","R2_SECRET_ACCESS_KEY"]
missing=[k for k in required if not os.environ.get(k)]
if missing:
    raise SystemExit("R2 delivery blocked: configure secure environment variables "+", ".join(missing)+"; do not paste secrets into chat or commit them.")
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
s3=boto3.client("s3",endpoint_url=os.environ["R2_ENDPOINT_URL"],aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],aws_session_token=os.environ.get("R2_SESSION_TOKEN"),region_name="auto",config=Config(signature_version="s3v4",retries={"max_attempts":1}))
campaign=json.loads((ROOT/"records/campaign.json").read_text())
bucket=campaign["bucket"]; prefix=campaign["r2_prefix"]
s3.head_bucket(Bucket=bucket)  # Missing/wrong account is a blocker, not permission to change settings.
verification={x["film_id"]:x for x in json.loads((ROOT/"records/technical-verification.json").read_text())}
now=datetime.now(timezone.utc)
ttl=int(os.environ.get("R2_DOWNLOAD_TTL_SECONDS","604800"))
ttl=max(60,min(ttl,604800))
public=[]; private=[]
for film in json.loads((ROOT/"records/films.json").read_text()):
    fid=film["id"]; path=ROOT/"films"/(fid+".mp4")
    if verification[fid]["status"]!="passed":
        raise RuntimeError(fid+" has not passed technical verification")
    key=prefix+path.name
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    try:
        existing=s3.head_object(Bucket=bucket,Key=key)
    except ClientError as e:
        if e.response["Error"]["Code"] not in ["404","NoSuchKey","NotFound"]:
            raise
        existing=None
    if existing:
        if existing.get("Metadata",{}).get("sha256")!=digest:
            raise RuntimeError("Refusing to overwrite an existing different object: "+key)
    else:
        with path.open("rb") as f:
            s3.put_object(Bucket=bucket,Key=key,Body=f,ContentType="video/mp4",Metadata={"sha256":digest},IfNoneMatch="*")
    head=s3.head_object(Bucket=bucket,Key=key)
    assert head["ContentLength"]==path.stat().st_size
    assert head["ContentType"]=="video/mp4"
    obj=s3.get_object(Bucket=bucket,Key=key)
    h=hashlib.sha256()
    with tempfile.NamedTemporaryFile(suffix=".mp4",dir=ROOT/"tmp") as tmp:
        for chunk in obj["Body"].iter_chunks(1024*1024):
            h.update(chunk); tmp.write(chunk)
        tmp.flush(); assert h.hexdigest()==digest
        subprocess.run(["ffmpeg","-v","error","-i",tmp.name,"-f","null","-"],check=True)
    row={"film_id":fid,"bucket":bucket,"object_key":key,"bytes":path.stat().st_size,"content_type":head["ContentType"],"sha256":digest,"etag":head["ETag"],"readback_sha256_matches":True,"downloaded_media_full_decode_passed":True}
    public.append(row)
    base=os.environ.get("R2_PUBLIC_BASE_URL")
    url=base.rstrip("/")+"/"+quote(key,safe="/") if base else s3.generate_presigned_url("get_object",Params={"Bucket":bucket,"Key":key,"ResponseContentType":"video/mp4"},ExpiresIn=ttl)
    private.append({**row,"download_url":url,"expires_at_utc":None if base else (now+timedelta(seconds=ttl)).isoformat(),"expiration_note":"Temporary session credentials can expire earlier than the URL's requested TTL" if os.environ.get("R2_SESSION_TOKEN") else None})
    print(fid,"uploaded and verified",key,flush=True)
(ROOT/"records/delivery.json").write_text(json.dumps(public,indent=2)+"\n")
(ROOT/"records/delivery-private.json").write_text(json.dumps(private,indent=2)+"\n")
