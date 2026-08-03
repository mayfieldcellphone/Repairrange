#!/usr/bin/env python3
"""Generate RepairRange pillar guide pages under /guides/ matching the site design system."""
import os, json, re

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "guides")
os.makedirs(OUT, exist_ok=True)

HEADER = '''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{META}">
<meta name="author" content="RepairRange">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://repairrange.io/guides/{SLUG}.html">
<meta property="og:url" content="https://repairrange.io/guides/{SLUG}.html">
<meta property="og:type" content="article">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{META}">
<meta property="og:site_name" content="RepairRange">
<title>{TITLE} | RepairRange</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
<script type="application/ld+json">
{SCHEMA_BREADCRUMB}
</script>
<script type="application/ld+json">
{SCHEMA_FAQ}
</script>
<style>
:root { --rr-teal-900:#0c4a45; --rr-teal-700:#0F766E; --rr-amber-600:#d97706; --rr-amber-500:#F59E0B; --rr-ink:#1C1917; --rr-muted:#78716C; --rr-line:#D6D3D1; --rr-paper:#F3F4F1; --rr-paper-2:#E7E5E4; --rr-hero:#E7E9E2; }
html { scroll-behavior: smooth; }
body { font-family:'Inter',system-ui,sans-serif; color:var(--rr-ink); background:var(--rr-paper); -webkit-font-smoothing:antialiased; }
.font-serif { font-family:'Fraunces','Iowan Old Style','Palatino',serif; font-feature-settings:'ss01'; }
.text-teal{color:var(--rr-teal-700);} .bg-teal-900{background:var(--rr-teal-900);}
.text-amber{color:var(--rr-amber-600);} .bg-amber{background:var(--rr-amber-500);}
.text-ink{color:var(--rr-ink);} .text-muted{color:var(--rr-muted);} .border-line{border-color:var(--rr-line);}
.bg-paper{background:var(--rr-paper);} .bg-paper-2{background:var(--rr-paper-2);}
.display { font-family:'Fraunces',serif; font-weight:400; letter-spacing:-0.025em; line-height:1.05; font-variation-settings:'opsz' 144; }
.eyebrow { font-size:0.75rem; font-weight:600; letter-spacing:0.18em; text-transform:uppercase; color:var(--rr-teal-700); }
.header-sticky { backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px); background:rgba(255,255,255,0.9); }
.ed-link { background-image:linear-gradient(currentColor,currentColor); background-position:0 100%; background-repeat:no-repeat; background-size:0% 1px; transition:background-size 220ms ease; }
.ed-link:hover { background-size:100% 1px; }
.btn { display:inline-flex; align-items:center; gap:0.5rem; padding:0.75rem 1.25rem; font-weight:600; font-size:0.9375rem; transition:all 200ms ease; border-radius:2px; }
.btn-primary { background:var(--rr-amber-500); color:var(--rr-ink); box-shadow:0 1px 0 var(--rr-amber-600); }
.btn-primary:hover { background:var(--rr-amber-600); color:white; transform:translateY(-1px); box-shadow:0 4px 0 var(--rr-amber-600); }
.card, .post-card { background:white; border:1px solid var(--rr-line); transition:all 300ms ease; display:block; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); }
.card:hover, .post-card:hover { border-color:var(--rr-ink); transform:translateY(-4px); }
.bg-mesh-hero { background-color: var(--rr-hero); background-image: radial-gradient(rgba(15, 118, 110, 0.15) 1.5px, transparent 0); background-size: 32px 32px; border-bottom: 2px solid var(--rr-line); }
.mobile-menu { transition:all 300ms ease-in-out; }
@media (max-width: 768px) { .mobile-menu.hidden{display:none;} .mobile-menu:not(.hidden){display:block;} }
.prose h2 { font-family:'Fraunces',serif; font-size:1.5rem; font-weight:500; margin-top:2.5rem; margin-bottom:0.75rem; color:var(--rr-ink); }
.prose h3 { font-size:1.05rem; font-weight:600; margin-top:1.5rem; margin-bottom:0.5rem; }
.prose p { line-height:1.75; color:var(--rr-ink); margin-bottom:1rem; }
.prose ul { list-style:disc; padding-left:1.5rem; margin-bottom:1rem; }
.prose li { line-height:1.7; margin-bottom:0.4rem; }
.prose a { color:var(--rr-teal-700); font-weight:600; text-decoration:underline; text-underline-offset:3px; }
.prose strong { font-weight:700; }
.faq-item { border:1px solid var(--rr-line); background:white; padding:1.25rem 1.5rem; margin-bottom:0.75rem; }
.faq-item h3 { margin:0 0 0.35rem 0; font-size:1rem; font-weight:700; }
.faq-item p { margin:0; line-height:1.65; color:var(--rr-muted); font-size:0.9375rem; }
</style>
</head>
<body class="bg-paper text-ink antialiased">
<header class="header-sticky sticky top-0 z-50 border-b border-line">
<nav class="max-w-6xl mx-auto px-6 md:px-8 py-4 flex items-center justify-between">
<a href="/index.html" class="flex items-center gap-2"><svg width="28" height="28" viewBox="0 0 28 28" fill="none"><rect x="1" y="1" width="26" height="26" rx="2" stroke="currentColor" stroke-width="1.5" class="text-teal"/><path d="M8 19 L8 9 L14 9 Q17 9 17 12 Q17 14.5 14.5 14.8 L18 19 M12 14.8 L8 14.8" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" class="text-teal" fill="none"/></svg><span class="font-serif text-2xl font-medium tracking-tight text-ink">RepairRange</span></a>
<div class="hidden md:flex items-center gap-8 text-sm">
<a href="/brands.html" class="ed-link font-medium text-ink hover:text-teal">Brands</a>
<a href="/repair/phone-repair-costs-australia.html" class="ed-link font-medium text-ink hover:text-teal">Repairs</a>
<a href="/guides/index.html" class="ed-link font-medium text-teal">Guides</a>
<a href="/fix.html" class="ed-link font-medium text-ink hover:text-teal">Troubleshoot</a>
<a href="/calculator.html" class="ed-link font-medium text-ink hover:text-teal">Repair Calculator</a>
<a href="/locations.html" class="ed-link font-medium text-ink hover:text-teal">Locations</a>
<a href="/blog.html" class="ed-link font-medium text-ink hover:text-teal">Blog</a>
<a href="/calculator.html" class="btn btn-primary text-sm">Get a Quote <i data-lucide="arrow-right" class="w-4 h-4"></i></a>
</div>
<button class="mobile-menu-button md:hidden text-ink" aria-label="Toggle menu"><i data-lucide="menu" class="w-6 h-6"></i></button>
</nav>
<div class="mobile-menu hidden md:hidden border-t border-line bg-paper"><div class="max-w-6xl mx-auto px-6 py-4 flex flex-col gap-1">
<a href="/brands.html" class="py-2 font-medium text-ink hover:text-teal">Brands</a>
<a href="/repair/phone-repair-costs-australia.html" class="py-2 font-medium text-ink hover:text-teal">Repairs</a>
<a href="/guides/index.html" class="py-2 font-medium text-teal">Guides</a>
<a href="/fix.html" class="py-2 font-medium text-ink hover:text-teal">Troubleshoot</a>
<a href="/calculator.html" class="py-2 font-medium text-ink hover:text-teal">Repair Calculator</a>
<a href="/locations.html" class="py-2 font-medium text-ink hover:text-teal">Locations</a>
<a href="/blog.html" class="py-2 font-medium text-ink hover:text-teal">Blog</a>
<a href="/calculator.html" class="btn btn-primary mt-3 self-start">Get a Quote</a>
</div></div>
</header>

<main class="bg-mesh-hero">
<section class="max-w-6xl mx-auto px-6 md:px-8 py-14 md:py-20">
<nav class="flex items-center gap-2 text-xs text-muted mb-6"><a href="/index.html" class="ed-link hover:text-teal">Home</a><span>/</span><a href="/guides/index.html" class="ed-link hover:text-teal">Repair Guides</a><span>/</span><span class="text-ink">{NAV_LAST}</span></nav>
<p class="eyebrow mb-4">Repair Guide</p>
<h1 class="display text-3xl md:text-5xl text-ink mb-6 max-w-3xl">{H1}</h1>
<p class="text-lg text-muted leading-relaxed mb-4 max-w-3xl">{LEDE}</p>
<div class="flex flex-wrap gap-3 mt-8">
<a href="/calculator.html" class="btn btn-primary">Get an Exact Estimate <i data-lucide="arrow-right" class="w-4 h-4"></i></a>
<a href="/repair/phone-repair-costs-australia.html" class="btn" style="border:1px solid var(--rr-line); background:white;">Browse 74+ Models</a>
</div>
</section>
</main>

<section class="max-w-6xl mx-auto px-6 md:px-8 py-12">
<div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
<div class="lg:col-span-2">
<div class="prose max-w-none">
{BODY}
</div>
</div>
<aside class="lg:col-span-1">
<div class="card p-6 sticky top-24">
<h3 class="eyebrow mb-4">Related Guides</h3>
<ul class="space-y-3 text-sm">
{RELATED_LINKS}
</ul>
<div class="mt-6 pt-6 border-t border-line">
<p class="text-xs text-muted mb-3">Need a precise number for your exact model?</p>
<a href="/calculator.html" class="btn btn-primary w-full justify-center text-sm">Try the Calculator</a>
</div>
</div>
</aside>
</div>
</section>

<footer class="bg-teal-900 text-white border-t border-white/10">
<div class="max-w-6xl mx-auto px-6 md:px-8 py-16 md:py-20">
<div class="grid grid-cols-1 md:grid-cols-12 gap-10 mb-12">
<div class="md:col-span-5"><div class="flex items-center gap-2 mb-4"><svg width="28" height="28" viewBox="0 0 28 28" fill="none"><rect x="1" y="1" width="26" height="26" rx="2" stroke="white" stroke-width="1.5"/><path d="M8 19 L8 9 L14 9 Q17 9 17 12 Q17 14.5 14.5 14.8 L18 19 M12 14.8 L8 14.8" stroke="white" stroke-width="1.5" stroke-linecap="square" fill="none"/></svg><span class="font-serif text-2xl font-medium">RepairRange</span></div><p class="text-white/70 text-sm max-w-sm leading-relaxed">Plain-English phone repair costs, fixes, and buying advice. Researched by people who actually do this work.</p></div>
<div class="md:col-span-3"><h3 class="eyebrow text-amber mb-4">Browse</h3><ul class="space-y-2 text-sm"><li><a href="/brands.html" class="text-white/80 hover:text-amber">Brands</a></li><li><a href="/fix.html" class="text-white/80 hover:text-amber">Troubleshooting</a></li><li><a href="/guides/index.html" class="text-white/80 hover:text-amber">Repair Guides</a></li><li><a href="/calculator.html" class="text-white/80 hover:text-amber">Cost Calculator</a></li><li><a href="/locations.html" class="text-white/80 hover:text-amber">Cities</a></li><li><a href="/blog.html" class="text-white/80 hover:text-amber">Blog</a></li></ul></div>
<div class="md:col-span-4"><h3 class="eyebrow text-amber mb-4">Ecosystem</h3><ul class="space-y-2 text-sm"><li><a href="https://selfrepairkit.com.au" class="text-white/80 hover:text-amber">SelfRepairKit — DIY Kits</a></li><li><a href="https://repairbill.shop" class="text-white/80 hover:text-amber">RepairBill — Shop Software</a></li><li><a href="https://www.mayfieldphonerepair.com.au" class="text-white/80 hover:text-amber">Mayfield Phone Repair</a></li><li><a href="/about.html" class="text-white/80 hover:text-amber">About RepairRange</a></li><li><a href="/privacy.html" class="text-white/80 hover:text-amber">Privacy Policy</a></li></ul></div>
</div>
<div class="pt-8 border-t border-white/15">
<p class="text-white/50 text-xs mb-3 max-w-3xl"><strong class="text-white/70">Affiliate disclosure:</strong> RepairRange may earn a commission when you click links to retailers.</p>
<div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3"><p class="text-white/50 text-xs">&copy; 2026 RepairRange. All rights reserved.</p><p class="text-white/50 text-xs">Not affiliated with Apple, Samsung, Google, or any device manufacturer.</p></div>
</div>
</div>
</footer>
<script>lucide.createIcons();</script>
</body>
</html>'''

