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
    if words < 700: fails.append("too short")
    if not post.get("title"): fails.append("missing title")
    if not post.get("body_html"): fails.append("missing body_html")
    if site_key in ("repairrange", "selfrepairkit"):
        if PRICE_RE.search(text): fails.append("price violation")
    return fails

def peek_topic(site_key):
    topic_file = ROOT / "topics" / f"{site_key}.txt"
    lines = [l.strip() for l in topic_file.read_text().splitlines()]
    live = [l for l in lines if l and not l.startswith("#")]
    if not live: raise SystemExit(f"[{site_key}] topic queue empty")
    return live[0]

def consume_topic(site_key, topic):
    q = ROOT / "topics" / f"{site_key}.txt"
    lines = q.read_text().splitlines()
    q.write_text("\n".join(l for l in lines if l.strip() != topic) + "\n")

def build_prompt(site_key, cfg, topic):
    links = "\n".join(f"- {l}" for l in cfg.get("internal_links", []))
    return f"""You are writing a blog post for {cfg['domain']}.
TOPIC: {topic}
VOICE: {cfg['voice']}
RULES: 
- Min 900 words. No prices. Australian spelling. 
- Links (1-3): {links}
- ALWAYS use absolute URLs for links (starting with https://).
Return ONLY JSON with these exact keys:
{{
  "title": "Title here",
  "slug": "url-handle-here",
  "meta_description": "110-160 chars",
  "body_html": "<h1>Title</h1><p>Content...</p>"
}}"""

def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={os.environ['GEMINI_API_KEY']}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.85, "maxOutputTokens": 4096, "responseMimeType": "application/json"}}
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.loads(r.read().decode())
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            detail = e.read().decode()[:500]
            if e.code == 429 and attempt < 5:
                time.sleep(min(60, 2**attempt) + random.uniform(0, 1)); continue
            print(f"[gemini {e.code}] {detail}"); raise
    raise Exception("API Failed")

def update_blog_index(site_root, site_key, post):
    blog_index = site_root / "blog.html"
    if not blog_index.exists(): return
    content = blog_index.read_text()
    today = dt.date.today()
    month_year = today.strftime("%B %Y")
    
    card = f'''
            <a href="blog/{post['slug']}.html" class="post-card group">
                <p class="eyebrow mb-3">Expert Insight &bull; 6 min read &bull; {month_year}</p>
                <h2 class="font-serif text-2xl md:text-3xl text-ink mb-3 leading-tight">{post['title']}</h2>
                <p class="text-muted leading-relaxed mb-4">{post['meta_description']}</p>
                <span class="inline-flex items-center gap-2 text-sm font-medium text-teal">Read the post <i data-lucide="arrow-right" class="w-4 h-4"></i></span>
            </a>
    '''
    marker = '<!-- BLOG_GRID_START -->'
    if marker in content:
        blog_index.write_text(content.replace(marker, marker + card))

def publish_git(site_key, cfg, post, dry):
    site_root = pathlib.Path(os.environ.get("SITE_ROOT", "."))
    tpl_path = ROOT / "templates" / f"{site_key}.html"
    tpl = tpl_path.read_text()
    today = dt.date.today()
    
    # Precise replacements
    html = tpl.replace("{{BODY}}", post.get("body_html", ""))
    html = html.replace("{{TITLE}}", post.get("title", ""))
    html = html.replace("{{META}}", post.get("meta_description", ""))
    html = html.replace("{{SLUG}}", post.get("slug", ""))
    html = html.replace("{{DATE_HUMAN}}", today.strftime("%d %B %Y"))
    html = html.replace("{{DATE_ISO}}", today.isoformat())
    html = html.replace("{{DOMAIN}}", cfg["domain"].rstrip("/"))
    
    # URL-encoded safety
    html = html.replace("%7B%7BDOMAIN%7D%7D", cfg["domain"].rstrip("/"))
    
    out = site_root / cfg["blog_dir"] / f"{post['slug']}.html"
    if not dry:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)
        if site_key == "repairrange":
            update_blog_index(site_root, site_key, post)
    return out

def run_site(site_key, dry):
    cfg = CONFIG[site_key]; topic = peek_topic(site_key)
    raw = call_gemini(build_prompt(site_key, cfg, topic))
    post = json.loads(re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.M).strip())
    fails = validate(site_key, cfg, post)
    if fails: raise Exception(f"Validation failed: {fails}")
    url = publish_git(site_key, cfg, post, dry)
    if not dry: consume_topic(site_key, topic)
    return [{"site": site_key, "url": str(url)}]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--site", required=True); ap.add_argument("--dry-run", action="store_true"); a = ap.parse_args()
    print(json.dumps(run_site(a.site, a.dry_run)))

if __name__ == "__main__": main()
