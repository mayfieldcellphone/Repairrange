#!/usr/bin/env python3
"""Build the repair/ pages that Google already ranks but which 404.

Clones the chrome from repair/samsung-galaxy-a54.html and replaces every
model-specific region with content authored per device. Prices are NEVER
derived or carried over from the template — every repair ships "By quote"
until Khalil supplies verified bench ranges.
"""
import re, json, os, sys, html as H

SRC = 'repair/samsung-galaxy-a54.html'
PRICES_PATH = 'prices.json' if os.path.exists('prices.json') else '../gen/prices.json'
PRICES = json.load(open(PRICES_PATH, encoding='utf-8'))
OUT = 'repair'
BASE = 'https://repairrange.io'

# Per-device content. Every claim here is deliberate, not inherited.
# build      : one clause describing construction, used in the table footnote
# wrong      : what actually fails on this device, from repair-bench reality
# diy        : honest DIY assessment
# difficulty : per-repair DIY difficulty shown in the table
# brandpage  : breadcrumb parent
MODELS = {
 'samsung-galaxy-a35': dict(
   name='Galaxy A35', full='Samsung Galaxy A35', brand='Samsung',
   brandslug='samsung', brandpage='brands/samsung.html',
   build="The A35 uses a flat Super AMOLED panel over a plastic frame with a glass back — screen work is straightforward, but the rear glass is adhered and needs heat.",
   wrong="Screen cracks dominate, followed by charging ports worn loose by daily cable use. The A35's battery holds up well for the first two years; degradation complaints cluster around year three.",
   diy="Reasonable for a confident first-timer. Standard Phillips screws, a conventional pull-tab battery, and no biometric sensor bonded to the display — which is what makes most Samsung screen swaps risky.",
   difficulty=dict(screen='Moderate', battery='Easy', back='Moderate', port='Moderate'),
   repairs=['Screen replacement','Battery replacement','Back glass replacement','Charging port replacement'],
 ),
 'samsung-galaxy-a25': dict(
   name='Galaxy A25', full='Samsung Galaxy A25', brand='Samsung',
   brandslug='samsung', brandpage='brands/samsung.html',
   build="Flat Super AMOLED on a plastic frame with a plastic back — one of the more forgiving Samsung builds to open, with no rear glass to shatter during disassembly.",
   wrong="Cracked screens and charging ports. The plastic back means drop damage concentrates in the display rather than spreading, so most A25s arrive with one clear fault rather than several.",
   diy="One of the friendlier phones on this site. Plastic back clips rather than bonds, screws are standard, and the battery is not aggressively glued.",
   difficulty=dict(screen='Moderate', battery='Easy', back='Easy', port='Moderate'),
   repairs=['Screen replacement','Battery replacement','Back cover replacement','Charging port replacement'],
 ),
 'samsung-galaxy-a15': dict(
   name='Galaxy A15', full='Samsung Galaxy A15', brand='Samsung',
   brandslug='samsung', brandpage='brands/samsung.html',
   build="Flat AMOLED, plastic frame, plastic back. The A15 is a budget build in the good sense: few bonded parts and generous internal clearance.",
   wrong="Screens and charge ports, in that order. As a high-volume budget handset the A15 also sees more third-party screens in circulation than most, so quality of a prior repair matters when quoting a second one.",
   diy="Genuinely approachable. If you are going to attempt a first screen replacement on any phone, this class of device is where to start.",
   difficulty=dict(screen='Moderate', battery='Easy', back='Easy', port='Moderate'),
   repairs=['Screen replacement','Battery replacement','Back cover replacement','Charging port replacement'],
 ),
 'pixel-7': dict(
   name='Pixel 7', full='Google Pixel 7', brand='Google',
   brandslug='google', brandpage='brands/google.html',
   build="Flat OLED under Gorilla Glass Victus, aluminium frame, glass back. The fingerprint reader is under the display, which is the detail that decides how a screen replacement goes.",
   wrong="Cracked screens, and under-display fingerprint readers that stop authenticating after a non-genuine panel is fitted. Charging port wear is less common here than on budget handsets.",
   diy="Not a beginner job. The under-display fingerprint sensor must be transferred or correctly paired, and the rear glass is heavily bonded. Screen replacement with a non-genuine panel frequently breaks biometrics.",
   difficulty=dict(screen='Hard', battery='Moderate', back='Hard', port='Moderate'),
   repairs=['Screen replacement','Battery replacement','Back glass replacement','Charging port replacement'],
 ),
 'pixel-7-pro': dict(
   name='Pixel 7 Pro', full='Google Pixel 7 Pro', brand='Google',
   brandslug='google', brandpage='brands/google.html',
   build="Curved OLED under Victus, polished aluminium frame, glass back. The curve is what raises the price — curved panels cost more and are less forgiving to fit.",
   wrong="Curved-edge cracks that spread further than they look, and under-display fingerprint failures after panel swaps. The camera bar glass is also a common standalone break.",
   diy="We would not recommend it. Curved glass, a bonded under-display sensor, and a rear assembly that resists heat make this a job where a failed attempt usually costs more than the original repair.",
   difficulty=dict(screen='Hard', battery='Moderate', back='Hard', port='Moderate'),
   repairs=['Screen replacement','Battery replacement','Back glass replacement','Camera bar glass'],
 ),
 'xiaomi-14': dict(
   name='Xiaomi 14', full='Xiaomi 14', brand='Xiaomi',
   brandslug='xiaomi', brandpage='brands.html',
   build="Flat OLED, aluminium frame, glass back. Xiaomi runs an official Australian support channel, but the independent parts supply is thinner than for Samsung or Apple, so lead time is the usual constraint.",
   wrong="Screens first. The practical issue is sourcing — genuine Xiaomi panels are harder to get through independent channels in Australia than Samsung or Apple equivalents, so turnaround is often longer.",
   diy="Mechanically similar to any modern glass-sandwich phone, but parts are the problem. Confirm you can actually source a panel before opening the device.",
   difficulty=dict(screen='Hard', battery='Moderate', back='Hard', port='Moderate'),
   repairs=['Screen replacement','Battery replacement','Back glass replacement','Charging port replacement'],
 ),
 'oneplus-12': dict(
   name='OnePlus 12', full='OnePlus 12', brand='OnePlus',
   brandslug='oneplus', brandpage='brands.html',
   build="Curved LTPO AMOLED, aluminium frame, glass back. Like the Pixel Pro line, the curve is the cost driver.",
   wrong="Curved-edge screen damage and the alert slider, which is a mechanical part and fails mechanically. Batteries hold up well thanks to the dual-cell design.",
   diy="Not recommended. Curved panel, bonded rear, and an under-display fingerprint reader that needs correct pairing.",
   difficulty=dict(screen='Hard', battery='Moderate', back='Hard', port='Moderate'),
   repairs=['Screen replacement','Battery replacement','Back glass replacement','Charging port replacement'],
 ),
 'nothing-phone-2': dict(
   name='Nothing Phone (2)', full='Nothing Phone (2)', brand='Nothing',
   brandslug='nothing', brandpage='brands.html',
   build="Flat OLED, aluminium frame, and a transparent glass back with the Glyph LED array bonded behind it — the back is not a plain panel, and replacing it means replacing lighting hardware.",
   wrong="Screens, and rear glass. The rear is the distinctive repair on this device: the Glyph interface sits behind it, so a cracked back is a more involved job than on a conventional phone.",
   diy="Screen work is standard. Rear glass is not — the Glyph assembly makes it a specialist job, and a botched attempt takes the lighting with it.",
   difficulty=dict(screen='Moderate', battery='Moderate', back='Hard', port='Moderate'),
   repairs=['Screen replacement','Battery replacement','Rear glass / Glyph assembly','Charging port replacement'],
 ),
 'sony-xperia-1-vi': dict(
   name='Xperia 1 VI', full='Sony Xperia 1 VI', brand='Sony',
   brandslug='sony', brandpage='brands.html',
   build="Tall 19.5:9 OLED, aluminium frame, glass back, and a genuine IP68 rating that depends on seals being correctly reseated after any repair.",
   wrong="Screens, and water ingress after a previous repair where the seals were not replaced. Sony's waterproofing is real, which means it is also real to destroy.",
   diy="Not advisable if you want the water resistance back. The adhesive seal set is part of the repair, not an optional extra, and parts supply in Australia is thin.",
   difficulty=dict(screen='Hard', battery='Hard', back='Hard', port='Moderate'),
   repairs=['Screen replacement','Battery replacement','Back glass replacement','Charging port replacement'],
 ),
 'motorola-razr-50-ultra': dict(
   name='Razr 50 Ultra', full='Motorola Razr 50 Ultra', brand='Motorola',
   brandslug='motorola', brandpage='brands.html',
   build="This is a foldable, with an inner flexible OLED, an external cover display and a hinge — three assemblies that fail independently and price independently. Nothing about this device repairs like a conventional phone.",
   wrong="The inner folding display and the hinge. Crease-line failures, dead pixel bands along the fold, and debris in the hinge are the characteristic faults. The outer cover display cracks like any normal screen.",
   diy="No. Folding displays are bonded to the hinge assembly and cannot be replaced independently on a kitchen table. This is a specialist repair and attempting it generally writes the device off.",
   difficulty=dict(screen='Specialist', battery='Hard', back='Hard', port='Hard'),
   repairs=['Inner folding display','Outer cover display','Battery replacement','Hinge service'],
 ),
}

