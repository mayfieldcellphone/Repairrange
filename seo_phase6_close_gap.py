#!/usr/bin/env python3
"""Phase 6: close the noindex gap — the first sweep matched only titles containing
'RepairRange News'. This pass classifies ALL remaining indexed blog posts:
- KEEP: repair/cost/guide content (explicit list below + anything linked from blog.html)
- NOINDEX: AI news aggregation, promo pages, off-topic posts (the rest)
Removes noindexed URLs from the sitemap.
"""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))

# Quality posts explicitly kept (not in blog.html index but clearly guide/cost content)
KEEP = {
    "esim-phone-repair-what-happens",
    "foldable-phone-repair-cost-guide",
    "how-to-back-up-phone-before-repair",
    "how-to-use-ai-on-your-phone",
    "ipad-repair-cost-guide-australia",
    "iphone-13-self-repair-service-alternative",
    "iphone-16-pro-touch-screen-lag-unresponsive-fix",
    "iphone-17-pro-max-repair-guide",
    "iphone-air-repair-cost-guide",
    "is-ai-on-your-phone-safe-privacy-myths",
    "lenovo-tablet-repair-cost-guide-australia",
    "macbook-laptop-repair-cost-guide-australia",
    "moisture-detected-samsung-bypass-charging",
    "phone-charging-port-not-working-troubleshoot",
    "phone-malware-ads-how-to-remove",
    "phone-repair-checklist-before-during-after",
    "phone-repair-cost-trends-australia",
    "phone-repair-costs-record-high-2026",
    "phone-repair-myths-debunked",
    "remove-adware-from-phone",
    "repair-or-replace-phone-decision-guide",
    "repair-vs-replace-2026-index",
    "right-to-repair-australia-phone-owners",
    "samsung-frp-bypass-google-lock-methods",
    "samsung-galaxy-s26-ultra-repair-guide",
    "screen-replacement-parts-glossary",
    "should-you-fix-phone-before-selling",
    "signs-phone-battery-needs-replacing",
    "water-damaged-phone-what-to-do",
    "drfone-vs-imyfone-comparison",
    "best-ai-phones-australia-2026",
}

# anything linked from blog.html is editorial keep
bh = open(os.path.join(ROOT, "blog.html"), encoding="utf-8").read()
blog_dir = os.path.join(ROOT, "blog")

noindexed = []
kept = []
for f in sorted(glob.glob(os.path.join(blog_dir, "*.html"))):
    slug = os.path.basename(f)[:-5]
    html = open(f, encoding="utf-8", errors="replace").read()
    if "noindex" in html:
        continue  # already handled
    if slug in KEEP or slug in bh:
        kept.append(slug)
        continue
    # noindex it
    html = html.replace("<head>", '<head>\n    <meta name="robots" content="noindex, nofollow">', 1)
    open(f, "w", encoding="utf-8").write(html)
    noindexed.append(slug)

print(f"NEW noindex: {len(noindexed)}")
print(f"kept: {len(kept)}")

# remove new noindexed URLs from sitemap
sm_path = os.path.join(ROOT, "sitemap.xml")
sm = open(sm_path, encoding="utf-8").read()
removed = 0
for slug in noindexed:
    url = f"https://repairrange.io/blog/{slug}.html"
    pat = re.compile(r"(?s)<url>\s*<loc>" + re.escape(url) + r"</loc>.*?</url>\s*")
    new_sm, n = pat.subn("", sm, count=1)
    if n:
        sm = new_sm
        removed += 1
open(sm_path, "w", encoding="utf-8").write(sm)
print(f"sitemap: removed {removed} URLs")

with open(os.path.join(ROOT, "..", "rr_noindexed_phase6.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(noindexed)))
print("list saved")
