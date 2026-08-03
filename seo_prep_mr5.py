#!/usr/bin/env python3
import json, os

payload = {
    "source_branch": "seo-phase5-polish",
    "target_branch": "main",
    "title": "SEO Phase 5: author bylines, duplicate consolidation, canonical sweep, noindex stragglers",
    "description": (
        "Final polish pass after a full-site review of the entire SEO update.\n\n"
        "## Author bylines + Article schema (E-A-A-T)\n"
        "- 123 indexed blog posts now show a By RepairRange byline under the H1, linking to the methodology page\n"
        "- 118 posts received Article JSON-LD (headline, publisher, author) - 167 valid JSON-LD blocks sitewide, 0 invalid\n\n"
        "## Duplicate consolidation\n"
        "- why-do-screen-repair-quotes-vary-so-much.html is now canonical+noindex to why-screen-repair-quotes-differ.html (kept the better-linked one, 8 vs 4 internal links)\n"
        "- All internal links rewritten; removed from sitemap\n\n"
        "## Noindex stragglers found in review\n"
        "- 2 /news/ posts (AI-generated) were still indexed - now noindexed\n"
        "- 3 pdfrange.com posts living in the blog (cross-domain canonical) - now noindexed + removed from sitemap\n"
        "- google_tag.html never actually got its noindex in Phase 1 (it had no head tag) - now wrapped in a proper noindex HTML skeleton\n"
        "- generate_tech_news.py template now emits noindex by default, preventing future news posts from being indexed\n\n"
        "## Canonical sweep\n"
        "- 245 indexed pages were missing self-referencing canonicals - all added\n"
        "- Removed empty template locations/city.html (0 bytes) from repo + sitemap\n"
        "- Sitemap now 415 URLs: zero noindexed pages, zero junk\n\n"
        "## Verification\n"
        "- Full review sweep: 0 remaining issues\n"
        "- 167 JSON-LD blocks, 0 invalid\n"
        "- Feature branch only, [skip ci]"
    ),
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_mr5_payload.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False)
print("written:", out)