PAGES = [
    {
        "slug": "phone-screen-repair-australia",
        "nav_last": "Screen Repair Guide",
        "h1": "Phone Screen Repair Australia — Costs, Quality Tiers & What to Expect in 2026",
        "lede": "Screen replacement is the most common phone repair in Australia — roughly 65% of repair-shop visits. The honest price range for a screen repair in 2026 is $120 to $740, and the number that matters far more than your phone model is which quality tier of part you choose.",
        "meta": "Complete 2026 guide to phone screen repair in Australia: costs by brand, incell vs aftermarket OLED vs refurbished OEM screens, DIY risk, and how to avoid overpaying.",
        "faqs": [
            ("How much does a phone screen repair cost in Australia in 2026?", "Between $120 and $740 depending on the phone and the part tier. An iPhone SE screen starts around $120 (incell), a flagship iPhone 17 Pro Max runs $250–$450 independent or $649 at Apple. Budget Android handsets are cheapest; foldables are the most expensive at $500+."),
            ("What is the difference between incell, aftermarket OLED and refurbished OEM screens?", "Incell is the budget tier — LCD with the touch layer fused in, used on older iPhones. Aftermarket OLED is a new third-party OLED panel, visually close to original. A refurbished OEM screen is the actual original panel, reclaimed and re-laminated with new glass — equivalent to a genuine new part."),
            ("Will a third-party screen repair affect Face ID or True Tone?", "Face ID is preserved by transferring the original front camera and dot projector during the repair. True Tone requires a display serial-code transfer, which skilled shops do with hardware programmers. Ask your shop whether both are restored — a good shop does it as standard."),
            ("Is it cheaper to repair at a chain or an independent shop?", "Independents are dramatically cheaper on incell and aftermarket OLED tiers — often less than half the manufacturer's price. On refurbished OEM screens the gap narrows or disappears; the benefits of a good independent shop are same-day turnaround, no data wipe, and no booking wait."),
            ("Can I repair my own phone screen to save money?", "It depends on the phone: older Pixels and iPhones are DIY-able (6/10 difficulty), Samsung flagships 7/10, foldables 9/10. The hidden costs are tools, adhesives, a second part when the first breaks, and the risk of killing the display or fingerprint sensor. See the DIY guide for model-by-model ratings."),
        ],
        "body": """<h2>What determines screen repair cost</h2>
<p>Two factors drive the price: <strong>the phone</strong> and <strong>the part</strong>. The part matters more. Every screen has a display panel, a touch digitiser, and an outer glass — and there are three quality tiers of replacement parts sold in Australia:</p>
<ul>
<li><strong>Incell</strong> — the budget tier. An LCD panel with the touch layer fused in. Used on older iPhones and entry-level models. Fine for a casual phone, noticeably different from OLED.</li>
<li><strong>Aftermarket OLED</strong> — a new third-party OLED panel. Visually close to the original, correct blacks and colour. The default choice for most repairs.</li>
<li><strong>Refurbished OEM</strong> — the original panel, reclaimed from a salvage device and re-laminated with new glass. This is a genuine original part in every way that matters, at a fraction of the manufacturer's price.</li>
</ul>
<p>Note that <strong>most Android flagships have no budget tier at all</strong> — Galaxy S, Pixel, and foldable screens are sold as a single expensive part. Apple is the only brand where you choose between tiers, which is why iPhone repairs show the widest price range.</p>

<h2>Screen repair prices by brand (2026 AUD, GST inclusive)</h2>
<ul>
<li><strong>Apple iPhone:</strong> $120 (iPhone SE, incell) up to $450+ (iPhone 17 Pro Max, refurbished OEM). Apple official: $379–$649.</li>
<li><strong>Samsung Galaxy S:</strong> $199–$389 for S-series, single part tier. Galaxy A-series from $119.</li>
<li><strong>Google Pixel:</strong> $129–$289 depending on generation; Pixel 9/9 Pro at the higher end.</li>
<li><strong>Foldables (Z Fold, Z Flip, Pixel Fold):</strong> $500+ — the most expensive screen repairs in Australia.</li>
<li><strong>Other brands (Oppo, Motorola, Xiaomi, Nothing, OnePlus):</strong> $89–$250 for mainstream models.</li>
</ul>
<p>Full model-by-model pricing with three tiers per phone is on the <a href="/repair/phone-repair-costs-australia.html">repair cost database</a>.</p>

<h2>Why quotes vary so much between shops</h2>
<p>Two shops on the same street can quote 30–50% differently for the same phone. The gap usually comes down to part tier, warranty terms, and whether the shop transfers serial codes (True Tone / Face ID). A $100 quote that uses a cheap incell panel on a flagship OLED phone is not a bargain — it's a downgrade. Read the breakdown of <a href="/blog/why-screen-repair-quotes-differ.html">why screen repair quotes vary</a> before you choose.</p>

<h2>What a quality screen repair should include</h2>
<ul>
<li><strong>Correct part tier</strong> — a refurbished OEM or quality aftermarket OLED, not a mismatched LCD on an OLED phone.</li>
<li><strong>Biometric preservation</strong> — Face ID and fingerprint sensors transferred or recalibrated. Samsung under-display ultrasonic sensors are a common casualty of bad repairs — see the <a href="/blog/samsung-fingerprint-sensor-screen-replacement-guide.html">Samsung fingerprint warning</a>.</li>
<li><strong>Original display features restored</strong> — True Tone, ambient light sensor, and auto-brightness working.</li>
<li><strong>Water-resistance resealing</strong> — a new perimeter seal, not just adhesive dots.</li>
<li><strong>Written warranty</strong> — 90 days is the Australian norm; some shops offer 6–12 months.</li>
</ul>

<h2>Genuine vs aftermarket — can you tell the difference?</h2>
<p>Yes, and you should check after a repair. Brightness, colour shift, True Tone, touch latency, and biometrics are the five tests a technician uses to verify a genuine screen. The <a href="/blog/how-to-tell-genuine-vs-aftermarket-screen.html">how to tell if your screen is genuine</a> guide walks through each test — no apps needed.</p>

<h2>DIY vs professional screen repair</h2>
<p>DIY kits start around $35 for parts plus $40–$70 in tools and adhesives. The realistic total, including a buffer for a second attempt, is usually within $30–$60 of a professional incell-tier repair — and you carry the risk of a cracked panel, a dead fingerprint sensor, or a phone that never seals properly again. The <a href="/blog/can-you-diy-phone-screen-repair.html">DIY screen repair guide</a> rates the difficulty model by model. If you do go DIY, the <a href="https://selfrepairkit.com.au">SelfRepairKit</a> guides cover screen protectors, panel fitting, and common mistakes.</p>

<h2>Related reading</h2>
<ul>
<li><a href="/blog/screen-quality-tiers-oem-aftermarket-refurbished-explained.html">OEM vs aftermarket vs refurbished screens explained</a></li>
<li><a href="/blog/iphone-vs-samsung-repair-cost-comparison.html">iPhone vs Samsung — which is cheaper to repair?</a></li>
<li><a href="/blog/what-happens-if-you-dont-fix-cracked-screen.html">What happens if you don't fix a cracked screen</a></li>
<li><a href="/blog/hidden-costs-cracked-phone-screen-diy-repair.html">The hidden costs of DIY screen repair</a></li>
</ul>""",
        "related": [
            ("All repair costs — 74+ models", "/repair/phone-repair-costs-australia.html"),
            ("Screen quality tiers explained", "/blog/screen-quality-tiers-oem-aftermarket-refurbished-explained.html"),
            ("iPhone vs Samsung repair cost", "/blog/iphone-vs-samsung-repair-cost-comparison.html"),
            ("Why screen quotes vary", "/blog/why-screen-repair-quotes-differ.html"),
            ("Can you DIY a screen repair?", "/blog/can-you-diy-phone-screen-repair.html"),
            ("Battery replacement guide", "/guides/phone-battery-replacement-australia.html"),
        ],
    },
    {
        "slug": "phone-battery-replacement-australia",
        "nav_last": "Battery Replacement Guide",
        "h1": "Phone Battery Replacement Australia — When to Replace & What It Costs in 2026",
        "lede": "A battery replacement costs $90–$200 in Australia and almost always beats buying a new phone. The catch: battery price barely moves as your phone ages, because you're not paying for the cell — you're paying for the risk of opening the device.",
        "meta": "2026 Australian guide to phone battery replacement: battery health thresholds, costs by brand, swollen battery safety, genuine vs aftermarket cells, and DIY vs professional.",
        "faqs": [
            ("How much does a phone battery replacement cost in Australia?", "Around $120–$150 for most iPhones at independent shops, $90–$200 across Samsung and Pixel. Apple charges $149–$199. DIY kits cost $35–$79 including tools. The price tracks the risk of opening the phone — the technician works through the display — not the cost of the cell."),
            ("When should I replace my phone battery?", "When Maximum Capacity drops below 80% or the phone shuts down above 20%. Most batteries retain 80% capacity after about 500 charge cycles (2–3 years of normal use). Below 80% you'll notice shorter days and unexpected shutdowns."),
            ("Is a swollen battery dangerous?", "Yes — it's a fire and explosion risk. If the screen or back panel is lifting, stop using the phone, don't charge it, and take it to a professional. Never puncture or try to remove a swollen battery yourself."),
            ("Is it worth replacing the battery on an old phone?", "Almost always. A $90–$150 battery on a phone that still receives security updates gives you 2–3 more years of life for a fraction of a new phone's cost. Use the 40% rule: if the repair is under 40% of a replacement device, repair it."),
            ("Why does battery replacement sometimes not fix the problem?", "About 80% of 'battery problems' are actually software, cable, or charging-port issues. If your phone drains fast but the health reads 90%+, check background apps and the charging port before paying for a new cell. The troubleshooting guide explains how to tell the difference."),
        ],
        "body": """<h2>Battery health — when to replace, when to wait</h2>
<p>Your phone tells you. iPhone: Settings → Battery → Battery Health & Charging. Samsung: Settings → Battery and Device Care → Diagnostics. Pixel: Settings → Battery → Battery Health. The number that matters is <strong>Maximum Capacity</strong>:</p>
<ul>
<li><strong>100–90%:</strong> No action needed. You're in the first year or two of normal use.</li>
<li><strong>89–81%:</strong> Watch it. Days are shorter but the phone is fine.</li>
<li><strong>80% and below:</strong> Replace it. Below 80% you get shutdowns above 20%, throttled performance, and faster degradation of the cell itself.</li>
</ul>
<p>The deeper explanation — including why a battery can degrade faster than the health number suggests — is in the <a href="/blog/battery-health-when-to-replace.html">battery health guide</a>.</p>

<h2>Battery replacement costs by brand (2026 AUD)</h2>
<ul>
<li><strong>Apple iPhone:</strong> $89–$150 independent; $149–$199 at Apple. Batteries are diagnosable — a programmed cell restores the Battery Health reading.</li>
<li><strong>Samsung Galaxy:</strong> $99–$200 depending on model. S-series and foldables at the higher end because of display risk during opening.</li>
<li><strong>Google Pixel:</strong> $89–$150. Pixel batteries are straightforward but require care with the display adhesive.</li>
<li><strong>Oppo, Motorola, Xiaomi, other brands:</strong> $69–$130 for mainstream models.</li>
</ul>
<p>Model-exact figures are on the <a href="/repair/phone-repair-costs-australia.html">repair cost database</a> and the <a href="/calculator.html">calculator</a>.</p>

<h2>Why the price doesn't fall as your phone ages</h2>
<p>This is the counter-intuitive fact of phone repair: a battery for a 5-year-old iPhone 11 costs about the same as one for a current iPhone 17. The cell itself is cheap — the cost is <strong>the risk of opening the handset</strong>. The technician goes in through the display, so a battery job inherits the display's fragility and replacement cost. That's also why premium shops quote batteries with a display-damage policy.</p>

<h2>Genuine vs aftermarket batteries</h2>
<ul>
<li><strong>Genuine / OEM-spec:</strong> Full cycle life, correct health reporting, safe chemistry certification. Costs more, lasts properly.</li>
<li><strong>Generic / cheap cells:</strong> Often 30–50% less capacity than rated, faster degradation, and some won't report health correctly.</li>
<li><strong>Diagnosable batteries (iPhone):</strong> Include a small controller board so the phone reports genuine-style Battery Health. Worth the premium.</li>
</ul>
<p>Swollen or leaking cells are never worth saving money on. A swollen battery is a fire risk and should be handled only by a professional — see the <a href="/blog/signs-phone-battery-needs-replacing.html">signs your battery needs replacing</a> guide for the full safety checklist.</p>

<h2>DIY vs professional battery replacement</h2>
<p>DIY kits run $35–$79 including tools — under half the professional price. The trade-offs: adhesive removal risk, the chance of breaking the display during opening (an instant $150–$400 mistake), and no warranty if the cell fails. Most people who attempt it succeed on older models; on modern water-resistant flagships the risk is real. <a href="https://selfrepairkit.com.au/blog/can-you-replace-phone-battery-guide.html">SelfRepairKit's battery guide</a> covers the process and the safety coordinates.</p>

<h2>Related reading</h2>
<ul>
<li><a href="/blog/battery-health-when-to-replace.html">Battery health explained — the degradation curve</a></li>
<li><a href="/blog/signs-phone-battery-needs-replacing.html">8 signs your battery needs replacing</a></li>
<li><a href="/blog/phone-insurance-vs-self-insuring-australia.html">Phone insurance vs self-insuring — the honest math</a></li>
<li><a href="/fix/battery-drains-fast.html">Battery drains in hours — diagnostic guide</a></li>
<li><a href="/guides/repair-or-replace-phone.html">Repair or replace your phone?</a></li>
</ul>""",
        "related": [
            ("Battery health explained", "/blog/battery-health-when-to-replace.html"),
            ("Signs you need a new battery", "/blog/signs-phone-battery-needs-replacing.html"),
            ("Battery drains fast — diagnose", "/fix/battery-drains-fast.html"),
            ("All repair costs — 74+ models", "/repair/phone-repair-costs-australia.html"),
            ("Repair or replace?", "/guides/repair-or-replace-phone.html"),
            ("Screen repair guide", "/guides/phone-screen-repair-australia.html"),
        ],
    },
    {
        "slug": "phone-water-damage-repair",
        "nav_last": "Water Damage Guide",
        "h1": "Water Damage Phone Repair Australia — The First 10 Minutes Decide Everything",
        "lede": "Water damage repair in Australia costs $80–$250 and succeeds in most cases — if the phone is powered off immediately. The first ten minutes matter more than the entire week after. Here's what to do, what to skip, and what it will cost.",
        "meta": "Australian water damage phone repair guide 2026: first 10 minutes emergency steps, rice myth debunked, IP ratings, repair costs, and data recovery from wet phones.",
        "faqs": [
            ("Can a water damaged phone be fixed?", "Yes, in many cases. If you power off immediately and avoid charging, a professional can often save the device. Success rates drop sharply if the phone stayed on or was charged while wet. Time to a technician is the single biggest factor."),
            ("Should I put my wet phone in rice?", "No. Rice does not effectively absorb moisture from inside a phone and introduces starch into ports and speakers. Power off, dry the exterior, and get to a professional. The rice myth has been debunked repeatedly."),
            ("How much does water damage repair cost in Australia?", "$80–$250 depending on severity and model. Light exposure (ultrasonic cleaning): $80–$120. Moderate (cleaning + minor parts): $120–$180. Severe or salt water (cleaning + microsoldering): $180–$250+. Data recovery from a wet phone is quoted separately and starts around $150."),
            ("Does IP68 mean my phone is waterproof?", "No. IP68 means resistance under controlled lab conditions — fresh water at a specific depth and time. Pool chemicals, salt water, soap, hot water, and movement break the seal. Apple and Samsung warranties don't cover water damage, which tells you what the rating really means."),
            ("Can data be recovered from a water damaged phone?", "Often yes, even from phones that won't power on. The board-level technician can bypass a dead display to extract storage, or remove the flash chip for chip-off recovery. Costs start around $150–$250 and depend on corrosion severity. The earlier it's treated, the better the odds."),
        ],
        "body": """<h2>The first 10 minutes — what to do</h2>
<ul>
<li><strong>1. Power it off immediately.</strong> Electricity + moisture = corrosion. Every second powered on spreads damage.</li>
<li><strong>2. Don't charge it.</strong> Charging a wet phone is the fastest way to kill the logic board.</li>
<li><strong>3. Remove the SIM tray and any case.</strong> More drying paths, less trapped moisture.</li>
<li><strong>4. Dry the exterior</strong> with a lint-free cloth. Don't shake — that pushes water deeper.</li>
<li><strong>5. Get it to a professional within hours.</strong> Corrosion starts immediately and accelerates. A repair shop can open, clean, and dry it properly — see the <a href="/fix/water-damage.html">water damage diagnostic guide</a> for the full first-aid sequence.</li>
</ul>
<p><strong>What NOT to do:</strong> don't use rice, don't use a hair dryer (heat warps seals and melts adhesive), don't insert cotton buds or cloth into ports, and don't power the phone on to 'check if it works'.</p>

<h2>What water damage repair actually involves</h2>
<ul>
<li><strong>Ultrasonic cleaning:</strong> the board is bathed in solvent and ultrasonic agitation to dissolve corrosion residue. $80–$120.</li>
<li><strong>Component replacement:</strong> charging ports, speakers, and connectors that corrode first. Adds $30–$80 in parts.</li>
<li><strong>Microsoldering:</strong> re-flowing or replacing corroded ICs, resistors, and board traces. This is where the $180–$250+ range comes in — and where skill separates a saved phone from a dead one.</li>
<li><strong>Corrosion arrest:</strong> treating the board so damage doesn't spread over the following weeks. A 'working' phone can die a month later if corrosion wasn't arrested.</li>
</ul>
<p>Salt water is a different story: the salt is conductive and aggressive, and corrosion spreads fast. If the phone went in salt water, tell the technician — they'll prioritize an immediate ultrasonic bath over drying.</p>

<h2>IP ratings — what your phone can actually survive</h2>
<p>IP67 (1 metre, 30 minutes) and IP68 (deeper, longer) sound impressive, but the ratings assume fresh water, static conditions, and intact seals. Real-world incidents fail the rating in seconds: pool chlorine, sea salt, soap, pressure from swimming, hot water from a sink. And every repair that opens a phone and doesn't reseal it properly lowers the rating further. The <a href="/blog/iphone-water-resistance-ip-rating-guide.html">IP rating explainer</a> has the details.</p>

<h2>Data recovery from a wet phone</h2>
<p>Your photos and messages are recoverable in most cases, even if the phone is dead. Techniques, in order of escalation:</p>
<ul>
<li><strong>Display bypass</strong> — extract data from a phone with a dead screen but working logic.</li>
<li><strong>Board-level recovery</strong> — clean the board enough to boot briefly and pull data.</li>
<li><strong>Chip-off recovery</strong> — remove the storage chip and read it directly. Last resort, most expensive ($300+).</li>
</ul>
<p>Backups are cheaper than any of these. The <a href="/blog/phone-repair-checklist-before-during-after.html">backup checklist</a> shows how to protect data before an incident, not after.</p>

<h2>Related reading</h2>
<ul>
<li><a href="/fix/water-damage.html">Water damage — first 10 minutes diagnostic</a></li>
<li><a href="/blog/water-damaged-phone-what-to-do.html">Water damaged phone — 60-minute emergency guide</a></li>
<li><a href="/blog/phone-repair-checklist-before-during-after.html">What to back up before any repair</a></li>
<li><a href="/blog/repair-or-replace-phone-decision-guide.html">Repair or replace after damage?</a></li>
<li><a href="/guides/phone-battery-replacement-australia.html">Battery replacement guide</a></li>
</ul>""",
        "related": [
            ("Water damage — first 10 minutes", "/fix/water-damage.html"),
            ("60-minute emergency guide", "/blog/water-damaged-phone-what-to-do.html"),
            ("IP ratings explained", "/blog/iphone-water-resistance-ip-rating-guide.html"),
            ("Backup before repair", "/blog/phone-repair-checklist-before-during-after.html"),
            ("Repair or replace?", "/guides/repair-or-replace-phone.html"),
            ("All repair costs", "/repair/phone-repair-costs-australia.html"),
        ],
    },
    {
        "slug": "repair-or-replace-phone",
        "nav_last": "Repair vs Replace Guide",
        "h1": "Repair or Replace Your Phone? The 2026 Australian Decision Guide",
        "lede": "The 40% rule: if the repair costs less than 40% of a comparable replacement, repair it. Most repairs pass that test easily — a $150 battery on a $1,500 phone is an obvious yes. The edge cases are where you actually need to think.",
        "meta": "Should you repair or replace your phone in 2026? The 40% rule, depreciation math, insurance comparison, trade-in timing, and when a repair genuinely isn't worth it — Australian guide.",
        "faqs": [
            ("When is it worth repairing a phone vs buying a new one?", "Use the 40% rule: repair if it costs less than 40% of a comparable replacement. A $200 screen on a $900 phone is a clear repair. A $500 repair on a $900 phone starts to be questionable — compare against the trade-in value and the age of the device."),
            ("How many years should you keep a phone?", "Most 2026 phones get 5–7 years of software updates (Apple 6+, Samsung and Google 7). With a battery replacement at year 2–3, a phone can comfortably last 5+ years. Replace on need — broken, unsupported, or genuinely slow — not on age."),
            ("Should I repair a 5-year-old phone?", "It depends. A $79–$150 battery on a phone that still gets security updates is good value. A $300+ screen on the same phone may not be, because resale value is likely below the repair cost. Check software support status first."),
            ("Is phone insurance worth it?", "Usually no, for most people. The honest math: AppleCare+ and carrier insurance cost more over a typical phone's life than the average repair bill, once deductibles are counted. Self-insuring — setting aside the premium — covers the typical case. The full comparison is in the insurance guide."),
            ("Does repairing a phone hurt its resale value?", "A repaired phone with a documented quality repair retains more value than a broken one, but less than an untouched one. A genuine-parts repair with paperwork holds value best. If you plan to sell, fix the phone first — a working device sells for materially more."),
        ],
        "body": """<h2>The 40% rule</h2>
<p>Compare the repair quote against the price of a comparable replacement — same tier, not the newest flagship. If the repair is under 40%, repair. Over 60%, replacing usually wins. Between 40–60%, weigh the intangibles: software support remaining, whether the phone is damaged elsewhere, and how long you planned to keep it.</p>
<ul>
<li><strong>Battery replacement ($90–$200)</strong> — almost always repair. Even on a 3-year-old phone, a new battery buys 2+ more years.</li>
<li><strong>Screen replacement ($120–$450)</strong> — usually repair on flagships under 4 years old; think twice on budget phones where the screen is a big fraction of the phone's value.</li>
<li><strong>Back glass ($80–$250 independent, $279–$899 at Apple)</strong> — repair, unless the phone is already end-of-life. Apple's chassis pricing makes the independent option obvious.</li>
<li><strong>Water damage ($80–$250)</strong> — repair only if the quote is moderate and the phone was otherwise healthy. Unrecoverable boards are common with salt water.</li>
<li><strong>Logic board / microsoldering ($150–$400+)</strong> — borderline. Compare against replacement; on older phones, replacement wins.</li>
</ul>
<p>The <a href="/blog/repair-vs-replace-decision-guide.html">full decision guide</a> walks through each scenario with worked examples.</p>

<h2>Depreciation — the maths nobody does</h2>
<p>Phones lose roughly 40–50% of their value in the first year, then ~15–20% per year after. A $1,500 iPhone is worth ~$600 after two years. That reframes repair decisions:</p>
<ul>
<li>A $200 repair on a 2-year-old phone returns the phone to full function for less than the phone's remaining value.</li>
<li>A $500 repair on the same phone is a worse deal than selling it damaged (~$250–$350) and buying a refurbished replacement.</li>
</ul>
<p>Trade-in values matter here — see <a href="/blog/should-you-fix-phone-before-selling.html">whether to fix before selling</a> for the numbers.</p>

<h2>Software support — the hidden clock</h2>
<p>Security updates define a phone's useful life more than hardware does. Apple supports iPhones 6+ years; Samsung and Google now promise 7 years for flagships. Once updates stop, banking apps, payments, and even web services start breaking. A phone that still receives updates is almost always worth repairing; one that doesn't is a candidate for replacement regardless of the repair math.</p>

<h2>Insurance vs self-insuring</h2>
<p>The short version: for most people, insurance is a bad bet. AppleCare+ on a mid-tier iPhone costs roughly $150–$300/year with deductibles on top; carrier insurance similar. The average Australian repair bill is $89–$250 — below the annual premium. The <a href="/blog/phone-insurance-vs-self-insuring-australia.html">insurance vs self-insuring analysis</a> does the full comparison, including the cases where insurance wins (accident-prone users, new flagships).</p>

<h2>Environmental angle</h2>
<p>Repairing keeps a working device out of landfill. Manufacturing a new phone emits roughly 50–80 kg of CO₂e before you even turn it on; a repair adds single-digit kilograms. The repair-first economy is not just sentiment — see <a href="/blog/repair-first-economy-e-waste-sustainability.html">the repair-first economy</a> and Australia's <a href="/blog/right-to-repair-australia-phone-owners.html">right to repair progress</a>.</p>

<h2>Related reading</h2>
<ul>
<li><a href="/blog/repair-vs-replace-decision-guide.html">Repair vs replace — the 40% rule in detail</a></li>
<li><a href="/blog/phone-insurance-vs-self-insuring-australia.html">Phone insurance — is it worth it?</a></li>
<li><a href="/blog/should-you-fix-phone-before-selling.html">Fix before selling? Trade-in math</a></li>
<li><a href="/blog/smartphone-longevity-pivot-2026-repair-trends.html">Why Australians are keeping phones 5+ years</a></li>
<li><a href="/blog/phone-repair-warranty-australia-consumer-rights.html">Your repair warranty rights</a></li>
<li><a href="/guides/phone-battery-replacement-australia.html">Battery replacement guide</a></li>
</ul>""",
        "related": [
            ("Repair vs replace — full guide", "/blog/repair-vs-replace-decision-guide.html"),
            ("Insurance vs self-insuring", "/blog/phone-insurance-vs-self-insuring-australia.html"),
            ("Fix before selling?", "/blog/should-you-fix-phone-before-selling.html"),
            ("All repair costs", "/repair/phone-repair-costs-australia.html"),
            ("Battery replacement guide", "/guides/phone-battery-replacement-australia.html"),
            ("Screen repair guide", "/guides/phone-screen-repair-australia.html"),
        ],
    },
    {
        "slug": "ipad-tablet-repair-costs-australia",
        "nav_last": "iPad & Tablet Repair Guide",
        "h1": "iPad & Tablet Repair Costs Australia — What Screens and Batteries Actually Cost in 2026",
        "lede": "Tablet repairs range from $69 for a budget Amazon Fire screen to $999 for a MacBook Pro panel. The repair-to-value ratio on tablets is worse than phones — a screen can be half the tablet's worth. Here's what each category costs and when to walk away.",
        "meta": "Australian iPad and tablet repair cost guide 2026: iPad Pro/Air/mini/standard screens and batteries, Samsung Galaxy Tab, Lenovo, Surface and Fire tablets, repair vs replace advice.",
        "faqs": [
            ("How much does an iPad screen repair cost in Australia?", "iPad 10th gen $149–$269, iPad mini $179–$329, iPad Air $199–$399, iPad Pro 11-inch $249–$549. iPad Pro 12.9-inch OLED models are the most expensive — the panel is a large fraction of the tablet's value."),
            ("Is it worth repairing a tablet screen?", "Run the 40% rule against a comparable replacement. Budget tablets (Amazon Fire $69–$149 screens) are often not worth repairing. Mid-tier iPads and Samsung Tabs usually are — a $200 screen on a $700 tablet is a sensible repair."),
            ("How much does a tablet battery replacement cost?", "iPad battery: $89–$199 depending on model. Samsung Galaxy Tab: $79–$189. Lenovo: $59–$139. Budget Fire tablets: $49–$89. iPad batteries are notoriously hard to access — the display is glued and must be removed to reach the cell."),
            ("Can I repair my iPad screen myself?", "Possible but harder than phones — large glued displays, fragile OLED panels, and Apple's parts pairing mean a botched repair can brick Face ID or True Tone. DIY difficulty is 7/10 for most iPads. Professional repair is usually the better value."),
            ("Why is MacBook repair so much more expensive?", "MacBook screens cost $349–$999 because the display assembly includes the full lid, and Apple's newer models pair the panel to the logic board — a non-genuine panel can trigger warnings. Retina panels and the aluminium unibody also make parts expensive."),
        ],
        "body": """<h2>iPad screen repair costs (2026 AUD)</h2>
<ul>
<li><strong>iPad 10th gen (budget):</strong> $149–$269</li>
<li><strong>iPad mini (6th/7th gen):</strong> $179–$329</li>
<li><strong>iPad Air (M2/M3):</strong> $199–$399</li>
<li><strong>iPad Pro 11-inch:</strong> $249–$549</li>
<li><strong>iPad Pro 12.9-inch (M4 OLED):</strong> at the top of the range — confirm with the shop, panel cost is steep</li>
</ul>
<p>Apple's official out-of-warranty pricing is typically 20–40% higher than independent shops on these. The full <a href="/blog/ipad-repair-cost-guide-australia.html">iPad repair cost guide</a> breaks down each generation.</p>

<h2>Samsung Galaxy Tab and other Android tablets</h2>
<ul>
<li><strong>Galaxy Tab S10 Ultra/Plus/FE:</strong> $249–$549 screens, $119–$189 batteries</li>
<li><strong>Galaxy Tab S9 series:</strong> $199–$499 screens, $99–$169 batteries</li>
<li><strong>Galaxy Tab A9 (budget):</strong> $109–$229 screens, $79–$129 batteries</li>
<li><strong>Lenovo Tab (P12 Pro, M11, M10):</strong> $89–$299 screens — the best value in tablet repair</li>
<li><strong>Microsoft Surface Pro/Go:</strong> $299–$699 screens — complex teardowns, high parts cost</li>
<li><strong>Amazon Fire HD:</strong> $69–$149 screens. Often not worth repairing — see below.</li>
</ul>
<p>Tablet pricing varies more than phone pricing because screen size, display technology (LCD vs OLED), and parts availability all swing the cost. Use the <a href="/calculator.html">calculator</a> for a model-specific estimate.</p>

<h2>When a tablet is NOT worth repairing</h2>
<p>Tablets have the worst repair-to-value ratio of any device category because:</p>
<ul>
<li>Budget tablets (Fire HD, Galaxy Tab A9) cost $149–$299 new — a $100+ screen repair is half the device's value, and a year later the tablet is obsolete.</li>
<li>Tablets are used longer than phones (often 4–6 years), so a repaired tablet may only get 1–2 more years before the next failure.</li>
<li>Parts pairing (Apple, and increasingly Samsung) can leave a repaired tablet with missing True Tone, Face ID, or battery-health reporting.</li>
</ul>
<p>The rule: if the screen repair is under 40% of a comparable replacement <em>and</em> the tablet still gets updates, repair. Otherwise, replace. See the <a href="/guides/repair-or-replace-phone.html">repair vs replace guide</a> for the framework.</p>

<h2>iPad battery replacement — the hidden difficulty</h2>
<p>iPad batteries are inside a glued-shut unibody. The technician must heat, cut, and peel the display to reach the cell — one slip and the screen cracks. That labour is why iPad battery jobs cost $89–$199 while the cell itself is worth $30. It's also why DIY iPad battery replacement is riskier than phone batteries.</p>

<h2>MacBook repair — why the prices shock people</h2>
<p>MacBook Air screens: $349–$699. MacBook Pro: $499–$999. The display assembly includes the whole lid — panel, glass, hinge components — and Apple pairs newer panels to the logic board. The <a href="/blog/macbook-laptop-repair-cost-guide-australia.html">MacBook repair cost guide</a> explains what you're paying for and how to get the genuine-parts price down.</p>

<h2>Related reading</h2>
<ul>
<li><a href="/blog/ipad-repair-cost-guide-australia.html">iPad repair cost guide by generation</a></li>
<li><a href="/blog/lenovo-tablet-repair-cost-guide-australia.html">Lenovo tablet repair costs</a></li>
<li><a href="/blog/macbook-laptop-repair-cost-guide-australia.html">MacBook repair costs</a></li>
<li><a href="/guides/repair-or-replace-phone.html">Repair vs replace framework</a></li>
<li><a href="/blog/phone-repair-warranty-australia-consumer-rights.html">Warranty and your rights</a></li>
</ul>""",
        "related": [
            ("iPad repair cost guide", "/blog/ipad-repair-cost-guide-australia.html"),
            ("Lenovo tablet costs", "/blog/lenovo-tablet-repair-cost-guide-australia.html"),
            ("MacBook repair costs", "/blog/macbook-laptop-repair-cost-guide-australia.html"),
            ("Repair vs replace", "/guides/repair-or-replace-phone.html"),
            ("All repair costs", "/repair/phone-repair-costs-australia.html"),
            ("Phone battery guide", "/guides/phone-battery-replacement-australia.html"),
        ],
    },
]

