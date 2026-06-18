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
    today_str = datetime.now().strftime("%B %d, %Y")
    template = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-CWRGPBDWZD"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-CWRGPBDWZD');
</script>

<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{article_data['summary'][:160]}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://repairrange.io/blog/{article_data['slug']}.html">
<title>{article_data['title']} | RepairRange Technical Briefing</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script><script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
<style>
:root{{
  --rr-teal-900:#0f172a; --rr-teal-700:#0d9488; --rr-amber-600:#d97706; --rr-amber-500:#F59E0B; --rr-ink:#1e293b; --rr-muted:#64748b; --rr-line:#e2e8f0; --rr-paper:#f8fafc;
}}
html{{scroll-behavior:smooth}}
body{{font-family:'Inter',system-ui,sans-serif;color:var(--rr-ink);background:var(--rr-paper);-webkit-font-smoothing:antialiased}}
.font-serif{{font-family:'Fraunces','Iowan Old Style','Palatino',serif;font-feature-settings:'ss01'}}
.text-teal{{color:var(--rr-teal-700)}}.bg-teal-900{{background:var(--rr-teal-900)}}.text-amber{{color:var(--rr-amber-600)}}
.display{{font-family:'Fraunces',serif;font-weight:400;letter-spacing:-0.025em;line-height:1.05}}
.eyebrow{{font-size:0.75rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--rr-teal-700)}}
.header-sticky{{backdrop-filter:blur(12px);background:rgba(248,250,252,0.85)}}
.btn{{display:inline-flex;align-items:center;gap:0.5rem;padding:0.75rem 1.25rem;font-weight:600;font-size:0.9375rem;transition:all 200ms ease;border-radius:8px}}
.btn-primary{{background:var(--rr-amber-500);color:var(--rr-teal-900);box-shadow:0 1px 0 var(--rr-amber-600)}}
.prose h2{{font-family:'Fraunces',serif;font-size:1.75rem;color:var(--rr-teal-700);margin-top:2.5rem;border-bottom:1px solid var(--rr-line);padding-bottom:0.5rem}}
.prose p{{margin-bottom:1.5rem;line-height:1.8;font-size:1.05rem}}
.sidebar-card{{background:white;border:1px solid var(--rr-line);border-radius:12px;padding:1.5rem;margin-bottom:1.5rem}}
</style>
</head>
<body>
<header class="header-sticky sticky top-0 z-50 border-b border-line">
<nav class="max-w-7xl mx-auto px-6 md:px-8 py-4 flex items-center justify-between">
<a href="../index.html" class="flex items-center gap-2">
    <svg width="28" height="28" viewBox="0 0 28 28" fill="none"><rect x="1" y="1" width="26" height="26" rx="2" stroke="currentColor" stroke-width="1.5" class="text-teal"/><path d="M8 19 L8 9 L14 9 Q17 9 17 12 Q17 14.5 14.5 14.8 L18 19 M12 14.8 L8 14.8" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" class="text-teal" fill="none"/></svg>
    <span class="font-serif text-2xl font-medium tracking-tight text-ink">RepairRange</span>
</a>
<div class="hidden md:flex items-center gap-8 text-sm">
    <a href="../brands.html" class="font-medium text-ink hover:text-teal">Brands</a>
    <a href="../repair/phone-repair-costs-australia.html" class="font-medium text-ink hover:text-teal">Repairs</a>
    <a href="../fix.html" class="font-medium text-ink hover:text-teal">Troubleshoot</a>
    <a href="../blog.html" class="font-medium text-ink hover:text-teal">Blog</a>
    <a href="../calculator.html" class="btn btn-primary text-sm">Get a Quote</a>
</div>
</nav>
</header>

<main class="max-w-full">
<div class="max-w-4xl mb-16">
<nav class="flex items-center gap-2 text-xs text-muted mb-8"><a href="../index.html" class="hover:text-teal">Home</a><span>/</span><a href="../blog.html" class="hover:text-teal">Blog</a><span>/</span><span class="text-ink font-bold">Tech News</span></nav>
<p class="eyebrow mb-4">Briefing · {today_str}</p>
<h1 class="display text-4xl md:text-6xl text-ink mb-6 leading-tight">{article_data['title']}</h1>
<p class="text-xl text-muted leading-relaxed">{article_data['summary']}</p>
</div>

