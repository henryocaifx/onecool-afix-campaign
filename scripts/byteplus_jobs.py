#!/usr/bin/env python3
"""Submit once, resume polling, download promptly. Credentials stay in memory.

Install byteplus-python-sdk-v2 in the active Python environment. Use the session's
VOLC_ACCESS_KEY, VOLC_SECRET_KEY_RAW, VOLC_ENDPOINT_SEEDANCE_25 variables. TLS and
the inherited network proxy remain enabled. No API request is retried here.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://ark.ap-southeast.bytepluses.com/api/v3"


def save(path, value):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    tmp.replace(path)


def token():
    import byteplussdkark
    import byteplussdkcore
    c = byteplussdkcore.Configuration()
    c.ak = os.environ["VOLC_ACCESS_KEY"]
    c.sk = os.environ["VOLC_SECRET_KEY_RAW"]
    c.region = "ap-southeast-1"
    c.scheme = "https"
    c.ssl_ca_cert = os.environ.get("SSL_CERT_FILE")
    c.debug = False
    byteplussdkcore.Configuration.set_default(c)
    response = byteplussdkark.ARKApi().get_api_key(
        byteplussdkark.GetApiKeyRequest(
            duration_seconds=3600,
            resource_type="endpoint",
            resource_ids=[os.environ["VOLC_ENDPOINT_SEEDANCE_25"]],
        )
    )
    return response.api_key


def request(auth, path, body=None):
    headers = {"Authorization": "Bearer " + auth}
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        BASE + path,
        data=None if body is None else json.dumps(body).encode(),
        headers=headers,
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        # Provider JSON can contain request details; redact credentials defensively.
        message = e.read().decode(errors="replace")
        for secret in [auth, os.environ.get("VOLC_ACCESS_KEY"), os.environ.get("VOLC_SECRET_KEY_RAW")]:
            if secret:
                message = message.replace(secret, "[REDACTED]")
        raise RuntimeError(f"HTTP {e.code}: {message[:4000]}") from None


def submit(film, auth):
    ledger = ROOT / "records" / (film["id"] + "-job.json")
    if ledger.exists():
        old = json.loads(ledger.read_text())
        print(film["id"], "reuse", old.get("job_id", old["status"]), flush=True)
        return
    ref = ROOT / film["reference"]
    raw = ref.read_bytes()
    record = {
        "film_id": film["id"],
        "status": "submission_in_progress",
        "submitted_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "endpoint_id": os.environ["VOLC_ENDPOINT_SEEDANCE_25"],
        "foundation_model": "dreamina-seedance-2-5-260628",
        "prompt": film["prompt"],
        "reference": {"path": film["reference"], "sha256": hashlib.sha256(raw).hexdigest(), "transport": "base64 data URL", "role": "reference_image"},
        "settings": {"duration": 27, "resolution": "1080p", "ratio": "21:9", "generate_audio": True, "watermark": False, "output_format": "mp4", "seed": film["seed"]},
    }
    save(ledger, record)  # An uncertain submission is never automatically repeated.
    body = {"model": record["endpoint_id"], "content": [
        {"type": "text", "text": film["prompt"]},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(raw).decode()}, "role": "reference_image"},
    ], **record["settings"]}
    try:
        r = request(auth, "/contents/generations/tasks", body)
        if not r.get("id"):
            raise RuntimeError("Provider response lacks a job ID")
        record.update(status="submitted", job_id=r["id"])
    except Exception as e:
        record.update(status="submission_error_or_uncertain", error=str(e))
        save(ledger, record)
        raise
    save(ledger, record)
    print(film["id"], "submitted", record["job_id"], flush=True)


def poll(film, auth):
    ledger = ROOT / "records" / (film["id"] + "-job.json")
    if not ledger.exists():
        return
    record = json.loads(ledger.read_text())
    if "job_id" not in record:
        print(film["id"], record["status"], flush=True)
        return
    r = request(auth, "/contents/generations/tasks/" + record["job_id"])
    # Signed source links stay only in a private ignored file, never in commits.
    content = r.get("content") or {}
    video_url = content.get("video_url")
    public = {k: v for k, v in r.items() if k != "content"}
    public["content"] = {k: "[temporary provider URL omitted]" if k.endswith("url") else v for k, v in content.items()}
    record.update(status=r.get("status"), result=public)
    usage = r.get("usage") or {}
    if usage.get("completion_tokens") is not None:
        record["cost"] = {"actual_invoice_usd": None, "list_price_usd_per_million_tokens": 11.7, "estimated_list_price_usd": round(usage["completion_tokens"] * 11.7 / 1000000, 6), "basis": "Published 1080p rate without input video; account discounts/credits unknown"}
    if video_url:
        path = ROOT / "sources" / (film["id"] + ".mp4")
        if not path.exists():
            tmp = path.with_suffix(".mp4.part")
            with urllib.request.urlopen(video_url, timeout=180) as source, tmp.open("wb") as dest:
                while chunk := source.read(1024 * 1024):
                    dest.write(chunk)
            tmp.replace(path)
        record["source"] = {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    save(ledger, record)
    print(film["id"], record["status"], record.get("source", {}).get("bytes", ""), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=["submit", "poll"])
    parser.add_argument("--film", help="Optional film ID; otherwise process all four")
    args = parser.parse_args()
    films = json.loads((ROOT / "records" / "films.json").read_text())
    auth = token()
    for film in films:
        if args.film and film["id"] != args.film:
            continue
        try:
            (submit if args.operation == "submit" else poll)(film, auth)
        except Exception as e:
            print(film["id"], type(e).__name__, str(e)[:4000], flush=True)
            # Stop on any submission error; inspect before continuing.
            if args.operation == "submit":
                raise SystemExit(1)
