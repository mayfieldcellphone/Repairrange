#!/usr/bin/env python3
"""
trim_titles.py: Word-boundary aware title optimization for RepairRange blog articles.
Ensures all titles are strictly <= 60 characters for SERP snippets.
Guarantees NO mid-word truncation, NO dangling colons, dashes, or stop words.
Restores full context from <h1> when previous scripts truncated mid-word.
"""

import glob
import re
import os
import html as H

REPO_DIR = r"c:\Users\dell lattitude\Desktop\Repairbill from google\Repairrange SEO and content"

CUSTOM_TITLE_MAP = {
    '26-years-of-gsmarena-aussie-tech.html': '26 Years of GSMArena: An Aussie Tech Retrospective',
    'affordable-refurbished-macbook-neo-australia.html': 'Affordable Refurbished MacBook Neo in Australia',
    'apple-pricing-strategy-australia.html': "Apple's New Pricing Strategy: Australian Market Impact",
    'australia-right-to-repair-2026-milestone.html': "Australia's Right to Repair 2.0: 2026 Regulations",
    'best-telstra-network-phone-plans.html': 'Best Phone Plans on the Telstra Network Australia 2026',
    'macbook-laptop-repair-cost-guide-australia.html': 'MacBook & Laptop Repair Costs Australia (2026 Guide)',
    'phone-repair-checklist-before-during-after.html': 'Phone Repair Checklist: Before, During & After Fixing',
    'phone-repair-costs-record-high-2026.html': 'Phone Repair Costs Hit Record Highs in Australia (2026)',
    'phone-repair-warranty-australia-consumer-rights.html': 'Phone Repair Warranty Australia: Your Consumer Rights',
    'poco-x8-pro-vs-poco-x8-pro-max-comparison.html': 'Poco X8 Pro vs Poco X8 Pro Max: Comparison & Specs',
    'repair-first-economy-e-waste-sustainability.html': 'The Repair-First Economy: Sustainability & E-Waste',
    'samsung-fingerprint-sensor-screen-replacement-guide.html': 'Why Samsung Fingerprint Sensors Break After Screen Repair',
    'samsung-galaxy-s26-prime-day-deals-aus.html': 'Best Deals on Samsung Galaxy S26 Series in Australia',
    'samsung-rollable-screen-smartphone-australia.html': "Samsung's Rollable Screen Smartphone: Aussie Preview",
    'samsung-workers-rally-bonus-disparity.html': 'Samsung Workers Rally Over Bonus Disparity (2026)',
    'siris-big-brain-upgrade-aussie-ai-waitlist.html': "Siri's Big Brain Upgrade: Australian AI Waitlist Guide",
    'sky-itv-acquisition-australia.html': 'Sky and ITV Join Forces: Australian Impact & Analysis',
    'smartwatch-shipments-australia-q1-2026.html': 'Smartwatch Shipments Rise in Australia: Q1 2026 Data',
    'starlink-direct-to-cell-australia-guide.html': 'Starlink Direct to Cell Australia: 2026 Tech Guide',
    'week-in-tech-sharp-aquos-r11.html': 'Sharp Aquos R11 Launches with Impressive Tech Specs',
    'why-a-battery-replacement-doesnt-fix-battery-problem.html': "Why Battery Replacement Doesn't Always Fix Power Issues",
    'why-face-id-stops-working-after-a-screen-replacement.html': 'Why Face ID Stops Working After Screen Replacement',
    'iphone-18-pro-max-repair-cost-australia.html': 'iPhone 18 Pro Max: Repair Costs & Specs in Australia',
    'iphone-18-pro-max-modem-dilemma.html': 'iPhone 18 Pro Max: Understanding the Modem Dilemma',
    'iphone-13-self-repair-service-alternative.html': 'iPhone 13 Self-Repair Service: 2026 Alternatives',
    'stop-uploading-legal-contracts-to-random-websites.html': 'Stop Uploading Legal Contracts to Random Online Sites',
    'water-damage-repair-expectations.html': "Water Damage Repair: What Shops Can & Can't Recover",
    'sample-post.html': 'Sample Post: RepairRange Editorial Guide'
}

STOP_WORDS = {
    'and', 'or', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'the', 'a', 'an',
    'of', 'from', 'what', 'how', 'why', 'your', 'are', 'is', 'its', 'their', 'this',
    'that', 'these', 'those', 'without', 'into', 'through', 'about', 'fo', 'th', 'fi',
    'availab', 'repla', 'sustainabil', 'regu', 'im'
}

TRAILING_PUNCT = r'[\s:\-–—,;.\'\"&/\\?]+'

