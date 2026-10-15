#!/usr/bin/env python3
"""Check each completed native source as it arrives; source bytes never change."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

p=argparse.ArgumentParser();p.add_argument('--project-root',required=True);p.add_argument('--max-minutes',type=float,default=30)
a=p.parse_args();root=Path(a.project_root).resolve()
films=json.loads((root/'records/films.json').read_text())
deadline=time.monotonic()+a.max_minutes*60
while time.monotonic()<deadline:
    need=False;complete=0;terminal=0
    for f in films:
        fid=f['id'];source=root/'sources'/(fid+'.mp4');record=root/'records'/(fid+'-native-verification.json')
        job=json.loads((root/'records'/(fid+'-job.json')).read_text())
        if job.get('status') in ['failed','cancelled','expired']:terminal+=1
        if source.exists():
            if record.exists() and (root/'review'/(fid+'-sheet.png')).exists() and (root/'posters'/(fid+'.png')).exists():complete+=1
            else:need=True
    if need:
        subprocess.run([sys.executable,str(root/'scripts/verify_native.py')],check=True)
        continue
    if complete+terminal==len(films):
        print('Native verification complete:',complete,'provider failures:',terminal,flush=True)
        break
    time.sleep(20)
