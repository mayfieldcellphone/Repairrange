#!/usr/bin/env python3
"""
blog-bot — scheduled blog generation for Khalil's properties.
"""

import time
import random
import argparse
import datetime as dt
import json
import os
import pathlib
import re
import sys
import urllib.request
import urllib.error

ROOT = pathlib.Path(__file__).parent
CONFIG = json.loads((ROOT / "config" / "sites.json").read_text())
TZ_LABEL = "AEST"

# ---------------------------------------------------------------- guardrails
PRICE_RE = re.compile(r"(?:\$|AUD\s*|USD\s*)\s?\d|(\d+\s?(?:dollars|bucks))", re.I)

def validate(site_key, cfg, post):
    fails = []
    body = post.get("body_html", "")
    text = re.sub(r"<[^>]+>", " ", body)
    words = len(text.split())
    
    if words < 700:
        fails.append("too short")
    if not post.get("title"):
        fails.append("no title")
        
    if site_key in ("repairrange", "selfrepairkit"):
        if PRICE_RE.search(text):
            fails.append("price violation")
    return fails

def peek_topic(site_key, offset=0):
    topic_file = ROOT / "topics" / f"{site_key}.txt"
    lines = [l.strip() for l in topic_file.read_text().splitlines()]
    live = [l for l in lines if l and not l.startswith("#")]
    return live[offset]

def consume_topic(site_key, topic):
    q = ROOT / "topics" / f"{site_key}.txt"
    lines = [l.strip() for l in q.read_text().splitlines()]
    q.write_text("\n".join(l for l in lines if l != topic) + "\n")

def build_prompt(site_key, cfg, topic):
    return f"Write a blog for {cfg['domain']} about {topic}. Voice: {cfg['voice']}. Min 900 words. No prices. Australian spelling. Return ONLY JSON with fields title, slug, meta_description, body_html."

MODEL = "gemini-3.1-flash-lite"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

def call_gemini(prompt):
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json"}}
    req = urllib.request.Request(f"{URL}?key={os.environ['GEMINI_API_KEY']}", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
    
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                res = json.loads(r.read().decode())
                return res["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            wait = min(60, 2 ** attempt) + random.uniform(0, 1)
            print(f"  [gemini] error, retry {attempt+1} in {wait:.1f}s")
            time.sleep(wait)
            continue
    raise Exception("Gemini API persistently failed")

def publish_git(site_key, cfg, post, dry):
    site_root = pathlib.Path(os.environ.get("SITE_ROOT", "."))
    tpl = (ROOT / "templates" / f"{site_key}.html").read_text()
    
    html = (tpl
            .replace("{{TITLE}}", post["title"])
            .replace("{{BODY}}", post["body_html"])
            .replace("{{META}}", post.get("meta_description", "")))
            
    out = site_root / cfg["blog_dir"] / f"{post['slug']}.html"
    
    if not dry:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)
        
        # Update sitemap
        sm = site_root / cfg["sitemap_file"]
        if sm.exists():
            url = f"{cfg['domain']}/{cfg['blog_dir']}/{post['slug']}.html"
            entry = f"  <url><loc>{url}</loc><lastmod>{dt.date.today().isoformat()}</lastmod><priority>0.8</priority></url>\n"
            txt = sm.read_text()
            if url not in txt:
                sm.write_text(txt.replace("</urlset>", entry + "</urlset>"))
    return out

def run_site(site_key, dry):
    cfg = CONFIG[site_key]
    topic = peek_topic(site_key)
    print(f"[{site_key}] generating: {topic}")
    
    post_raw = call_gemini(build_prompt(site_key, cfg, topic))
    # Clean possible markdown blocks
    post_raw = re.sub(r"^```(?:json)?|```$", "", post_raw.strip(), flags=re.M).strip()
    post = json.loads(post_raw)
    
    fails = validate(site_key, cfg, post)
    if fails:
        print(f"  validation failed: {fails}")
        return [{"site": site_key, "status": "failed", "errors": fails}]
        
    url = publish_git(site_key, cfg, post, dry)
    if not dry:
        consume_topic(site_key, topic)
    return [{"site": site_key, "url": str(url), "status": "success"}]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    
    try:
        results = run_site(a.site, a.dry_run)
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
