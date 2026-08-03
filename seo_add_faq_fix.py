#!/usr/bin/env python3
"""Add FAQPage JSON-LD to the 10 /fix/ diagnostic pages, grounded in each page's actual content."""
import os, json, re

ROOT = os.path.dirname(os.path.abspath(__file__))
FIX_DIR = os.path.join(ROOT, "fix")

FAQS = {
    "battery-drains-fast": [
        ("How do I check my phone battery health?",
         "iPhone: Settings \u2192 Battery \u2192 Battery Health & Charging \u2192 Maximum Capacity. Samsung: Settings \u2192 Battery \u2192 Battery Status (or Samsung Members diagnostics) \u2014 it shows Good/Normal/Weak. Google Pixel: Settings \u2192 Battery \u2192 Battery Health. Below 80% capacity is when Apple considers the battery degraded and replacement is recommended."),
        ("Why does my phone battery drain fast even when battery health is OK?",
         "If health reads 80\u2013100%, the drain is almost certainly software: a rogue background app, poor cellular signal, or a misbehaving setting. Check Settings \u2192 Battery \u2192 Battery Usage to find the culprit before paying for a new battery \u2014 about half of 'fast drain' cases are not a battery fault at all."),
        ("When should I replace my phone battery?",
         "Below 75\u201380% capacity is the replacement zone. At 75\u201380% the phone may throttle CPU performance to prevent unexpected shutdowns; a $79\u2013$149 battery replacement restores 18\u201324 months of full-day life. Below 75%, unexpected shutdowns at 20\u201330% charge are likely and replacement is recommended."),
        ("How much does a phone battery replacement cost in Australia?",
         "Independent repair shops typically charge $79\u2013$149 for most iPhones, Samsung and Pixel models. The price tracks the risk of opening the phone (the technician works through the display), not the cost of the cell itself."),
    ],
    "black-screen": [
        ("Why is my phone screen black but the phone is still on?",
         "The phone is alive (you can hear notifications or feel vibration) but the display isn't working. The cause is usually one of four things: a software freeze (fix with a force restart), a disconnected display cable after a drop ($0\u2013$39 to reseat), a failed OLED/LCD panel ($109\u2013$619), or display IC failure on the logic board ($149\u2013$399)."),
        ("How do I force restart an iPhone, Samsung or Pixel?",
         "iPhone (Face ID models): quick-press Volume Up, quick-press Volume Down, hold the Side button 10\u201315 seconds. Samsung: hold Power + Volume Down 10\u201315 seconds. Pixel: hold Power for 30 seconds. If the screen returns, it was a one-off crash with no repair needed."),
        ("How much does a black screen repair cost in Australia?",
         "From $0\u2013$39 for a disconnected display cable reseat (often free if the same shop does the repair) up to $109\u2013$619 for a full panel replacement and $149\u2013$399 for board-level display IC repair. A free diagnostic identifies which one you need."),
        ("Can I recover data from a phone with a black screen?",
         "Usually yes. A technician can connect the phone to a computer and back up data, or bypass the dead display to extract storage. Back up early \u2014 a display failure can progress to board-level failure if left powered on."),
    ],
    "charging-port": [
        ("Why is my phone not charging?",
         "90% of 'broken charging ports' are actually pocket lint compacted into the bottom of the port. The cable connector can't reach the contact pins, creating a loose feel and intermittent charging. Clean the port before paying for any repair."),
        ("How do I clean my phone charging port?",
         "Power off the phone, shine a torch into the port, then gently scrape along the bottom with a wooden or plastic toothpick \u2014 never metal, which can short the contacts. You'll often pull out a solid plug of compressed lint. Try the cable again; it should click in firmly."),
        ("How much does a charging port replacement cost in Australia?",
         "Professional charging port replacement typically costs $69\u2013$149 depending on the model. Before that, rule out the cheap fixes: a different cable, a different wall charger, wireless charging, and a port clean \u2014 cables fail far more often than ports do."),
        ("What are the four types of charging problems?",
         "Cable failure (most common), charger/brick failure, dirty or damaged port, and battery degradation. Work through them in that order \u2014 swapping the cable and charger is free and solves a large share of cases before any repair is needed."),
    ],
    "cracked-screen-still-works": [
        ("Can I keep using a phone with a cracked screen?",
         "It depends on the crack type. Glass-only cracks (touch and display still perfect) are safe to use with a screen protector over them. If you see black spots, colour bleeding or lines, fix it soon \u2014 display damage spreads. If touch fails anywhere, fix it now \u2014 ghost touch is a security risk."),
        ("Why does a cracked screen get worse over time?",
         "Cracks spread under everyday stress: temperature changes expand and contract the glass, pocket pressure extends fractures, and minor bumps add new branches. A corner crack can become a spider web within weeks \u2014 and the crack voids the phone's water resistance immediately."),
        ("How much does a cracked screen repair cost in Australia?",
         "$109\u2013$619 depending on the model and part tier. Incell, aftermarket OLED, and refurbished OEM parts each have different prices \u2014 the choice matters more than the phone model. Fixing early costs less: display damage spreads, so a $249 fix today can become a $349 fix in a month."),
        ("Should I put a screen protector over a cracked screen?",
         "As a temporary fix, yes \u2014 a tempered glass protector over a glass-only crack prevents cuts and slows further spreading. It does not restore water resistance or fix display damage. Treat it as a stopgap, not a repair."),
    ],
    "dropped-and-broken": [
        ("I dropped my phone \u2014 what should I check?",
         "Work through the damage checklist: front screen (glass only vs display damage vs touch failure), back glass, whether the phone powers on at all, camera (cracked lens vs damaged sensor), and frame/buttons. Each 'yes' is a separate repair that needs its own price."),
        ("My phone is completely dead after a drop \u2014 what's wrong?",
         "Try a force restart first \u2014 it fixes 60\u201370% of 'dead after drop' cases (software freeze). If it vibrates or makes sounds but the screen is black, it's likely a disconnected display cable ($0\u2013$39 to reseat). If completely unresponsive, it may be a battery cable, dead screen, or logic board damage \u2014 a shop diagnostic identifies which."),
        ("How much does it cost to fix a phone after a drop?",
         "Screen replacement $109\u2013$619, back glass $89\u2013$259 (Apple's own pricing is competitive on iPhone 12+ at $119\u2013$159), camera lens $49\u2013$149, camera module $99\u2013$399, diagnostic $0\u2013$39. Add up every damaged item before deciding repair vs replace."),
        ("Is it worth repairing a phone after a bad drop?",
         "Use the 40% rule: if the total repair cost is under 40% of a comparable replacement, repair it. Severe frame damage is often the exception \u2014 the repair cost can approach the phone's replacement value, making a new phone the better call."),
    ],
    "ghost-touch": [
        ("What causes ghost touch on a phone?",
         "Ghost touch is a digitiser fault \u2014 the touch-sensing layer sends false signals the phone believes are real. The most common causes are a cracked screen, moisture damage, a cheap aftermarket screen from a previous repair, and static interference. It is a hardware fault, not a software issue."),
        ("Is ghost touch dangerous?",
         "Yes \u2014 it's a genuine security risk. The phone can make calls, send messages, or authorise payments without your input. Enable Airplane Mode immediately to prevent unintended communication while you arrange a repair."),
        ("How much does ghost touch repair cost in Australia?",
         "Ghost touch requires screen replacement in most cases \u2014 typically $109\u2013$619 depending on the model and part tier, with most common phones landing around $150\u2013$350. Cleaning and software fixes rarely resolve a genuine digitiser failure."),
        ("Can ghost touch be fixed without replacing the screen?",
         "Rarely. Try a screen clean and a restart first \u2014 a tiny fraction of cases are caused by dirt or a temporary glitch. If the phantom taps persist, the digitiser itself has failed and the screen assembly must be replaced."),
    ],
    "green-lines": [
        ("What causes green lines on an OLED phone screen?",
         "A green line is a hardware fault in the OLED panel \u2014 the driver circuit for a column of pixels has failed, leaving the green sub-pixel permanently stuck on. Causes: drop impact (most common, even without visible damage), manufacturing defect, moisture, or flex/pressure damage on larger panels."),
        ("Can a software fix remove a green line?",
         "No. A green line is a physical failure inside the OLED panel \u2014 no software update, factory reset, or settings change will fix it. The panel must be replaced."),
        ("Is a green line covered by warranty?",
         "Potentially, if it appeared without any drop, damage or water exposure \u2014 that points to a manufacturing defect. Samsung has acknowledged this on certain Galaxy S20/S21/S22 models with extended coverage in some regions. Contact the manufacturer with proof of purchase before paying for a repair."),
        ("How much does green line screen repair cost in Australia?",
         "OLED panel replacement typically costs $119\u2013$619 depending on the model. Flagship curved OLEDs (Samsung S-series, iPhone Pro) are at the higher end. A free diagnostic confirms the panel is the fault before you commit."),
    ],
    "overheating": [
        ("Why is my phone getting hot?",
         "Phones generate heat under load \u2014 gaming, video recording, fast charging, direct sunlight, and the 24\u201372 hours after a major OS update are all normal causes. The problem signs are different: hot while idle with no apps running, repeated thermal shutdowns indoors, or heat localised around the charging port."),
        ("When is phone overheating dangerous?",
         "Persistent heat while idle, repeated thermal shutdowns during normal use, and localised heat at the charging port all point to hardware faults (degraded battery, faulty charging IC, or board issue). A single thermal shutdown in direct sunlight is normal \u2014 repeated shutdowns indoors are not."),
        ("How do I fix an overheating phone?",
         "Start with software: check Settings \u2192 Battery \u2192 Battery Usage for a rogue background app and restart the phone. If it's still hot with no apps running, or the port area is hot even unplugged, it's hardware \u2014 charging port repair is $69\u2013$149, and a degraded battery should be replaced."),
        ("Does overheating damage the battery?",
         "Yes. Persistent heat accelerates lithium-ion degradation and permanently shortens battery life. If your phone runs hot regularly, fix the cause \u2014 a battery replacement now costs less than a battery plus display damage later."),
    ],
    "water-damage": [
        ("My phone fell in water \u2014 what should I do right now?",
         "Power it off immediately and do not charge or plug anything in. Remove the case and SIM tray, gently shake out excess water with the port facing down, pat dry with a lint-free cloth, then leave the phone in a dry, well-ventilated spot for 48 hours. Every minute it stays powered on while wet raises the repair cost."),
        ("Should I put a wet phone in rice?",
         "No. Rice does not effectively dry the inside of a phone and pushes starch into ports and speakers. The correct move is power off, dry the exterior, and get it to a technician \u2014 a professional ultrasonic cleaning within 48 hours gives the best survival odds."),
        ("How much does water damage repair cost in Australia?",
         "A phone treated fast \u2014 powered off and brought in quickly \u2014 is often just a $49\u2013$80 ultrasonic clean. A phone left powered on or charged while wet can need $180\u2013$300+ of cleaning and component repair. The single biggest cost factor is how long it stayed powered on."),
        ("My phone is IP68 waterproof \u2014 do I still need to worry?",
         "Yes. IP68 means resistance under controlled lab conditions \u2014 fresh water, static, intact seals. Pool chemicals, salt water, soap, hot water, and pressure all break the rating, and manufacturers don't cover water damage in warranty. Treat any dunk as an emergency regardless of the rating."),
    ],
    "wont-turn-on": [
        ("Why won't my phone turn on?",
         "About 60\u201370% of 'dead' phones are a software freeze \u2014 the phone is on but unresponsive, fixed by a force restart. 15\u201320% are simply a completely flat battery that needs 30 minutes on a wall charger. The rest are hardware: disconnected cables, a dead screen, or board damage."),
        ("How do I force restart my phone?",
         "iPhone (Face ID models): quick-press Volume Up, quick-press Volume Down, hold Side 10\u201315 seconds. Samsung: hold Power + Volume Down 10\u201315 seconds (up to 30 for deep freezes). Pixel: hold Power for 30 seconds. Release if it vibrates."),
        ("How long should I charge a dead phone before giving up?",
         "A deeply discharged battery shows no sign of life for the first 5\u201315 minutes of charging \u2014 no icon, no vibration. Plug into a wall charger with a known-good cable, leave it alone for 30 minutes, then try a force restart. Most people give up too early."),
        ("How much does it cost to fix a phone that won't turn on?",
         "A diagnostic is usually $0\u2013$39 (often free with the repair). Battery replacement $79\u2013$149, disconnected cable reseat $0\u2013$39, and board-level repair $149\u2013$399. Use the 40% rule: if the repair exceeds 40% of a replacement device, replacing wins."),
    ],
}

def build_schema(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }

changed = 0
for slug, faqs in FAQS.items():
    path = os.path.join(FIX_DIR, slug + ".html")
    if not os.path.exists(path):
        print(f"MISSING: {slug}")
        continue
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()
    if "FAQPage" in html:
        print(f"SKIP (has FAQ): {slug}")
        continue
    if "</head>" not in html:
        print(f"NO head close: {slug}")
        continue
    block = '\n<script type="application/ld+json">' + json.dumps(build_schema(faqs), ensure_ascii=False) + "</script>\n"
    html = html.replace("</head>", block + "</head>", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"ADDED FAQ: {slug}")
    changed += 1

print(f"DONE: {changed} fix pages got FAQ schema")
