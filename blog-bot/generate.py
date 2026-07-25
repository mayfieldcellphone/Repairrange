#!/usr/bin/env python3
import time, random, argparse, datetime as dt, json, os, pathlib, re, sys, urllib.request, urllib.error
ROOT = pathlib.Path(__file__).parent
CONFIG = json.loads((ROOT / "config" / "sites.json").read_text())
PRICE_RE = re.compile(r"(?:\$|AUD\s*|USD\s*)\s?\d|(\d+\s?(?:dollars|bucks))", re.I)
SLOP_RE = re.compile(r"\b(in today's world|delve into|in conclusion,|game-?changer|revolutioniz)\b", re.I)
MIN_WORDS = 700; MAX_WORDS = 1600

def validate(site_key, cfg, post):
    fails = []; body = post.get("body_html", ""); text = re.sub(r"<[^>]+>", " ", body); words = len(text.split())
    if words < MIN_WORDS: fails.append("too short"); if not post.get("title"): fails.append("no title")
    if site_key in ("repairrange", "selfrepairkit"):
        if PRICE_RE.search(text): fails.append("price violation")
    return fails

def peek_topic(site_key, offset=0):
    lines = [l.strip() for l in (ROOT / "topics" / f"{site_key}.txt").read_text().splitlines()]
    live = [l for l in lines if l and not l.startswith("#")]
    return live[offset]

def consume_topic(site_key, topic):
    q = ROOT / "topics" / f"{site_key}.txt"; lines = [l.strip() for l in q.read_text().splitlines()]
    q.write_text("\n".join(l for l in lines if l != topic) + "\n")

def build_prompt(site_key, cfg, topic):
    return f"Write a blog for {cfg['domain']} about {topic}. Voice: {cfg['voice']}. Min 900 words. No prices. Australian spelling. Return ONLY JSON."

MODEL = "gemini-3.1-flash-lite"; URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

def call_gemini(prompt):
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json"}}
    req = urllib.request.Request(f"{URL}?key={os.environ['GEMINI_API_KEY']}", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read().decode())["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            time.sleep(2**attempt); continue
    raise Exception("API Failed")

def publish_git(site_key, cfg, post, dry):
    site_root = pathlib.Path(os.environ.get("SITE_ROOT", "."))
    tpl = (ROOT / "templates" / f"{site_key}.html").read_text()
    html = tpl.replace("{{TITLE}}", post["title"]).replace("{{BODY}}", post["body_html"]).replace("{{META}}", post.get("meta_description", ""))
    out = site_root / cfg["blog_dir"] / f"{post['slug']}.html"
    if not dry: out.parent.mkdir(parents=True, exist_ok=True); out.write_text(html)
    return out

def run_site(site_key, dry):
    cfg = CONFIG[site_key]; topic = peek_topic(site_key); post_raw = call_gemini(build_prompt(site_key, cfg, topic))
    post = json.loads(re.sub(r"^```(?:json)?|```$", "", post_raw.strip(), flags=re.M).strip())
    url = publish_git(site_key, cfg, post, dry); consume_topic(site_key, topic)
    return [{"site": site_key, "url": str(url)}]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--site", required=True); ap.add_argument("--dry-run", action="store_true"); a = ap.parse_args()
    print(json.dumps(run_site(a.site, a.dry_run)))
if __name__ == "__main__": main()
