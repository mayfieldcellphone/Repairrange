#!/usr/bin/env python3
"""Phase 5b fixes from full review:
1. google_tag.html noindex (lost in phase 1)
2. remove 2 noindexed news URLs from sitemap
3. noindex 3 pdfrange-canonical posts + remove from sitemap
4. add self-referencing canonical to all indexed pages missing one
"""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))

# 1. google_tag noindex
gt = os.path.join(ROOT, "google_tag.html")
html = open(gt, encoding="utf-8", errors="replace").read()
if "noindex" not in html:
    html = html.replace("<head>", '<head>\n    <meta name="robots" content="noindex, nofollow">', 1)
    open(gt, "w", encoding="utf-8").write(html)
    print("google_tag.html: noindex added")

# 2+3. pdfrange posts -> noindex; sitemap cleanup
PDFRANGE = [
    "blog/browser-side-vs-server-side-pdf-tools.html",
    "blog/how-to-redact-a-pdf-properly.html",
    "blog/stop-uploading-legal-contracts-to-random-websites.html",
]
for rel in PDFRANGE:
    p = os.path.join(ROOT, rel.replace("/", os.sep))
    html = open(p, encoding="utf-8", errors="replace").read()
    if "noindex" not in html:
        html = html.replace("<head>", '<head>\n    <meta name="robots" content="noindex, nofollow">', 1)
        open(p, "w", encoding="utf-8").write(html)
        print(f"noindex added: {rel}")

# sitemap: remove news + pdfrange URLs
sm_path = os.path.join(ROOT, "sitemap.xml")
sm = open(sm_path, encoding="utf-8").read()
removed = 0
for rel in [
    "news/apple-ai-siri-ios27-australia-waitlist.html",
    "news/samsung-galaxy-z-flip8-charging-frustration-australia.html",
] + PDFRANGE:
    url = "https://repairrange.io/" + rel.replace("\\", "/")
    pat = re.compile(r"(?s)<url>\s*<loc>" + re.escape(url) + r"</loc>.*?</url>\s*")
    new_sm, n = pat.subn("", sm, count=1)
    if n:
        sm = new_sm
        removed += 1
open(sm_path, "w", encoding="utf-8").write(sm)
print(f"sitemap: removed {removed} URLs (news + pdfrange)")

# 4. canonicals on indexed pages missing one
def derive_canonical(rel_path):
    rel = rel_path.replace("\\", "/").lstrip("/")
    if rel == "index.html":
        return "https://repairrange.io/"
    return f"https://repairrange.io/{rel}"

added = 0
for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    rel = os.path.relpath(f, ROOT)
    if ".git" in rel or "blog-bot" in rel:
        continue
    html = open(f, encoding="utf-8", errors="replace").read()
    if "noindex" in html or 'rel="canonical"' in html:
        continue
    # skip files that canonical to another domain (should be noindexed now)
    canon = derive_canonical(rel)
    if "<head>" in html:
        html = html.replace("<head>", f'<head>\n    <link rel="canonical" href="{canon}">', 1)
        open(f, "w", encoding="utf-8").write(html)
        added += 1
print(f"canonicals added: {added}")
print("DONE 5b")