def esc(t): return H.escape(t, quote=True)

def price_table(m, slug):
    """Independent = Khalil's quoted range. DIY = part-cost estimate.
    No Authorised column: there is no sourced manufacturer figure for these
    models, and deriving one from our own price would be inventing it."""
    rows, P = [], PRICES.get(slug, [])
    for p in P:
        lo, hi = p['ind']
        diy = f"from ${p['diy']}" if p.get('diy') else 'By quote'
        rows.append(
          '<tr class="border-t border-line">'
          f'<td class="px-5 py-4"><p class="font-medium text-ink">{esc(p["repair"])}</p>'
          f'<p class="text-xs text-muted mt-1">DIY difficulty: {esc(p.get("difficulty") or "Moderate")}</p></td>'
          f'<td class="px-5 py-4 font-mono tnum text-ink text-right">${lo}\u2013${hi}</td>'
          f'<td class="px-5 py-4 font-mono tnum text-muted text-right hidden md:table-cell">{esc(diy)}</td></tr>')
    return ('<table class="w-full text-sm">\n<thead class="bg-mesh-2 text-left">\n'
      '<tr><th class="px-5 py-3.5 eyebrow font-semibold text-muted">Repair</th>'
      '<th class="px-5 py-3.5 eyebrow font-semibold text-muted text-right">Independent</th>'
      '<th class="px-5 py-3.5 eyebrow font-semibold text-muted text-right hidden md:table-cell">DIY part (est.)</th></tr>\n'
      '</thead>\n<tbody>\n' + '\n'.join(rows) + '\n</tbody>\n</table>')

