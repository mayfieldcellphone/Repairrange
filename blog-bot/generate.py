#!/usr/bin/env python3
"""
blog-bot — scheduled blog generation for Khalil's properties.
"""

import time, random, argparse, datetime as dt, json, os, pathlib, re, sys, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).parent
CONFIG = json.loads((ROOT / "config" / "sites.json").read_text())

def validate(site_key, cfg, post):
    fails = []
    body = post.get("body_html", "")
    text = re.sub(r"<[^>]+>", " ", body)
    words = len(text.split())
    if words < 700: fails.append("too short")
    if not post.get("title"): fails.append("missing title")
    return fails

def peek_topic(site_key):
    lines = [l.strip() for l in (ROOT / "topics" / f"{site_key}.txt").read_text().splitlines()]
    live = [l for l in lines if l and not l.startswith("#")]
    if not live: raise SystemExit(f"[{site_key}] topic queue empty")
    return live[0]

def consume_topic(site_key, topic):
    q = ROOT / "topics" / f"{site_key}.txt"; lines = q.read_text().splitlines()
    q.write_text("\n".join(l for l in lines if l.strip() != topic) + "\n")

def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={os.environ['GEMINI_API_KEY']}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.85, "maxOutputTokens": 4096, "responseMimeType": "application/json"}}
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read().decode())["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 5:
                time.sleep(min(60, 2**attempt) + random.uniform(0, 1)); continue
            raise
    raise Exception("API persistently failed")

def update_blog_index(site_root, site_key, post):
    blog_index = site_root / "blog.html"
    if not blog_index.exists(): return
    content = blog_index.read_text(); today = dt.date.today(); month_year = today.strftime("%B %Y")
    label = "Expert Insight" if site_key == "pdfrange" else "Repair Analysis"
    card = f'''
            <a href="blog/{post['slug']}.html" class="post-card group">
                <p class="eyebrow mb-3">{label} &bull; 6 min read &bull; {month_year}</p>
                <h2 class="font-serif text-2xl md:text-3xl text-ink mb-3 leading-tight">{post['title']}</h2>
                <p class="text-muted leading-relaxed mb-4">{post['meta_description']}</p>
                <span class="inline-flex items-center gap-2 text-sm font-medium text-teal">Read the post <i data-lucide="arrow-right" class="w-4 h-4"></i></span>
            </a>
    '''
    if '<!-- BLOG_GRID_START -->' in content:
        blog_index.write_text(content.replace('<!-- BLOG_GRID_START -->', '<!-- BLOG_GRID_START -->' + card))

def publish_git(site_key, cfg, post, dry):
    site_root = pathlib.Path(os.environ.get("SITE_ROOT", "."))
    tpl = (ROOT / "templates" / f"{site_key}.html").read_text()
    today = dt.date.today()
    subs = {
        "{{BODY}}": post.get("body_html", ""),
        "{{TITLE}}": post.get("title", ""),
        "{{META}}": post.get("meta_description", ""),
        "{{SLUG}}": post.get("slug", ""),
        "{{DATE_HUMAN}}": today.strftime("%d %B %Y"),
        "{{DOMAIN}}": cfg["domain"].rstrip("/")
    }
    html = tpl
    for k, v in subs.items(): html = html.replace(k, str(v))
    html = html.replace("%7B%7BDOMAIN%7D%7D", cfg["domain"].rstrip("/"))
    out = site_root / cfg["blog_dir"] / f"{post['slug']}.html"
    if not dry:
        out.parent.mkdir(parents=True, exist_ok=True); out.write_text(html)
        update_blog_index(site_root, site_key, post)
    return out

def run_site(site_key, dry):
    cfg = CONFIG[site_key]; topic = peek_topic(site_key); last_err = ""
    prompt = f"Write a blog for {cfg['domain']} about {topic}. Voice: {cfg['voice']}. Australian spelling. No prices. Return ONLY JSON with keys: title, slug, meta_description, body_html."
    for attempt in range(3):
        try:
            raw = call_gemini(prompt if not last_err else prompt + f"\n\nERROR: {last_err}. Fix JSON.")
            post = json.loads(re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.M).strip())
            fails = validate(site_key, cfg, post)
            if fails: raise Exception(f"Validation: {fails}")
            url = publish_git(site_key, cfg, post, dry)
            if not dry: consume_topic(site_key, topic)
            return [{"site": site_key, "url": str(url)}]
        except Exception as e:
            last_err = str(e); print(f"  Attempt {attempt+1} failed: {e}")
    raise Exception("Generation failed")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--site", required=True); ap.add_argument("--dry-run", action="store_true"); a = ap.parse_args()
    print(json.dumps(run_site(a.site, a.dry_run)))

if __name__ == "__main__": main()
