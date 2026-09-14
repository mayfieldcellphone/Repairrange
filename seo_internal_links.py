#!/usr/bin/env python3
import re, glob, os, sys, argparse, html as H

SENTINEL = "<!-- rr-links:v1 -->"
SENTINEL_END = "<!-- /rr-links -->"
BASE_URL = "https://repairrange.io"

CITIES = [
    ("Sydney", "/locations/sydney.html"),
    ("Melbourne", "/locations/melbourne.html"),
    ("Brisbane", "/locations/brisbane.html"),
    ("Perth", "/locations/perth.html"),
    ("Adelaide", "/locations/adelaide.html"),
    ("Newcastle", "/locations/newcastle.html")
]

SKIP_FILES = {
    "repair/index.html", "repair/model.html",
    "repair/phone-repair-costs-australia.html",
    "repair/google-pixel-repair-guide.html"
}

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def get_style_classes(doc):
    style = ' '.join(re.findall(r'(?s)<style>(.*?)</style>', doc))
    return {c for c in ['card', 'eyebrow', 'ed-link', 'text-ink', 'text-muted', 'border-line']
            if re.search(r'\.' + re.escape(c) + r'\s*[,{ ]', style)}

def strip_tags(s):
    s = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", H.unescape(s)).strip()

def get_model_name(fp):
    doc = open(fp, encoding='utf-8', errors='replace').read()
    m = re.search(r"(?is)<h1[^>]*>(.*?)</h1>", doc)
    if not m: return os.path.basename(fp).replace(".html", "").replace("-", " ").title()
    t = strip_tags(m.group(1))
    t = re.sub(r"(?i)\s*repair costs?\.?\s*$", "", t).strip().rstrip(".")
    return t

def build_repair_links(fp, siblings, style_classes, city_links, group_hub):
    has_card = 'card' in style_classes
    has_eyebrow = 'eyebrow' in style_classes
    has_ink = 'text-ink' in style_classes
    has_muted = 'text-muted' in style_classes
    has_ed = 'ed-link' in style_classes

    header_class = "eyebrow mb-6" if has_eyebrow else "text-sm font-medium mb-6"
    card_class = "card p-4 block" if has_card else "border bg-white p-4 block"
    title_class = "font-medium text-ink" if has_ink else "font-medium"
    desc_class = "block text-sm text-muted" if has_muted else "block text-sm"
    hub_link_class = "ed-link" if has_ed else "text-teal-900 hover:text-teal-700 underline"

    cards_html = ""
    for sib_fp, sib_name in siblings:
        href = "/" + sib_fp.replace(os.sep, "/")
        cards_html += f"""
    <a class="{card_class}" href="{href}">
      <span class="{title_class}">{sib_name} repair cost</span>
      <span class="{desc_class}">Screen, battery and back glass pricing</span>
    </a>"""

    city_anchors = " · ".join([f'<a class="{hub_link_class}" href="{url}">{city} phone repair prices</a>' for city, url in city_links])
    
    hub_name = "all models"
    if "iphone" in group_hub: hub_name = "all iPhone models"
    elif "samsung" in group_hub: hub_name = "all Samsung models"
    elif "ipad" in group_hub: hub_name = "all iPad models"
    elif "macbook" in group_hub: hub_name = "all MacBook models"
    elif "google" in group_hub: hub_name = "all Google Pixel models"

    hub_anchor = f'<a class="{hub_link_class}" href="{group_hub}">{hub_name}</a>'

    return f"""{SENTINEL}
<section class="max-w-6xl mx-auto px-6 mt-16">
  <p class="{header_class}">Related repair costs</p>
  <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
{cards_html}
  </div>
  <p class="text-sm mt-16">
    More: {hub_anchor} · {city_anchors}
  </p>
</section>
{SENTINEL_END}"""

def process_file(fp, content_to_inject):
    doc = open(fp, encoding='utf-8', errors='replace').read()
    # Strip existing
    doc = re.sub(re.escape(SENTINEL) + r".*?" + re.escape(SENTINEL_END), "", doc, flags=re.S)
    
    if not content_to_inject:
        open(fp, 'w', encoding='utf-8').write(doc)
        return False

    idx = -1
    for pattern in [r'(?is)<footer\b', r'(?is)</section>(?=[^<]*$)', r'(?is)</body>']:
        m = re.search(pattern, doc)
        if m:
            idx = m.start()
            break
    
    if idx == -1:
        print(f"SKIP (no anchor): {fp}")
        return False
    
    new_doc = doc[:idx] + content_to_inject + "\n" + doc[idx:]
    open(fp, 'w', encoding='utf-8').write(new_doc)
    return True

