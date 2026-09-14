#!/usr/bin/env python3
"""RR-01: inject Product/AggregateOffer/FAQPage/BreadcrumbList into repair + city pages.
Additive and idempotent. Never invents prices -- everything is parsed from rendered HTML."""
import re, json, glob, os, html as H

SENTINEL = "<!-- rr-schema:v1 -->"
BASE = "https://repairrange.io"
DASH = r"[–—\-]"

def strip_tags(s):
    s = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", H.unescape(s)).strip()

def model_name(doc):
    m = re.search(r"(?is)<h1[^>]*>(.*?)</h1>", doc)
    if not m: return None
    t = strip_tags(m.group(1))
    t = re.sub(r"(?i)\s*repair costs?\.?\s*$", "", t).strip().rstrip(".")
    return t or None

def price_rows(doc):
    """-> [(label, low, high)] parsed from the rendered price table. Empty if none."""
    out = []
    for tbl in re.findall(r"(?is)<table[^>]*class=\"[^\"]*price-table[^\"]*\"[^>]*>.*?</table>", doc):
        for row in re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", tbl):
            cells = re.findall(r"(?is)<td[^>]*>.*?</td>", row)
            label = price = None
            for c in cells:
                if label is None and "font-medium text-ink" in c:
                    lab = strip_tags(c)
                    lab = re.sub(r"(?i)\s*DIY difficulty:.*$", "", lab).strip()
                    label = lab or None
                elif price is None and "font-mono tnum" in c:
                    price = strip_tags(c)
            if not label or not price: continue
            m = re.search(rf"\$\s?([\d,]+)\s*{DASH}\s*\$?\s?([\d,]+)", price)
            if m:
                lo, hi = m.group(1), m.group(2)
            else:
                m1 = re.search(r"\$\s?([\d,]+)", price)
                if not m1: continue
                lo = hi = m1.group(1)
            out.append((label, int(lo.replace(",", "")), int(hi.replace(",", ""))))
    return out

def faqs(doc):
    out = []
    for d in re.findall(r"(?is)<details\b.*?(?=<details\b|</section>|<footer\b)", doc):
        q = re.search(r"(?is)<summary[^>]*>.*?<h3[^>]*>(.*?)</h3>", d)
        a = re.search(r"(?is)<div class=\"px-5 md:px-6 pb-6[^\"]*\"[^>]*>(.*?)(?:</div>|$)", d)
        if q and a:
            qt, at = strip_tags(q.group(1)), strip_tags(a.group(1))
            if qt and at: out.append((qt, at))
    return out

def breadcrumb(path, name):
    seg = path.split("/")[0]
    trail = [("Home", f"{BASE}/")]
    if seg == "repair":
        trail.append(("Repair costs", f"{BASE}/repair/phone-repair-costs-australia.html"))
    elif seg == "locations":
        trail.append(("Locations", f"{BASE}/locations.html"))
    trail.append((name, f"{BASE}/{path}"))
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                                for i, (n, u) in enumerate(trail)]}

def build(path, doc):
    name = model_name(doc)
    if not name: return None
    blocks = [breadcrumb(path, name)]
    rows = price_rows(doc)
    byquote = bool(re.search(r"(?i)by quote", doc)) and not rows

    if rows:
        lo = min(r[1] for r in rows); hi = max(r[2] for r in rows)
        blocks.append({
            "@context": "https://schema.org", "@type": "Product",
            "name": f"{name} repair",
            "description": f"Independent repair pricing for the {name} in Australia.",
            "category": "Mobile device repair",
            "brand": {"@type": "Brand", "name": name.split()[0]},
            "offers": {
                "@type": "AggregateOffer", "priceCurrency": "AUD",
                "lowPrice": lo, "highPrice": hi, "offerCount": len(rows),
                "availability": "https://schema.org/InStock",
                "offers": [{"@type": "Offer", "name": lab, "priceCurrency": "AUD",
                            "priceSpecification": {"@type": "PriceSpecification",
                                                   "priceCurrency": "AUD",
                                                   "minPrice": a, "maxPrice": b}}
                           for lab, a, b in rows],
            },
        })
    elif byquote:
        blocks.append({
            "@context": "https://schema.org", "@type": "Service",
            "name": f"{name} repair", "serviceType": "Mobile device repair",
            "areaServed": {"@type": "Country", "name": "Australia"},
            "provider": {"@type": "Organization", "name": "RepairRange", "url": BASE + "/"},
        })

    f = faqs(doc)
    if f:
        blocks.append({"@context": "https://schema.org", "@type": "FAQPage",
                       "mainEntity": [{"@type": "Question", "name": q,
                                       "acceptedAnswer": {"@type": "Answer", "text": a}}
                                      for q, a in f]})
    return blocks

def write(fp):
    doc = open(fp, encoding="utf-8").read()
    doc = re.sub(re.escape(SENTINEL) + r".*?" + re.escape("<!-- /rr-schema -->"), "", doc, flags=re.S)
    blocks = build(fp.replace(os.sep, "/"), doc)
    if not blocks: return None
    payload = SENTINEL + "\n" + "\n".join(
        '<script type="application/ld+json">' + json.dumps(b, ensure_ascii=False) + "</script>"
        for b in blocks) + "\n<!-- /rr-schema -->\n"
    i = doc.lower().rfind("</head>")
    if i < 0: return None
    open(fp, "w", encoding="utf-8").write(doc[:i] + payload + doc[i:])
    return [b["@type"] for b in blocks]

SKIP = {"repair/index.html", "repair/phone-repair-costs-australia.html"}
if __name__ == "__main__":
    tally, touched = {}, 0
    for fp in sorted(glob.glob("repair/*.html")) + sorted(glob.glob("locations/*.html")):
        k = fp.replace(os.sep, "/")
        if k in SKIP: print(f"skip (hub)  {k}"); continue
        r = write(k)
        if r is None: print(f"SKIP (no h1/head)  {k}"); continue
        touched += 1
        for t in r: tally[t] = tally.get(t, 0) + 1
        print(f"ok  {k}  ->  {'+'.join(r)}")
    print(f"\nfiles touched: {touched}")
    print("blocks written:", tally)
