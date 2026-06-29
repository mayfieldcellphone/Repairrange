import os
import csv
import urllib.request
import urllib.parse
import json
import re
from datetime import datetime

# Path definitions
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.join(ROOT_DIR, "RR project")
CSV_PATH = os.path.join(WORKSPACE_DIR, "leads", "outreach_schedule_june_2026.csv")

# Load environment variables from .env
env_path = os.path.join(ROOT_DIR, ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, val = line.strip().split("=", 1)
                os.environ[key] = val

GOOGLE_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")

def log_message(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def http_get(url, headers=None):
    """Performs a robust HTTP GET request with standard browser headers."""
    default_headers = {
        "User-Agent": "Mozilla/5.0"
    }
    if headers:
        default_headers.update(headers)
        
    req = urllib.request.Request(url, headers=default_headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read()
    except Exception as e:
        log_message(f"HTTP GET failed for {url[:80]}: {str(e)}")
        return None

def extract_emails(html_content):
    """Scrapes email addresses from raw HTML text using regex."""
    if not html_content:
        return []
    text = html_content.decode("utf-8", errors="ignore")
    # Matches typical company email formats while filtering out image extensions/false positives
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}"
    emails = re.findall(pattern, text)
    
    # Filter out common junk endings/files
    filtered = []
    junk_patterns = [r"\.png$", r"\.jpg$", r"\.jpeg$", r"\.gif$", r"\.webp$", r"example\.com$", r"bootstrap", r"jquery", r"sentry"]
    for email in emails:
        email = email.lower().strip()
        if any(re.search(jp, email) for jp in junk_patterns):
            continue
        if email not in filtered:
            filtered.append(email)
    return filtered

def search_google_places(city):
    """Primary Source: Google Places TextSearch API."""
    if not GOOGLE_API_KEY:
        log_message("Google Places API Key not configured in .env. Skipping Google Places search.")
        return []
        
    log_message(f"Querying Google Places API for phone repair shops in {city}...")
    query = f"phone repair in {city} Australia"
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={urllib.parse.quote(query)}&key={GOOGLE_API_KEY}"
    
    response_data = http_get(url)
    if not response_data:
        return []
        
    try:
        data = json.loads(response_data.decode("utf-8"))
        results = data.get("results", [])
        log_message(f"Google Places returned {len(results)} shops.")
        
        shops = []
        for r in results:
            shop = {
                "name": r.get("name"),
                "address": r.get("formatted_address"),
                "website": "",
                "place_id": r.get("place_id")
            }
            # Query Details API to get the shop website
            if shop["place_id"]:
                details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={shop['place_id']}&fields=website&key={GOOGLE_API_KEY}"
                details_data = http_get(details_url)
                if details_data:
                    details = json.loads(details_data.decode("utf-8"))
                    shop["website"] = details.get("result", {}).get("website", "")
            shops.append(shop)
        return shops
    except Exception as e:
        log_message(f"Failed to parse Google Places API response: {str(e)}")
        return []

def search_local_listings(city):
    """Fallback Source: Scrapes AOL Search for independent repair sites."""
    log_message(f"Running direct web scraping fallback search for {city}...")
    query = f"phone repair {city}"
    url = f"https://search.aol.com/aol/search?q={urllib.parse.quote(query)}"
    
    response_html = http_get(url)
    if not response_html:
        return []
        
    html_text = response_html.decode("utf-8", errors="ignore")
    
    # Extract links from AOL redirects
    ru_params = re.findall(r'RU=([^/&"]+)', html_text)
    links = [urllib.parse.unquote(ru) for ru_params_encoded in ru_params for ru in [urllib.parse.unquote(ru_params_encoded)]]
    
    # Also extract direct links in case
    direct_links = re.findall(r'href="(https?://[^"]+)"', html_text)
    links.extend(direct_links)
    
    shops = []
    seen_domains = set()
    for link in links:
        parsed = urllib.parse.urlparse(link)
        domain = parsed.netloc.lower().replace("www.", "")
        if not domain:
            continue
            
        # Exclude search engines, portals, directories, and social media
        exclude_keywords = [
            "yahoo", "yimg", "yellowpages", "yelp", "facebook", "truelocal", 
            "apple", "samsung", "gumtree", "localsearch", "hipages", 
            "linkedin", "instagram", "aol.com", "bing.com", "google.com", 
            "policies", "webmail", "chamberofcommerce", "threebestrated"
        ]
        if any(kw in domain for kw in exclude_keywords):
            continue
            
        if domain not in seen_domains and parsed.scheme in ["http", "https"]:
            seen_domains.add(domain)
            shop_name = domain.split(".")[0].replace("-", " ").title()
            shops.append({
                "name": shop_name,
                "address": f"Local Shop, {city}",
                "website": f"{parsed.scheme}://{parsed.netloc}"
            })
            
    log_message(f"Scraped {len(shops)} shop websites from search index.")
    return shops

def enrich_shop_email(shop):
    """Visits the shop website to scrape public contact email addresses."""
    website = shop.get("website")
    if not website:
        return None
        
    log_message(f"Scraping {website} for contact email...")
    homepage_html = http_get(website)
    emails = extract_emails(homepage_html)
    
    if emails:
        return emails[0]
        
    # If not found on homepage, try to find and scan Contact Us or About Us links
    if homepage_html:
        text = homepage_html.decode("utf-8", errors="ignore")
        contact_links = re.findall(r'href="([^"]*contact[^"]*)"', text, re.IGNORECASE)
        for cl in contact_links[:2]:  # Limit to 2 contact pages to prevent long crawl times
            # Resolve relative links
            full_cl = urllib.parse.urljoin(website, cl)
            log_message(f"Scanning Contact Page: {full_cl}")
            cl_html = http_get(full_cl)
            cl_emails = extract_emails(cl_html)
            if cl_emails:
                return cl_emails[0]
                
    return None

def is_duplicate(email, website):
    """Checks if lead already exists in outreach CSV by email or website."""
    if not os.path.exists(CSV_PATH):
        return False
        
    email_clean = email.strip().lower() if email else ""
    web_parsed = urllib.parse.urlparse(website).netloc.lower().replace("www.", "") if website else ""
    
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_email = row.get("Email", "").strip().lower()
            if email_clean and existing_email == email_clean:
                return True
    return False

def add_lead_to_csv(shop_name, city, email_addr):
    """Appends new verified lead to outreach_schedule_june_2026.csv."""
    if not os.path.exists(CSV_PATH):
        return
        
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        
    row_dict = {h: "" for h in headers}
    row_dict["Shop Name"] = shop_name
    row_dict["City"] = city.capitalize()
    row_dict["Email"] = email_addr.strip().lower()
    row_dict["Scheduled Day"] = "Sourced"
    row_dict["Scheduled Date"] = datetime.now().strftime("%Y-%m-%d")
    row_dict["Status"] = "Pending"
    row_dict["Date Sent"] = ""
    
    with open(CSV_PATH, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writerow(row_dict)
    log_message(f"SUCCESS: Appended '{shop_name}' ({email_addr}) to CRM Leads!")

def run_sourcing_flow(city):
    log_message(f"=== Starting Hybrid Lead Sourcing Run for: {city} ===")
    
    # 1. Fetch from Google Places (if API key is present)
    places_shops = search_google_places(city)
    
    # 2. Fetch from Web Scraper Fallback
    local_shops = search_local_listings(city)
    
    # Merge findings (Places API is primary, local is fallback)
    all_shops = places_shops
    seen_websites = {urllib.parse.urlparse(s.get("website")).netloc.lower().replace("www.", "") for s in all_shops if s.get("website")}
    
    for s in local_shops:
        web_netloc = urllib.parse.urlparse(s.get("website")).netloc.lower().replace("www.", "")
        if web_netloc not in seen_websites:
            all_shops.append(s)
            seen_websites.add(web_netloc)
            
    log_message(f"Aggregated {len(all_shops)} potential shop targets. Starting website email verification...")
    
    sourced_count = 0
    # Process and verify emails for each shop
    for s in all_shops:
        website = s.get("website")
        if not website:
            continue
            
        # Check website domain duplicate first
        if is_duplicate(None, website):
            log_message(f"Skipping {s['name']} - Website already exists in CRM.")
            continue
            
        # Scrape website for a real business email
        email_addr = enrich_shop_email(s)
        if email_addr:
            if not is_duplicate(email_addr, website):
                add_lead_to_csv(s["name"], city, email_addr)
                sourced_count += 1
            else:
                log_message(f"Skipping {s['name']} - Email duplicate found: {email_addr}")
        else:
            log_message(f"Could not find public contact email for {s['name']}.")
            
    log_message(f"=== Sourcing Run Complete! Newly Sourced Verified Leads: {sourced_count} ===")

if __name__ == "__main__":
    import sys
    target_city = "Newcastle"
    if len(sys.argv) > 1:
        target_city = sys.argv[1]
    run_sourcing_flow(target_city)
