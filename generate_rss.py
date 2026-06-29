import os
import re
from datetime import datetime
from xml.sax.saxutils import escape

def generate_rss():
    blog_dir = 'selfrepairkit/blog'
    rss_path = 'selfrepairkit/feed.xml'
    base_url = 'https://selfrepairkit.com.au/blog/'

    rss_items = []
    
    if not os.path.exists(blog_dir):
        print("Blog directory not found.")
        return

    files = [f for f in os.listdir(blog_dir) if f.endswith('.html')]
    
    for filename in files:
        path = os.path.join(blog_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        title_match = re.search(r'<title>(.*?)</title>', content)
        title = title_match.group(1) if title_match else filename
        
        desc_match = re.search(r'content="(.*?)"', content)
        description = desc_match.group(1) if desc_match else "Technical Lab Notes from SelfRepairKit."
        
        pub_date = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%a, %d %b %Y %H:%M:%S +0000')
        
        item = f"""
        <item>
            <title>{escape(title)}</title>
            <link>{base_url}{filename}</link>
            <description>{escape(description)}</description>
            <pubDate>{pub_date}</pubDate>
            <guid>{base_url}{filename}</guid>
        </item>"""
        rss_items.append(item)

    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>SelfRepairKit Technical Lab Notes</title>
    <link>https://selfrepairkit.com.au/blog.html</link>
    <description>Expert DIY phone repair guides and tech news from Australia.</description>
    <language>en-au</language>
    {''.join(rss_items)}
</channel>
</rss>"""

    with open(rss_path, 'w', encoding='utf-8') as f:
        f.write(rss_content)
    print(f"RSS Feed successfully generated at {rss_path}")

if __name__ == "__main__":
    generate_rss()
