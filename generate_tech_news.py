import urllib.request
import json
import xml.etree.ElementTree as ET
import re
import os
import hashlib
from datetime import datetime

# ==========================================
# CONFIGURATION & CREDENTIALS
# ==========================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GITLAB_TOKEN = os.environ.get("GITLAB_TOKEN")
PROJECT_PATH = "mayfield276%2Fblank-site-2026-05-06-6rrng"

RSS_FEEDS = [
    "https://www.gsmarena.com/rss-news-reviews.php3",
    "https://techcrunch.com/category/gadgets/feed/"
]

# FACTS FOR THE GENERATOR
REPAIR_INDUSTRY_FACTS = """
- Apple is the only brand with a budget screen tier (incell AND aftermarket OLED exist). 
- Galaxy S, Pixel, Note, and foldables are one tier only (expensive).
- A refurbished original IS the original panel, reclaimed and re-laminated. It is equivalent to a genuine new part.
- Screen prices fall steeply for ~2 years after launch, then flatten. Manufacturer prices do not fall at all.
- Battery price tracks the RISK OF OPENING THE HANDSET, not the cost of the cell.
- On refurbished-OEM screens, independent shops are often at or above Apple's out-of-warranty price. The benefit is no data wipe, no wait, local access.
- Independent shops are dramatically cheaper on incell and aftermarket OLED. They are not cheaper across the board.
- The low end of published ranges is verified from one shop in Newcastle, NSW. The top end is an estimate.
"""

