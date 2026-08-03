#!/usr/bin/env python3
import json, os, subprocess

payload = {
    "source_branch": "seo-phase3-eaat-faq",
    "target_branch": "main",
    "title": "SEO Phase 3: FAQ schema on diagnostic pages + data methodology page",
    "description": (
        "E-A-T and rich-result upgrades for repairrange.io.\n\n"
        "## FAQ schema (10 /fix/ diagnostic pages)\n"
        "Every diagnostic page now carries FAQPage JSON-LD with 4 questions each, grounded in that page's actual content: "
        "battery-drains-fast, black-screen, charging-port, cracked-screen-still-works, dropped-and-broken, "
        "ghost-touch, green-lines, overheating, water-damage, wont-turn-on.\n\n"
        "## Data methodology page (E-A-T)\n"
        "New /how-we-collect-data.html explains:\n"
        "- Where prices come from (verified shop low end, manufacturer pricing, researched top end)\n"
        "- What the three screen tiers mean\n"
        "- Update cadence (quarterly + event-driven)\n"
        "- What we deliberately exclude\n"
        "- How readers can challenge/correct data\n"
        "Linked from: about.html footer, repair cost hub hero, site footer, sitemap (420 URLs).\n\n"
        "## Verification\n"
        "- 45 JSON-LD blocks sitewide, 0 invalid\n"
        "- All changed pages HTML well-formed\n"
        "- Feature branch only, [skip ci]"
    ),
}

tok = os.environ.get("RR_TOKEN", "")
payload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_mr3_payload.json")
with open(payload_path, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False)

cmd = [
    "curl.exe", "-s", "-X", "POST",
    "https://gitlab.com/api/v4/projects/mayfield276%2Fblank-site-2026-05-06-6rrng/merge_requests",
    "-H", f"PRIVATE-TOKEN: {tok}",
    "-H", "Content-Type: application/json",
    "--data-binary", f"@{payload_path}",
]
out = subprocess.run(cmd, capture_output=True, text=True)
try:
    d = json.loads(out.stdout)
    print("MR !" + str(d.get("iid")))
    print(d.get("web_url"))
    if "error" in d:
        print("API ERROR:", d["error"])
except Exception as e:
    print("parse failed:", e)
    print(out.stdout[:500])