def get_group_hub(prefix, fp):
    if prefix == "samsung":
        if "tab" in fp.lower(): return "/brands/samsung-tab.html"
        return "/brands/samsung.html"
    if prefix == "iphone": return "/brands/apple-iphone.html"
    if prefix == "macbook": return "/repair/macbook-repair-costs-australia.html"
    if prefix == "ipad": return "/brands/apple-ipad.html"
    if prefix == "pixel" or prefix == "google": return "/brands/google.html"
    return "/repair/phone-repair-costs-australia.html"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    
    if args.apply: args.dry_run = False

    repair_files = sorted(glob.glob("repair/*.html"))
    repair_files = [f for f in repair_files if f.replace(os.sep, "/") not in SKIP_FILES]
    
    groups = {
        "samsung": [],
        "iphone": [],
        "macbook": [],
        "ipad": [],
        "google": [] # pixel-* or google-*
    }
    
    for f in repair_files:
        base = os.path.basename(f)
        if base.startswith("samsung-"): groups["samsung"].append(f)
        elif base.startswith("iphone-"): groups["iphone"].append(f)
        elif base.startswith("macbook-"): groups["macbook"].append(f)
        elif base.startswith("ipad-"): groups["ipad"].append(f)
        elif base.startswith("pixel-") or base.startswith("google-"): groups["google"].append(f)
        else:
            # Fallback
            pass
            
    for k in groups:
        groups[k] = sorted(groups[k], key=lambda x: natural_sort_key(os.path.basename(x)))

    model_names = {f: get_model_name(f) for f in repair_files}
    
    files_touched = {"repair": 0, "blog": 0, "brands": 0}
    links_added = {"sibling": 0, "city": 0, "blog": 0}
    
    # Process Repair Files
    for group_name, group_files in groups.items():
        n = len(group_files)
        for i, fp in enumerate(group_files):
            indices = []
            if n < 7:
                indices = [j for j in range(n) if j != i]
            else:
                indices = [(i + offset) % n for offset in [-3, -2, -1, 1, 2, 3]]
            
            siblings = [(group_files[idx], model_names[group_files[idx]]) for idx in indices]
            
            doc = open(fp, encoding='utf-8', errors='replace').read()
            style_classes = get_style_classes(doc)
            
            # City rotation: 3 cities per page
            city_idx = (repair_files.index(fp)) % len(CITIES)
            city_links = [CITIES[(city_idx + j) % len(CITIES)] for j in range(3)]
            
            hub = get_group_hub(group_name, fp)
            block = build_repair_links(fp, siblings, style_classes, city_links, hub)
            
            if not args.dry_run:
                if process_file(fp, block):
                    files_touched["repair"] += 1
                    links_added["sibling"] += len(siblings)
                    links_added["city"] += 3
            else:
                files_touched["repair"] += 1
                links_added["sibling"] += len(siblings)
                links_added["city"] += 3

    # Blog Edge D
    blog_files = glob.glob("blog/*.html")
    repair_models = sorted([(name, "/" + fp.replace(os.sep, "/")) for fp, name in model_names.items()], 
                           key=lambda x: len(x[0]), reverse=True)
    
    orphaned_blogs = []
    for fp in blog_files:
        doc = open(fp, encoding='utf-8', errors='replace').read()
        if 'noindex' in doc.lower() or SENTINEL in doc:
            continue
        
        style_classes = get_style_classes(doc)
        has_ed = 'ed-link' in style_classes
        link_class = "ed-link" if has_ed else "text-teal-900 hover:text-teal-700 underline"
        
        # Injection logic: longest match first, first mention only, cap 3
        # Exclude headers, summary, nav, footer, existing links
        def is_safe(m, doc):
            # Check if inside forbidden tag
            start = m.start()
            # Simple check: search backwards for < and forwards for >
            # This is naive but often sufficient for well-formed HTML
            prev_tag = doc.rfind("<", 0, start)
            next_tag = doc.find(">", start)
            if prev_tag != -1 and next_tag != -1:
                tag_content = doc[prev_tag:next_tag+1].lower()
                if any(tag_content.startswith("<" + t) for t in ["h1", "h2", "h3", "summary", "nav", "footer", "a"]):
                    return False
            
            # Better check: find parent tag
            # Actually, the requirement says "Never link inside h1-h3, summary, nav, footer, or existing a"
            # We can use a regex to find all text nodes outside these tags
            return True # Will refine

        links_count = 0
        new_doc = doc
        for model_name, url in repair_models:
            if links_count >= 3: break
            
            # Case insensitive match, ensuring not inside a tag or already linked
            # Using a more robust regex for "not inside a tag"
            pattern = re.compile(rf'(?i)(?<![a-zA-Z0-9])({re.escape(model_name)})(?![a-zA-Z0-9])')
            
            matches = list(pattern.finditer(new_doc))
            for m in matches:
                if links_count >= 3: break
                
                # Check context
                pre = new_doc[:m.start()]
                if re.search(r'<[hH][1-3][^>]*>[^<]*$', pre) or \
                   re.search(r'<summary[^>]*>[^<]*$', pre) or \
                   re.search(r'<nav[^>]*>[^<]*$', pre) or \
                   re.search(r'<footer[^>]*>[^<]*$', pre) or \
                   re.search(r'<a[^>]*>[^<]*$', pre):
                    continue
                
                # Replace
                link_html = f'<a class="{link_class}" href="{url}">{m.group(1)}</a>'
                new_doc = new_doc[:m.start()] + link_html + new_doc[m.end():]
                links_count += 1
                links_added["blog"] += 1
                break # First mention only
        
        if links_count > 0:
            if not args.dry_run:
                open(fp, 'w', encoding='utf-8').write(new_doc)
            files_touched["blog"] += 1
        else:
            orphaned_blogs.append(fp)

    print(f"Files touched: {files_touched}")
    print(f"Links added: {links_added}")
    print(f"Still orphaned blogs ({len(orphaned_blogs)}): {orphaned_blogs[:10]}...")

if __name__ == "__main__":
    main()
