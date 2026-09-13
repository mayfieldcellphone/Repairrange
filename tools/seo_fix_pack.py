#!/usr/bin/env python3
import os, pathlib, re, html

ROOT = pathlib.Path(".").resolve()
SITE = "https://repairrange.io"

# 1. MOJIBAKE MAP (Fixing broken characters)
REPAIRS = [
    ("â€”", "—"), ("â€“", "–"), ("â€™", "’"), 
    ("â€œ", "“"), ("â€", "”"), ("Â ", " ")
]

# 2. CITY LOCALIZATION MAP
CITY_FIXES = {
    "locations/sydney.html": ("Sydney Metro", "the CBD, Parramatta, and Northern Beaches"),
    "locations/melbourne.html": ("Melbourne Metro", "St Kilda, Richmond, and Box Hill"),
    "locations/brisbane.html": ("Brisbane Metro", "Fortitude Valley, Chermside, and Sunnybank"),
    "locations/perth.html": ("Perth Metro", "Fremantle, Joondalup, and the CBD"),
    "locations/adelaide.html": ("Adelaide Metro", "North Adelaide, Glenelg, and the CBD")
}

def fix_files():
    for p in ROOT.rglob("*.html"):
        if ".git" in str(p): continue
        content = p.read_text(encoding="utf-8", errors="ignore")
        orig = content
        
        # Repair characters
        for bad, good in REPAIRS: content = content.replace(bad, good)
        
        # Localize Cities
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        if rel in CITY_FIXES:
            city, suburbs = CITY_FIXES[rel]
            content = content.replace("the wider Hunter", city)
            content = content.replace("Mayfield, Hamilton, Islington, Waratah, Jesmond and out toward Maitland", suburbs)
            content = content.replace("Getting a repair done in the Hunter", f"Getting a repair done in {city}")

        if content != orig:
            p.write_text(content, encoding="utf-8")
            print(f"Fixed: {rel}")

def fix_robots():
    rb = ROOT / "robots.txt"
    if rb.exists():
        text = "User-agent: *\nAllow: /\n\n# Allow AI\nUser-agent: GPTBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\nUser-agent: PerplexityBot\nAllow: /"
        rb.write_text(text, encoding="utf-8")
        print("Fixed: robots.txt")

if __name__ == "__main__":
    fix_files()
    fix_robots()
