import urllib.request
import json
import xml.etree.ElementTree as ET
import re
import os
import sys
from datetime import datetime

# ==========================================
# CONFIGURATION & CREDENTIALS
# ==========================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAhSJXdqCwOGd0o5laOQkU1Yl_QLWf_cXQ")
GITLAB_TOKEN = os.environ.get("GITLAB_TOKEN", "glpat-hRoTs91bL94GiUsNmHljCmM6MQpvOjEKdTpsdG44dQ8.01.1709y1suj")
PROJECT_PATH = "mayfield276%2Fblank-site-2026-05-06-6rrng"

RSS_FEEDS = [
    "https://www.gsmarena.com/rss-news-reviews.php3",
    "https://techcrunch.com/category/gadgets/feed/",
    "https://www.xda-developers.com/feed/",
    "https://www.androidpolice.com/feed/",
    "https://www.macrumors.com/macrumors.xml"
]

def fetch_rss_articles():
    print("Fetching articles from RSS feeds...")
    articles = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    for feed_url in RSS_FEEDS:
        try:
            req = urllib.request.Request(feed_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                for item in root.findall(".//item")[:3]:
                    title = item.find("title").text if item.find("title") is not None else ""
                    link = item.find("link").text if item.find("link") is not None else ""
                    desc = item.find("description").text if item.find("description") is not None else ""
                    desc_clean = re.sub("<[^<]+?>", "", desc)[:300]
                    if title:
                        articles.append({"title": title, "link": link, "summary": desc_clean})
        except Exception as e:
            print(f"Error fetching feed {feed_url}: {e}")
    return articles

def ask_gemini_to_rewrite(article):
    print(f"Asking Gemini to rewrite and localize: '{article['title']}'...")
    # FIXED: Using stable gemini-1.5-flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"""
    You are an expert Australian tech journalist writing for RepairRange.io.
    Rewrite this article into a unique, localized guide or blog post.
    
    Article: {article['title']}
    Summary: {article['summary']}
    
    Constraints:
    1. Aussie tone (spellings like 'centre', 'colour').
    2. Unique content for SEO.
    3. Structure with <h2> headings.
    4. Provide JSON: {{"title", "slug", "summary", "html_body", "icon"}}.
    5. For "icon", choose ONE Lucide icon name from: [cpu, smartphone, shield-check, wrench, zap, activity, lock, unlock, monitor, battery, help-circle, alert-triangle].
    """
    
    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            text_response = res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
            if text_response.startswith("```json"): text_response = text_response[7:]
            if text_response.endswith("```"): text_response = text_response[:-3]
            return json.loads(text_response.strip())
    except Exception as e:
        print(f"Error querying Gemini API: {e}")
        return None

def build_full_html_page(article_data):
    today_str = datetime.now().strftime("%B %d, 2026")
    template = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article_data["title"]} | RepairRange Blog</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
    <style>
        :root{{--rr-teal-900:#0f172a;--rr-teal-700:#0d9488;--rr-amber-500:#f59e0b;--rr-ink:#1e293b;--rr-muted:#64748b;--rr-line:#e2e8f0;--rr-paper:#f8fafc}}
        body{{font-family:'Inter',sans-serif;color:var(--rr-ink);background:var(--rr-paper)}}
        .display{{font-family:'Fraunces',serif;font-weight:700;letter-spacing:-0.025em}}
        .prose h2{{font-family:'Fraunces',serif;font-size:1.75rem;color:var(--rr-teal-700);margin-top:2rem;border-bottom:1px solid var(--rr-line);padding-bottom:0.5rem}}
        .prose p{{margin-bottom:1.25rem;line-height:1.75}}
    </style>
</head>
<body class="p-6 md:p-12">
    <main class="max-w-3xl mx-auto">
        <header class="mb-8">
            <h1 class="display text-4xl md:text-5xl mb-4">{article_data["title"]}</h1>
            <p class="text-muted">Published on {today_str} • Written by RepairRange Editorial</p>
        </header>
        <article class="prose">
            {article_data["html_body"]}
        </article>
    </main>
    <script>lucide.createIcons();</script>
</body>
</html>"""
    return template

def commit_article_to_gitlab(slug, html_content, title, summary, icon="zap"):
    actions = [
        {"action": "create", "file_path": f"blog/{slug}.html", "content": html_content, "encoding": "text"}
    ]
    
    try:
        raw_blog_url = f"https://gitlab.com/api/v4/projects/{PROJECT_PATH}/repository/files/tech-news.html/raw?ref=main"
        req_get = urllib.request.Request(raw_blog_url)
        req_get.add_header("PRIVATE-TOKEN", GITLAB_TOKEN)
        with urllib.request.urlopen(req_get) as resp:
            blog_content = resp.read().decode("utf-8")
        
        new_card = f"""
        <a href="blog/{slug}.html" class="post-card group flex flex-col h-full bg-white border border-line hover:border-teal hover:shadow-xl transition-all rounded-xl overflow-hidden shadow-sm">
            <div class="h-32 bg-slate-50 border-b border-line flex items-center justify-center group-hover:bg-teal/5 transition-colors">
                <i data-lucide=\"{icon}\" class=\"w-12 h-12 text-teal/30 group-hover:text-teal group-hover:scale-110 transition-all\"></i>
            </div>
            <div class="p-6">
                <p class="eyebrow text-[10px] mb-2 font-bold text-teal/60">News \u2022 {datetime.now().strftime("%B %Y")}</p>
                <h2 class="font-serif text-xl md:text-2xl text-ink mb-3 leading-tight group-hover:text-teal transition-colors">{title}</h2>
                <p class="text-muted text-xs leading-relaxed mb-4 line-clamp-3">{summary}</p>
                <span class=\"inline-flex items-center gap-2 text-[10px] font-bold text-teal tracking-widest uppercase\">Read Full Guide <i data-lucide=\"arrow-right\" class=\"w-4 h-4\"></i></span>
            </div>
        </a>
        """
        
        pattern = r'(<div id="tech-news-container"[^>]*>)(.*?)(</div>)'
        match = re.search(pattern, blog_content, re.DOTALL)
        if match:
            cards = re.findall(r'<a[^>]+post-card[^>]*>.*?</a>', match.group(2), re.DOTALL)
            all_cards = [new_card.strip()] + [c.strip() for c in cards]
            new_container_body = '\n            ' + '\n            '.join(all_cards[:12]) + '\n        '
            updated_blog_content = blog_content.replace(match.group(0), f"{match.group(1)}{new_container_body}{match.group(3)}")
            actions.append({"action": "update", "file_path": "tech-news.html", "content": updated_blog_content, "encoding": "text"})

    except Exception as e:
        print(f"Error updating tech-news: {e}")

    commit_url = f"https://gitlab.com/api/v4/projects/{PROJECT_PATH}/repository/commits"
    payload = json.dumps({"branch": "main", "commit_message": f"Stability Fix: Correct Gemini Model ID for automated news", "actions": actions}).encode("utf-8")
    req = urllib.request.Request(commit_url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("PRIVATE-TOKEN", GITLAB_TOKEN)
    urllib.request.urlopen(req)

def main():
    articles = fetch_rss_articles()
    if not articles: return
    ai_content = ask_gemini_to_rewrite(articles[0])
    if not ai_content: return
    full_html = build_full_html_page(ai_content)
    commit_article_to_gitlab(ai_content["slug"], full_html, ai_content["title"], ai_content["summary"], ai_content.get("icon", "zap"))

if __name__ == "__main__": main()
