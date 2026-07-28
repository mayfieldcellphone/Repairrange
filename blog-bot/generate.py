#!/usr/bin/env python3
"""
blog-bot — scheduled blog generation for Khalil's properties.
"""

import time, random, argparse, datetime as dt, json, os, pathlib, re, sys, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).parent
CONFIG = json.loads((ROOT / "config" / "sites.json").read_text())

BANNED_PHRASES = [
    "delve", "in today's world", "in today's digital", "game-changer", "game changer",
    "unlock the power", "unlock the potential", "dive into", "landscape", "realm of",
    "tapestry", "testament to", "in conclusion", "it is important to note",
    "elevate your", "navigate the", "in the world of", "let's explore",
]

def validate(site_key, cfg, post):
    fails = []
    body = post.get("body_html", "")
    text = re.sub(r"<[^>]+>", " ", body)
    words = len(text.split())
    if words < 700 or words > 1700:
        fails.append(f"word count out of range ({words} words, need 700-1700)")
    if not post.get("title"):
        fails.append("missing title")
    meta = post.get("meta_description", "")
    if not (100 <= len(meta) <= 165):
        fails.append(f"meta description length {len(meta)} chars, need 100-165")
    low = text.lower()
    hit = [p for p in BANNED_PHRASES if p in low]
    if hit:
        fails.append(f"AI-slop phrases found: {hit}")
    if cfg.get("no_price_mentions") and re.search(r"\$\s?\d|AUD|\bdollars\b", body, re.I):
        fails.append("price mention found (guardrail: never state a price)")
    links = re.findall(r'href="([^"]+)"', body)
    allowed_domains = [cfg["domain"].replace("https://", "").replace("http://", "")]
    allowed_domains += [u.replace("https://", "").replace("http://", "") for u in cfg.get("internal_links", [])]
    if not any(any(dom.split("/")[0] in l for dom in allowed_domains) for l in links):
        fails.append("no internal link found")
    if len(links) > 6:
        fails.append(f"too many links ({len(links)}, max 6)")
    for domain, limit in cfg.get("link_limits", {}).items():
        count = sum(1 for l in links if domain in l)
        if count > limit:
            fails.append(f"too many links to {domain} ({count}, max {limit})")
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
    raise Exception("API failed")

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
    subs = {"{{BODY}}": post.get("body_html", ""), "{{TITLE}}": post.get("title", ""), "{{META}}": post.get("meta_description", ""), "{{SLUG}}": post.get("slug", ""), "{{DATE_HUMAN}}": today.strftime("%d %B %Y"), "{{DATE_ISO}}": today.isoformat(), "{{DOMAIN}}": cfg["domain"].rstrip("/")}
    html = tpl
    for k, v in subs.items(): html = html.replace(k, str(v))
    html = html.replace("%7B%7BDOMAIN%7D%7D", cfg["domain"].rstrip("/"))
    out = site_root / cfg["blog_dir"] / f"{post['slug']}.html"
    if not dry:
        out.parent.mkdir(parents=True, exist_ok=True); out.write_text(html)
        update_blog_index(site_root, site_key, post)
    return out

def build_prompt(site_key, cfg, topic):
    guardrails = "\n".join(f"- {g}" for g in cfg.get("guardrails", []))
    links = "\n".join(f"- {l}" for l in cfg.get("internal_links", []))
    return (
        f"Write a deeply detailed, well-researched blog post for {cfg['domain']} about: {topic}\n\n"
        f"Voice: {cfg['voice']}\n"
        f"Target length: 1100-1400 words.\n"
        f"Australian spelling throughout.\n"
        f"Write naturally -- avoid AI cliches like 'delve', 'in today's world', 'game-changer', "
        f"'unlock', 'landscape', 'tapestry', 'in conclusion'.\n"
        f"Structure: a strong opening paragraph, 3-5 <h2> sections with real substance, and a short "
        f"closing that does NOT summarise with 'in conclusion'.\n"
        f"Include at least one <a href> link to one of these pages, worked in naturally where relevant:\n{links}\n\n"
        f"Hard rules -- breaking any of these fails the post:\n{guardrails if guardrails else '- None beyond the voice and structure above.'}\n\n"
        f"Return ONLY valid JSON with keys: title, slug, meta_description (100-165 characters), "
        f"body_html (semantic HTML: <p>, <h2>, <ul>/<ol>, <a href> -- no <html>/<body> wrapper, no markdown)."
    )

def run_site(site_key, dry):
    cfg = CONFIG[site_key]; topic = peek_topic(site_key); last_err = ""
    prompt = build_prompt(site_key, cfg, topic)
    for attempt in range(3):
        try:
            raw = call_gemini(prompt if not last_err else prompt + f"\n\nPREVIOUS ATTEMPT FAILED: {last_err}. Fix this and return valid JSON only.")
            post = json.loads(re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.M).strip())
            fails = validate(site_key, cfg, post)
            if fails: raise Exception(f"Validation: {fails}")
            url = publish_git(site_key, cfg, post, dry)
            if not dry: consume_topic(site_key, topic)
            state = "PUBLISHED (dry-run, not pushed)" if dry else "PUBLISHED"
            return [{"site": site_key, "url": str(url), "title": post.get("title", ""), "meta": post.get("meta_description", ""), "state": state}]
        except Exception as e:
            last_err = str(e); print(f"  Attempt {attempt+1} failed: {e}")
    raise Exception("Generation failed")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--site", required=True); ap.add_argument("--dry-run", action="store_true"); a = ap.parse_args()
    results = run_site(a.site, a.dry_run)
    print(json.dumps(results))
    if not a.dry_run:
        try:
            import notify
            notify.send(results)
        except Exception as e:
            print(f"  notify failed (non-blocking): {e}")

if __name__ == "__main__": main()
