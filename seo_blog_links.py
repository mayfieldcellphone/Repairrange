#!/usr/bin/env python3
import re, glob, os, math, json, argparse, html as H
from collections import Counter

SENTINEL = "<!-- rr-blog-links:v1 -->"
SENTINEL_END = "<!-- /rr-blog-links -->"
BASE_URL = "https://repairrange.io"

STOP_WORDS = {
    'the', 'and', 'for', 'your', 'with', 'that', 'this', 'from', 'are', 'was', 'were', 'will', 'been',
    'has', 'have', 'had', 'but', 'not', 'what', 'all', 'any', 'each', 'few', 'more', 'most', 'some',
    'such', 'than', 'too', 'very', 'can', 'just', 'should', 'now', 'into', 'out', 'off', 'over',
    'under', 'again', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'who', 'whom',
    'which', 'each', 'than', 'then', 'they', 'them', 'their', 'theirs', 'these', 'those', 'about'
}

def strip_tags(s):
    s = re.sub(r"(?is)<(script|style|nav|footer|head)\b.*?</\1>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", H.unescape(s)).strip()

def get_tokens(text):
    tokens = re.findall(r'[a-z0-9]{3,}', text.lower())
    return [t for t in tokens if t not in STOP_WORDS]

def get_blog_metadata(fp):
    doc = open(fp, encoding='utf-8', errors='replace').read()
    noindex = 'noindex' in doc.lower()
    
    # Extract body text for similarity
    body_match = re.search(r'(?is)<body\b.*?>(.*?)</body>', doc)
    body_text = body_match.group(1) if body_match else doc
    cleaned_body = strip_tags(body_text)
    
    h1_match = re.search(r'(?is)<h1[^>]*>(.*?)</h1>', doc)
    h1 = strip_tags(h1_match.group(1)) if h1_match else os.path.basename(fp).replace('.html', '').replace('-', ' ').title()
    
    # Trim H1 for anchor
    anchor = h1
    if len(anchor) > 70:
        anchor = anchor[:67].rsplit(' ', 1)[0] + '...'
    
    slug_tokens = get_tokens(os.path.basename(fp).replace('.html', ''))
    body_tokens = get_tokens(cleaned_body)
    
    # Weighted tokens
    weighted_tokens = Counter(body_tokens)
    for t in slug_tokens:
        weighted_tokens[t] += 3
        
    return {
        'fp': fp.replace(os.sep, '/'),
        'noindex': noindex,
        'h1': h1,
        'anchor': anchor,
        'tokens': weighted_tokens,
        'full_text': cleaned_body,
        'doc': doc
    }

def cosine_similarity(v1, v2):
    common = set(v1.keys()) & set(v2.keys())
    dot_product = sum(v1[t] * v2[t] for t in common)
    mag1 = math.sqrt(sum(v1[t]**2 for t in v1.keys()))
    mag2 = math.sqrt(sum(v2[t]**2 for t in v2.keys()))
    if not mag1 or not mag2: return 0.0
    return dot_product / (mag1 * mag2)

