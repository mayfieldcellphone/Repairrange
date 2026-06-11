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
# 1. Google AI Studio (Gemini) Free API Key
# Get your free key at: https://aistudio.google.com/
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAhSJXdqCwOGd0o5laOQkU1Yl_QLWf_cXQ")

# 2. GitLab Repository Details for RepairRange.io
GITLAB_TOKEN = os.environ.get("GITLAB_TOKEN", "glpat-hRoTs91bL94GiUsNmHljCmM6MQpvOjEKdTpsdG44dQ8.01.1709y1suj")
PROJECT_PATH = "mayfield276%2Fblank-site-2026-05-06-6rrng"

# 3. RSS Feeds to Source News From (Tech, Repair & Unlock related)
RSS_FEEDS = [
    "https://www.gsmarena.com/rss-news-reviews.php3",
    "https://techcrunch.com/category/gadgets/feed/",
    "https://www.xda-developers.com/feed/",
    "https://www.androidpolice.com/feed/",
    "https://www.macrumors.com/macrumors.xml"
]

def fetch_rss_articles():
    """Fetches and parses the latest articles from RSS feeds."""
    print("Fetching articles from RSS feeds...")
    articles = []
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    for feed_url in RSS_FEEDS:
        try:
            req = urllib.request.Request(feed_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                
                # Parse Channel Items
                for item in root.findall('.//item')[:3]:  # Grab top 3 from each feed
                    title = item.find('title').text if item.find('title') is not None else ""
                    link = item.find('link').text if item.find('link') is not None else ""
                    desc = item.find('description').text if item.find('description') is not None else ""
                    
                    # Clean description from HTML tags
                    desc_clean = re.sub('<[^<]+?>', '', desc)[:300]
                    
                    if title:
                        articles.append({
                            'title': title,
                            'link': link,
                            'summary': desc_clean
                        })
        except Exception as e:
            print(f"Error fetching feed {feed_url}: {e}")
            
    return articles

def ask_gemini_to_rewrite(article):
    """Sends the article to the Google AI Studio Gemini Free API to rewrite & localize."""
    if GEMINI_API_KEY == "YOUR_FREE_GEMINI_API_KEY_HERE":
        print("Error: Please set your GEMINI_API_KEY environment variable.")
        return None
        
    print(f"Asking Gemini to rewrite and localize: '{article['title']}'...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    # Dynamic check if the article is about unlocking, FRP, iCloud, or bypass
    combined_text = (article['title'] + " " + article['summary']).lower()
    is_unlock = any(kw in combined_text for kw in ["unlock", "bypass", "frp", "icloud", "activation lock", "google lock", "bootloader", "passcode", "reset", "firmware", "patch", "recovery", "password"])
    
    if is_unlock:
        prompt = f"""
    You are an expert Australian tech journalist, mobile security specialist, and phone repair expert writing for RepairRange.io (an independent Australian phone repair price directory).
    
    Take this tech news or mobile security/unlocking article and rewrite it into a highly detailed, comprehensive tutorial or technical guide.
    
    Original Title: {article['title']}
    Original Summary: {article['summary']}
    Source Link: {article['link']}
    
    Constraints:
    1. Write in a professional, engaging, localized Australian tone (use spelling like 'centre' instead of 'center', 'colour' instead of 'color', referencing 'Australia', 'Aussie tech', or 'AUD' where relevant).
    2. Rewrite the content 100% in your own words so that it is completely unique and passes Google's duplicate/scraped content checks.
    3. Structure the article into 3-4 clear, logical sections. Each section MUST start with an engaging, localized sub-heading wrapped in <h2> tags.
    4. For any safety warnings (such as avoiding malicious or sketchy executable download sites), wrap the entire block inside a `<div class="warn-box"><p><strong>⚠️ Warning:</strong> ...</p></div>` container. Wrap helpful tips inside `<div class="tip-box"><p><strong>✅ Good to know:</strong> ...</p></div>`.
    5. For monetization, dynamically include high-converting callout buttons wrapping affiliate programs:
       - If iOS/iCloud: Highlight 'Wondershare Dr.Fone (Screen Unlock)' [https://partner.wondershare.com/affiliate-program.html] or 'iMyFone LockWiper' [https://www.imyfone.com/join-affiliate/].
       - If Android/FRP: Highlight 'Tenorshare 4uKey for Android' [https://www.tenorshare.com/affiliate.html] or 'Wondershare Dr.Fone'.
    6. Include a clear call-to-action for walk-in services: "If bypassing this lock is too technical, bring it to Mayfield Phone Repair in Newcastle or find a certified workshop on RepairRange.io to get it unlocked safely for $49 AUD."
    7. Provide the output in clean JSON format with exactly four fields: 'title', 'slug', 'summary', and 'html_body' (body of article in clean HTML using <h2>, <h3>, <p>, <strong>, <ul>, and <li> tags, but NO <html>, <body>, or <head> tags).
    
    Output EXACTLY the JSON object, nothing else. Do not wrap it in markdown code blocks.
    """
    else:
        prompt = f"""
    You are an expert Australian tech journalist and mobile phone repair specialist writing for RepairRange.io (an independent Australian phone repair price directory).
    
    Take this tech news article and rewrite it completely into a unique, highly engaging blog post.
    
    Original Title: {article['title']}
    Original Summary: {article['summary']}
    Source Link: {article['link']}
    
    Constraints:
    1. Write in a professional, engaging, localized Australian tone (use spelling like 'centre' instead of 'center', 'colour' instead of 'color', referencing 'Australia', 'Aussie tech', or 'AUD' where relevant).
    2. Rewrite the content 100% in your own words so that it is completely unique and passes Google's duplicate/scraped content checks.
    3. Structure the article into 3-4 clear, logical sections. Each section MUST start with an engaging, localized sub-heading wrapped in <h2> tags. Use <strong> and <p> tags for emphasis and paragraph text. If there are lists or bullet points, wrap them in clean <ul> and <li> tags.
    4. Include a dedicated conclusion section under its own <h2> heading explaining why keeping track of screen and battery repair costs on RepairRange.io is critical for owners of these devices.
    5. Provide the output in clean JSON format with exactly four fields:
       - 'title': Create a new, catchy, click-worthy SEO title.
       - 'slug': A url-friendly slug (e.g., 'new-iphone-screen-durability-trends').
       - 'summary': A brief 1-2 sentence compelling teaser summary of the post to display on blog lists.
       - 'html_body': The body of the article structured in clean HTML (using <h2>, <h3>, <p>, <strong>, <ul>, and <li> tags, but NO <html>, <body>, or <head> tags).
       
    Output EXACTLY the JSON object, nothing else. Do not wrap it in markdown code blocks.
    """
    
    payload = json.dumps({
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=payload, method='POST')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            text_response = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
            
            # Remove potential markdown wrapping if Gemini ignores the system prompt
            if text_response.startswith("```json"):
                text_response = text_response[7:]
            if text_response.endswith("```"):
                text_response = text_response[:-3]
                
            parsed_json = json.loads(text_response.strip())
            return parsed_json
    except Exception as e:
        print(f"Error querying Gemini API: {e}")
        return None

def build_full_html_page(article_data):
    """Wraps the AI-generated HTML body into your site's standard template."""
    today_str = datetime.now().strftime("%B %d, 2026")
    
    template = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Latest Aussie phone repair updates, tech news, and device durability trends from RepairRange.">
    <meta name="author" content="RepairRange">
    <title>{article_data['title']} | RepairRange Blog</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
    <style>
        :root {{ --rr-teal-900:#0c4a45; --rr-teal-700:#0F766E; --rr-amber-600:#d97706; --rr-amber-500:#F59E0B; --rr-ink:#1C1917; --rr-muted:#78716C; --rr-line:#E7E5E4; --rr-paper:#FAFAF9; --rr-paper-2:#F5F5F4; }}
        html {{ scroll-behavior: smooth; }}
        body {{ font-family:'Inter',system-ui,sans-serif; color:var(--rr-ink); background:var(--rr-paper); -webkit-font-smoothing:antialiased; }}
        .font-serif {{ font-family:'Fraunces','Iowan Old Style','Palatino',serif; font-feature-settings:'ss01'; }}
        .font-mono {{ font-family:'JetBrains Mono',ui-monospace,monospace; }}
        .text-teal{{color:var(--rr-teal-700);}} .bg-teal-900{{background:var(--rr-teal-900);}}
        .text-amber{{color:var(--rr-amber-600);}} .bg-amber{{background:var(--rr-amber-500);}}
        .text-ink{{color:var(--rr-ink);}} .text-muted{{color:var(--rr-muted);}} .border-line{{border-color:var(--rr-line);}}
        .bg-paper{{background:var(--rr-paper);}} .bg-paper-2{{background:var(--rr-paper-2);}}
        .display {{ font-family:'Fraunces',serif; font-weight:400; letter-spacing:-0.025em; line-height:1.05; font-variation-settings:'opsz' 144; }}
        .eyebrow {{ font-size:0.75rem; font-weight:600; letter-spacing:0.18em; text-transform:uppercase; color:var(--rr-teal-700); }}
        .header-sticky {{ backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px); background:rgba(250,250,249,0.85); }}
        .ed-link {{ background-image:linear-gradient(currentColor,currentColor); background-position:0 100%; background-repeat:no-repeat; background-size:0% 1px; transition:background-size 220ms ease; }}
        .ed-link:hover {{ background-size:100% 1px; }}
        .btn {{ display:inline-flex; align-items:center; gap:0.5rem; padding:0.75rem 1.25rem; font-weight:600; font-size:0.9375rem; transition:all 200ms ease; border-radius:2px; }}
        .btn-primary {{ background:var(--rr-amber-500); color:var(--rr-ink); box-shadow:0 1px 0 var(--rr-amber-600); }}
        .btn-primary:hover {{ background:var(--rr-amber-600); color:white; transform:translateY(-1px); box-shadow:0 4px 0 var(--rr-amber-600); }}
        .mobile-menu {{ transition:all 300ms ease-in-out; }}
        @media (max-width: 768px) {{ .mobile-menu.hidden{{display:none;}} .mobile-menu:not(.hidden){{display:block;}} }}
        
        /* Prose style overrides for beautiful article typography */
        .prose h2 {{ font-family:'Fraunces',serif; font-size: 1.625rem; font-weight: 500; color: var(--rr-teal-700); margin-top: 2.25rem; margin-bottom: 1rem; border-bottom: 1px solid var(--rr-line); padding-bottom: 0.5rem; }}
        .prose h3 {{ font-family:'Inter',sans-serif; font-size: 1.25rem; font-weight: 600; color: var(--rr-ink); margin-top: 1.75rem; margin-bottom: 0.75rem; }}
        .prose p {{ margin-bottom: 1.25rem; line-height: 1.75; font-size: 1.0625rem; color: #292524; }}
        .prose strong {{ color: var(--rr-ink); font-weight: 600; }}
        .prose ul, .prose ol {{ margin-bottom: 1.25rem; padding-left: 1.5rem; }}
        .prose ul {{ list-style-type: disc; }}
        .prose ol {{ list-style-type: decimal; }}
        .prose li {{ margin-bottom: 0.5rem; line-height: 1.6; font-size: 1.0625rem; }}
    </style>
</head>
<body class="bg-paper text-ink antialiased">
    <header class="header-sticky sticky top-0 z-50 border-b border-line">
        <nav class="max-w-6xl mx-auto px-6 md:px-8 py-4 flex items-center justify-between">
            <a href="/index.html" class="flex items-center gap-2 group">
                <svg width="28" height="28" viewBox="0 0 28 28" fill="none" class="flex-shrink-0"><rect x="1" y="1" width="26" height="26" rx="2" stroke="currentColor" stroke-width="1.5" class="text-teal"/><path d="M8 19 L8 9 L14 9 Q17 9 17 12 Q17 14.5 14.5 14.8 L18 19 M12 14.8 L8 14.8" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" class="text-teal" fill="none"/></svg>
                <span class="font-serif text-2xl font-medium tracking-tight text-ink">RepairRange</span>
            </a>
            <div class="hidden md:flex items-center gap-8 text-sm">
                <a href="/brands.html" class="ed-link font-medium text-ink hover:text-teal">Brands</a>
                <a href="/repair/phone-repair-costs-australia.html" class="ed-link font-medium text-ink hover:text-teal">Repairs</a>
                <a href="/fix.html" class="ed-link font-medium text-ink hover:text-teal">Troubleshoot</a>
                <a href="/calculator.html" class="ed-link font-medium text-ink hover:text-teal">Repair Calculator</a>
                <a href="/locations.html" class="ed-link font-medium text-ink hover:text-teal">Locations</a>
                <a href="/blog.html" class="ed-link font-medium text-teal">Blog</a>
                <a href="/calculator.html" class="btn btn-primary text-sm">Get a Quote <i data-lucide="arrow-right" class="w-4 h-4"></i></a>
            </div>
            <button class="mobile-menu-button md:hidden text-ink" aria-label="Toggle menu"><i data-lucide="menu" class="w-6 h-6"></i></button>
        </nav>
    </header>

    <main class="max-w-3xl mx-auto px-6 py-12 md:py-16">
        <div class="mb-6">
            <a href="/blog.html" class="inline-flex items-center gap-2 text-sm font-medium text-teal hover:underline">
                <i data-lucide="arrow-left" class="w-4 h-4"></i> Back to Blog
            </a>
        </div>
        
        <article class="bg-white border border-line rounded-lg p-8 md:p-12 shadow-sm">
            <header class="mb-8">
                <span class="eyebrow">Tech & Repair Editorial</span>
                <h1 class="font-serif text-3xl md:text-4xl lg:text-5xl font-medium tracking-tight text-ink mt-2 mb-4">{article_data['title']}</h1>
                <p class="text-muted text-sm">Published on {today_str} • Written by RepairRange Editorial</p>
            </header>
            
            <div class="prose max-w-none text-ink leading-relaxed space-y-6">
                {article_data['html_body']}
            </div>
        </article>
    </main>

    <footer class="bg-teal-900 text-white border-t border-white/10">
        <div class="max-w-6xl mx-auto px-6 md:px-8 py-16 md:py-20">
            <div class="grid grid-cols-1 md:grid-cols-12 gap-10 mb-12">
                <div class="md:col-span-5">
                    <div class="flex items-center gap-2 mb-4">
                        <svg width="28" height="28" viewBox="0 0 28 28" fill="none"><rect x="1" y="1" width="26" height="26" rx="2" stroke="white" stroke-width="1.5"/><path d="M8 19 L8 9 L14 9 Q17 9 17 12 Q17 14.5 14.5 14.8 L18 19 M12 14.8 L8 14.8" stroke="white" stroke-width="1.5" stroke-linecap="square" fill="none"/></svg>
                        <span class="font-serif text-2xl font-medium">RepairRange</span>
                    </div>
                    <p class="text-white/70 leading-relaxed max-w-sm text-sm">Plain-English phone repair costs, fixes, and buying advice. Researched by people who actually do this work.</p>
                </div>
                <div class="md:col-span-3"><h3 class="eyebrow text-amber mb-4">Browse</h3><ul class="space-y-2 text-sm"><li><a href="/brands.html" class="text-white/80 hover:text-amber">Brands</a></li><li><a href="/fix.html" class="text-white/80 hover:text-amber">Troubleshooting</a></li><li><a href="/calculator.html" class="text-white/80 hover:text-amber">Cost Calculator</a></li><li><a href="/locations.html" class="text-white/80 hover:text-amber">Cities</a></li><li><a href="/blog.html" class="text-white/80 hover:text-amber">Blog</a></li></ul></div>
                <div class="md:col-span-4"><h3 class="eyebrow text-amber mb-4">About</h3><ul class="space-y-2 text-sm"><li><a href="/about.html" class="text-white/80 hover:text-amber">About RepairRange</a></li><li><a href="/tools/software-stack-for-repair-shops.html" class="text-white/80 hover:text-amber">Tools we recommend</a></li><li><a href="/privacy.html" class="text-white/80 hover:text-amber">Privacy Policy</a></li><li><a href="/terms.html" class="text-white/80 hover:text-amber">Terms of Use</a></li></ul></div>
            </div>
            <div class="pt-8 border-t border-white/15">
                <p class="text-white/50 text-xs leading-relaxed mb-3 max-w-3xl"><strong class="text-white/70">Affiliate disclosure:</strong> RepairRange may earn a commission when you click links to retailers (including Amazon) and complete a purchase. This never affects the price you pay or our editorial recommendations.</p>
                <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3"><p class="text-white/50 text-xs">&copy; 2026 RepairRange. All rights reserved.</p><p class="text-white/50 text-xs">Not affiliated with Apple, Samsung, Google, or any device manufacturer.</p></div>
            </div>
        </div>
    </footer>

    <script>
        // Initialize lucide icons
        lucide.createIcons();
    </script>
</body>
</html>
"""
    return template

def generate_or_update_rss_feed(slug, title, summary):
    """
    Fetches the existing feed.xml from GitLab (if it exists), adds the new article
    as an item, and returns a tuple (updated_xml_content, commit_action_type).
    """
    from datetime import datetime
    import re
    
    # RFC 822 Date format: Sun, 07 Jun 2026 12:00:00 GMT (GMT/UTC is standard)
    rfc_date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    article_link = f"https://repairrange.io/blog/{slug}.html"
    
    base_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>RepairRange Tech News</title>
    <link>https://repairrange.io/blog.html</link>
    <description>Daily Mobile Phone &amp; Tech Repair Pricing Guides &amp; Australian Industry News</description>
    <language>en-au</language>
    <lastBuildDate>{rfc_date}</lastBuildDate>
    <atom:link href="https://repairrange.io/feed.xml" rel="self" type="application/rss+xml" />
    <item>
      <title>{title}</title>
      <link>{article_link}</link>
      <guid isPermaLink="true">{article_link}</guid>
      <pubDate>{rfc_date}</pubDate>
      <description>{summary}</description>
    </item>
  </channel>
</rss>"""

    try:
        raw_feed_url = f"https://gitlab.com/api/v4/projects/{PROJECT_PATH}/repository/files/feed.xml/raw?ref=main"
        req_get = urllib.request.Request(raw_feed_url)
        req_get.add_header('PRIVATE-TOKEN', GITLAB_TOKEN)
        
        with urllib.request.urlopen(req_get) as resp:
            existing_xml = resp.read().decode('utf-8')
            
        if article_link in existing_xml:
            print("Article already exists in feed.xml. Skipping feed update.")
            return existing_xml, "update"
            
        item_pattern = r'<item>.*?</item>'
        existing_items = re.findall(item_pattern, existing_xml, re.DOTALL)
        
        new_item = f"""    <item>
      <title>{title}</title>
      <link>{article_link}</link>
      <guid isPermaLink="true">{article_link}</guid>
      <pubDate>{rfc_date}</pubDate>
      <description>{summary}</description>
    </item>"""
        
        all_items = [new_item] + existing_items
        top_items = all_items[:15]
        
        items_block = "\n".join(top_items)
        
        updated_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>RepairRange Tech News</title>
    <link>https://repairrange.io/blog.html</link>
    <description>Daily Mobile Phone &amp; Tech Repair Pricing Guides &amp; Australian Industry News</description>
    <language>en-au</language>
    <lastBuildDate>{rfc_date}</lastBuildDate>
    <atom:link href="https://repairrange.io/feed.xml" rel="self" type="application/rss+xml" />
{items_block}
  </channel>
</rss>"""
        print("Successfully updated existing feed.xml with the new article.")
        return updated_xml, "update"
        
    except Exception as e:
        print(f"Could not fetch existing feed.xml ({e}). Creating a new one.")
        return base_xml, "create"

def commit_article_to_gitlab(slug, html_content, title, summary):
    """Commits the newly generated article, automatically links it in tech-news.html, and updates feed.xml."""
    file_path = f"blog/{slug}.html"
    print(f"Committing new page to GitLab: {file_path}...")
    
    actions = [{
        "action": "create",
        "file_path": file_path,
        "content": html_content,
        "encoding": "text"
    }]
    
    # Generate and append feed.xml update
    feed_content, feed_action = generate_or_update_rss_feed(slug, title, summary)
    actions.append({
        "action": feed_action,
        "file_path": "feed.xml",
        "content": feed_content,
        "encoding": "text"
    })
    
    # Fetch live tech-news.html to auto-link the post
    try:
        raw_blog_url = f"https://gitlab.com/api/v4/projects/{PROJECT_PATH}/repository/files/tech-news.html/raw?ref=main"
        req_get = urllib.request.Request(raw_blog_url)
        req_get.add_header('PRIVATE-TOKEN', GITLAB_TOKEN)
        
        with urllib.request.urlopen(req_get) as resp:
            blog_content = resp.read().decode('utf-8')
            
        if f"blog/{slug}.html" in blog_content:
            print("Article already linked in tech-news.html. Skipping homepage update.")
        else:
            print("Auto-linking the new article inside tech-news.html...")
            today_month_year = datetime.now().strftime("%B %Y")
            
            # Format post-card layout matching RepairRange standard
            new_card = f"""
            <a href="blog/{slug}.html" class="post-card group">
                <p class="eyebrow mb-3">News &bull; 5 min read &bull; {today_month_year}</p>
                <h2 class="font-serif text-2xl md:text-3xl text-ink mb-3 leading-tight">{title}</h2>
                <p class="text-muted leading-relaxed mb-4">{summary}</p>
                <span class="inline-flex items-center gap-2 text-sm font-medium text-teal">Read the post <i data-lucide="arrow-right" class="w-4 h-4"></i></span>
            </a>
            """
            
            import re
            pattern = r'(<div id="tech-news-container"[^>]*>)(.*?)(</div>)'
            match = re.search(pattern, blog_content, re.DOTALL)
            if match:
                full_match = match.group(0)
                header = match.group(1)
                container_body = match.group(2)
                footer = match.group(3)
                
                # Extract individual cards inside the container
                cards = re.findall(r'<a[^>]+post-card[^>]*>.*?</a>', container_body, re.DOTALL)
                
                # Prepend new card and keep top 9
                all_cards = [new_card.strip()] + [c.strip() for c in cards]
                top_cards = all_cards[:9]
                
                new_container_body = '\n            ' + '\n            '.join(top_cards) + '\n        '
                new_full_container = f"{header}{new_container_body}{footer}"
                updated_blog_content = blog_content.replace(full_match, new_full_container)
                
                actions.append({
                    "action": "update",
                    "file_path": "tech-news.html",
                    "content": updated_blog_content,
                    "encoding": "text"
                })
                print("Successfully queued bounded (max 9) tech-news.html link update.")
            else:
                print("Warning: Could not find the standard #tech-news-container inside tech-news.html.")
    except Exception as e:
        print(f"Could not auto-link in tech-news.html: {e}. Publishing article only.")

    commit_url = f"https://gitlab.com/api/v4/projects/{PROJECT_PATH}/repository/commits"
    
    payload = json.dumps({
        "branch": "main",
        "commit_message": f"Auto-Publish: Added article '{slug}' & auto-linked in tech-news.html",
        "actions": actions
    }).encode('utf-8')
    
    req = urllib.request.Request(commit_url, data=payload, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('PRIVATE-TOKEN', GITLAB_TOKEN)
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"Article successfully published! Commit ID: {result.get('id')}")
            return True
    except Exception as e:
        print(f"Error committing to GitLab: {e}")
        return False

def main():
    if GEMINI_API_KEY == "YOUR_FREE_GEMINI_API_KEY_HERE":
        print("\n=== SYSTEM INSTRUCTION ===")
        print("Please set your Google AI Studio Free Gemini API Key!")
        print("Get your free key in 10 seconds at: https://aistudio.google.com/")
        print("To run, configure your command line with: set GEMINI_API_KEY=your_key")
        print("==========================\n")
        return

    # 1. Fetch RSS feed items
    raw_articles = fetch_rss_articles()
    if not raw_articles:
        print("No articles found in RSS feeds. Exiting.")
        return
        
    # 2. Prioritize unlock/bypass/reset articles first to dominate this niche, fallback to top gadget news
    unlock_keywords = ["unlock", "bypass", "frp", "icloud", "activation lock", "google lock", "bootloader", "passcode", "reset", "firmware", "patch", "recovery", "password"]
    selected_article = None
    
    for art in raw_articles:
        combined_text = (art['title'] + " " + art['summary']).lower()
        if any(kw in combined_text for kw in unlock_keywords):
            selected_article = art
            print(f"Selected High-Target Unlock/Bypass Article: '{art['title']}'")
            break
            
    if not selected_article:
        selected_article = raw_articles[0]
        print(f"Selected Fallback Tech News Article: '{selected_article['title']}'")
    
    # 3. Ask Gemini Free API to localize, expand and rewrite
    ai_content = ask_gemini_to_rewrite(selected_article)
    if not ai_content or 'html_body' not in ai_content:
        print("AI generation failed or returned invalid format. Exiting.")
        return
        
    # 4. Generate the full template HTML page
    full_html = build_full_html_page(ai_content)
    
    # 5. Commit directly to your live website repository!
    commit_article_to_gitlab(ai_content['slug'], full_html, ai_content['title'], ai_content['summary'])

if __name__ == "__main__":
    main()
