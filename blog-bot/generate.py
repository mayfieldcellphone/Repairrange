#!/usr/bin/env python3
"""
blog-bot — scheduled blog generation for Khalil's properties.

Runs from CI on a pipeline schedule. No human in the loop at runtime.

Usage:
    python generate.py --site repairrange
    python generate.py --site repairrange --dry-run     # no write, no publish, no email
    python generate.py --site all

Env vars required:
    LLM_PROVIDER        "gemini" (default) or "anthropic"
    GEMINI_API_KEY      if provider=gemini
    ANTHROPIC_API_KEY   if provider=anthropic
    SMTP_USER           gmail address used to send
    SMTP_PASS           gmail APP PASSWORD (not your account password)
    NOTIFY_TO           engrkhalil77@gmail.com
    LMS_API_TOKEN       LaunchMyStore API token (only for launchmystore sites)

Exit codes: 0 ok, 1 config/topic error, 2 generation failed validation, 3 publish failed.
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

# ... (rest of imports remains similar)

ROOT = pathlib.Path(__file__).parent
CONFIG = json.loads((ROOT / "config" / "sites.json").read_text())
TZ_LABEL = "AEST"

# ---------------------------------------------------------------- guardrails

# Any dollar figure at all. Khalil's standing rule: never invent or estimate a price.
PRICE_RE = re.compile(r"(?:\$|AUD\s*|USD\s*)\s?\d|(\d+\s?(?:dollars|bucks))", re.I)

# Quantified environmental claims. Killed the Mayfield Gadgets homepage block once already.
CO2_RE = re.compile(
    r"\b\d[\d,.]*\s*(kg|kilograms?|tonnes?|tons?|g)\s*(of\s*)?(co2|carbon|e-?waste)"
    r"|\b\d[\d,.]*\s*(%|per\s?cent|percent)\s*(less|fewer|lower)\s*(carbon|co2|emissions|waste)",
    re.I,
)

# Model hedging that makes content read as AI slop and adds zero search value.
SLOP_RE = re.compile(
    r"\b(in today's (fast-paced|digital) world|delve into|it's important to note that|"
    r"in conclusion,|unlock the (power|potential)|game-?changer|revolutioniz|"
    r"navigating the (world|landscape) of|when it comes to)\b",
    re.I,
)

MIN_WORDS = 700
MAX_WORDS = 1600


def validate(site_key, cfg, post):
    """Return list of failures. Empty list == publishable."""
    fails = []
    body = post.get("body_html", "")
    text = re.sub(r"<[^>]+>", " ", body)
    words = len(text.split())

    if words < MIN_WORDS:
        fails.append(f"too short: {words} words (min {MIN_WORDS})")
    if words > MAX_WORDS:
        fails.append(f"too long: {words} words (max {MAX_WORDS})")
    if not post.get("title"):
        fails.append("missing title")
    if not post.get("meta_description"):
        fails.append("missing meta_description")
    elif not (110 <= len(post["meta_description"]) <= 160):
        fails.append(f"meta_description {len(post['meta_description'])} chars (need 110-160)")

    if site_key in ("repairrange", "selfrepairkit", "mayfieldgadgets"):
        m = PRICE_RE.search(text)
        if m:
            fails.append(f"PRICE VIOLATION: found {m.group(0)!r} — prices are never invented")

    if site_key == "mayfieldgadgets":
        m = CO2_RE.search(text)
        if m:
            fails.append(f"ENVIRONMENTAL CLAIM VIOLATION: found {m.group(0)!r}")

    slop = set(m.group(0).lower() for m in SLOP_RE.finditer(text))
    if slop:
        fails.append(f"slop phrases: {sorted(slop)}")

    # At least one internal link, no more than four.
    links = re.findall(r'href="(https?://[^"]+)"', body)
    internal = [l for l in links if any(l.startswith(d.rstrip("/")) for d in
                [cfg["domain"]] + cfg.get("internal_links", []))]
    if not internal:
        fails.append("no internal links")
    if len(links) > 4:
        fails.append(f"{len(links)} outbound links (max 4)")

    # Mayfield Phone Repair link must appear at most once (PBN hygiene).
    mpr = [l for l in links if "mayfieldphonerepair.com.au" in l]
    if len(mpr) > 1:
        fails.append(f"{len(mpr)} links to mayfieldphonerepair.com.au (max 1)")

    return fails


# ---------------------------------------------------------------- topic queue

def peek_topic(site_key, offset=0):
    """Read the next topic WITHOUT consuming it. Nothing is burned until publish."""
    q = ROOT / "topics" / f"{site_key}.txt"
    lines = [l.strip() for l in q.read_text().splitlines()]
    live = [l for l in lines if l and not l.startswith("#")]
    if len(live) <= offset:
        raise SystemExit(f"[{site_key}] topic queue empty — refill topics/{site_key}.txt")
    return live[offset]


def consume_topic(site_key, topic):
    """Called ONLY after a post is successfully written/published."""
    q = ROOT / "topics" / f"{site_key}.txt"
    used = ROOT / "topics" / f"{site_key}_used.txt"
    lines = [l.strip() for l in q.read_text().splitlines()]
    q.write_text("\n".join(l for l in lines if l != topic) + "\n")
    with used.open("a") as f:
        f.write(f"{dt.date.today().isoformat()}\t{topic}\n")


# ---------------------------------------------------------------- llm

def build_prompt(site_key, cfg, topic):
    guards = "\n".join(f"- {g}" for g in cfg.get("guardrails", []))
    links = "\n".join(f"- {l}" for l in cfg.get("internal_links", []))
    return f"""You are writing one blog post for {cfg['domain']}.

