#!/usr/bin/env python3
"""Capture the real public AIFX site without inventing authenticated workflows."""
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/chromium",headless=True,args=["--no-sandbox"],proxy={"server":os.environ["HTTPS_PROXY"]})
    page=b.new_page(viewport={"width":1920,"height":1080},device_scale_factor=1)
    # Chromium doesn't use the injected CA store here. API transport trusts
    # NODE_EXTRA_CA_CERTS and performs verified requests through the same proxy.
    page.route("**/*",lambda route: route.fulfill(response=route.fetch(timeout=20000)))
    routes=[]
    for name,path in [("home","/"),("cast","/cast"),("cine","/cine"),("movi2","/movi2")]:
        page.goto("https://charsiufan.onecool.ai"+path,wait_until="domcontentloaded",timeout=45000)
        page.wait_for_timeout(6000)
        page.screenshot(path=str(ROOT/"assets/captures"/(name+".png")))
        (ROOT/"assets/captures"/(name+".txt")).write_text(page.locator("body").inner_text())
        routes.append({"requested":path,"final_url":page.url,"title":page.title(),"requires_signin":"/auth/signin" in page.url})
    (ROOT/"research/capture-routes.json").write_text(json.dumps(routes,indent=2)+"\n")
    b.close()
