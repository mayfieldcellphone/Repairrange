#!/usr/bin/env python3
"""Phase 7: remove the two off-topic Starlink/spacex news posts from blog.html,
noindex them, and drop from sitemap."""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SLUGS = ["spacex-starlink-ipo-investor-guide", "starlink-direct-to-cell-australia-guide"]

# 1. remove cards from blog.html
bh_path = os.path.join(ROOT, "blog.html")
bh = open(bh_path, encoding="utf-8").read()
for slug in SLUGS:
    idx = bh.find(f"blog/{slug}.html")
    if idx < 0:
        print(f"blog.html: {slug} not found")
        continue
    start = bh.rfind("<a ", 0, idx)
    end = bh.find("</a>", idx) + 4
    # also consume trailing whitespace/newlines after the card
    after = end
    while after < len(bh) and bh[after] in " \t\r\n":
        after += 1
    removed = bh[start:after]
    bh = bh[:start] + bh[after:]
    print(f"blog.html: removed card for {slug} ({len(removed)} chars)")
open(bh_path, "w", encoding="utf-8").write(bh)

# 2. noindex the two files
for slug in SLUGS:
    p = os.path.join(ROOT, "blog", slug + ".html")
    html = open(p, encoding="utf-8", errors="replace").read()
    if "noindex" not in html:
        html = html.replace("<head>", '<head>\n    <meta name="robots" content="noindex, nofollow">', 1)
        open(p, "w", encoding="utf-8").write(html)
        print(f"noindex added: {slug}")

# 3. remove from sitemap
sm_path = os.path.join(ROOT, "sitemap.xml")
sm = open(sm_path, encoding="utf-8").read()
for slug in SLUGS:
    url = f"https://repairrange.io/blog/{slug}.html"
    pat = re.compile(r"(?s)<url>\s*<loc>" + re.escape(url) + r"</loc>.*?</url>\s*")
    new_sm, n = pat.subn("", sm, count=1)
    if n:
        sm = new_sm
        print(f"sitemap: removed {slug}")
open(sm_path, "w", encoding="utf-8").write(sm)
print("DONE phase 7")
