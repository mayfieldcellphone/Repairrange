#!/usr/bin/env python3
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
LI = '<li><a href="/guides/index.html" class="text-white/80 hover:text-amber">Repair Guides</a></li>'
PAT = re.compile(r'(<h3 class="eyebrow text-amber mb-4">Browse</h3>\s*<ul class="space-y-2 text-sm">)', re.I)

p = os.path.join(ROOT, "brands.html")
html = open(p, encoding="utf-8", errors="replace").read()
if "guides/index.html" not in html:
    new_html, n = PAT.subn(lambda m: m.group(1) + "\n" + LI, html, count=1)
    if n:
        open(p, "w", encoding="utf-8").write(new_html)
        print("brands.html linked via regex")
    else:
        print("brands.html: regex no match")
else:
    print("brands.html already linked")
