import urllib.request
import re
import json
import os
from datetime import datetime

# GitLab Configuration for committing the feed
GITLAB_TOKEN = os.environ.get("GITLAB_TOKEN", "glpat-hRoTs91bL94GiUsNmHljCmM6MQpvOjEKdTpsdG44dQ8.01.1709y1suj")
PROJECT_PATH = "mayfield276%2Fblank-site-2026-05-06-6rrng"

def get_mayfield_blog_urls():
    sitemap_url = "https://mayfieldphonerepair.com.au/sitemap.xml"
    req = urllib.request.Request(sitemap_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            xml = resp.read().decode('utf-8')
        urls = re.findall(r'<loc>(https://mayfieldphonerepair.com.au/blog/.*?)</loc>', xml)
        # Unique list preserving order
        unique_urls = []
        for url in urls:
            if url not in unique_urls:
                unique_urls.append(url)
        return unique_urls
    except Exception as e:
        print("Error fetching sitemap:", e)
        return []

def get_article_details(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
        
        # Parse title
        title_match = re.search(r'<title>(.*?)</title>', html)
        title = title_match.group(1) if title_match else "Mayfield Blog Post"
        title = title.split(" | ")[0].strip()
        
        # Parse description
        desc_match = re.search(r'<meta[^>]+name=\"description\"[^>]+content=\"(.*?)\"', html)
        if not desc_match:
            desc_match = re.search(r'<meta[^>]+content=\"(.*?)\"[^>]+name=\"description\"', html)
        desc = desc_match.group(1) if desc_match else "Expert mobile phone and tablet repair in Mayfield, Newcastle."
        
        # Parse date from URL or assume current
        date_match = re.search(r'datetime=\"(.*?)\"', html)
        if date_match:
            date_str = date_match.group(1)[:10] # YYYY-MM-DD
            try:
                pub_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%a, %d %b %Y %H:%M:%S GMT")
            except Exception:
                pub_date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        else:
            pub_date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
            
        return {
            "title": title,
            "link": url,
            "description": desc,
            "pubDate": pub_date
        }
    except Exception as e:
        print(f"Error fetching article details for {url}: {e}")
        return None

def build_rss_xml(articles):
    rfc_date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    items = []
    for art in articles:
        # Escape special XML characters in title and description
        title_esc = art['title'].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("'", "&apos;")
        desc_esc = art['description'].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("'", "&apos;")
        
        item_xml = f"""    <item>
      <title>{title_esc}</title>
      <link>{art['link']}</link>
      <guid isPermaLink="true">{art['link']}</guid>
      <pubDate>{art['pubDate']}</pubDate>
      <description>{desc_esc}</description>
    </item>"""
        items.append(item_xml)
        
    items_block = "\n".join(items)
    
    rss_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Mayfield Phone Repair Blog</title>
    <link>https://mayfieldphonerepair.com.au/blog</link>
    <description>Newcastle's Premier Mobile Phone, Tablet &amp; Laptop Repair Service Blogs &amp; Repair Guides</description>
    <language>en-au</language>
    <lastBuildDate>{rfc_date}</lastBuildDate>
    <atom:link href="https://repairrange.io/mayfield_feed.xml" rel="self" type="application/rss+xml" />
{items_block}
  </channel>
</rss>"""
    return rss_xml

def commit_to_gitlab(xml_content):
    url = f"https://gitlab.com/api/v4/projects/{PROJECT_PATH}/repository/commits"
    
    # Test if file exists
    action = "update"
    try:
        raw_feed_url = f"https://gitlab.com/api/v4/projects/{PROJECT_PATH}/repository/files/mayfield_feed.xml/raw?ref=main"
        req_test = urllib.request.Request(raw_feed_url, method="HEAD")
        req_test.add_header('PRIVATE-TOKEN', GITLAB_TOKEN)
        with urllib.request.urlopen(req_test) as resp:
            pass
    except Exception:
        action = "create"
        
    payload = {
        "branch": "main",
        "commit_message": "Automated update of Mayfield Phone Repair RSS Feed",
        "actions": [
            {
                "action": action,
                "file_path": "mayfield_feed.xml",
                "content": xml_content,
                "encoding": "text"
            }
        ]
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("PRIVATE-TOKEN", GITLAB_TOKEN)
    
    try:
        with urllib.request.urlopen(req) as resp:
            print("Successfully committed to GitLab:", resp.read().decode("utf-8"))
    except Exception as e:
        print("Error committing to GitLab:", e)

if __name__ == "__main__":
    print("Fetching Mayfield blog URLs from sitemap...")
    urls = get_mayfield_blog_urls()
    print(f"Found {len(urls)} blog URLs.")
    
    articles = []
    # Limit to latest 15 to keep it lightweight
    for url in urls[:15]:
        print(f"Fetching details for: {url}...")
        details = get_article_details(url)
        if details:
            articles.append(details)
            
    if articles:
        print("Building RSS XML...")
        rss_xml = build_rss_xml(articles)
        print("Committing to GitLab...")
        commit_to_gitlab(rss_xml)
        print("Done!")
    else:
        print("No articles found to generate feed.")
