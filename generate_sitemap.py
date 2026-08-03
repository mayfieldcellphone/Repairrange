import os
from datetime import datetime

# Configuration
BASE_URL = "https://repairrange.io"
REPO_ROOT = "."
SITEMAP_FILE = "sitemap.xml"

# Folders to scan for HTML files
FOLDERS = ["fix", "locations", "repair", "brands", "tools", "blog", "unlock", "news", "guides"]

def generate_sitemap():
    print(f"Generating sitemap for {BASE_URL}...")
    urls = []
    
    # 1. Add root HTML files
    for file in os.listdir(REPO_ROOT):
        if file.endswith(".html") and file != "404.html":
            urls.append(f"{BASE_URL}/{file}")
            
    # 2. Add subfolder HTML files
    for folder in FOLDERS:
        folder_path = os.path.join(REPO_ROOT, folder)
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(".html"):
                    urls.append(f"{BASE_URL}/{folder}/{file}")
                    
    # Sort for consistency
    urls = sorted(list(set(urls)))
    
    # Build XML
    today = datetime.now().strftime("%Y-%m-%d")
    xml_content = "<?xml version='1.0' encoding='utf-8'?>\n"
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        if url.endswith("index.html") or url == BASE_URL + "/":
            priority = "1.0"
        elif "/blog/" in url or "/news/" in url:
            priority = "0.8"
        else:
            priority = "0.5"
        xml_content += "  <url>\n"
        xml_content += f"    <loc>{url}</loc>\n"
        xml_content += f"    <lastmod>{today}</lastmod>\n"
        xml_content += f"    <priority>{priority}</priority>\n"
        xml_content += "  </url>\n"
        
    xml_content += "</urlset>"
    
    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write(xml_content)
        
    print(f"Successfully generated {SITEMAP_FILE} with {len(urls)} URLs.")

if __name__ == "__main__":
    generate_sitemap()