INDEX_FAQ = [
    ("What is RepairRange?", "RepairRange is an independent Australian phone repair price database. We publish real, verified repair costs for 74+ phone models across three screen quality tiers, plus battery, back glass, and manufacturer pricing — all 2026 AUD, GST inclusive, researched by working technicians."),
    ("How do I find out how much my repair will cost?", "Use the cost calculator for an instant estimate, or browse the full repair cost database which lists every model with screen, battery, and back glass pricing. The low end of each range is verified retail from an independent shop; the top end is an estimate."),
    ("Is it cheaper to repair or replace my phone?", "Usually repair — the 40% rule says repair if the cost is under 40% of a comparable replacement. Our repair vs replace guide walks through the decision with real numbers."),
    ("What phone brands do you cover?", "Apple iPhone (28 models), Samsung Galaxy (24 models), Google Pixel (11 models), plus OnePlus, Nothing, Xiaomi, OPPO, Motorola, and Sony. Tablet and laptop ranges are covered in the iPad & tablet guide."),
]

INDEX_BODY = """<h2>Start with your symptom</h2>
<p>Not sure what's wrong? The <a href="/fix.html">troubleshooting library</a> works symptom-first — pick what your phone is doing (cracked screen, battery draining, won't charge, water damage) and get a likely cause, a likely cost, and an honest repair-vs-replace take.</p>

<h2>Screen repair</h2>
<p>The most common repair in Australia. Costs range $120–$740 depending on the phone and which part tier you choose — incell, aftermarket OLED, or refurbished OEM. The <a href="/guides/phone-screen-repair-australia.html">screen repair guide</a> explains the tiers, brand-by-brand prices, and what a quality repair must include.</p>

<h2>Battery replacement</h2>
<p>Batteries run $90–$200 and are almost always worth it — the price tracks the risk of opening the phone, not the cost of the cell. The <a href="/guides/phone-battery-replacement-australia.html">battery guide</a> covers health thresholds, genuine vs aftermarket cells, and the swollen-battery safety warning.</p>

<h2>Water damage</h2>
<p>The first 10 minutes decide everything. Power off, don't charge, get to a professional — repair runs $80–$250 and succeeds in most cases treated fast. The <a href="/guides/phone-water-damage-repair.html">water damage guide</a> has the full emergency sequence and the rice-myth debunk.</p>

<h2>Repair or replace?</h2>
<p>Use the 40% rule, then check software support and trade-in value. The <a href="/guides/repair-or-replace-phone.html">decision guide</a> works through battery, screen, back glass, and logic-board scenarios with real numbers.</p>

<h2>iPad & tablets</h2>
<p>Tablet repairs run $69–$999 with the worst repair-to-value ratio in the industry. The <a href="/guides/ipad-tablet-repair-costs-australia.html">tablet guide</a> tells you what each category costs and when to walk away.</p>

<h2>Get an exact number</h2>
<p>Every guide links back to the <a href="/repair/phone-repair-costs-australia.html">74-model repair cost database</a> and the <a href="/calculator.html">interactive calculator</a> for a model-specific estimate — not a marketing number.</p>"""