def build_related_reading_block(target_posts, repair_links, style_classes):
    has_card = 'card' in style_classes
    has_eyebrow = 'eyebrow' in style_classes
    has_ink = 'text-ink' in style_classes
    has_muted = 'text-muted' in style_classes
    has_ed = 'ed-link' in style_classes

    header_class = "eyebrow mb-6" if has_eyebrow else "text-sm font-medium mb-6"
    card_class = "card p-4 block" if has_card else "border bg-white p-4 block"
    title_class = "font-medium text-ink" if has_ink else "font-medium"
    hub_link_class = "ed-link" if has_ed else "text-teal-900 hover:text-teal-700 underline"

    cards_html = ""
    for post in target_posts:
        href = "/" + post['fp']
        cards_html += f"""
    <a class="{card_class}" href="{href}">
      <span class="{title_class}">{post['anchor']}</span>
    </a>"""

    repair_html = ""
    if repair_links:
        anchors = " · ".join([f'<a class="{hub_link_class}" href="{url}">{name} repair cost</a>' for name, url in repair_links])
        repair_html = f'\n  <p class="text-sm mt-16">\n    Repair costs: {anchors}\n  </p>'

    return f"""{SENTINEL}
<section class="max-w-6xl mx-auto px-6 mt-16">
  <p class="{header_class}">Related reading</p>
  <div class="grid grid-cols-2 md:grid-cols-2 gap-4">
{cards_html}
  </div>{repair_html}
</section>
{SENTINEL_END}"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.apply: args.dry_run = False

    all_blogs = [get_blog_metadata(f) for f in glob.glob("blog/*.html")]
    indexable = [b for b in all_blogs if not b['noindex']]
    
    # 1. Compute Similarities
    n = len(indexable)
    sim_matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            s = cosine_similarity(indexable[i]['tokens'], indexable[j]['tokens'])
            sim_matrix[i][j] = sim_matrix[j][i] = s

    # 2. Assignment Algorithm
    # best_sim_score: max similarity to any other post
    best_scores = []
    for i in range(n):
        scores = [sim_matrix[i][j] for j in range(n) if i != j]
        best_scores.append((i, max(scores) if scores else 0))
    
    # Order by "hard to place" (best similarity score ascending)
    hardest_first = [idx for idx, score in sorted(best_scores, key=lambda x: x[1])]
    
    related_to = [set() for _ in range(n)] # outbound links
    targeted_by = [0] * n # inbound link count
    
    # Phase 1: Coverage (Ensure each post is targeted 3 times)
    for target_idx in hardest_first:
        # Posts that can link to this target (not self, doesn't already link, has slots)
        candidates = []
        for source_idx in range(n):
            if source_idx == target_idx: continue
            if target_idx in related_to[source_idx]: continue
            if len(related_to[source_idx]) < 4:
                candidates.append((source_idx, sim_matrix[source_idx][target_idx]))
        
        # Pick 3 most similar candidates
        needed = max(0, 3 - targeted_by[target_idx])
        top_candidates = sorted(candidates, key=lambda x: x[1], reverse=True)[:needed]
        for src_idx, sim in top_candidates:
            related_to[src_idx].add(target_idx)
            targeted_by[target_idx] += 1

    # Phase 2: Fill (Ensure each post links to 4 posts)
    for i in range(n):
        if len(related_to[i]) < 4:
            candidates = []
            for j in range(n):
                if i == j: continue
                if j in related_to[i]: continue
                candidates.append((j, sim_matrix[i][j]))
            
            top_candidates = sorted(candidates, key=lambda x: x[1], reverse=True)[:4 - len(related_to[i])]
            for j, sim in top_candidates:
                related_to[i].add(j)
                targeted_by[j] += 1

    # 3. Model Matching
    repair_files = glob.glob("repair/*.html")
    # Exclude hubs
    repair_files = [f for f in repair_files if f.replace(os.sep, '/') not in {
        "repair/index.html", "repair/model.html", "repair/phone-repair-costs-australia.html", "repair/google-pixel-repair-guide.html"
    }]
    
    # Map from slug to model name (from <h1>)
    model_data = []
    for rf in repair_files:
        content = open(rf, encoding='utf-8', errors='replace').read()
        m = re.search(r'(?is)<h1[^>]*>(.*?)</h1>', content)
        if m:
            t = re.sub(r"(?is)<[^>]+>", " ", m.group(1))
            name = re.sub(r"(?i)\s*repair costs?\.?\s*$", "", t).strip().rstrip(".")
            model_data.append((name, "/" + rf.replace(os.sep, '/')))
    
    model_data.sort(key=lambda x: len(x[0]), reverse=True)

    # 4. Injection
    touched = 0
    repair_lines = 0
    skipped = 0
    for i, blog in enumerate(indexable):
        fp = blog['fp']
        doc = blog['doc']
        
        # Style check
        style = ' '.join(re.findall(r'(?s)<style>(.*?)</style>', doc))
        style_classes = {c for c in ['card', 'eyebrow', 'ed-link', 'text-ink', 'text-muted', 'border-line']
                         if re.search(r'\.' + re.escape(c) + r'\s*[,{ ]', style)}
        
        # Related posts
        targets = [indexable[j] for j in related_to[i]]
        
        # Repair links
        post_repair_links = []
        for name, url in model_data:
            if len(post_repair_links) >= 2: break
            if re.search(rf'(?i)\b{re.escape(name)}\b', blog['full_text']):
                post_repair_links.append((name, url))
        
        if post_repair_links: repair_lines += 1
        
        block = build_related_reading_block(targets, post_repair_links, style_classes)
        
        # Strip existing
        doc = re.sub(re.escape(SENTINEL) + r".*?" + re.escape(SENTINEL_END), "", doc, flags=re.S)
        
        # Anchor
        idx = -1
        for pattern in [r'(?is)<footer\b', r'(?is)</section>(?=[^<]*$)', r'(?is)</body>']:
            m = re.search(pattern, doc)
            if m:
                idx = m.start()
                break
        
        if idx == -1:
            print(f"SKIP (no anchor): {fp}")
            skipped += 1
            continue
            
        new_doc = doc[:idx] + block + "\n" + doc[idx:]
        
        if not args.dry_run:
            open(fp, 'w', encoding='utf-8').write(new_doc)
        touched += 1

    # Output Sample for verification (§8)
    print("\n--- SAMPLE RELATED LISTS ---")
    for i in range(min(6, n)):
        blog = indexable[i]
        targets = [indexable[j]['fp'] for j in related_to[i]]
        print(f"Source: {blog['fp']}")
        for t in targets: print(f"  -> {t}")

    print(f"\nFiles touched: {touched}")
    print(f"Repair lines added: {repair_lines}")
    print(f"Files skipped: {skipped}")
    print(f"Min inbound: {min(targeted_by)}, Mean inbound: {sum(targeted_by)/n:.2f}")

if __name__ == "__main__":
    main()
