#!/usr/bin/env python3
import pathlib, re

ROOT = pathlib.Path(".").resolve()

def universal_scrub():
    for p in ROOT.rglob("*.html"):
        if ".git" in str(p) or "node_modules" in str(p): continue
        
        # Read file with 'ignore' to handle any weird encoding artifacts
        content = p.read_text(encoding="utf-8", errors="ignore")
        orig = content
        
        # 1. Fix Mojibake (the weird symbols)
        content = content.replace("â", "—").replace("â", "–").replace("â", "’")
        content = content.replace("âœ", "“").replace("â", "”").replace("Â ", " ")

        # 2. Force-Replace Hunter/Newcastle text with generic placeholders
        # This uses Regex to find the text even if dashes/symbols are broken
        content = re.sub(r"the wider Hunter", "Sydney Metro", content)
        content = re.sub(r"Mayfield, Hamilton, Islington, Waratah, Jesmond.*?Maitland", 
                         "the CBD, Parramatta, and Northern Beaches", content)
        content = re.sub(r"Getting a repair done in the Hunter", "Getting a repair done in Sydney Metro", content)
        content = re.sub(r"if you're in the Hunter.*?exact quote\.", 
                         "our symptom check and cost calculator can give you a realistic quote range.", content)

        if content != orig:
            p.write_text(content, encoding="utf-8")
            print(f"SCRUBBED: {p.name}")

if __name__ == "__main__":
    universal_scrub()
