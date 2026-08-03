#!/usr/bin/env python3
"""Phase 5 polish:
1. noindex the 2 existing /news/ posts + make generate_tech_news.py emit noindex by default
2. consolidate near-duplicate why-do-screen-repair-quotes-vary-so-much into why-screen-repair-quotes-differ
3. add author bylines + Article schema to indexed blog posts
"""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------- 1. news/ posts noindex ----------
news_dir = os.path.join(ROOT, "news")
for f in os.listdir(news_dir):
    if not f.endswith(".html"):
        continue
    p = os.path.join(news_dir, f)
    html = open(p, encoding="utf-8", errors="replace").read()
    if "noindex" not in html and "<head>" in html:
        html = html.replace("<head>", '<head>\n    <meta name="robots" content="noindex, nofollow">', 1)
        open(p, "w", encoding="utf-8").write(html)
        print(f"noindex added: news/{f}")

# ---------- 1b. preventive: generate_tech_news.py template ----------
gen = os.path.join(ROOT, "generate_tech_news.py")
src = open(gen, encoding="utf-8").read()
if 'noindex' not in src:
    old = '<meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <link rel="canonical" href="{canonical_url}">'
    new = ('<meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
           '    <meta name="robots" content="noindex, nofollow">\n    <link rel="canonical" href="{canonical_url}">')
    if old in src:
        src = src.replace(old, new, 1)
        open(gen, "w", encoding="utf-8").write(src)
        print("generate_tech_news.py: noindex added to template")
    else:
        # try a looser match
        m = re.search(r'(<meta charset="UTF-8">.*?\n)(\s*<link rel="canonical")', src, re.S)
        if m:
            src = src.replace(m.group(2), '\n    <meta name="robots" content="noindex, nofollow">' + m.group(2), 1)
            open(gen, "w", encoding="utf-8").write(src)
            print("generate_tech_news.py: noindex added (loose match)")
        else:
            print("generate_tech_news.py: head pattern not found, manual check needed")
else:
    print("generate_tech_news.py: already has noindex")

# ---------- 2. consolidate duplicate ----------
KEEP = "why-screen-repair-quotes-differ.html"
DROP = "why-do-screen-repair-quotes-vary-so-much.html"
keep_p = os.path.join(ROOT, "blog", KEEP)
drop_p = os.path.join(ROOT, "blog", DROP)
drop_html = open(drop_p, encoding="utf-8").read()
if "noindex" not in drop_html:
    # canonical already exists in head; set canonical to keeper
    drop_html = re.sub(
        r'<link rel="canonical" href="https://repairrange.io/blog/why-do-screen-repair-quotes-vary-so-much\.html">',
        '<link rel="canonical" href="https://repairrange.io/blog/why-screen-repair-quotes-differ.html">',
        drop_html, count=1)
    drop_html = drop_html.replace("<head>", '<head>\n    <meta name="robots" content="noindex, nofollow">', 1)
    open(drop_p, "w", encoding="utf-8").write(drop_html)
    print(f"dup consolidated: {DROP} -> canonical+noindex to {KEEP}")

# rewrite internal links from dropped to keeper
for root_dir, dirs, files in os.walk(ROOT):
    if ".git" in root_dir or "blog-bot" in root_dir:
        continue
    for f in files:
        if not f.endswith(".html"):
            continue
        p = os.path.join(root_dir, f)
        html = open(p, encoding="utf-8", errors="replace").read()
        if "why-do-screen-repair-quotes-vary-so-much" in html:
            html = html.replace("why-do-screen-repair-quotes-vary-so-much.html", "why-screen-repair-quotes-differ.html")
            open(p, "w", encoding="utf-8").write(html)
            print(f"link rewritten: {os.path.relpath(p, ROOT)}")

# remove dropped from sitemap
sm_path = os.path.join(ROOT, "sitemap.xml")
sm = open(sm_path, encoding="utf-8").read()
pat = re.compile(r"(?s)<url>\s*<loc>https://repairrange\.io/blog/" + re.escape(DROP) + r"</loc>.*?</url>\s*")
new_sm, n = pat.subn("", sm, count=1)
if n:
    open(sm_path, "w", encoding="utf-8").write(new_sm)
    print(f"sitemap: removed {DROP}")

# ---------- 3. author bylines + Article schema on indexed blog posts ----------
blog_dir = os.path.join(ROOT, "blog")
added_byline = 0
added_schema = 0
for f in sorted(os.listdir(blog_dir)):
    if not f.endswith(".html"):
        continue
    p = os.path.join(blog_dir, f)
    html = open(p, encoding="utf-8", errors="replace").read()
    if "noindex" in html:
        continue  # skip news posts
    if f == DROP:
        continue
    # byline under H1
    if "By RepairRange" not in html and "<h1" in html:
        m = re.search(r"(<h1[^>]*>.*?</h1>)", html, re.S)
        if m:
            byline = m.group(1) + '\n  <p class="article-byline">By RepairRange &middot; <a href="/how-we-collect-data.html" class="text-teal">Independently researched pricing</a></p>'
            html = html.replace(m.group(1), byline, 1)
            added_byline += 1
    # Article schema if no JSON-LD present
    if 'application/ld+json' not in html and "</head>" in html:
        title_m = re.search(r"<title>([^<]+)</title>", html)
        headline = title_m.group(1).replace(" | RepairRange", "") if title_m else f.replace(".html", "").replace("-", " ").title()
        schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": headline,
            "publisher": {"@type": "Organization", "name": "RepairRange", "url": "https://repairrange.io"},
            "author": {"@type": "Organization", "name": "RepairRange", "url": "https://repairrange.io"},
            "mainEntityOfPage": f"https://repairrange.io/blog/{f}",
            "inLanguage": "en-AU",
        }
        block = '\n<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + "</script>\n"
        html = html.replace("</head>", block + "</head>", 1)
        added_schema += 1
    open(p, "w", encoding="utf-8").write(html)

print(f"bylines added: {added_byline}, Article schema added: {added_schema}")
print("DONE phase 5")