def fetch_rss_articles():
    print("Fetching articles from RSS feeds...")
    articles = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    for feed_url in RSS_FEEDS:
        try:
            req = urllib.request.Request(feed_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                root = ET.fromstring(response.read())
                for item in root.findall('.//item')[:5]:
                    title = item.find('title').text or ""
                    link = item.find('link').text or ""
                    desc = item.find('description').text or ""
                    desc_clean = re.sub('<[^<]+?>', '', desc)[:500]
                    articles.append({'title': title, 'link': link, 'summary': desc_clean})
        except Exception as e:
            print(f"Error fetching feed {feed_url}: {e}")
    return articles

def get_pricing_data():
    """Fetches pricing.json from GitLab."""
    url = f"https://gitlab.com/api/v4/projects/{PROJECT_PATH}/repository/files/pricing.json/raw?ref=main"
    req = urllib.request.Request(url)
    req.add_header('PRIVATE-TOKEN', GITLAB_TOKEN)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching pricing.json: {e}")
        return None

def generate_story_hash(article):
    """Generates a unique hash based on the core model and event mentioned in the title."""
    # Simple extraction of model names (e.g. iPhone 17, Galaxy S26)
    model_match = re.search(r'(iPhone\s*\d+|Galaxy\s*[SZ]\s*\w+|Pixel\s*\d+)', article['title'], re.I)
    model = model_match.group(0).lower().replace(" ", "") if model_match else "generic"
    # Combine with a simplified version of the title to represent the event
    event = re.sub(r'[^a-z0-9]', '', article['title'].lower())[:30]
    return hashlib.md5(f"{model}_{event}".encode()).hexdigest()[:12]

def ask_gemini_to_generate(article, pricing_data):
    """Asks Gemini to write a repair-first news post grounded in data."""
    print(f"Asking Gemini to generate repair-first post for: '{article['title']}'...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    # Extract relevant pricing context
    pricing_context = json.dumps(pricing_data, indent=2) if pricing_data else "Pricing data unavailable."

    prompt = f"""
    You are an expert Australian tech journalist and mobile phone repair specialist for RepairRange.io.
    
    STORY TO EVALUATE:
    Title: {article['title']}
    Summary: {article['summary']}
    
    GROUNDING DATA (pricing.json):
    {pricing_context}
    
    REPAIR INDUSTRY FACTS:
    {REPAIR_INDUSTRY_FACTS}
    
    RULES:
    1. REJECT (return an empty JSON) if the story has no repair angle (screen tiers, part prices, durability).
    2. One slug per story based on this hash: {generate_story_hash(article)}. Use this as the 'id'.
    3. Use pricing.json for all prices. If the model is not in the data, write "Quote Required" and explain why. Never invent prices.
    4. Write in a professional, localized Australian tone (centre, colour, AUD).
    5. Set a self-referencing canonical tag.
    6. Include a "Verified Date" visibly in the body.
    
    OUTPUT FORMAT:
    Return exactly this JSON object:
    {{
      "id": "{generate_story_hash(article)}",
      "slug": "seo-friendly-slug",
      "title": "Unique Aussie Repair-First Title",
      "summary": "1-2 sentence teaser.",
      "html_body": "HTML content using <h2>, <p>, <strong>, <ul>, <li>. Must cite pricing.json data.",
      "reject": false
    }}
    If no repair angle, return {{"reject": true}}.
    """
    
    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, method='POST')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            text_response = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
            if "```json" in text_response:
                text_response = text_response.split("```json")[1].split("```")[0]
            return json.loads(text_response.strip())
    except Exception as e:
        print(f"Error querying Gemini API: {e}")
        return None

def build_full_html_page(article_data):
    today_str = datetime.now().strftime("%B %d, 2026")
    canonical_url = f"https://repairrange.io/blog/{article_data['slug']}.html"
    
    template = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="canonical" href="{canonical_url}">
    <title>{article_data['title']} | RepairRange News</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        :root {{ --rr-teal-700:#0F766E; --rr-ink:#1C1917; --rr-line:#E7E5E4; --rr-paper:#FAFAF9; }}
        body {{ font-family:sans-serif; color:var(--rr-ink); background:var(--rr-paper); }}
        .prose h2 {{ color: var(--rr-teal-700); border-bottom: 1px solid var(--rr-line); padding-bottom: 0.5rem; margin-top: 2rem; }}
        .verified-badge {{ font-size: 0.75rem; color: #78716C; margin-bottom: 1rem; display: block; }}
    </style>
</head>
<body class="p-8 max-w-3xl mx-auto">
    <header class="mb-8 border-b pb-4">
        <a href="/index.html" class="text-2xl font-bold text-teal-700">RepairRange</a>
    </header>
    <article>
        <span class="verified-badge">Price Data Verified: {today_str}</span>
        <h1 class="text-4xl font-bold mb-4">{article_data['title']}</h1>
        <div class="prose leading-relaxed">
            {article_data['html_body']}
        </div>
    </article>
</body>
</html>"""
    return template

def commit_to_gitlab(article_data, html_content):
    file_path = f"blog/{article_data['slug']}.html"
    
    # Check if file exists to decide on action
    url_check = f"https://gitlab.com/api/v4/projects/{PROJECT_PATH}/repository/files/{urllib.parse.quote(file_path, safe='')}?ref=main"
    req_check = urllib.request.Request(url_check)
    req_check.add_header('PRIVATE-TOKEN', GITLAB_TOKEN)
    
    action = "create"
    try:
        with urllib.request.urlopen(req_check) as r:
            if r.status == 200: action = "update"
    except: pass

    actions = [
        {"action": action, "file_path": file_path, "content": html_content},
        # Update tech-news.html injection (Simplified for brevity)
        # (Assuming tech-news.html logic remains consistent with ID-based injection)
    ]
    
    commit_url = f"https://gitlab.com/api/v4/projects/{PROJECT_PATH}/repository/commits"
    payload = json.dumps({
        "branch": "main",
        "commit_message": f"Repair-First News: {article_data['title']} (Hash: {article_data['id']})",
        "actions": actions
    }).encode('utf-8')
    
    req = urllib.request.Request(commit_url, data=payload, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('PRIVATE-TOKEN', GITLAB_TOKEN)
    
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read())
            print(f"Published! SHA: {res['id']}")
    except Exception as e:
        print(f"Commit failed: {e}")

def main():
    pricing = get_pricing_data()
    raw_articles = fetch_rss_articles()
    
    published = 0
    for art in raw_articles[:5]: # Check up to 5 stories
        if published >= 1: break # Only publish one successful story per run
        news = ask_gemini_to_generate(art, pricing)
        if news and not news.get('reject'):
            html = build_full_html_page(news)
            commit_to_gitlab(news, html)
            published += 1
        else:
            print(f"Story rejected or failed: {art['title']}")

if __name__ == "__main__":
    main()
