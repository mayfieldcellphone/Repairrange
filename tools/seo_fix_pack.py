#!/usr/bin/env python3
"""
RepairRange SEO fix pack — 2026-09-13.

Idempotent: safe to run repeatedly. Every step skips work already done.
Run from the repo root:  python tools/seo_fix_pack.py

Fixes, in dependency order:
  1. Create assets/og-default.png + favicon.ico (nothing else can reference
     an image until one exists — every image path on the site 404s today).
  2. Repair double-encoded UTF-8 (mojibake) in HTML.
  3. Fix Organization.logo in index.html (points at an HTML page, which
     invalidates the whole JSON-LD block).
  4. Add Open Graph / Twitter tags + favicon link site-wide.
  5. Add BreadcrumbList + CollectionPage JSON-LD to the four brand hubs.
  6. Add unique prose to the two thinnest brand hubs.
  7. Patch generate_sitemap.py to emit real per-file git commit dates.

ENCODING: every read and write is explicit UTF-8. A previous pass used the
platform default and put mojibake into a live <title>. Do not "simplify"
these calls.

CSS: this site ships a purged static Tailwind stylesheet. Classes not
already in the built CSS are stripped and render broken. Step 6 reuses the
exact class attribute of each page's existing hero paragraph. Do not
invent classes.
"""

import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(".").resolve()
SITE = "https://repairrange.io"
OG_IMAGE = f"{SITE}/assets/og-default.png"

# Folders that are not part of the published repairrange.io site, or are
# separate sites that happen to live in this repo.
SKIP_DIRS = {
    ".old_data", ".git", "bizhub-saas-production-v2", "repairhub-saas",
    "test_extract", "selfrepairkit", "RR project", "blog-bot", "downloads",
    "tools", "node_modules",
}

report = {}


def html_files():
    for p in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        yield p


# --------------------------------------------------------------------------
# 1. Image assets
# --------------------------------------------------------------------------
def step_images():
    from PIL import Image, ImageDraw, ImageFont

    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    made = []

    def font(size):
        for path in (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
        return ImageFont.load_default()

    BG, FG, ACCENT = (15, 23, 42), (248, 250, 252), (56, 189, 248)

    og = assets / "og-default.png"
    if not og.exists():
        img = Image.new("RGB", (1200, 630), BG)
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, 1200, 14], fill=ACCENT)
        d.text((80, 236), "RepairRange", font=font(104), fill=FG)
        d.text((84, 372), "Honest phone repair costs", font=font(44), fill=ACCENT)
        d.text((84, 436), "Australia", font=font(44), fill=ACCENT)
        d.rectangle([80, 548, 300, 552], fill=FG)
        img.save(og, "PNG", optimize=True)
        made.append(str(og.relative_to(ROOT)))

    ico = ROOT / "favicon.ico"
    if not ico.exists():
        i = Image.new("RGB", (256, 256), BG)
        di = ImageDraw.Draw(i)
        di.text((36, 54), "RR", font=font(148), fill=ACCENT)
        i.save(ico, sizes=[(32, 32), (16, 16)])
        made.append(str(ico.relative_to(ROOT)))

    report["1. images created"] = made or ["(already present)"]


# --------------------------------------------------------------------------
# 2. Mojibake
# --------------------------------------------------------------------------
MOJIBAKE = [
    ("â€”", "—"),   # em dash
    ("â€“", "–"),   # en dash
    ("â€™", "’"),   # right single quote
    ("â€œ", "“"),   # left double quote
    ("â€", "”"),   # right double quote
    ("â€¦", "…"),   # ellipsis
    ("Â ", " "),               # nbsp artifact
]


def step_mojibake():
    fixed = []
    for p in html_files():
        s = original = p.read_text(encoding="utf-8")
        for bad, good in MOJIBAKE:
            s = s.replace(bad, good)
        if s != original:
            p.write_text(s, encoding="utf-8")
            fixed.append(str(p.relative_to(ROOT)))
    report["2. mojibake repaired"] = fixed or ["(none found)"]


# --------------------------------------------------------------------------
# 3. Organization.logo
# --------------------------------------------------------------------------
def step_logo():
    p = ROOT / "index.html"
    s = p.read_text(encoding="utf-8")
    bad = f'"logo":"{SITE}/index.html"'
    if bad in s:
        p.write_text(s.replace(bad, f'"logo":"{OG_IMAGE}"'), encoding="utf-8")
        report["3. logo"] = ["index.html — logo repointed to og-default.png"]
    else:
        report["3. logo"] = ["(already fixed or pattern changed)"]


