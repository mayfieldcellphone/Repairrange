#!/usr/bin/env python3
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
LI = '<li><a href="/guides/index.html" class="text-white/80 hover:text-amber">Repair Guides</a></li>'
MARKER = '<h3 class="eyebrow text-amber mb-4">Browse</h3><ul class="space-y-2 text-sm">'

p = os.path.join(ROOT, "brands.html")
html = open(p, encoding="utf-8", errors="replace").read()
if "guides/index.html" not in html:
    if MARKER in html:
        html = html.replace(MARKER, MARKER + LI, 1)
        open(p, "w", encoding="utf-8").write(html)
        print("brands.html linked")
    else:
        print("brands.html: marker not found")
else:
    print("brands.html already linked")