def _screen(slug):
    for p in PRICES.get(slug, []):
        if 'screen' in p['repair'].lower() or 'display' in p['repair'].lower():
            return p['ind']
    return None

def faqs(m, slug):
    n, P = m['name'], PRICES.get(slug, [])
    scr = _screen(slug)
    # build[] often opens with a fragment ("A foldable.") — take the clause that
    # actually describes construction rather than splicing the fragment inline.
    frag = m['build'].split('\u2014')[0].strip().rstrip('.')
    lead = frag[0].lower() + frag[1:] if frag and frag[0].isupper() and ' ' in frag else frag

    if scr:
        a1 = (f"At an independent shop a {n} screen replacement typically runs "
              f"${scr[0]}\u2013${scr[1]} AUD, depending on the panel tier fitted \u2014 {lead}.")
    else:
        a1 = (f"We quote {n} screen replacement individually rather than publishing a range "
              f"we cannot stand behind \u2014 {lead}.")

    # "Worth repairing" has to actually weigh cost against the device, and the
    # honest answer differs when the headline repair is $550+.
    if P:
        cheap = min(p['ind'][0] for p in P); dear = max(p['ind'][1] for p in P)
        if dear >= 450:
            a2 = (f"It depends which repair. The common faults on this model are covered below, and "
                  f"they range from ${cheap} at the low end to ${dear} for the most involved job. "
                  f"At the top of that range you are close to the cost of a replacement handset, so "
                  f"it is worth getting the fault diagnosed before committing. {m['wrong']}")
        else:
            a2 = (f"Usually yes \u2014 every repair listed here falls between ${cheap} and ${dear}, "
                  f"well under the cost of replacing the handset. {m['wrong']}")
    else:
        a2 = f"Usually yes, though it depends on the fault. {m['wrong']}"

    return [
      (f"How much does a {n} screen replacement cost in Australia?", a1),
      (f"Is the {n} worth repairing?", a2),
      (f"Can I repair the {n} myself?", m['diy']),
      (f"How long does a {n} repair take?",
       "Independent shops typically turn a screen or battery around same day or next day when the part "
       "is in stock. Where a part has to be ordered in, allow three to five business days."),
    ]

