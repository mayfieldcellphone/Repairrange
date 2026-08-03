#!/usr/bin/env python3
"""SEO Phase 1: Add noindex,noindex to AI-curated news posts + fix canonical bugs.
Safe: only inserts a robots meta tag into <head>; never deletes content.
"""
import os, re, glob

BLOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blog")

def is_news_post(html: str) -> bool:
    return "RepairRange News" in html

def add_noindex(path: str) -> bool:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()
    if "noindex" in html:
        return False  # already handled
    m = re.search(r"<head[^>]*>", html, re.I)
    if not m:
        return False
    tag = '<meta name="robots" content="noindex, nofollow">'
    html = html[:m.end()] + "\n    " + tag + html[m.end():]
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return True

changed = 0
already = 0
skipped = 0
for path in sorted(glob.glob(os.path.join(BLOG_DIR, "*.html"))):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()
    if not is_news_post(html):
        # still fix canonical bugs in quality posts
        if "{{SLUG}}" in html:
            fixed = html.replace(
                'https://repairrange.io/blog/{{SLUG}}.html',
                f'https://repairrange.io/blog/{os.path.basename(path)}')
            with open(path, "w", encoding="utf-8") as f:
                f.write(fixed)
            print(f"FIXED canonical bug: {os.path.basename(path)}")
            changed += 1
        continue
    if "noindex" in html:
        already += 1
        continue
    if add_noindex(path):
        changed += 1
    else:
        skipped += 1

print(f"DONE: noindex added={changed}, already={already}, skipped={skipped}")
