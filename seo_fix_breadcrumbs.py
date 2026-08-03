#!/usr/bin/env python3
"""Add BreadcrumbList JSON-LD to key hub pages before </head>."""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))

# page -> (list of crumbs: (name, url-path))  url-path "" = homepage
CRUMBS = {
    "blog.html": [("Home", ""), ("Blog", "blog.html")],
    "fix.html": [("Home", ""), ("Troubleshoot", "fix.html")],
    "unlock.html": [("Home", ""), ("Phone Unlock", "unlock.html")],
    "locations.html": [("Home", ""), ("Locations", "locations.html")],
    "brands.html": [("Home", ""), ("Brands", "brands.html")],
    "calculator.html": [("Home", ""), ("Repair Calculator", "calculator.html")],
    "repair/phone-repair-costs-australia.html": [("Home", ""), ("Repairs", "repair/phone-repair-costs-australia.html")],
    "about.html": [("Home", ""), ("About", "about.html")],
}

def build_schema(page, crumbs):
    items = []
    pos = 1
    for name, path in crumbs:
        url = "https://repairrange.io/" + path if path else "https://repairrange.io/"
        items.append({"@type": "ListItem", "position": pos, "name": name, "item": url})
        pos += 1
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }

changed = 0
for page, crumbs in CRUMBS.items():
    path = os.path.join(ROOT, page)
    if not os.path.exists(path):
        print(f"MISSING: {page}")
        continue
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()
    if "BreadcrumbList" in html:
        print(f"SKIP (already has): {page}")
        continue
    schema = json.dumps(build_schema(page, crumbs))
    block = '\n<script type="application/ld+json">' + schema + '</script>\n'
    if "</head>" in html:
        html = html.replace("</head>", block + "</head>", 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"ADDED: {page}")
        changed += 1
    else:
        print(f"NO </head> found: {page}")

print(f"DONE: {changed} pages updated")
