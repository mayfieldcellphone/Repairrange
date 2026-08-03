#!/usr/bin/env python3
"""Remove noindexed AI-news posts from sitemap.xml and teach generate_sitemap.py to skip them."""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

# 1. find all blog files with noindex
noindex_slugs = set()
blog_dir = os.path.join(ROOT, "blog")
for f in os.listdir(blog_dir):
    if not f.endswith(".html"):
        continue
    with open(os.path.join(blog_dir, f), encoding="utf-8", errors="replace") as fh:
        if "noindex" in fh.read():
            noindex_slugs.add(f)

print(f"noindexed posts found: {len(noindex_slugs)}")

# 2. remove their URL blocks from sitemap.xml
sp = os.path.join(ROOT, "sitemap.xml")
with open(sp, encoding="utf-8") as f:
    sm = f.read()
removed = 0
for slug in noindex_slugs:
    url = f"https://repairrange.io/blog/{slug}"
    pattern = re.compile(r"(?s)<url>\s*<loc>" + re.escape(url) + r"</loc>.*?</url>\s*")
    new_sm, n = pattern.subn("", sm, count=1)
    if n:
        sm = new_sm
        removed += 1
with open(sp, "w", encoding="utf-8") as f:
    f.write(sm)
print(f"sitemap: removed {removed} noindexed URLs")

# 3. teach generate_sitemap.py to skip noindexed files
gen = os.path.join(ROOT, "generate_sitemap.py")
with open(gen, encoding="utf-8") as f:
    src = f.read()
old = """    for file in os.listdir(folder_path):
        if file.endswith(".html"):
            urls.append(f"{BASE_URL}/{folder}/{file}")"""
new = """    for file in os.listdir(folder_path):
        if file.endswith(".html"):
            fp = os.path.join(folder_path, file)
            try:
                with open(fp, encoding="utf-8", errors="replace") as _f:
                    if "noindex" in _f.read():
                        continue
            except Exception:
                pass
            urls.append(f"{BASE_URL}/{folder}/{file}")"""
if old in src:
    src = src.replace(old, new)
    with open(gen, "w", encoding="utf-8") as f:
        f.write(src)
    print("generate_sitemap.py: now skips noindexed files")
else:
    print("generate_sitemap.py: pattern not found")
