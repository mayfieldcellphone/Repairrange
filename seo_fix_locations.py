#!/usr/bin/env python3
"""Fix wrong-city copy on location pages (template copy-paste bugs) + add city pages to sitemap & guides index."""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

FIXES = {
    "melbourne": {
        "region": "Independent repair pricing for Melbourne and wider Victoria — the CBD, inner north and west, and the south-eastern suburbs.",
        "suburb": "Melbourne prices vary by suburb. CBD shops charge a premium for speed; inner-north and western suburbs are routinely 20\u201330% cheaper.",
    },
    "brisbane": {
        "region": "Independent repair pricing for Brisbane and wider South-East Queensland.",
        "suburb": "Brisbane prices vary by suburb. CBD shops charge a premium for speed; outer suburbs like Logan and Caboolture are routinely 20\u201330% cheaper.",
    },
    "perth": {
        "region": "Independent repair pricing for Perth and wider Western Australia.",
        "suburb": "Perth prices vary by suburb. CBD shops charge a premium for speed; outer suburbs like Fremantle and Joondalup are routinely 20\u201330% cheaper.",
    },
    "adelaide": {
        "region": "Independent repair pricing for Adelaide and wider South Australia.",
        "suburb": "Adelaide prices vary by suburb. CBD shops charge a premium for speed; outer suburbs like Salisbury and Marion are routinely 20\u201330% cheaper.",
    },
    "newcastle": {
        "region": None,  # Newcastle region text is already correct (Hunter)
        "suburb": "Newcastle prices vary by suburb. CBD and Charlestown shops charge a premium for convenience; local shops like Mayfield are routinely 20\u201330% cheaper.",
    },
}

REGION_RE = re.compile(r"pricing for (Melbourne|Brisbane|Perth|Adelaide|Newcastle) and the wider Hunter[^<]*")
SUBURB_RE = re.compile(r"(Sydney|Melbourne|Brisbane|Perth|Adelaide|Newcastle) prices vary by suburb\. CBD shops charge a premium for speed; outer suburbs like Parramatta or Bankstown are routinely 20[-–]30% cheaper\.")

for city, fixes in FIXES.items():
    p = os.path.join(ROOT, "locations", city + ".html")
    html = open(p, encoding="utf-8").read()
    before = html
    if fixes["region"]:
        html = REGION_RE.sub(fixes["region"].replace("—", "\\u2014") if False else fixes["region"], html, count=1)
    html = SUBURB_RE.sub(fixes["suburb"], html, count=1)
    if html != before:
        open(p, "w", encoding="utf-8").write(html)
        print(f"FIXED: {city}.html")
    else:
        print(f"NO CHANGE: {city}.html")

# --- add city pages to sitemap ---
sm_path = os.path.join(ROOT, "sitemap.xml")
sm = open(sm_path, encoding="utf-8").read()
for slug in ["phone-repair-costs-australia-cities", "phone-repair-costs-sydney-vs-melbourne"]:
    url = f"https://repairrange.io/guides/{slug}.html"
    if url not in sm:
        sm = sm.replace("</urlset>",
            f'  <url>\n    <loc>{url}</loc>\n    <lastmod>2026-08-03</lastmod>\n    <priority>0.7</priority>\n  </url>\n</urlset>')
        print(f"sitemap += {slug}")
open(sm_path, "w", encoding="utf-8").write(sm)

# --- link city pages from the guides index ---
idx = os.path.join(ROOT, "guides", "index.html")
html = open(idx, encoding="utf-8").read()
if "phone-repair-costs-australia-cities" not in html:
    add = ('<h2>Repair costs by city</h2>\n'
           '<p>Repair prices are national, then local. Compare <a href="/guides/phone-repair-costs-australia-cities.html">all six Australian cities</a>, '
           'or the <a href="/guides/phone-repair-costs-sydney-vs-melbourne.html">Sydney vs Melbourne head-to-head</a>, then check your '
           '<a href="/locations.html">city&rsquo;s pricing page</a>.</p>\n')
    html = html.replace("<h2>Start with your symptom</h2>", add + "<h2>Start with your symptom</h2>", 1)
    open(idx, "w", encoding="utf-8").write(html)
    print("guides index: city section added")
else:
    print("guides index: already linked")
