#!/usr/bin/env python3
"""Resume existing jobs, save native media promptly, never submit or retry jobs."""
import argparse
import contextlib
import io
import json
from pathlib import Path
import time
import byteplus_jobs as jobs

p=argparse.ArgumentParser()
p.add_argument('--project-root',required=True)
p.add_argument('--max-minutes',type=float,default=30)
p.add_argument('--interval',type=float,default=30)
a=p.parse_args()
jobs.ROOT=Path(a.project_root).resolve()
films=json.loads((jobs.ROOT/'records/films.json').read_text())
auth=jobs.token()
seen={}
deadline=time.monotonic()+a.max_minutes*60
while time.monotonic()<deadline:
    terminal=0; failed=[]
    for f in films:
        ledger=jobs.ROOT/'records'/(f['id']+'-job.json')
        if not ledger.exists():raise RuntimeError('Missing submission ledger: '+f['id'])
        old=json.loads(ledger.read_text())
        source=jobs.ROOT/'sources'/(f['id']+'.mp4')
        if not(old.get('status')=='succeeded' and source.exists()) and old.get('status') not in ['failed','cancelled','expired']:
            try:
                with contextlib.redirect_stdout(io.StringIO()):jobs.poll(f,auth)
            except Exception as e:
                print(f['id'],'poll/download error',type(e).__name__,flush=True)
        r=json.loads(ledger.read_text());state=(r.get('status'),r.get('source',{}).get('bytes'))
        if seen.get(f['id'])!=state:
            print(f['id'],*state,flush=True);seen[f['id']]=state
        if r.get('status')=='succeeded' and source.exists():terminal+=1
        elif r.get('status') in ['failed','cancelled','expired']:
            terminal+=1;failed.append(f['id'])
    if terminal==len(films):
        print('All jobs terminal; failed:',len(failed),flush=True)
        raise SystemExit(1 if failed else 0)
    time.sleep(a.interval)
print('Watch window ended; rerun safely to continue existing jobs.',flush=True)
