#!/usr/bin/env python3
import json, os, subprocess

payload = {
    "source_branch": "seo-phase4-city-comparisons",
    "target_branch": "main",
    "title": "SEO Phase 4: city cost-comparison guides + fix wrong-city copy on location pages",
    "description": (
        "Two new pillar guides plus a content-quality bug fix discovered while building them.\n\n"
        "## New guides (both with FAQ + breadcrumb schema, grounded in published database ranges)\n"
        "1. /guides/phone-repair-costs-australia-cities.html - all six cities compared: national model ranges, what differs by city (rent, competition, parts market), city-by-city snapshot.\n"
        "2. /guides/phone-repair-costs-sydney-vs-melbourne.html - head-to-head: which city is cheaper, why Sydney's top end runs hotter, what's identical in both cities, how to get the cheapest honest quote.\n"
        "Linked from: guides index, sitemap (now 422 URLs).\n\n"
        "## Location page bug fix (important)\n"
        "The non-Sydney location pages were template-generated with wrong city copy:\n"
        "- melbourne/brisbane/perth/adelaide pages said 'the wider Hunter - Mayfield, Hamilton...' (Newcastle copy) and 'Sydney prices vary by suburb... Parramatta or Bankstown'\n"
        "- newcastle page also referenced Parramatta/Bankstown\n"
        "All 5 pages now have correct city-specific region and suburb copy (e.g. Melbourne: inner north & west; Perth: Fremantle & Joondalup). Sydney page was already correct.\n\n"
        "## Verification\n"
        "- 49 JSON-LD blocks sitewide, 0 invalid\n"
        "- New pages HTML well-formed\n"
        "- Feature branch only, [skip ci]"
    ),
}

tok = os.environ.get("RR_TOKEN", "")
payload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_mr4_payload.json")
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
except Exception:
    print("RAW:", out.stdout[:400])
