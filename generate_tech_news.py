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
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GITLAB_TOKEN = os.environ.get("GITLAB_TOKEN", "")
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
    today_str = datetime.now().strftime("%B %d, %Y")
    dynamic_sidebar_js = """<script>
(function(){var g=[{t:'10 repair myths debunked',u:'phone-repair-myths-debunked.html'},{t:'Phone repair checklist',u:'phone-repair-checklist-before-during-after.html'},{t:'Your warranty rights (ACL)',u:'phone-repair-warranty-australia-consumer-rights.html'},{t:'Finding a trustworthy shop',u:'how-to-find-trustworthy-phone-repair-shop.html'},{t:'iPhone vs Samsung costs',u:'iphone-vs-samsung-repair-cost-comparison.html'},{t:'How long repairs take',u:'how-long-does-phone-repair-take.html'},{t:'DIY screen repair?',u:'can-you-diy-phone-screen-repair.html'},{t:'Screen quality tiers',u:'screen-quality-tiers-oem-aftermarket-refurbished-explained.html'},{t:'Samsung fingerprint trap',u:'samsung-fingerprint-sensor-screen-replacement-guide.html'},{t:'Battery health guide',u:'battery-health-when-to-replace.html'},{t:'eSIM and phone repair',u:'esim-phone-repair-what-happens.html'},{t:'Foldable phone repair',u:'foldable-phone-repair-cost-guide.html'},{t:'iPad repair costs',u:'ipad-repair-cost-guide-australia.html'},{t:'MacBook & laptop costs',u:'macbook-laptop-repair-cost-guide-australia.html'},{t:'Lenovo tablet repair',u:'lenovo-tablet-repair-cost-guide-australia.html'},{t:'S26 Ultra guide',u:'samsung-galaxy-s26-ultra-repair-guide.html'},{t:'iPhone 17 PM guide',u:'iphone-17-pro-max-repair-guide.html'},{t:'Insurance vs self-insuring',u:'phone-insurance-vs-self-insuring-australia.html'},{t:'Fix before selling?',u:'should-you-fix-phone-before-selling.html'},{t:'Repair vs replace',u:'repair-vs-replace-decision-guide.html'}];var m=[{t:'iPhone 17 Pro Max',u:'../repair/iphone-17-pro-max.html'},{t:'iPhone 16 Pro Max',u:'../repair/iphone-16-pro-max.html'},{t:'iPhone 15 Pro Max',u:'../repair/iphone-15-pro-max.html'},{t:'iPhone 15',u:'../repair/iphone-15.html'},{t:'Galaxy S26 Ultra',u:'../repair/samsung-galaxy-s26-ultra.html'},{t:'Galaxy S25 Ultra',u:'../repair/samsung-galaxy-s25-ultra.html'},{t:'Galaxy S24 Ultra',u:'../repair/samsung-galaxy-s24-ultra.html'},{t:'Pixel 9 Pro',u:'../repair/pixel-9-pro.html'},{t:'Pixel 8 Pro',u:'../repair/pixel-8-pro.html'}];var f=[{t:'Water damage',u:'../fix/water-damage.html'},{t:'Won\\'t turn on',u:'../fix/wont-turn-on.html'},{t:'Cracked screen',u:'../fix/cracked-screen-still-works.html'},{t:'Battery drain',u:'../fix/battery-drains-fast.html'},{t:'Ghost touch',u:'../fix/ghost-touch.html'},{t:'Charging issues',u:'../fix/charging-port.html'}];function sh(a){for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t}return a}function rl(arr,n,al,at){var items=sh(arr.slice()).slice(0,n);var h='';for(var i=0;i<items.length;i++)h+='<a href="'+items[i].u+'" class="sidebar-link">'+items[i].t+'</a>';if(al)h+='<a href="'+al+'" class="sidebar-link" style="color:var(--rr-teal-700);font-weight:600">'+at+'</a>';return h}function render(id,arr,n,al,at){var el=document.getElementById(id);if(!el)return;el.innerHTML=el.innerHTML+rl(arr,n,al,at)}render('sb-guides',g,6,'../blog.html','All guides \\u2192');render('sb-models',m,5,'../repair/phone-repair-costs-australia.html','All 75+ models \\u2192');render('sb-fix',f,5,'../fix.html','All 10 guides \\u2192');})()
</script>"""
    template = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{article_data['summary'][:160]}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://repairrange.io/blog/{article_data['slug']}.html">
