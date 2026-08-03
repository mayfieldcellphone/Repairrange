#!/usr/bin/env python3
import re, json, glob, os

root = os.path.dirname(os.path.abspath(__file__))
bad = []
count = 0
for path in glob.glob(os.path.join(root, "**", "*.html"), recursive=True):
    if "node_modules" in path or ".git" in path:
        continue
    with open(path, encoding="utf-8", errors="replace") as f:
        html = f.read()
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S):
        count += 1
        try:
            json.loads(m.group(1).strip())
        except Exception as e:
            bad.append((path.replace(root, ""), str(e)[:100]))
print(f"JSON-LD blocks checked: {count}, invalid: {len(bad)}")
for b in bad[:10]:
    print("INVALID:", b)