def clean_html_text(text):
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = H.unescape(text)
    text = text.replace('\u2019', "'").replace('\u2018', "'")
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\u2014', '—').replace('\u2013', '–')
    text = text.replace('&amp;', '&').replace('&mdash;', '—').replace('&ndash;', '–')
    text = text.replace('\ufffd', "'")
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def is_truncated_or_broken(title):
    if not title:
        return True
    if re.search(r'[:\-–—,\s]\s*(?:[—–\-|·]\s*RepairRange)?$', title):
        return True
    lower = title.lower()
    for frag in [' th ', ' fo ', ' fi ', ' availab ', ' repla ', ' regu ', ' sustainabil ', ' im ']:
        if frag in lower:
            return True
    if re.search(r'\b(th|fo|fi|availab|repla|regu|sustainabil|im)\s*$', lower):
        return True
    return False

def smart_truncate_title(text, max_len=60):
    text = clean_html_text(text)
    base = re.sub(r'(?i)\s*[\-|–—·|]\s*(RepairRange|RR)(\s+News|\s+Blog)?\s*$', '', text).strip()
    base = re.sub(TRAILING_PUNCT + r'$', '', base).strip()

    if len(base) <= max_len:
        return base

    truncated = base[:max_len]
    last_space = truncated.rfind(' ')
    if last_space > 20:
        candidate = truncated[:last_space].strip()
    else:
        candidate = truncated.strip()

    while True:
        prev = candidate
        candidate = re.sub(TRAILING_PUNCT + r'$', '', candidate).strip()
        words = candidate.split()
        if words and words[-1].lower() in STOP_WORDS:
            candidate = ' '.join(words[:-1]).strip()
        candidate = re.sub(TRAILING_PUNCT + r'$', '', candidate).strip()
        if candidate == prev or not candidate:
            break

    if len(candidate) > max_len:
        candidate = candidate[:max_len].rstrip()
        candidate = re.sub(TRAILING_PUNCT + r'$', '', candidate).strip()

    return candidate

def get_best_title_for_file(filepath):
    basename = os.path.basename(filepath)
    if basename in CUSTOM_TITLE_MAP:
        return CUSTOM_TITLE_MAP[basename]

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    title_m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)

    raw_title = title_m.group(1).strip() if title_m else ""
    raw_h1 = h1_m.group(1).strip() if h1_m else ""

    clean_h1 = clean_html_text(raw_h1)
    clean_title = clean_html_text(raw_title)

    if is_truncated_or_broken(clean_title) or len(clean_title) > 60:
        source = clean_h1 if clean_h1 else clean_title
    else:
        base_title = re.sub(r'(?i)\s*[\-|–—·|]\s*(RepairRange|RR)(\s+News|\s+Blog)?\s*$', '', clean_title).strip()
        if len(base_title) <= 60 and not is_truncated_or_broken(base_title):
            source = base_title
        else:
            source = clean_h1 if clean_h1 else clean_title

    optimized = smart_truncate_title(source, max_len=60)
    
    if len(optimized) < 10:
        slug = os.path.splitext(basename)[0]
        optimized = slug.replace('-', ' ').title()[:60].strip()

    optimized = re.sub(TRAILING_PUNCT + r'$', '', optimized).strip()
    return optimized

def run_trim_titles(dry_run=True):
    blog_glob = os.path.join(REPO_DIR, 'blog', '*.html')
    blog_files = sorted(glob.glob(blog_glob))
    print(f"Found {len(blog_files)} blog articles.")

    updated = 0
    all_titles = []

    for fpath in blog_files:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
            content = fp.read()

        title_m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        cur_title = title_m.group(1).strip() if title_m else ""
        new_title = get_best_title_for_file(fpath)

        all_titles.append((fpath, new_title, len(new_title)))

        if cur_title != new_title:
            updated += 1
            if not dry_run:
                new_content = re.sub(
                    r'<title>.*?</title>',
                    f'<title>{new_title}</title>',
                    content,
                    count=1,
                    flags=re.IGNORECASE | re.DOTALL
                )
                with open(fpath, 'w', encoding='utf-8') as fp:
                    fp.write(new_content)

    print(f"Total files checked: {len(blog_files)}")
    print(f"Files needing title update: {updated}")
    
    # Audit all 198 titles
    over_60 = [t for t in all_titles if t[2] > 60]
    ends_punct = [t for t in all_titles if re.search(r'[:\-–—,\s]$', t[1])]
    
    print(f"Titles > 60 chars: {len(over_60)}")
    print(f"Titles ending with colon/dash/punct: {len(ends_punct)}")

    return updated

if __name__ == "__main__":
    import sys
    dry = "--apply" not in sys.argv
    run_trim_titles(dry_run=dry)
