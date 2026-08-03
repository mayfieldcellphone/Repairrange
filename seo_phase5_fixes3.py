#!/usr/bin/env python3
"""Final stragglers: wrap google_tag.html in noindex HTML; drop empty city.html template from sitemap."""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

# 1. google_tag.html — wrap in proper HTML with noindex
gt = os.path.join(ROOT, "google_tag.html")
raw = open(gt, encoding="utf-8", errors="replace").read()
if "<html" not in raw:
    wrapped = (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '    <meta charset="UTF-8">\n'
        '    <meta name="robots" content="noindex, nofollow">\n'
        "    <title>Tag | RepairRange</title>\n"
        "</head>\n"
        "<body>\n"
        + raw +
        "</body>\n"
        "</html>\n"
    )
    open(gt, "w", encoding="utf-8").write(wrapped)
    print("google_tag.html: wrapped in noindex HTML skeleton")
else:
    print("google_tag.html: already has html skeleton")

# 2. remove empty city.html template from sitemap
sm_path = os.path.join(ROOT, "sitemap.xml")
sm = open(sm_path, encoding="utf-8").read()
url = "https://repairrange.io/locations/city.html"
pat = re.compile(r"(?s)<url>\s*<loc>" + re.escape(url) + r"</loc>.*?</url>\s*")
new_sm, n = pat.subn("", sm, count=1)
if n:
    open(sm_path, "w", encoding="utf-8").write(new_sm)
    print("sitemap: removed locations/city.html")
else:
    print("city.html not found in sitemap (already clean)")