<title>{article_data['title']} — RepairRange</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script><script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
<style>
:root{{--rr-teal-900:#0c4a45;--rr-teal-700:#0F766E;--rr-amber-600:#d97706;--rr-amber-500:#F59E0B;--rr-ink:#1C1917;--rr-muted:#78716C;--rr-line:#E7E5E4;--rr-paper:#FAFAF9}}
body{{font-family:'Inter',system-ui,sans-serif;color:var(--rr-ink);background:var(--rr-paper);-webkit-font-smoothing:antialiased}}
.font-serif{{font-family:'Fraunces','Palatino',serif;font-feature-settings:'ss01'}}
.text-teal{{color:var(--rr-teal-700)}}.bg-teal-900{{background:var(--rr-teal-900)}}.text-amber{{color:var(--rr-amber-600)}}
.display{{font-family:'Fraunces',serif;font-weight:400;letter-spacing:-0.025em;line-height:1.05}}
.eyebrow{{font-size:0.75rem;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;color:var(--rr-teal-700)}}
.header-sticky{{backdrop-filter:blur(12px);background:rgba(250,250,249,0.85)}}
.ed-link{{background-image:linear-gradient(currentColor,currentColor);background-position:0 100%;background-repeat:no-repeat;background-size:0% 1px;transition:background-size 220ms ease}}.ed-link:hover{{background-size:100% 1px}}
.btn{{display:inline-flex;align-items:center;gap:0.5rem;padding:0.75rem 1.25rem;font-weight:600;font-size:0.9375rem;transition:all 200ms ease;border-radius:2px}}
.btn-primary{{background:var(--rr-amber-500);color:var(--rr-ink);box-shadow:0 1px 0 var(--rr-amber-600)}}.btn-primary:hover{{background:var(--rr-amber-600);color:white}}
.prose p{{margin-bottom:1.5rem;line-height:1.75}}
.prose h2{{font-family:'Fraunces',serif;font-size:1.75rem;font-weight:400;letter-spacing:-0.025em;margin-top:3rem;margin-bottom:1rem}}
.prose h3{{font-size:1.125rem;font-weight:600;margin-top:2rem;margin-bottom:0.75rem}}
.prose a{{color:var(--rr-teal-700);text-decoration:underline;text-underline-offset:2px}}
.sidebar-card{{background:white;border:1px solid var(--rr-line);padding:1.25rem;margin-bottom:1rem}}
.sidebar-card h4{{font-size:0.75rem;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:var(--rr-teal-700);margin-bottom:0.75rem}}
.sidebar-link{{display:block;padding:0.5rem 0;font-size:0.875rem;color:var(--rr-ink);border-bottom:1px solid var(--rr-line);transition:color 150ms}}.sidebar-link:last-child{{border-bottom:none}}.sidebar-link:hover{{color:var(--rr-teal-700)}}
</style>
</head>
<body>
<header class="header-sticky sticky top-0 z-50 border-b" style="border-color:var(--rr-line)"><nav class="max-w-6xl mx-auto px-6 md:px-8 py-4 flex items-center justify-between"><a href="../index.html" class="flex items-center gap-2"><svg width="28" height="28" viewBox="0 0 28 28" fill="none"><rect x="1" y="1" width="26" height="26" rx="2" stroke="currentColor" stroke-width="1.5" class="text-teal"/><path d="M8 19 L8 9 L14 9 Q17 9 17 12 Q17 14.5 14.5 14.8 L18 19 M12 14.8 L8 14.8" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" class="text-teal" fill="none"/></svg><span class="font-serif text-2xl font-medium tracking-tight" style="color:var(--rr-ink)">RepairRange</span></a><div class="hidden md:flex items-center gap-8 text-sm"><a href="../brands.html" class="ed-link font-medium" style="color:var(--rr-ink)">Brands</a><a href="../repair/phone-repair-costs-australia.html" class="ed-link font-medium" style="color:var(--rr-ink)">Repairs</a><a href="../fix.html" class="ed-link font-medium" style="color:var(--rr-ink)">Troubleshoot</a><a href="../calculator.html" class="ed-link font-medium" style="color:var(--rr-ink)">Repair Calculator</a><a href="../locations.html" class="ed-link font-medium" style="color:var(--rr-ink)">Locations</a><a href="../blog.html" class="ed-link font-medium text-teal">Blog</a><a href="../calculator.html" class="btn btn-primary text-sm">Get a Quote</a></div></nav></header>

<article class="max-w-6xl mx-auto px-6 md:px-8 py-16 md:py-24">
<div class="max-w-4xl mb-12">
<nav class="flex items-center gap-2 text-xs" style="color:var(--rr-muted);margin-bottom:2rem"><a href="../index.html" class="ed-link hover:text-teal">Home</a><span>/</span><a href="../blog.html" class="ed-link hover:text-teal">Blog</a><span>/</span><span style="color:var(--rr-ink)">Tech News</span></nav>
<p class="eyebrow mb-4">Tech News · {today_str}</p>
<h1 class="display text-3xl md:text-5xl lg:text-6xl mb-6" style="color:var(--rr-ink)">{article_data['title']}</h1>
<p class="text-lg leading-relaxed" style="color:var(--rr-muted)">{article_data['summary']}</p>
</div>
<div class="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-12">
<div class="lg:col-span-8">
<div class="prose">
{article_data['html_body']}
<p>For repair pricing on any model mentioned: <a href="../calculator.html">Repair Calculator</a> | <a href="../repair/phone-repair-costs-australia.html">All 75+ models</a></p>
</div>
</div>
<aside class="lg:col-span-4">
<div class="lg:sticky lg:top-24 space-y-4">
<div class="sidebar-card" style="background:var(--rr-teal-900);border-color:var(--rr-teal-900)"><h4 style="color:var(--rr-amber-500)">Get a repair quote</h4><p style="color:rgba(255,255,255,0.7);font-size:0.875rem;line-height:1.6;margin-bottom:1rem">Find exact pricing for your phone model.</p><a href="../calculator.html" class="btn btn-primary" style="width:100%;justify-content:center;font-size:0.875rem">Open Repair Calculator</a></div>
<div class="sidebar-card" id="sb-guides"><h4>Popular guides</h4></div>
<div class="sidebar-card" id="sb-models"><h4>Popular models</h4></div>
<div class="sidebar-card" id="sb-fix"><h4>Fix it yourself?</h4></div>
</div>
</aside>
</div>
</article>

<footer class="bg-teal-900 text-white" style="border-top:1px solid rgba(255,255,255,0.1)"><div class="max-w-6xl mx-auto px-6 md:px-8 py-16"><div class="pt-8" style="border-top:1px solid rgba(255,255,255,0.15)"><p style="color:rgba(255,255,255,0.5);font-size:0.75rem">&copy; 2026 RepairRange. Not affiliated with any manufacturer.</p></div></div></footer>
<script>if(window.lucide)window.lucide.createIcons();</script>
{dynamic_sidebar_js}
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
<a href="blog/{slug}.html" class="post-card group">
<p class="eyebrow mb-2" style="font-size:0.65rem">News \u00b7 {datetime.now().strftime("%B %Y")}</p>
<h2 class="font-serif text-xl text-ink mb-2 leading-tight">{title}</h2>
<p class="text-muted text-sm leading-relaxed mb-3 line-clamp-3">{summary[:200]}</p>
<span class="inline-flex items-center gap-2 text-xs font-medium text-teal">Read more <i data-lucide="arrow-right" class="w-3 h-3"></i></span>
</a>"""
        
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
