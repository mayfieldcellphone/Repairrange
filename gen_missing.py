#!/usr/bin/env python3
"""Build the repair/ pages that Google already ranks but which 404.

Clones the chrome from repair/samsung-galaxy-a54.html and replaces every
model-specific region with content authored per device. Prices are NEVER
derived or carried over from the template — every repair ships "By quote"
until Khalil supplies verified bench ranges.
"""
import re, json, os, sys, html as H

SRC = 'repair/samsung-galaxy-a54.html'
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
   build="Flat OLED, aluminium frame, glass back. Parts availability in Australia is the constraint here rather than the repair itself — Xiaomi does not run a broad authorised network locally.",
   wrong="Screens first. The bigger practical issue is sourcing: genuine Xiaomi panels are harder to get in Australia than Samsung or Apple equivalents, so turnaround is often longer.",
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
   build="A foldable. Inner flexible OLED, external cover display, and a hinge — three assemblies that fail independently and price independently. Nothing about this device repairs like a conventional phone.",
   wrong="The inner folding display and the hinge. Crease-line failures, dead pixel bands along the fold, and debris in the hinge are the characteristic faults. The outer cover display cracks like any normal screen.",
   diy="No. Folding displays are bonded to the hinge assembly and cannot be replaced independently on a kitchen table. This is a specialist repair and attempting it generally writes the device off.",
   difficulty=dict(screen='Specialist', battery='Hard', back='Hard', port='Hard'),
   repairs=['Inner folding display','Outer cover display','Battery replacement','Hinge service'],
 ),
}

def esc(t): return H.escape(t, quote=True)

def price_table(m):
    rows = []
    dk = list(m['difficulty'].values())
    for i, r in enumerate(m['repairs']):
        diff = dk[i] if i < len(dk) else 'Moderate'
        rows.append(
          '<tr class="border-t border-line">'
          f'<td class="px-5 py-4"><p class="font-medium text-ink">{esc(r)}</p>'
          f'<p class="text-xs text-muted mt-1">DIY difficulty: {esc(diff)}</p></td>'
          '<td class="px-5 py-4 font-mono tnum text-ink text-right">By quote</td>'
          '<td class="px-5 py-4 font-mono tnum text-muted text-right hidden md:table-cell">By quote</td>'
          '<td class="px-5 py-4 font-mono tnum text-muted text-right hidden md:table-cell">By quote</td></tr>')
    return ('<table class="w-full text-sm">\n<thead class="bg-mesh-2 text-left">\n'
      '<tr><th class="px-5 py-3.5 eyebrow font-semibold text-muted">Repair</th>'
      '<th class="px-5 py-3.5 eyebrow font-semibold text-muted text-right">Independent</th>'
      '<th class="px-5 py-3.5 eyebrow font-semibold text-muted text-right hidden md:table-cell">Authorised</th>'
      '<th class="px-5 py-3.5 eyebrow font-semibold text-muted text-right hidden md:table-cell">DIY (est.)</th></tr>\n'
      '</thead>\n<tbody>\n' + '\n'.join(rows) + '\n</tbody>\n</table>')

def faqs(m):
    n, f = m['name'], m['full']
    return [
      (f"How much does a {n} screen replacement cost in Australia?",
       f"We quote {n} screen replacement individually rather than publishing a range we cannot stand behind. "
       f"{m['build'].split('—')[0].strip()} Send us the model and the fault and you will get a real number, not an estimate."),
      (f"Is the {n} worth repairing?",
       f"In most cases yes. {m['wrong']}"),
      (f"Can I repair the {n} myself?",
       m['diy']),
      (f"How long does a {n} repair take?",
       "Independent shops typically turn a screen or battery around same day or next day when the part is in stock. "
       "Where a part has to be ordered in, allow three to five business days."),
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

    svc = {"@context":"https://schema.org","@type":"Service","name":f"{m['name']} repair",
           "serviceType":"Mobile device repair","description":f"Independent repair service for the {m['full']} in Australia.",
           "areaServed":{"@type":"Country","name":"Australia"},
           "provider":{"@type":"Organization","name":"RepairRange","url":BASE+"/"}}
    s = re.sub(r'(?is)<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "Product".*?</script>',
               '<script type="application/ld+json">'+json.dumps(svc,ensure_ascii=False)+'</script>', s, count=1)

    F = faqs(m)
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
    s = re.sub(r'(?is)<table class="w-full text-sm">.*?</table>', lambda _: price_table(m), s, count=1)
    s = re.sub(r'(?is)<p class="text-xs text-muted mt-5 max-w-2xl">.*?</p>',
               f'<p class="text-xs text-muted mt-5 max-w-2xl">{esc(m["build"])} '
               'Every repair on this page is quoted individually — we do not publish a range we have not verified on the bench.</p>', s, count=1)
    s = re.sub(r'(?is)(<h2 class="display text-3xl md:text-5xl text-ink mb-6">)What goes wrong[^<]*(</h2>\s*<p class="text-muted leading-relaxed">).*?(</p>)',
               rf'\g<1>What goes wrong with the {esc(m["name"])}.\g<2>{esc(m["wrong"])}\g<3>', s, count=1)
    s = re.sub(r'(?is)(<p class="eyebrow mb-3">DIY note</p><p class="text-ink leading-relaxed">).*?(</p>)',
               rf'\g<1>{esc(m["diy"])}\g<2>', s, count=1)

    # --- hero "Starting from $X" card: the template hard-codes the A54's battery
    #     price. Leaving it would assert a number we have not verified for this
    #     device, so it becomes an explicit quote prompt instead. ---
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
    os.makedirs('../gen/repair', exist_ok=True)
    for slug in only:
        out = build(slug, MODELS[slug], tpl)
        p = f'../gen/repair/{slug}.html'
        open(p, 'w', encoding='utf-8').write(out)
        print(f'wrote {p}  {len(out)} chars')