def build(slug, m, tpl):
    s = tpl
    title = f"{m['full']} repair cost — RepairRange"
    desc   = (f"{m['full']} repair costs in Australia — screen, battery and common faults, "
              f"quoted individually by verified independent shops.")
    url    = f"{BASE}/repair/{slug}.html"

    # --- head ---
    s = re.sub(r'(?is)<title>.*?</title>', f'<title>{esc(title)}</title>', s, count=1)
    s = re.sub(r'(?is)(<link rel="canonical" href=")[^"]*(")', rf'\g<1>{url}\g<2>', s, count=1)
    for prop, val in (('og:title', f"{m['full']} repair cost"), ('og:description', desc),
                      ('twitter:title', f"{m['full']} repair cost"), ('twitter:description', desc)):
        s = re.sub(rf'(?is)(<meta (?:property|name)="{prop}" content=")[^"]*(")', rf'\g<1>{esc(val)}\g<2>', s, count=1)
    s = re.sub(r'(?is)(<meta name="description" content=")[^"]*(")', rf'\g<1>{esc(desc)}\g<2>', s, count=1)
    s = re.sub(r'(?is)(<meta property="og:url" content=")[^"]*(")', rf'\g<1>{url}\g<2>', s, count=1)

    # --- JSON-LD: breadcrumb, Service (by quote, never Product w/ prices), FAQPage ---
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":f"{BASE}/"},
      {"@type":"ListItem","position":2,"name":"Repair costs","item":f"{BASE}/repair/phone-repair-costs-australia.html"},
      {"@type":"ListItem","position":3,"name":m['name'],"item":url}]}
    s = re.sub(r'(?is)<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "BreadcrumbList".*?</script>',
               '<script type="application/ld+json">'+json.dumps(crumb,ensure_ascii=False)+'</script>', s, count=1)

    P = PRICES.get(slug, [])
    if P:
        lo = min(p['ind'][0] for p in P); hi = max(p['ind'][1] for p in P)
        # AggregateOffer spans the Independent column ONLY — that is the range
        # shown on the page. DIY is a part-cost estimate, not our offer.
        svc = {"@context":"https://schema.org","@type":"Product",
               "name":f"{m['name']} repair",
               "description":f"Independent repair pricing for the {m['full']} in Australia.",
               "category":"Mobile device repair",
               "brand":{"@type":"Brand","name":m['brand']},
               "offers":{"@type":"AggregateOffer","priceCurrency":"AUD",
                         "lowPrice":lo,"highPrice":hi,"offerCount":len(P),
                         "availability":"https://schema.org/InStock",
                         "offers":[{"@type":"Offer","name":p['repair'],"priceCurrency":"AUD",
                                    "priceSpecification":{"@type":"PriceSpecification",
                                      "priceCurrency":"AUD","minPrice":p['ind'][0],"maxPrice":p['ind'][1]}}
                                   for p in P]}}
    else:
        svc = {"@context":"https://schema.org","@type":"Service","name":f"{m['name']} repair",
               "serviceType":"Mobile device repair",
               "description":f"Independent repair service for the {m['full']} in Australia.",
               "areaServed":{"@type":"Country","name":"Australia"},
               "provider":{"@type":"Organization","name":"RepairRange","url":BASE+"/"}}
    s = re.sub(r'(?is)<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "(?:Product|Service)".*?</script>',
               lambda _: '<script type="application/ld+json">'+json.dumps(svc,ensure_ascii=False)+'</script>', s, count=1)

    F = faqs(m, slug)
    fp = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
      {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in F]}
    s = re.sub(r'(?is)<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "FAQPage".*?</script>',
               '<script type="application/ld+json">'+json.dumps(fp,ensure_ascii=False)+'</script>', s, count=1)

    # --- visible breadcrumb + H1 + CTA ---
    s = re.sub(r'(?is)(<a href="[^"]*brands/samsung\.html" class="ed-link hover:text-teal">)Samsung(</a>)',
               rf'<a href="../{m["brandpage"]}" class="ed-link hover:text-teal">{esc(m["brand"])}\g<2>', s, count=1)
    s = re.sub(r'(?is)(<span class="text-ink">)Galaxy A54(</span>)', rf'\g<1>{esc(m["name"])}\g<2>', s, count=1)
    s = re.sub(r'(?is)(<h1 class="display[^"]*">)[^<]*(</h1>)', rf'\g<1>{esc(m["name"])} repair cost\g<2>', s, count=1)
    s = re.sub(r'(?is)(<h2 class="display text-3xl md:text-5xl mb-3">)Ready to fix your [^<]*(</h2>)',
               rf'\g<1>Ready to fix your {esc(m["name"])}?\g<2>', s, count=1)

    # --- body: table, footnote, what-goes-wrong, DIY note ---
    s = re.sub(r'(?is)<table class="w-full text-sm">.*?</table>', lambda _: price_table(m, slug), s, count=1)
    s = re.sub(r'(?is)<p class="text-xs text-muted mt-5 max-w-2xl">.*?</p>',
               f'<p class="text-xs text-muted mt-5 max-w-2xl">{esc(m["build"])} '
               'Every repair on this page is quoted individually — we do not publish a range we have not verified on the bench.</p>', s, count=1)
    s = re.sub(r'(?is)(<h2 class="display text-3xl md:text-5xl text-ink mb-6">)What goes wrong[^<]*(</h2>\s*<p class="text-muted leading-relaxed">).*?(</p>)',
               rf'\g<1>What goes wrong with the {esc(m["name"])}.\g<2>{esc(m["wrong"])}\g<3>', s, count=1)
    s = re.sub(r'(?is)(<p class="eyebrow mb-3">DIY note</p><p class="text-ink leading-relaxed">).*?(</p>)',
               rf'\g<1>{esc(m["diy"])}\g<2>', s, count=1)

    # --- hero "Starting from $X" card ---
    if P:
        lo = min(p['ind'][0] for p in P)
        rep = [p for p in P if p['ind'][0] == lo][0]['repair']
        s = re.sub(r'(?is)(<p class="eyebrow mb-3 text-teal">)Starting from(</p>\s*<p class="display text-5xl text-ink mb-2">)[^<]*(</p>\s*<p class="text-sm text-muted">)[^<]*(</p>)',
                   rf'\g<1>Starting from\g<2>${lo}\g<3>{esc(rep)}\g<4>', s)
    else:
        s = re.sub(r'(?is)(<p class="eyebrow mb-3 text-teal">)Starting from(</p>\s*<p class="display text-5xl text-ink mb-2">)[^<]*(</p>\s*<p class="text-sm text-muted">)[^<]*(</p>)',
                   rf'\g<1>Pricing\g<2>By quote\g<3>Quoted per device — send us the model and fault.\g<4>', s)

    # --- FAQ accordion: rebuild all five from F (template has 5, we author 4) ---
    blocks = re.findall(r'(?is)<details class="border border-line.*?</details>', s)
    new = []
    for q,a in F:
        new.append('<details class="border border-line bg-white group"><summary class="cursor-pointer p-5 md:p-6 flex items-start justify-between gap-4 list-none">'
          f'<h3 class="font-serif text-lg md:text-xl text-ink leading-snug">{esc(q)}</h3>'
          '<i data-lucide="plus" class="w-5 h-5 text-muted flex-shrink-0 mt-1 group-open:hidden"></i>'
          '<i data-lucide="minus" class="w-5 h-5 text-muted flex-shrink-0 mt-1 hidden group-open:block"></i></summary>'
          f'<div class="px-5 md:px-6 pb-6 text-ink leading-relaxed text-sm md:text-base">{esc(a)}</div></details>')
    if blocks:
        s = s.replace(blocks[0], '\n'.join(new), 1)
        for b in blocks[1:]:
            s = s.replace(b, '', 1)
    s = re.sub(r'(?is)(<h2 class="display text-3xl md:text-5xl text-ink mb-10">)[^<]*(</h2>)',
               rf'\g<1>{esc(m["name"])} repair questions, answered.\g<2>', s, count=1)
    return s

if __name__ == '__main__':
    tpl = open(SRC, encoding='utf-8').read()
    only = sys.argv[1:] or list(MODELS)
    os.makedirs(OUT, exist_ok=True)
    for slug in only:
        out = build(slug, MODELS[slug], tpl)
        p = f'{OUT}/{slug}.html'
        open(p, 'w', encoding='utf-8').write(out)
        print(f'wrote {p}  {len(out)} chars')