def build_schema_breadcrumb(nav_last, slug):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://repairrange.io/"},
            {"@type": "ListItem", "position": 2, "name": "Repair Guides", "item": "https://repairrange.io/guides/index.html"},
            {"@type": "ListItem", "position": 3, "name": nav_last, "item": f"https://repairrange.io/guides/{slug}.html"},
        ],
    }

def build_schema_faq(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }

def related_links_html(items):
    return "".join(
        f'<li><a href="{url}" class="text-teal font-semibold hover:underline">{label}</a></li>'
        for label, url in items
    )

def render(page, is_index=False):
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

def render_index():
    faq_html = "".join(
        f'<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>' for q, a in INDEX_FAQ
    )
    body = INDEX_BODY + "\n\n<h2>Frequently asked questions</h2>\n" + faq_html
    repl = {
        "{META}": "Australian phone repair guides: screen repair, battery replacement, water damage, repair vs replace, and iPad & tablet costs. Researched by working technicians, prices verified 2026.",
        "{SLUG}": "index",
        "{TITLE}": "Repair Guides — Phone Repair Costs, Screens, Batteries & More",
        "{SCHEMA_BREADCRUMB}": json.dumps({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://repairrange.io/"},
                {"@type": "ListItem", "position": 2, "name": "Repair Guides", "item": "https://repairrange.io/guides/index.html"},
            ],
        }, ensure_ascii=False),
        "{SCHEMA_FAQ}": json.dumps(build_schema_faq(INDEX_FAQ), ensure_ascii=False),
        "{NAV_LAST}": "Repair Guides",
        "{H1}": "Repair Guides — Australia's Independent Phone Repair Reference",
        "{LEDE}": "Five plain-English guides to phone repair costs and decisions in Australia, researched by working technicians. Every figure links back to the 74-model price database and the interactive calculator.",
        "{BODY}": body,
        "{RELATED_LINKS}": related_links_html([
            ("Phone screen repair guide", "/guides/phone-screen-repair-australia.html"),
            ("Battery replacement guide", "/guides/phone-battery-replacement-australia.html"),
            ("Water damage repair guide", "/guides/phone-water-damage-repair.html"),
            ("Repair or replace?", "/guides/repair-or-replace-phone.html"),
            ("iPad & tablet repair costs", "/guides/ipad-tablet-repair-costs-australia.html"),
            ("All repair costs — 74+ models", "/repair/phone-repair-costs-australia.html"),
        ]),
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
    idx = os.path.join(OUT, "index.html")
    with open(idx, "w", encoding="utf-8") as f:
        f.write(render_index())
    print("WROTE:", idx)
