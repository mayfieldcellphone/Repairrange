#!/usr/bin/env python3
import pathlib

ROOT = pathlib.Path(".").resolve()

# List of precise text replacements
CLEANUP = [
    ("â€”", "—"), ("â€“", "–"), ("â€™", "’"), ("â€œ", "“"), ("â€", "”"), ("Â ", " "),
    ("Independent repair pricing for Sydney and the wider Hunter — Mayfield, Hamilton, Islington, Waratah, Jesmond and out toward Maitland.", 
     "Independent repair pricing for Sydney Metro — from the CBD to Parramatta, Blacktown, and the Northern Beaches."),
    ("Getting a repair done in the Hunter", "Getting a repair done in Sydney Metro"),
    ("if you're in the Hunter, the workshop above can give you an exact quote.", "our symptom check and cost calculator can give you a realistic quote range.")
]

def force_fix():
    for p in ROOT.rglob("*.html"):
        if ".git" in str(p): continue
        content = p.read_text(encoding="utf-8", errors="ignore")
        original = content
        for bad, good in CLEANUP:
            content = content.replace(bad, good)
        
        if content != original:
            p.write_text(content, encoding="utf-8")
            print(f"CLEANED: {p.name}")

if __name__ == "__main__":
    force_fix()
