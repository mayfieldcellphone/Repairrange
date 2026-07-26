#!/usr/bin/env python3
import time, random, argparse, datetime as dt, json, os, pathlib, re, sys, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).parent
CONFIG = json.loads((ROOT / "config" / "sites.json").read_text())

def peek_topic(site_key):
    lines = [l.strip() for l in (ROOT / "topics" / f"{site_key}.txt").read_text().splitlines()]
    return [l for l in lines if l and not l.startswith("#")][0]

def consume_topic(site_key, topic):
    q = ROOT / "topics" / f"{site_key}.txt"
    lines = q.read_text().splitlines()
    q.write_text("\n".join(l for l in lines if l.strip() != topic) + "\n")

def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={os.environ['GEMINI_API_KEY']}"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.85, "maxOutputTokens": 4096, "responseMimeType": "application/json"}}
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read().decode())["candidates"][0]["content"]["parts"][0]["text"]
        except: time.sleep(2**attempt); continue
    raise Exception("API Failed")

def update_blog_index(site_root, site_key, post):
    blog_index = site_root / "blog.html"
    if not blog_index.exists(): return
    content = blog_index.read_text()
    today = dt.date.today().strftime("%d %b %Y")
    card = f'''
        <a href="blog/{post['slug']}.html" class="post-card p-6 rounded-xl bg-white border border-line hover:border-teal transition-all group">
            <p class="eyebrow text-[10px] mb-2">{today}</p>
            <h3 class="font-serif text-xl text-ink mb-3 group-hover:text-teal transition-colors">{post['title']}</h3>
            <p class="text-muted text-xs leading-relaxed line-clamp-3">{post['meta_description']}</p>
            <span class="inline-flex items-center gap-1 text-teal text-[10px] font-bold uppercase tracking-wider mt-4">Read Article <i data-lucide="arrow-right" class="w-3 h-3"></i></span>
        </a>
    '''
    marker = '<!-- BLOG_GRID_START -->'
    if marker in content:
        new_content = content.replace(marker, marker + card)
        blog_index.write_text(new_content)

def publish_git(site_key, cfg, post, dry):
    site_root = pathlib.Path(os.environ.get("SITE_ROOT", "."))
    tpl_path = ROOT / "templates" / f"{site_key}.html"
    tpl = tpl_path.read_text()
    today = dt.date.today()
    
    # Layer 1: Global replacements including body
    subs = {
        "{{BODY}}": post["body_html"],
        "{{TITLE}}": post["title"],
        "{{META}}": post["meta_description"],
        "{{SLUG}}": post["slug"],
        "{{DATE_HUMAN}}": today.strftime("%d %B %Y"),
        "{{DATE_ISO}}": today.isoformat(),
        "{{DOMAIN}}": cfg["domain"].rstrip("/")
    }
    
    html = tpl
    for k, v in subs.items():
        html = html.replace(k, str(v))
        
    # Layer 2: Cleanup any double-escaped or AI-inserted placeholders in the body
    html = html.replace("%7B%7BDOMAIN%7D%7D", cfg["domain"].rstrip("/"))
    html = html.replace("{{DOMAIN}}", cfg["domain"].rstrip("/"))
    
    out = site_root / cfg["blog_dir"] / f"{post['slug']}.html"
    if not dry:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)
        if site_key == "repairrange":
            update_blog_index(site_root, site_key, post)
    return out

def run_site(site_key, dry):
    cfg = CONFIG[site_key]; topic = peek_topic(site_key)
    prompt = f"Write a blog for {cfg['domain']} about {topic}. Voice: {cfg['voice']}. Min 900 words. No prices. ALWAYS use absolute URLs for links (starting with https://). Return ONLY JSON."
    post = json.loads(re.sub(r"^```(?:json)?|```$", "", call_gemini(prompt).strip(), flags=re.M).strip())
    url = publish_git(site_key, cfg, post, dry)
    if not dry: consume_topic(site_key, topic)
    return [{"site": site_key, "url": str(url)}]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--site", required=True); ap.add_argument("--dry-run", action="store_true"); a = ap.parse_args()
    print(json.dumps(run_site(a.site, a.dry_run)))

if __name__ == "__main__": main()