TOPIC: {topic}

VOICE: {cfg['voice']}

NON-NEGOTIABLE RULES — a single breach makes the post unusable:
{guards}
- Australian spelling throughout (organise, colour, centre, metre, licence as noun).
- No em dashes. Use commas or full stops.
- Never open with "In today's world", "When it comes to", "Delve", "Unlock", "Game-changer", "Navigating the landscape of", or any variant. No "In conclusion".
- No filler. If a sentence does not carry information, delete it.
- Do not fabricate statistics, studies, survey results, dates or named sources. If you cannot verify it, do not write it.
- 900 to 1300 words.
- Between 1 and 3 links total, drawn ONLY from this list, placed where a reader would actually want them:
{links}

STRUCTURE:
- One H1 (the title).
- 3 to 5 H2 sections. Use H3 only if a section genuinely needs it.
- Short paragraphs, two to four sentences.
- Lead with the answer. Do not warm up.

Return ONLY a JSON object, no markdown fences, no preamble:
{{
  "title": "under 60 characters, contains the primary keyword, not clickbait",
  "slug": "lowercase-hyphenated-max-6-words",
  "meta_description": "110 to 160 characters, describes the payoff",
  "body_html": "<h1>...</h1><p>...</p> — semantic HTML only: h1 h2 h3 p ul ol li a strong em. No divs, no classes, no inline styles, no scripts."
}}"""


def call_gemini(prompt):
    key = os.environ["GEMINI_API_KEY"]
    url = ("https://generativelanguage.googleapis.com/v1beta/models/"
           f"gemini-1.5-flash:generateContent?key={key}")
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.85, "maxOutputTokens": 4096,
                             "responseMimeType": "application/json"},
    }
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"})
    
    max_attempts = 6
    for attempt in range(max_attempts):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.loads(r.read())
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_attempts - 1:
                ra = e.headers.get("Retry-After")
                wait = int(ra) if (ra and ra.isdigit()) else min(60, 2 ** attempt) + random.uniform(0, 1)
                print(f"  [429] rate-limited, retry {attempt+1}/{max_attempts} in {wait:.1f}s")
                time.sleep(wait)
                continue
            raise


def call_anthropic(prompt):
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps({
            "model": "claude-sonnet-4-6",
            "max_tokens": 4096,
            "temperature": 0.85,
            "messages": [{"role": "user", "content": prompt}],
        }).encode(),
        headers={
            "Content-Type": "application/json",
            "x-api-key": os.environ["ANTHROPIC_API_KEY"],
            "anthropic-version": "2023-06-01",
        })
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.loads(r.read())
    return "".join(b.get("text", "") for b in data["content"])


def generate(site_key, cfg, topic, attempts=3):
    provider = os.environ.get("LLM_PROVIDER", "gemini")
    need = "ANTHROPIC_API_KEY" if provider == "anthropic" else "GEMINI_API_KEY"
    if need not in os.environ:
        raise SystemExit(
            f"{need} is not set. LLM_PROVIDER={provider}.\n"
            f"  Locally:  export {need}=...\n"
            f"  In CI:    Settings > CI/CD > Variables (masked + protected)")
    fn = call_anthropic if provider == "anthropic" else call_gemini
    prompt = build_prompt(site_key, cfg, topic)
    last_fails = []
    for i in range(1, attempts + 1):
        raw = fn(prompt if i == 1 else
                 prompt + "\n\nYour previous attempt was rejected for: "
                 + "; ".join(last_fails) + "\nFix every one of these.")
        raw = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.M).strip()
        try:
            post = json.loads(raw)
        except json.JSONDecodeError as e:
            last_fails = [f"invalid JSON: {e}"]
            print(f"  attempt {i}: {last_fails[0]}")
            continue
        fails = validate(site_key, cfg, post)
        if not fails:
            print(f"  attempt {i}: passed validation")
            return post
        last_fails = fails
        print(f"  attempt {i} rejected: {fails}")
    raise SystemExit(2)


# ---------------------------------------------------------------- adapters

def publish_git(site_key, cfg, post, dry):
    """Writes an HTML file into the repo. CI commits and pushes it."""
    site_root = pathlib.Path(os.environ.get("SITE_ROOT", "."))
    tpl = (ROOT / "templates" / f"{site_key}.html").read_text()
    today = dt.date.today()
    html = (tpl
            .replace("{{TITLE}}", post["title"])
            .replace("{{META}}", post["meta_description"])
            .replace("{{SLUG}}", post["slug"])
            .replace("{{DATE_ISO}}", today.isoformat())
            .replace("{{DATE_HUMAN}}", today.strftime("%d %B %Y"))
            .replace("{{DOMAIN}}", cfg["domain"])
            .replace("{{BODY}}", post["body_html"]))
    out = site_root / cfg["blog_dir"] / f"{post['slug']}.html"
    url = f"{cfg['domain']}/{cfg['blog_dir']}/{post['slug']}.html"
    if dry:
        print(f"  [dry-run] would write {out}")
        return url
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)

    # Append to sitemap rather than regenerating.
    # Gitpage's generate_sitemap tool overwrites CI output — verify after any manual run.
    sm = site_root / cfg["sitemap_file"]
    if sm.exists():
        entry = (f"  <url><loc>{url}</loc>"
                 f"<lastmod>{today.isoformat()}</lastmod>"
                 f"<changefreq>monthly</changefreq><priority>0.6</priority></url>\n")
        txt = sm.read_text()
        if url not in txt:
            sm.write_text(txt.replace("</urlset>", entry + "</urlset>"))
    print(f"  wrote {out}")
    return url


def publish_lms(site_key, cfg, post, dry):
    """Pushes to LaunchMyStore via REST. Requires LMS_API_TOKEN."""
    token = os.environ.get("LMS_API_TOKEN")
    if not token:
        raise SystemExit("LMS_API_TOKEN not set — cannot publish to LaunchMyStore")
    body = {
        "store_id": cfg["store_id"],
        "title": post["title"],
        "handle": post["slug"],
        "content": post["body_html"],
        "seo_title": post["title"],
        "seo_description": post["meta_description"],
        "status": "published" if cfg["autopublish"] else "draft",
    }
    url = f"{cfg['domain']}/blogs/{post['slug']}"
    if dry:
        print(f"  [dry-run] would POST blog {post['slug']} to store {cfg['store_id']}")
        return url
    req = urllib.request.Request(
        "https://api.launchmystore.io/v1/blogs",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        resp = json.loads(r.read())
    print(f"  LaunchMyStore responded: {resp.get('id', resp)}")
    return url


ADAPTERS = {"git": publish_git, "launchmystore": publish_lms}


# ---------------------------------------------------------------- run

def run_site(site_key, dry):
    cfg = CONFIG[site_key]
    print(f"[{site_key}] {cfg['domain']}")
    results = []
    for i in range(cfg.get("posts_per_run", 1)):
        if i > 0:
            time.sleep(4)  # respect RPM limits
        topic = peek_topic(site_key, offset=i)
        print(f"  topic: {topic}")
        post = generate(site_key, cfg, topic)
        url = ADAPTERS[cfg["adapter"]](site_key, cfg, post, dry)
        if not dry:
            consume_topic(site_key, topic)   # only now is it burned
        results.append({
            "site": site_key,
            "title": post["title"],
            "url": url,
            "state": "PUBLISHED" if cfg["autopublish"] else "DRAFT — needs your approve",
            "meta": post["meta_description"],
        })
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-email", action="store_true")
    a = ap.parse_args()

    keys = list(CONFIG) if a.site == "all" else [a.site]
    for k in keys:
        if k not in CONFIG:
            raise SystemExit(f"unknown site {k!r}; known: {list(CONFIG)}")

    all_results = []
    for k in keys:
        all_results += run_site(k, a.dry_run)

    if all_results and not a.no_email and not a.dry_run:
        from notify import send
        send(all_results)
        print("email sent")

    print(json.dumps(all_results, indent=2))


if __name__ == "__main__":
    main()