<div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
    <div class="lg:col-span-8">
        <article class="prose max-w-none text-ink">
            <div class="bg-paper p-8 rounded-3xl border border-line mb-12 flex items-center justify-center">
                <i data-lucide="{article_data.get('icon', 'zap')}" class="w-16 h-16 text-teal/40"></i>
            </div>
            {article_data['html_body']}
            <div class="mt-12 pt-8 border-t border-line text-sm text-muted italic">
                Reported by RepairRange Editorial. Sourced from technical benchmarks across Australia.
            </div>
        </article>
    </div>

    <!-- DYNAMIC SIDEBAR -->
    <aside class="lg:col-span-4 w-full">
        <div class="lg:sticky lg:top-24 space-y-6">
            
            <!-- PROMOTION: SELF REPAIR KIT -->
            <div class="sidebar-card bg-teal-900 text-white border-none shadow-xl">
                <span class="eyebrow text-amber-500 mb-2 block">Premium Option</span>
                <h3 class="font-serif text-2xl mb-3">Self-Repair Kits</h3>
                <p class="text-sm text-white/70 mb-6 leading-relaxed">Fix it yourself with engineer-approved parts and professional toolsets. Save 65% on retail repair costs.</p>
                <a href="https://selfrepairkit.com.au" class="btn btn-primary w-full justify-center">Browse Kits</a>
            </div>

            <!-- PROMOTION: REPAIRBILL -->
            <div class="sidebar-card bg-slate-50 border-2 border-slate-200">
                <div class="flex items-center gap-2 mb-3">
                    <i data-lucide="wrench" class="w-5 h-5 text-teal"></i>
                    <h4 class="font-bold text-sm text-ink m-0">Repair Shop Owner?</h4>
                </div>
                <p class="text-xs text-muted mb-4 leading-relaxed">Manage your repair business with **RepairBill SaaS**. Professional invoicing, parts tracking, and technician management.</p>
                <a href="https://repairbill.shop" class="text-teal font-bold text-xs hover:underline flex items-center gap-1 uppercase tracking-widest">Start Free Trial <i data-lucide="chevron-right" class="w-3 h-3"></i></a>
            </div>

            <!-- DIRECTORY: LOCATIONS -->
            <div class="sidebar-card">
                <h4 class="mb-4">Local Repair Hubs</h4>
                <ul class="space-y-3">
                    <li><a href="../locations/sydney.html" class="text-sm text-ink hover:text-teal flex justify-between">Sydney <span>&rarr;</span></a></li>
                    <li><a href="../locations/melbourne.html" class="text-sm text-ink hover:text-teal flex justify-between">Melbourne <span>&rarr;</span></a></li>
                    <li><a href="../locations/brisbane.html" class="text-sm text-ink hover:text-teal flex justify-between">Brisbane <span>&rarr;</span></a></li>
                    <li><a href="../locations/perth.html" class="text-sm text-ink hover:text-teal flex justify-between">Perth <span>&rarr;</span></a></li>
                </ul>
            </div>

            <!-- PARTNER CTA -->
            <div class="sidebar-card bg-amber-50 border-amber-200">
                <h4 class="text-amber-700 mb-2">Verified Partner</h4>
                <p class="text-xs text-amber-800/70 mb-4">Get listed in our Aussie repair directory and reach 1,000+ local customers monthly.</p>
                <a href="https://selfrepairkit.com.au/pages/wholesale" class="bg-ink text-white px-4 py-2 rounded-lg text-xs font-bold inline-block">Join for $49/6mo</a>
            </div>

        </div>
    </aside>
</div>
</main>

<footer class="bg-teal-900 text-white border-t border-white/10 mt-20">
    <div class="max-w-7xl mx-auto px-6 md:px-8 py-16 md:py-20 text-center">
        <div class="flex items-center justify-center gap-2 mb-8">
            <svg width="28" height="28" viewBox="0 0 28 28" fill="none"><rect x="1" y="1" width="26" height="26" rx="2" stroke="white" stroke-width="1.5"/><path d="M8 19 L8 9 L14 9 Q17 9 17 12 Q17 14.5 14.5 14.8 L18 19 M12 14.8 L8 14.8" stroke="white" stroke-width="1.5" stroke-linecap="square" fill="none"/></svg>
            <span class="font-serif text-2xl font-medium tracking-tight">RepairRange</span>
        </div>
        <p class="text-white/50 text-xs">&copy; 2026 RepairRange. Independent Australian Tech Analysis.</p>
    </div>
</footer>

<script>if(window.lucide)window.lucide.createIcons();</script>
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
    payload = json.dumps({"branch": "main", "commit_message": f"UI Upgrade: Stable Sidebar Template for Blog & News", "actions": actions}).encode("utf-8")
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
