import os
from datetime import datetime
import subprocess

# Configuration
BASE_URL = "https://repairrange.io"
REPO_ROOT = "."
SITEMAP_FILE = "sitemap.xml"

# Folders to scan for HTML files
FOLDERS = ["fix", "locations", "repair", "brands", "tools", "blog", "unlock", "news", "guides", "selfrepairkit", "downloads"]

# GUARD (added Aug 2026): URLs with a 301 rule in _redirects are pruned/consolidated
# pages. Keep them out of the sitemap even if their noindex meta is ever stripped
# by a future sweep -- the redirect rule is the source of truth.
REDIRECTED = set()
if os.path.exists("_redirects"):
    with open("_redirects", encoding="utf-8") as _f:
        for _line in _f:
            _parts = _line.split()
            if len(_parts) >= 2 and _parts[0].startswith("/"):
                REDIRECTED.add(_parts[0].lstrip("/"))

def generate_sitemap():
    print(f"Generating sitemap for {BASE_URL}...")
    urls = []
    
    # 1. Add root HTML files
    for file in os.listdir(REPO_ROOT):
        if file.endswith(".html") and file != "404.html":
            if file in REDIRECTED:
                continue
            if file == "index.html":
                urls.append(f"{BASE_URL}/")
            else:
                urls.append(f"{BASE_URL}/{file}")
            
    # 2. Add subfolder HTML files
    for folder in FOLDERS:
        folder_path = os.path.join(REPO_ROOT, folder)
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(".html"):
                    if f"{folder}/{file}" in REDIRECTED:
                        continue
                    fp = os.path.join(folder_path, file)
                    try:
                        with open(fp, encoding="utf-8", errors="replace") as _f:
                            if "noindex" in _f.read():
                                continue
                    except Exception:
                        pass
                    urls.append(f"{BASE_URL}/{folder}/{file}")
                    
    # Sort for consistency
    urls = sorted(list(set(urls)))
    
    # Build XML
    today = datetime.now().strftime("%Y-%m-%d")

    # Real per-file dates from git history. Needs full history: a shallow
    # clone reports one identical date for every file, which is the bug this
    # replaced. See fetch-depth: 0 in .github/workflows/deploy.yml.
    _date_cache = {}

    def _lastmod(u):
        rel = u[len(BASE_URL):].lstrip("/") or "index.html"
        if rel not in _date_cache:
            try:
                out = subprocess.run(
                    ["git", "log", "-1", "--format=%cs", "--", rel],
                    capture_output=True, text=True, timeout=20).stdout.strip()
            except Exception:
                out = ""
            _date_cache[rel] = out or today
        return _date_cache[rel]
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
        xml_content += f"    <lastmod>{_lastmod(url)}</lastmod>\n"
        xml_content += f"    <priority>{priority}</priority>\n"
        xml_content += "  </url>\n"
        
    xml_content += "</urlset>"
    
    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write(xml_content)
        
    print(f"Successfully generated {SITEMAP_FILE} with {len(urls)} URLs.")

if __name__ == "__main__":
    generate_sitemap()
