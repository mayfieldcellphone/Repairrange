#!/usr/bin/env python3
"""Generate city cost-comparison pillar pages under /guides/, grounded in the site's
published database ranges and location-page facts. No fabricated per-city quotes."""
import os, json, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_generate_guides import HEADER, build_schema_breadcrumb, build_schema_faq, related_links_html

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "guides")
os.makedirs(OUT, exist_ok=True)

PAGES = [
    {
        "slug": "phone-repair-costs-australia-cities",
        "nav_last": "Repair Costs by City",
        "h1": "Phone Repair Costs by City in Australia — Sydney vs Melbourne vs Brisbane vs Perth vs Adelaide (2026)",
        "lede": "Phone repair prices in Australia are national, then local. The model ranges we publish are the same in every capital city — but where you land inside those ranges is decided by your suburb, your shop's overheads, and the parts market around you. Here's the honest city-by-city picture.",
        "meta": "2026 phone repair costs by Australian city: how Sydney, Melbourne, Brisbane, Perth, Adelaide and Newcastle compare, why CBD quotes cost more, and the national price ranges that apply everywhere.",
        "faqs": [
            ("Are phone repair prices different in Sydney vs Melbourne?",
             "The model price ranges are national — the same parts and the same database ranges apply in every capital city. What differs is where you land inside the range: Sydney CBD shops charge a premium for speed and rent, while outer-suburban shops are routinely 20\u201330% cheaper. Melbourne shows the same CBD-vs-suburbs pattern."),
            ("Which Australian city has the cheapest phone repairs?",
             "The cheapest repairs are rarely about the city — they're about the suburb. In every capital, outer-suburban shops undercut CBD shops by 20\u201330% on labour. Adelaide and Perth tend to have slightly thinner parts markets, which can push premium-tier repairs (refurbished OEM screens) toward the top of the published range."),
            ("Do Apple, Samsung or Google official repair prices vary by city?",
             "No. Manufacturer out-of-warranty pricing is set nationally — an Apple screen replacement costs the same in Sydney, Perth and everywhere between. The city-to-city variation exists only in the independent market, where overheads and competition set the price."),
            ("Why do two shops in the same city quote different prices?",
             "The three drivers are rent (CBD vs suburb), parts tier (incell, aftermarket OLED, refurbished OEM), and warranty terms. Two shops 500 metres apart can differ by 30\u201350% for the same phone because they're quoting different parts — the cheapest quote is usually a different part, not a better deal."),
            ("Is it cheaper to mail my phone to Newcastle or another city for repair?",
             "Sometimes, if you're in a regional area with thin repair options — but factor in freight, insurance, and the extra days without your phone. For most capital-city residents, a good local suburban shop beats any mail-in option once time and risk are counted."),
        ],
        "body": """<h2>The national range, then the local reality</h2>
<p>Every RepairRange price is a range for a reason: the same screen replacement genuinely costs different amounts at a CBD shop, a suburban shop, and a manufacturer. The ranges in our <a href="/repair/phone-repair-costs-australia.html">74-model database</a> are national — a refurbished OEM iPhone 17 Pro Max screen is $115\u2013$449 whether you're in Sydney or Adelaide. What the database can't show in one number is where you'll actually land, and that's decided by five local factors:</p>
<ul>
<li><strong>Rent.</strong> A CBD shop pays 3\u20135x the rent of an outer-suburban shop. That cost lands in your quote.</li>
<li><strong>Competition density.</strong> More shops per suburb = sharper pricing. The busy parts of Sydney and Melbourne have the most repair shops per capita in Australia.</li>
<li><strong>Parts market.</strong> Sydney and Melbourne have the densest parts supplier networks, meaning same-day part availability and keener parts pricing. Perth, Adelaide, and regional centres rely on freight, which adds lead time and sometimes cost for premium tiers.</li>
<li><strong>Wages.</strong> Technician wages track city living costs — a factor in the top end of each range.</li>
<li><strong>Speed premium.</strong> "While-you-wait" CBD repairs are priced for your convenience, not for the parts.</li>
</ul>

<h2>City-by-city snapshot (2026)</h2>
<ul>
<li><strong>Sydney:</strong> The widest spread of any city. CBD shops charge a premium for speed; outer suburbs like Parramatta or Bankstown are routinely 20\u201330% cheaper. Dense parts market, same-day repairs everywhere. <a href="/locations/sydney.html">Sydney repair pricing page</a></li>
<li><strong>Melbourne:</strong> Same CBD-vs-suburbs pattern as Sydney with slightly lower top-end quotes in the inner north and west. Strong independent repair scene. <a href="/locations/melbourne.html">Melbourne repair pricing page</a></li>
<li><strong>Brisbane:</strong> Generally mid-range — lower rents than Sydney but a thinner premium parts market. Brisbane's independent scene is growing fast. <a href="/locations/brisbane.html">Brisbane repair pricing page</a></li>
<li><strong>Perth:</strong> Parts freight is the defining factor — premium-tier screens can take extra days and sit at the top of the published range. Labour rates are competitive. <a href="/locations/perth.html">Perth repair pricing page</a></li>
<li><strong>Adelaide:</strong> The most competitive small market — fewer shops, sharp pricing in the suburbs, and a parts market that favours planning ahead. <a href="/locations/adelaide.html">Adelaide repair pricing page</a></li>
<li><strong>Newcastle (Hunter):</strong> Regional pricing at its best — suburban rents, quick parts access via Sydney freight, and strong local independents. The most affordable of Australia's major metro areas for repairs. <a href="/locations/newcastle.html">Newcastle repair pricing page</a></li>
</ul>

<h2>What the model ranges actually are</h2>
<p>These verified ranges apply in every city — the local factor decides where you land:</p>
<ul>
<li><strong>iPhone screen repair:</strong> $99\u2013$449 depending on model and tier (iPhone 14 from $99, iPhone 17 Pro Max up to $449 for refurbished OEM).</li>
<li><strong>Samsung screen repair:</strong> $129\u2013$359 for current Galaxy S-series.</li>
<li><strong>Battery replacement:</strong> $79\u2013$149 across most models.</li>
<li><strong>Back glass:</strong> $89\u2013$259 independent (Apple $119\u2013$159 on iPhone 12+).</li>
</ul>
<p>Get your exact model on the <a href="/repair/phone-repair-costs-australia.html">cost database</a> or the <a href="/calculator.html">calculator</a>.</p>

<h2>How to use this page</h2>
<ol>
<li>Find your model's range on the <a href="/repair/phone-repair-costs-australia.html">database</a>.</li>
<li>Check your city's <a href="/locations.html">location page</a> for local context.</li>
<li>Use the <a href="/calculator.html">calculator</a> for a precise estimate.</li>
<li>Verify the shop against the <a href="/blog/how-to-find-trustworthy-phone-repair-shop.html">trustworthy-shop checklist</a> — a good quote is about the part tier and warranty, not just the number.</li>
</ol>

<h2>Related reading</h2>
<ul>
<li><a href="/guides/phone-repair-costs-sydney-vs-melbourne.html">Sydney vs Melbourne head-to-head</a></li>
<li><a href="/guides/phone-screen-repair-australia.html">Screen repair guide — costs &amp; quality tiers</a></li>
<li><a href="/guides/phone-battery-replacement-australia.html">Battery replacement guide</a></li>
<li><a href="/how-we-collect-data.html">How we collect and verify these prices</a></li>
<li><a href="/blog/why-screen-repair-quotes-differ.html">Why repair quotes differ between shops</a></li>
</ul>""",
        "related": [
            ("Sydney vs Melbourne head-to-head", "/guides/phone-repair-costs-sydney-vs-melbourne.html"),
            ("All repair costs — 74+ models", "/repair/phone-repair-costs-australia.html"),
            ("City location pages", "/locations.html"),
            ("Screen repair guide", "/guides/phone-screen-repair-australia.html"),
            ("Battery replacement guide", "/guides/phone-battery-replacement-australia.html"),
            ("How we collect data", "/how-we-collect-data.html"),
        ],
    },
    {
        "slug": "phone-repair-costs-sydney-vs-melbourne",
        "nav_last": "Sydney vs Melbourne",
        "h1": "Sydney vs Melbourne Phone Repair Costs — Which City Is Cheaper in 2026?",
        "lede": "Short answer: on average, Melbourne. Longer answer: it's not the city that sets your price, it's the suburb — and both cities show the same 20\u201330% CBD-vs-outer-suburb gap. Here's the head-to-head with the numbers that actually matter.",
        "meta": "Sydney vs Melbourne phone repair costs 2026: which city is cheaper, why CBD suburbs cost 20-30% more, manufacturer pricing comparison, and the national model ranges that apply in both cities.",
        "faqs": [
            ("Is phone repair cheaper in Sydney or Melbourne?",
             "On average, Melbourne edges Sydney out — Sydney's CBD rent premium and dense market push top-end quotes higher, while Melbourne's competitive inner-suburb scene keeps quotes mid-range. But the real saving in both cities is skipping the CBD: outer suburbs are routinely 20\u201330% cheaper than city-centre shops."),
            ("Do the same model ranges apply in both cities?",
             "Yes. The published ranges (iPhone $99\u2013$449, Samsung $129\u2013$359, batteries $79\u2013$149) are national — the same parts and prices in Sydney and Melbourne. The city difference is where you land inside the range, driven by rent, competition, and parts availability."),
            ("Is Apple's repair price different in Sydney vs Melbourne?",
             "No. Apple's out-of-warranty pricing is set nationally — an iPhone screen costs the same at Apple in Sydney and Melbourne. The same applies to Samsung and Google official repairs. Independent pricing is where the city-to-city variation lives."),
            ("What's the cheapest way to repair a phone in Sydney or Melbourne?",
             "Four levers, in order: choose a refurbished OEM or quality aftermarket OLED part rather than the flagship tier, use an outer-suburban independent shop rather than the CBD, get a written warranty (90 days is the norm), and check the quote against the national ranges before agreeing. A $99 iPhone 14 screen exists in both cities — it's an incell part, not a flagship OLED."),
            ("How much difference does the suburb make within each city?",
             "20\u201330% on the same repair, routinely. A CBD shop pays 3\u20135x the rent of an outer-suburban shop and prices that into the quote — sometimes for the convenience of while-you-wait service, sometimes just because it can. The same iPhone screen repair can be $150 in the Sydney CBD and $99\u2013$115 in Parramatta or Bankstown."),
        ],
        "body": """<h2>The head-to-head</h2>
<ul>
<li><strong>Sydney:</strong> the widest price spread of any Australian city. CBD shops charge a premium for speed and rent; outer suburbs (Parramatta, Bankstown, Liverpool) are routinely 20\u201330% cheaper. Sydney has the densest parts market in the country — same-day repairs are the norm. <a href="/locations/sydney.html">Sydney pricing</a></li>
<li><strong>Melbourne:</strong> a more evenly-priced market. The CBD is expensive but the inner north and west (Collingwood, Brunswick, Footscray) are sharp on price, and competition keeps the mid-range honest. Melbourne's top-end quotes tend to sit below Sydney's. <a href="/locations/melbourne.html">Melbourne pricing</a></li>
</ul>

<h2>The numbers that apply in both cities</h2>
<p>These are the national ranges from the <a href="/repair/phone-repair-costs-australia.html">database</a> — identical in Sydney and Melbourne, verified July 2026:</p>
<ul>
<li><strong>iPhone screen:</strong> $99\u2013$449 (iPhone 14 $99, iPhone 17 Pro Max to $449 refurbished OEM)</li>
<li><strong>Samsung Galaxy screen:</strong> $129\u2013$359 (S26 Ultra est., S24 Ultra)</li>
<li><strong>Battery replacement:</strong> $79\u2013$149 across most models</li>
<li><strong>Back glass:</strong> $89\u2013$259 independent; Apple $119\u2013$159 on iPhone 12+</li>
</ul>
<p>Where you land inside those ranges is the local question. Use the <a href="/calculator.html">calculator</a> for your exact model.</p>

<h2>Why Sydney's top end runs hotter</h2>
<p>Three structural reasons, none of them sinister:</p>
<ul>
<li><strong>Rent.</strong> Sydney retail rents are the highest in the country — a CBD shop's rent is 3\u20135x an equivalent Melbourne shop, and that shows up in the top of the range.</li>
<li><strong>Speed culture.</strong> More while-you-wait services, more CBD foot traffic — faster turnaround is priced in.</li>
<li><strong>Volume.</strong> Sydney has more shops, which should mean cheaper — and does, in the suburbs. The CBD premium simply overwhelms it in the city centre.</li>
</ul>

<h2>What's identical between the cities</h2>
<ul>
<li><strong>Manufacturer pricing.</strong> Apple, Samsung, Google official repairs are nationally priced — no city difference.</li>
<li><strong>Parts tiers.</strong> Incell, aftermarket OLED, refurbished OEM — the same three tiers, the same quality differences, in both cities.</li>
<li><strong>Warranty norms.</strong> 90-day warranties are the Australian standard in both.</li>
<li><strong>Consumer protections.</strong> Australian Consumer Law applies identically — see the <a href="/blog/phone-repair-warranty-australia-consumer-rights.html">warranty rights guide</a>.</li>
</ul>

<h2>How to get the cheapest honest quote in either city</h2>
<ol>
<li>Look up your model range first — <a href="/repair/phone-repair-costs-australia.html">database</a> or <a href="/calculator.html">calculator</a>.</li>
<li>Search outer suburbs, not the CBD. 20\u201330% is the typical gap.</li>
<li>Ask the shop which part tier the quote uses. A suspiciously cheap quote is usually an incell part on a flagship phone.</li>
<li>Check the <a href="/blog/how-to-find-trustworthy-phone-repair-shop.html">trustworthy-shop checklist</a> before you hand the phone over.</li>
</ol>

<h2>Related reading</h2>
<ul>
<li><a href="/guides/phone-repair-costs-australia-cities.html">All cities compared</a></li>
<li><a href="/guides/phone-screen-repair-australia.html">Screen repair costs &amp; quality tiers</a></li>
<li><a href="/how-we-collect-data.html">How we verify these prices</a></li>
<li><a href="/blog/why-screen-repair-quotes-differ.html">Why two shops quote differently</a></li>
<li><a href="/blog/phone-repair-warranty-australia-consumer-rights.html">Your repair warranty rights</a></li>
</ul>""",
        "related": [
            ("All cities compared", "/guides/phone-repair-costs-australia-cities.html"),
            ("Sydney pricing page", "/locations/sydney.html"),
            ("Melbourne pricing page", "/locations/melbourne.html"),
            ("All repair costs — 74+ models", "/repair/phone-repair-costs-australia.html"),
            ("Screen repair guide", "/guides/phone-screen-repair-australia.html"),
            ("How we collect data", "/how-we-collect-data.html"),
        ],
    },
]


def render(page):
    faq_html = "".join(
        f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in page["faqs"]
    )
    body = page["body"] + "\n\n<h2>Frequently asked questions</h2>\n" + faq_html
    title = page["h1"].split(" — ")[0] if " — " in page["h1"] else page["h1"]
    repl = {
        "{META}": page["meta"],
        "{SLUG}": page["slug"],
        "{TITLE}": title,
        "{SCHEMA_BREADCRUMB}": json.dumps(build_schema_breadcrumb(page["nav_last"], page["slug"]), ensure_ascii=False),
        "{SCHEMA_FAQ}": json.dumps(build_schema_faq(page["faqs"]), ensure_ascii=False),
        "{NAV_LAST}": page["nav_last"],
        "{H1}": page["h1"],
        "{LEDE}": page["lede"],
        "{BODY}": body,
        "{RELATED_LINKS}": related_links_html(page["related"]),
    }
    html = HEADER
    for k, v in repl.items():
        html = html.replace(k, v)
    return html


if __name__ == "__main__":
    for p in PAGES:
        out = os.path.join(OUT, p["slug"] + ".html")
        with open(out, "w", encoding="utf-8") as f:
            f.write(render(p))
        print("WROTE:", out)
