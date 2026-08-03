#!/usr/bin/env python3
"""Cross-link: add Repair Guides to footer Browse lists + update sitemap + sitemap generator."""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

PAGES = [
    "index.html", "blog.html", "fix.html", "unlock.html", "locations.html",
    "brands.html", "calculator.html", "about.html", "phone-plans.html",
    "repair/phone-repair-costs-australia.html", "list-your-shop.html",
]

GUIDES_LI = '<li><a href="/guides/index.html" class="text-white/80 hover:text-amber">Repair Guides</a></li>'

PATTERN = re.compile(r'(<h3 class="eyebrow text-amber[^"]*">Browse</h3><ul class="space-y-2 text-sm">)', re.I)

changed = 0
for page in PAGES:
    path = os.path.join(ROOT, page)
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()
    if "guides/index.html" in html:
        print(f"SKIP (already linked): {page}")
        continue
    new_html, n = PATTERN.subn(lambda m: m.group(1) + "\n" + GUIDES_LI, html, count=1)
    if n:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"LINKED: {page}")
        changed += 1
    else:
        print(f"NO Browse footer found: {page}")

# --- update generate_sitemap.py to include guides folder ---
sp = os.path.join(ROOT, "generate_sitemap.py")
with open(sp, "r", encoding="utf-8") as f:
    src = f.read()
old_folders = 'FOLDERS = ["fix", "locations", "repair", "brands", "tools", "blog", "unlock", "news"]'
new_folders = 'FOLDERS = ["fix", "locations", "repair", "brands", "tools", "blog", "unlock", "news", "guides"]'
if old_folders in src:
    src = src.replace(old_folders, new_folders)
    with open(sp, "w", encoding="utf-8") as f:
        f.write(src)
    print("generate_sitemap.py: added guides folder")
else:
    print("generate_sitemap.py: pattern not found, check manually")

# --- append guide URLs to sitemap.xml if missing ---
sitemap = os.path.join(ROOT, "sitemap.xml")
with open(sitemap, "r", encoding="utf-8") as f:
    sm = f.read()
guide_urls = [
    "https://repairrange.io/guides/index.html",
    "https://repairrange.io/guides/phone-screen-repair-australia.html",
    "https://repairrange.io/guides/phone-battery-replacement-australia.html",
    "https://repairrange.io/guides/phone-water-damage-repair.html",
    "https://repairrange.io/guides/repair-or-replace-phone.html",
    "https://repairrange.io/guides/ipad-tablet-repair-costs-australia.html",
]
added = 0
for u in guide_urls:
    if u not in sm:
        sm = sm.replace("</urlset>",
            f'  <url>\n    <loc>{u}</loc>\n    <lastmod>2026-08-03</lastmod>\n    <priority>0.7</priority>\n  </url>\n</urlset>')
        added += 1
with open(sitemap, "w", encoding="utf-8") as f:
    f.write(sm)
print(f"sitemap: added {added} guide URLs")

print(f"DONE: {changed} pages linked")