# --------------------------------------------------------------------------
# 4. Open Graph / Twitter / favicon
# --------------------------------------------------------------------------
RE_TITLE = re.compile(r"<title>(.*?)</title>", re.S | re.I)
RE_CANON = re.compile(
    r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', re.I)
RE_DESC = re.compile(
    r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)["\']', re.I)


def clean_title(t):
    t = html.unescape(t).strip()
    for sep in (" | RepairRange", " — RepairRange", " - RepairRange"):
        if t.endswith(sep):
            t = t[: -len(sep)]
    return t.strip()


def step_og():
    added, skipped_no_canonical, already = 0, [], 0
    for p in html_files():
        s = p.read_text(encoding="utf-8")
        rel = str(p.relative_to(ROOT))

        if "og:title" in s:
            already += 1
        else:
            mt, mc = RE_TITLE.search(s), RE_CANON.search(s)
            if not (mt and mc):
                skipped_no_canonical.append(rel)
                continue
            md = RE_DESC.search(s)
            title = html.escape(clean_title(mt.group(1)), quote=True)
            desc = html.escape(html.unescape(md.group(1)).strip(), quote=True) if md else ""
            url = mc.group(1).strip()
            og_type = "article" if rel.startswith("blog/") else "website"
            block = (
                f'\n<meta property="og:type" content="{og_type}">'
                f'\n<meta property="og:site_name" content="RepairRange">'
                f'\n<meta property="og:locale" content="en_AU">'
                f'\n<meta property="og:url" content="{url}">'
                f'\n<meta property="og:title" content="{title}">'
                f'\n<meta property="og:description" content="{desc}">'
                f'\n<meta property="og:image" content="{OG_IMAGE}">'
                f'\n<meta property="og:image:width" content="1200">'
                f'\n<meta property="og:image:height" content="630">'
                f'\n<meta name="twitter:card" content="summary_large_image">'
                f'\n<meta name="twitter:title" content="{title}">'
                f'\n<meta name="twitter:description" content="{desc}">'
                f'\n<meta name="twitter:image" content="{OG_IMAGE}">'
            )
            s = s.replace(mt.group(0), mt.group(0) + block, 1)
            added += 1

        if 'rel="icon"' not in s and "rel='icon'" not in s:
            mt = RE_TITLE.search(s)
            if mt:
                s = s.replace(
                    mt.group(0),
                    mt.group(0) + '\n<link rel="icon" href="/favicon.ico" sizes="any">',
                    1,
                )

        p.write_text(s, encoding="utf-8")

    report["4. og tags added"] = [f"{added} pages"]
    report["4. og already present"] = [f"{already} pages"]
    report["4. skipped (no canonical)"] = skipped_no_canonical or ["(none)"]


# --------------------------------------------------------------------------
# 5. Brand hub structured data
# --------------------------------------------------------------------------
HUBS = [
    ("brands/apple.html", "Apple", "Apple Repair Costs Australia 2026", "Apple"),
    ("brands/apple-iphone.html", "iPhone", "iPhone Repair Costs Australia 2026", "Apple"),
    ("brands/samsung.html", "Samsung", "Samsung Galaxy Repair Costs Australia 2026", "Samsung"),
    ("brands/google.html", "Google Pixel", "Google Pixel Repair Costs Australia 2026", "Google"),
]


def step_hub_schema():
    done = []
    has_brands_index = (ROOT / "brands.html").exists()
    for relpath, leaf, name, brand in HUBS:
        p = ROOT / relpath
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8")
        if "BreadcrumbList" in s:
            continue
        crumbs = [f'{{"@type":"ListItem","position":1,"name":"Home","item":"{SITE}/"}}']
        pos = 2
        if has_brands_index:
            crumbs.append(
                f'{{"@type":"ListItem","position":2,"name":"Brands","item":"{SITE}/brands.html"}}')
            pos = 3
        crumbs.append(
            f'{{"@type":"ListItem","position":{pos},"name":"{leaf}","item":"{SITE}/{relpath}"}}')
        block = (
            '\n<script type="application/ld+json">\n'
            '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
            + ",".join(crumbs) + "]}\n</script>\n"
            '<script type="application/ld+json">\n'
            f'{{"@context":"https://schema.org","@type":"CollectionPage","name":"{name}",'
            f'"url":"{SITE}/{relpath}","isPartOf":{{"@type":"WebSite","url":"{SITE}/"}},'
            f'"about":{{"@type":"Brand","name":"{brand}"}},"inLanguage":"en-AU"}}\n</script>\n'
        )
        if "</head>" not in s:
            continue
        p.write_text(s.replace("</head>", block + "</head>", 1), encoding="utf-8")
        done.append(relpath)
    report["5. hub schema"] = done or ["(already present)"]


# --------------------------------------------------------------------------
# 6. Prose on the two thinnest hubs
# --------------------------------------------------------------------------
PROSE = {
    "brands/google.html": (
        "Select your Pixel",
        "Pixel repair pricing behaves differently from iPhone or Galaxy pricing in "
        "Australia, and the reason is supply. Pixel screens are not stocked at the "
        "volume Apple and Samsung parts are, so independent shops quote in a wider "
        "band and lead times run longer — a Pixel 8 Pro screen can sit a week "
        "behind an equivalent Galaxy job. Google's own authorised channel routes most "
        "out-of-warranty work through a mail-in partner, which adds shipping days on "
        "top. That combination is why the figures below are ranges rather than fixed "
        "prices: what you pay depends as much on whether the part is on a shelf in "
        "Sydney as on the repair itself. Pixels from the 6 series onward also use an "
        "under-display fingerprint sensor laminated to the screen, so a screen "
        "replacement that preserves the original sensor costs less than one that "
        "doesn't — worth asking any shop to confirm before you book."
    ),
    "brands/apple.html": (
        "What are you repairing?",
        "Apple repair pricing in Australia splits cleanly into three lanes, and knowing "
        "which lane you're in explains almost every quote you'll be given. Apple "
        "authorised service is the most expensive and the most predictable, uses "
        "genuine parts, and keeps your warranty intact. AppleCare+ collapses the cost "
        "to a fixed excess, but only if the plan was bought within 60 days of the "
        "device. Independent shops sit well below both, with the trade-off landing on "
        "part grade — and on newer iPhones, on the “unknown part” notice "
        "iOS shows after a non-genuine screen or battery goes in. That notice is "
        "cosmetic on most models, but it is worth knowing about before you choose. The "
        "model pages below break each device into screen, battery, back glass and "
        "charging port, with the independent range and the authorised figure side by "
        "side so the gap is visible rather than implied."
    ),
}

MARKER = "<!-- hub-intro -->"


def step_prose():
    done = []
    for relpath, (anchor_text, prose) in PROSE.items():
        p = ROOT / relpath
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8")
        if MARKER in s:
            continue
        # Reuse the exact class attribute of the page's hero paragraph so the
        # purged Tailwind build already contains every class used here.
        hero = re.search(r'<p class="(text-xl text-muted[^"]*)"', s)
        cls = hero.group(1) if hero else "text-xl text-muted max-w-2xl leading-relaxed"
        anchor = re.search(r"<h2[^>]*>" + re.escape(anchor_text) + r"</h2>", s)
        if not anchor:
            continue
        para = f'{anchor.group(0)}\n{MARKER}\n<p class="{cls}">{prose}</p>'
        p.write_text(s.replace(anchor.group(0), para, 1), encoding="utf-8")
        done.append(relpath)
    report["6. hub prose"] = done or ["(already present)"]


# --------------------------------------------------------------------------
# 7. Real sitemap lastmod
# --------------------------------------------------------------------------
OLD_TODAY = '    today = datetime.now().strftime("%Y-%m-%d")'
NEW_TODAY = '''    today = datetime.now().strftime("%Y-%m-%d")

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
        return _date_cache[rel]'''

OLD_LM = '        xml_content += f"    <lastmod>{today}</lastmod>\\n"'
NEW_LM = '        xml_content += f"    <lastmod>{_lastmod(url)}</lastmod>\\n"'


def step_sitemap_script():
    p = ROOT / "generate_sitemap.py"
    if not p.exists():
        report["7. sitemap script"] = ["(generate_sitemap.py not found)"]
        return
    s = p.read_text(encoding="utf-8")
    if "_lastmod" in s:
        report["7. sitemap script"] = ["(already patched)"]
        return
    if OLD_TODAY not in s or OLD_LM not in s:
        report["7. sitemap script"] = ["!! anchors not found — patch by hand"]
        return
    if "import subprocess" not in s:
        s = s.replace("from datetime import datetime",
                      "from datetime import datetime\nimport subprocess", 1)
    s = s.replace(OLD_TODAY, NEW_TODAY, 1).replace(OLD_LM, NEW_LM, 1)
    p.write_text(s, encoding="utf-8")
    report["7. sitemap script"] = ["generate_sitemap.py now uses git commit dates"]


def main():
    step_images()
    step_mojibake()
    step_logo()
    step_og()
    step_hub_schema()
    step_prose()
    step_sitemap_script()

    print("\n=== RepairRange SEO fix pack ===")
    for k in sorted(report):
        v = report[k]
        print(f"\n{k}:")
        for line in v[:12]:
            print(f"  - {line}")
        if len(v) > 12:
            print(f"  ... and {len(v) - 12} more")
    print()


if __name__ == "__main__":
    sys.exit(main())
