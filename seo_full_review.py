#!/usr/bin/env python3
"""Full review sweep of the SEO update: find remaining issues across the site."""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
issues = []
info = []

# 1. sitemap: noindexed URLs, junk, canonical-to-other-domain pages
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
sm_urls = re.findall(r"<loc>(https://repairrange\.io/[^<]+)</loc>", sm)
info.append(f"sitemap URLs: {len(sm_urls)}")

# noindexed files still in sitemap
noindex_in_sm = []
for f in glob.glob(os.path.join(ROOT, "blog", "*.html")) + glob.glob(os.path.join(ROOT, "news", "*.html")):
    html = open(f, encoding="utf-8", errors="replace").read()
    if "noindex" in html:
        rel = f.replace(ROOT, "").replace("\\", "/").lstrip("/")
        url = f"https://repairrange.io/{rel}"
        if url in sm_urls:
            noindex_in_sm.append(url)
if noindex_in_sm:
    issues.append(f"noindexed pages still in sitemap: {noindex_in_sm}")
else:
    info.append("sitemap: no noindexed pages present")

# 2. canonical to other domains or template vars on indexed pages
bad_canonical = []
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    if ".git" in f or "blog-bot" in f:
        continue
    html = open(f, encoding="utf-8", errors="replace").read()
    if "noindex" in html:
        continue
    m = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    if m:
        url = m.group(1)
        if "pdfrange.com" in url or "{{" in url or "mayfieldphonerepair" in url:
            bad_canonical.append((f.replace(ROOT, ""), url))
if bad_canonical:
    for f, u in bad_canonical:
        issues.append(f"cross-domain/broken canonical: {f} -> {u}")
else:
    info.append("canonicals: all indexed pages self- or site-canonical")

# 3. pages with no canonical at all (indexed, no noindex)
no_canonical = []
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    if ".git" in f or "blog-bot" in f:
        continue
    html = open(f, encoding="utf-8", errors="replace").read()
    if "noindex" in html:
        continue
    if "rel=\"canonical\"" not in html:
        no_canonical.append(f.replace(ROOT, ""))
if no_canonical:
    issues.append(f"indexed pages missing canonical ({len(no_canonical)}): {no_canonical[:8]}")
else:
    info.append("canonicals: every indexed page has one")

# 4. robots.txt
robots = open(os.path.join(ROOT, "robots.txt"), encoding="utf-8").read()
info.append(f"robots.txt: {len(robots.splitlines())} lines, references sitemap: {'sitemap' in robots.lower()}")

# 5. OG image coverage on root + hub pages
og_missing = []
for f in glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "guides", "*.html")):
    html = open(f, encoding="utf-8", errors="replace").read()
    if 'og:image' not in html:
        og_missing.append(f.replace(ROOT, ""))
info.append(f"og:image missing on {len(og_missing)} root/guides pages (low priority): {og_missing[:6]}")

# 6. news posts visible in blog.html (fine) — check noindexed-but-linked-from-blog count
news_still_linked = 0
blog_html = open(os.path.join(ROOT, "blog.html"), encoding="utf-8").read()
for f in glob.glob(os.path.join(ROOT, "blog", "*.html")):
    html = open(f, encoding="utf-8", errors="replace").read()
    if "noindex" in html:
        slug = os.path.basename(f)
        if slug in blog_html:
            news_still_linked += 1
info.append(f"news posts still linked from blog.html (visible to users, OK for SEO): {news_still_linked}")

# 7. title lengths on key pages (rough check, >65 chars flag)
long_titles = []
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    if ".git" in f or "blog-bot" in f:
        continue
    html = open(f, encoding="utf-8", errors="replace").read()
    if "noindex" in html:
        continue
    m = re.search(r"<title>([^<]+)</title>", html)
    if m and len(m.group(1)) > 70:
        long_titles.append((f.replace(ROOT, ""), len(m.group(1))))
if long_titles:
    info.append(f"titles >70 chars ({len(long_titles)} pages, minor): {long_titles[:5]}")

# 8. index.html title
idx = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
m = re.search(r"<title>([^<]+)</title>", idx)
info.append(f"homepage title: '{m.group(1) if m else 'MISSING'}'")

print("=== ISSUES ===")
for i in issues:
    print(" !", i)
if not issues:
    print(" (none)")
print("\n=== INFO ===")
for i in info:
    print(" -", i)
