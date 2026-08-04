#!/usr/bin/env python3
import json, os

payload = {
    "source_branch": "seo-phase6-close-gap",
    "target_branch": "main",
    "title": "SEO Phase 6: close the noindex gap - 67 more AI-news posts cleaned",
    "description": (
        "While preparing the GSC sitemap submission, a review gap surfaced: the Phase 1 noindex sweep only matched posts whose titles contained 'RepairRange News'. "
        "67 AI-generated news/aggregation posts with different title formats stayed indexed and in the sitemap.\n\n"
        "## What happened\n"
        "Classified all 121 remaining indexed blog posts: posts linked from blog.html (23, editorial picks) + 31 explicitly kept quality guides = 54 kept. "
        "The other 67 are AI news aggregation (device launches, leaks, waitlists, industry news), near-duplicates, promo content, and off-topic posts - now noindexed and removed from the sitemap.\n\n"
        "## Noindexed (67) - sample of the full list\n"
        "honor-x80-pro-max-10000-nit-brightness, spacex-starlink-ipo-investor-guide, openai-trump-ai-review-australia, fox-acquires-roku, "
        "ultrahuman-m2-live-glucose-monitoring, 26-years-of-gsmarena (x2 dups), 10x samsung-one-ui-9 rollout posts, 7x siri-ai waitlist posts, "
        "3x starlink/satellite, 2x trump-t1, 2x poco-x8 (dups), 2x smartwatch-shipments (dups), 2x sony-1000x (dups), "
        "getting-started-with-our-platform (SelfRepairKit sales page), where-your-pdf-goes (pdfrange content), "
        "unlocking-cheap-enterprise-storage-hba-cards (off-topic guide), plus iPhone Air 2 / foldable-leak / galaxy news posts.\n\n"
        "## Kept (54)\n"
        "All repair-cost guides, decision guides, how-to-fix guides, glossary, and the blog.html editorial index. "
        "Full keep list is in the branch (seo_phase6_close_gap.py KEEP set).\n\n"
        "## Also fixed\n"
        "- 3 quality posts (drfone-vs-imyfone, remove-adware, screen-parts-glossary) were missing from the sitemap - added\n"
        "- Sitemap now 351 URLs, zero noindexed pages, zero junk\n\n"
        "## Verification\n"
        "- 167 JSON-LD blocks valid, 0 errors\n"
        "- Full review sweep: 0 issues\n"
        "- Feature branch only, [skip ci]"
    ),
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_mr6_payload.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False)
print("written")
