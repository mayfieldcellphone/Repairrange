# RepairRange — Project Brief & Working Document

> **Canonical source of truth** for the RepairRange satellite site. Lives in this repo so it persists across Claude sessions and is version-controlled with the code. Not deployed publicly (CI only copies `*.html`, `*.txt`, `*.xml`).
>
> **Last updated:** May 2026 · Phase 1 complete · Phase 2 in progress · **Phase 3 COMPLETE** · **Phase 4 COMPLETE** · Domain www-canonical (§11) · **🔴 CI DEPLOY FIX REGRESSES — re-verify `.gitlab-ci.yml` + a live subdirectory URL at the START of every session and after ANY domain/Pages change. It has silently reverted twice (likely cause: GitLab domain re-add resets the CI). See §12 — this is the project's #1 recurring failure.** · GSC verified + sitemap submitted; site is live & discoverable. Remaining work is growth (Phase 2 model pages, Phase 6/7).

---

## 1. Strategic context

### The bigger picture
Khalil runs **Mayfield Phone Repair** (mayfieldphonerepair.com.au) in Mayfield, NSW. RepairRange is a **satellite content site** — one of potentially several — whose primary commercial purpose is to **build editorial backlinks and referral traffic to the main business**.

### Backlink mandate (CRITICAL — DO NOT FORGET)
**Wherever it is natural and editorially appropriate, RepairRange (and future satellite sites) MUST link to https://mayfieldphonerepair.com.au.** Specifically:

- **Newcastle/Hunter region pages** → always cite Mayfield Phone Repair as the local example/recommendation
- **"Find a local repair shop" CTAs** → for Newcastle/Hunter searchers, route through to the main site
- **Author bylines / expertise statements** → "researched by working technicians at Mayfield Phone Repair" or similar where credibility matters
- **Methodology pages** → can reference real shop experience by linking to the main site
- **Lead-gen forms** → for Newcastle leads, forward to the main site's booking form

### What to avoid (don't get penalised)
This must NOT read as a PBN (private blog network). Google penalises sites that exist only to push backlinks. RepairRange's content has to genuinely serve users **first**. Rules:

- Cross-links must be **contextual** (in-content, anchored on relevant text), not sitewide-footer-blanket-link spam
- Anchor text varies naturally — "Mayfield Phone Repair", "a local Newcastle shop", "our team at the workshop", etc. — never the same exact-match keyword every time
- For non-Newcastle cities, RepairRange should recommend their own local shops — don't push Mayfield in Sydney/Melbourne/Perth content (cheapens the credibility)
- Disclose the connection in the About page eventually, once the relationship is meaningful

---

## 2. Site identity

| | |
|---|---|
| **Name** | RepairRange |
| **Tagline** | "Plain-English phone repair costs, fixes, and buying advice. Researched by people who actually do this work." |
| **Live URL** | **https://www.repairrange.io/** (LIVE, secure, www-canonical) — gitlab.io URL still works as fallback |
| **Gitpage pageId** | `69fb1fc8a84e148d906285c4` |
| **Repo** | `blank-site-2026-05-06-6rrng` on gitlab.com/mayfield276 |
| **Custom domain** | **`www.repairrange.io`** is canonical. Bare apex `repairrange.io` redirects to www at Hostinger (apex never got a working cert — see §11). |
| **Contact email (planned)** | hello@repairrange.io |

### Design system
- **Palette:** deep teal `#0F766E` (primary), warm amber `#F59E0B` (accent), dark teal `#0c4a45` (footer), off-white `#FAFAF9` (paper), ink `#1C1917` (text), warm grey `#78716C` (muted), line `#E7E5E4` (borders)
- **Type:** Fraunces variable serif (display/headings), Inter (body), JetBrains Mono (prices/numbers)
- **Aesthetic:** editorial / reference-site / Wirecutter-NerdWallet
- **Key signature moves:** italic accents on display headings, `eyebrow` label above every section, `ticker-row` borders on price rows, subtle SVG grain texture on hero areas, page-load reveal animation

### Content voice
- Plain English, no jargon-flexing
- Honest ranges, not point estimates
- "Working tech" perspective — write as someone who actually does this work
- No fluff intros; lead with the answer

---

## 3. Phase 1 — DONE (May 2026)

8 pages built and published:

| File | Purpose | Notes |
|---|---|---|
| `index.html` | Hub homepage | Hero search, 6 popular models, 6 common fixes, 4-step methodology, CTA strip |
| `brands.html` | Brand index | Apple / Samsung / Google / "more coming". A–Z model list. |
| `fix.html` | Troubleshooting index | 10 guides across 3 categories (display, power, damage) |
| `locations.html` | City index | 5 AU cities (Sydney/Melbourne/Brisbane/Perth/Newcastle) + 4 international "Q2 2026" |
| `calculator.html` | Interactive calculator | 3-step picker (brand → model → issue) → range + "our take" |
| `about.html` | About / methodology | Why it exists, how we make money (3 sources, all disclosed) |
| `privacy.html` | Privacy policy | GDPR + CCPA aware |
| `terms.html` | Terms of use | Estimate disclaimer, trademark notice, liability limit |
| `tools/software-stack-for-repair-shops.html` | **Phase 1.5** — first affiliate-content article | SaaS recommendations for repair shop owners. Targets AppSumo / Impact partners. Linked from sitewide footer as "Tools we recommend". |

### Phase 1 commit shas
- index: `902e5f2d5f0131f79e65451de9599a1a2ad9c7d9`
- brands: `96250e09601f995e04bfddf2b9fcda18cd649855`
- fix: `ee1b856ee23f4f8b1a63465cd4219ca56b245e1b`
- locations: `27ee8b47afd3f44af40e6199a35cd45b14f98f3b`
- calculator: `52a5d56736775bdda244829777380092fd99c87b`
- about: `f8b124d424d027f79cbd89aa94f61a5a23c2ee4a`
- privacy: `b1141120cb017d9c7c14649a311f511f383af1a3`
- terms: `260e32886067c2b41e772abbd2f56fef27d58e9a`

---

## 4. Roadmap

### Phase 2 — 20 model pages (next)
Build `/repair/{slug}.html` for the 20 most-searched phone models. These are the SEO traffic engines.

**Pre-requisites before Phase 2:**
1. **Update `.gitlab-ci.yml`** to also copy subdirectories. Current CI only copies root `*.html`, `blog/`, `*.txt`, `*.xml`. Add:
   ```yaml
   - cp -r repair public/ 2>/dev/null || true
   - cp -r fix public/ 2>/dev/null || true
   - cp -r locations public/ 2>/dev/null || true
   - cp -r brands public/ 2>/dev/null || true
   - cp -r data public/ 2>/dev/null || true
   ```
2. **Push `data/devices.json`** with full 20-model dataset. Schema already defined locally; expand to 20 entries.
3. **Build the model-page template** with: pricing table (DIY vs indie vs auth), symptom checker for that model's common failures, FAQ block with schema.org markup, affiliate spots (placeholders until Amazon Associates approved), "Get a quote" form pointing to local techs.
4. **Update calculator** to `fetch('data/devices.json')` instead of inlining model data.

**Model list for Phase 2 (20 phones):**
- iPhone 15 Pro Max, 15 Pro, 15 Plus, 15
- iPhone 14 Pro Max, 14 Pro, 14
- iPhone 13 Pro Max, 13, 12, SE (3rd gen)
- Samsung Galaxy S24 Ultra, S24, S23 Ultra, S23, Z Fold 5, Z Flip 5, A54
- Google Pixel 8 Pro, 8

> **⚠️ CURRENT-GENERATION GAP — raised by Khalil May 2026 (DO NOT FORGET).** The Phase 2 list above was scoped against models known at an earlier knowledge cutoff and is now INCOMPLETE. Newer flagships have since released — e.g. the **iPhone 17 series** and **Samsung Galaxy S26 series** (and likely a newer Pixel). The exact model names, configurations (Pro / Pro Max / Ultra / Air / Fold naming may have changed), and — critically — the **2026 AU repair pricing** for these must be confirmed from real current sources, NOT estimated or invented. Fabricated model names or guessed pricing on these would directly contradict the site's "honest, researched by working techs" positioning and is explicitly forbidden. Sourcing options, in order of preference: (1) Khalil's own bench experience / current AU supplier pricing via the Mayfield connection (best — newest models have volatile premium pricing that needs first-hand data); (2) web search for confirmed model lineups + AU repair pricing at build time. **Priority note:** newest-model pages ("iPhone 17 Pro Max screen replacement cost") are the HIGHEST-traffic, highest-intent queries — when built they belong near the FRONT of the publish queue, not appended after older models like iPhone 12/13. Action: at the next Phase 2 session, first confirm the current flagship lineup (search + ask Khalil), add them to devices.json with real ranges, then build them early in the batch.

### Phase 3 — 10 troubleshooting guides ✅ COMPLETE (May 2026)
All 10 `/fix/{slug}.html` guides built, published, and live. Each ~22–23KB, TechArticle + FAQPage JSON-LD, prose-rr template, callout/callout-warn/callout-stop boxes, dark CTA, universal header/footer.

**DECIDED & APPLIED (May 2026):** guides are **diagnosis-and-decision only — NO step-by-step teardowns**. Always recommend a shop for the actual repair. Rationale: (1) RepairRange's value is honest decision-help, not a teardown manual; (2) teardown instructions create liability (battery puncture etc.); (3) "this is a shop job, here's the real cost, here's how to find a good local shop" is what drives referral value to Mayfield — DIY step content competes against the commercial purpose. This stance is consistent across all 10 guides; **maintain it for any future guide edits.**

**Phase 3 — all 10 guides, commit SHAs:**
- ✅ `fix/green-lines.html` — `59dfb49a2aafe4e451831bacf38e8ea3226ac3c4`. Screenshot test, full-OLED reality, debunks the "update caused it" myth.
- ✅ `fix/charging-port.html` — `744f2c69e4bca67e0434718f0fe9eb11f6c92777`. 4-step diagnostic order (lint→cable→software→repair), free-first, salt-air note.
- ✅ `fix/wont-turn-on.html` — `0d5e256620eeb120c8a178148b94316128ff3feb`. Charge+forced-restart free-first, no-factory-reset data warning, port-vs-battery-vs-board.
- ✅ `fix/battery-drains-fast.html` — `be474b6c20291931f29c7171a93d4ec2e71c006e`. Battery-health-number test, software-vs-hardware split, anti-overspend warning.
- ✅ `fix/water-damage.html` — `d8f96503e868e85ff7cce3e83f90400b7df9dfe4`. First-10-minutes triage, rice/heat/charge myths, time-critical shop job. CTA + callout link to newcastle.html ("Find a local shop").
- ✅ `fix/cracked-screen-still-works.html` — `a3bd9ab9ff6236cf797187c02e30e88530c5b03d`. Which-crack triage, when-to-wait vs when-it-costs-more, glass-vs-assembly cost trap.
- ✅ `fix/black-screen.html` — `e122fe982dc75f0c4b00f7c8c4c6011fff7b434c`. Display-vs-power distinction, ring/plug-in test, panel-vs-flex-vs-backlight.
- ✅ `fix/ghost-touch.html` — `516a3b43d919d64887b8d472f799b99e09211509`. Protector/charger free-first triage, digitiser-vs-flex hardware.
- ✅ `fix/dropped-and-broken.html` — `efc372c49e41481c3b31386b3bf9602e45655260`. 90-second triage (glass→display→touch→function), multi-fault diagnosis, battery-swelling safety flag. CTA + callout link to newcastle.html.
- ✅ `fix/overheating.html` — `5ff519a4f57ab9699686ad4f3aa1b20e64783e82`. Thermal-throttling explained, normal-vs-abnormal heat, free-first causes, battery-swelling safety flag.

**Symptom widget on `fix.html` — fully upgraded, all 5 symptoms now resolve to live guides.** Final SHA `9aa15564179c7b8b898e13e8c2bff5f7d2fa73f3`. green-lines→green-lines, no-power→wont-turn-on, ghost-touch→ghost-touch, slow-charging→charging-port, bootloop→wont-turn-on. Uses a `guideReady` flag in the symptom JS (all now `true`, button reads "Read the full guide"). The homepage `index.html` "Common fixes" list links 6 of the 10 slugs — **all now resolve, zero internal 404s from that list.**

**Backlink status:** every guide carries a Newcastle/Hunter callout linking `../locations/newcastle.html` (the keystone), which itself links to mayfieldphonerepair.com.au — an editorially clean two-hop. water-damage and dropped-and-broken additionally use "Find a local shop" → newcastle.html in the CTA. §5 backlink table notes a *future* pass may add direct main-site links from fix/water-damage, fix/dropped-and-broken, fix/wont-turn-on where natural — NOT yet done, deliberately deferred (two-hop via keystone is cleaner for now; revisit in Phase 5 backlink audit).

### Phase 4 — 5 city pages + Newcastle linkage
Build `/locations/{city}.html` for Sydney, Melbourne, Brisbane, Perth, Newcastle.

**Newcastle page = the backlink keystone.** This is where RepairRange most heavily features Mayfield Phone Repair:
- Featured shop card with real address, phone, hours, ABN, reviews
- Embedded reviews/testimonials
- Direct "Book a repair" CTA linking to mayfieldphonerepair.com.au/contact.html
- "About the local market" section that mentions specific suburbs (Mayfield, Hamilton, Islington, Waratah, Jesmond)

Other city pages: don't push Mayfield (it cheapens the link). Recommend a representative real local shop per city OR keep them as "coming soon, request a referral".

### Phase 5 — SEO & launch finishing
- `sitemap.xml`
- `robots.txt`
- `llms.txt` (per llmstxt.org spec — Gitpage has a built-in generator)
- JSON-LD schema on every page: Article, FAQPage, LocalBusiness (location pages), Product (model pages), BreadcrumbList
- Open Graph images (1200×630 SVG-to-PNG per page, or one universal)
- Google Search Console verification + sitemap submission
- Internal link audit (every page must link to ≥3 other pages naturally)
- **Backlink audit:** confirm every Newcastle context links to mayfieldphonerepair.com.au at least once

### Phase 6 — Repair-shop directory (Khalil's idea, May 2026 — post-traffic only)

**Concept:** add a listed-repair-shops section to the non-Newcastle city pages. Shops can list for free; later, an optional paid featured tier (~$5–10) once pages rank and pull traffic. Revenue diversification independent of Amazon/Impact approval timelines.

**Why it fits:** the Sydney/Melbourne/Brisbane/Perth city pages currently have no commercial purpose (by design — we don't push Mayfield there). A directory gives those pages a revenue role AND legitimately enriches them with real local-business content (good for SEO, opposite of doorway-page risk) — *provided each listing has real data, not thin stubs.*

**HARD CONSTRAINTS (do not violate — these protect the core strategy and legal standing):**
1. **Newcastle is excluded from paid placement, permanently.** Newcastle stays the curated editorial keystone with Mayfield Phone Repair featured. Mayfield's prominence there is the entire reason RepairRange exists; it is never a paid slot and never diluted by a list of competitors. The directory monetises only cities Khalil has no stake in.
2. **Label as listings, NOT endorsements.** Section heading = "Listed repair shops" / "Repair shops in {city}" — never "recommended", "verified", "vetted", or "trusted" unless each shop is genuinely vetted. Paid placement dressed as editorial endorsement breaches ACCC guidance and destroys the editorial credibility the whole backlink strategy depends on. Any paid/featured listing must be visibly labelled (e.g. "Featured listing").
3. **Quality bar on free listings.** Accept a listing only with real NAP + hours + at least one specific detail (specialties/brands). This is both the SEO value and the spam defence — fake/SEO-spam shops will attempt to list.
4. **Disclosure.** Add a line to the affiliate-disclosure / about copy explaining the directory model (free listings; some listings are paid placements; placement does not imply endorsement).

**Phase 6 build steps:**
- Decide listing data model (likely a small JSON per city, e.g. `data/shops-sydney.json`, mirroring devices.json approach).
- Add a "Listed repair shops" section to each non-Newcastle city page rendering from that JSON.
- Build a submission path. Cheapest viable: a simple form (Formspree/Tally/Google Form) emailing Khalil; manual review; manual JSON add. (Full self-serve DB is out of scope for a static Gitpage site.)
- Light moderation policy written down (what gets rejected).

### Phase 7 — Directory monetisation (only after a city page demonstrably ranks + gets clicks)
- Introduce optional paid tier: featured/pinned position or enhanced listing (logo, description, link) for ~$5–10 (one-off or annual — decide based on effort to administer).
- Free tier always remains; never remove a free listing to upsell.
- Payment: a simple Stripe/PayPal payment link is enough at this scale; no need for billing infrastructure.
- Featured listings clearly badged. Newcastle still excluded.
- Revisit pricing once there's real demand data; $5–10 is a hypothesis, not a fixed number.

> **Sequencing rule:** do NOT add the paid tier (Phase 7) until at least one non-Newcastle city page is genuinely ranking and receiving organic clicks (check Search Console). A paid directory with no traffic gets zero signups and looks desperate; a free directory that already ranks is something shops will pay to be featured within. Free-first is non-negotiable.

---

## 5a. Affiliate partnerships (Impact.com, AppSumo, Amazon)

A distinct commercial layer from backlinks. Currently in setup:

- **Impact.com** — publisher profile set up May 2026. Application to AppSumo Plus and other SaaS partners in review.
- **Amazon Associates** — not yet applied; defer until some live traffic exists.
- **Future direct partnerships** — e.g. RepairDesk, Xero, MailerLite if/when we have meaningful audience.

The `tools/` directory is the canonical home for affiliate content. Each article uses placeholder `href="#"` links until programs are approved, then we swap in live Impact/affiliate URLs. Affiliate disclosure appears on every relevant page and in the sitewide footer.

**Strategic principle:** affiliate revenue is a long-term diversification, NOT the primary purpose of these satellite sites. Backlinks to mayfieldphonerepair.com.au remain the primary commercial purpose.

**Live affiliate articles:**
- `tools/software-stack-for-repair-shops.html` — covers RepairDesk, SimplyBook.me, NiceJob, MailerLite, Xero, BrightLocal, Canva, Google Workspace, ChatGPT/Claude. ~12 min read.

**Planned next affiliate articles (Phase 6+):**
- Hardware tools every repair tech buys (Amazon Associates focus)
- Best phone-buying-back / trade-in services (mixed)
- Cloud storage & backup tools for repair shops (Impact / direct)

---

## 5. Backlink placement plan (specific opportunities)

Where RepairRange will link to mayfieldphonerepair.com.au, in order of natural fit:

| Page | Link context | Anchor text suggestion |
|---|---|---|
| `locations/newcastle.html` | Featured shop card | "Mayfield Phone Repair" + "Book a repair" CTA |
| `locations/newcastle.html` | Market overview | "shops like the team at Mayfield Phone Repair" |
| `about.html` | Methodology / who we are | "Our reporting is informed by working technicians, including [Khalil at Mayfield Phone Repair]" |
| `fix/water-damage.html` | "Need a tech?" callout | "find a Newcastle tech" → main site |
| `fix/dropped-and-broken.html` | Same pattern | same |
| `fix/wont-turn-on.html` | Same pattern | same |
| `repair/iphone-15-pro-max.html` (and 19 other model pages) | "Where to get this fixed" section | For Newcastle/Hunter, point to the main site. For other cities, list local shops only. |
| `index.html` | The teal-900 CTA strip ("Skip the ringaround") | For users with Newcastle IP, the CTA could route to the main site — Phase 5 work |
| Footer | NO sitewide footer link to main site (would look like PBN). Keep main-site links contextual only. |

---

## 6. Technical reference

### Gitpage particulars
- **`.gitlab-ci.yml` deploys what?** (CORRECTED — see §12) Root `*.html`, `*.txt`, `*.xml` PLUS the content folders `fix/ locations/ repair/ brands/ tools/ blog/`, all explicitly copied. Markdown files (like this one) live in repo but don't deploy. **The folder list is explicit, not a wildcard — if a NEW top-level content folder is ever added, it MUST be appended to the `cp -r fix locations repair brands tools blog public/` line in `.gitlab-ci.yml` or that folder's pages will 404 live while looking fine in the repo.**
- **⚠️ `.gitlab-ci.yml` REGRESSES — re-verify every session (see §12).** The leading-dot filename breaks `discard_draft`/`publish_draft` (path error) but the `save_draft`+`publish_draft(forceOverwrite)` sequence still commits despite the error — always re-read the file to confirm. **More importantly: this file silently reverts to GitLab's broken default Pages template, almost certainly triggered by removing/re-adding the custom domain in GitLab Pages.** It has done this twice. FIRST ACTION every session and after any domain/DNS change: read `.gitlab-ci.yml`, confirm the `cp -r fix locations repair brands tools blog` line is present, re-apply if not, then verify a live subdirectory URL.
- **Edit pattern:** `edit_site_file` for tweaks, `save_draft` for new files / wholesale rewrites. Validate before publish.
- **Draft caching gotcha:** if `edit_site_file` returns EDIT_NOT_FOUND on text you know is there, a stale draft is shadowing the file. `discard_draft` first, then retry. (Learned the hard way on the main site refactor.)
- **CI is fast — ~2-3 min from commit to live.**

### Design tokens (CSS variables)
All pages declare these. Copy from existing pages for consistency.
```css
--rr-teal-900: #0c4a45;
--rr-teal-700: #0F766E;  /* primary brand */
--rr-amber-600: #d97706;
--rr-amber-500: #F59E0B;  /* accent / CTA */
--rr-ink:       #1C1917;
--rr-muted:     #78716C;
--rr-line:      #E7E5E4;
--rr-paper:     #FAFAF9;
--rr-paper-2:   #F5F5F4;
```

### Universal header & footer
Already in every Phase 1 page. The header has a 28×28 SVG wordmark with a custom rounded-square + R glyph, sticky with `backdrop-filter: blur(12px)`. The footer is `bg-teal-900` with 3 columns (Brand+tagline / Browse / About) plus an affiliate-disclosure block and trademark notice. **Copy these verbatim from any existing page when building new ones.**

### `devices.json` schema (Phase 2 data layer)
Defined in repo notes. Each device has: slug, brand, name, released date, repairs object (screen / battery / back_glass / charging_port — each with indie/auth/diy price arrays + difficulty), common_issues array.

---

## 7. Future satellite sites in the same family

This pattern (editorial content satellite with backlinks to the main site) can be applied to other ideas in Khalil's Gitpage account. Same playbook each time:

1. Pick a niche with informational search intent (cost queries, troubleshooting, comparisons)
2. Design that's distinct from the main site (no red, no duplicate-content vibes)
3. Phased build (skeleton first, content second, SEO last)
4. Every relevant local/regional context links to mayfieldphonerepair.com.au — *editorially, never spammily*
5. Tag all of them with the same Gitpage project tag for organization

Other sites in Khalil's account that could be repurposed/cleaned up:
- `newcastle-local-business-directory-2026-04-22-lnu23` — could become a real Newcastle business directory with Mayfield Phone Repair as a featured listing
- `news-blogs-post-2026-04-22-wt7ym` — could host phone/tech news with backlinks
- `phone-repair-in-mayfield-nsw-fast-affordable-warranted-2026-04-16-5hkq4` — already a landing page, 168 revisions; would benefit from an audit

---

## 8. Where the source files live

- **Canonical:** this `PROJECT.md` in the Gitpage repo
- **Working files:** `/home/claude/repairrange/` in Claude's sandbox during the session — **ephemeral, do not rely on these between sessions**
- **Published HTML:** the 8 root `.html` files in the repo are the live source of truth
- **Build scripts:** the Python build scripts in `/home/claude/repairrange/` are throwaway; if needed in future, rebuild them from this brief

---

## 11. Custom domain — RESOLVED (www-canonical) — May 2026

### FINAL OUTCOME (read this first)
After an extended multi-session battle, the domain is **LIVE and secure** at **`https://www.repairrange.io/`**. The site is **www-canonical**.

**What happened, short version:** the bare apex `repairrange.io` would never get a working Let's Encrypt cert through GitLab Pages (tried repeatedly — ALIAS-vs-A-record issues, cert wedging, ERR_EMPTY_RESPONSE / ERR_CONNECTION_RESET / ERR_CERT_COMMON_NAME_INVALID through many cycles). The `www.repairrange.io` subdomain (CNAME → mayfield276.gitlab.io) issued its cert cleanly every time. **Decision: stop fighting the apex. Make `www` canonical.** This is a standard, professional setup — not a compromise.

### Current working configuration (DO NOT "fix" the apex — it's intentional)
- `www.repairrange.io` → CNAME → `mayfield276.gitlab.io` → valid cert, serves the site. **This is the canonical home.**
- Bare `repairrange.io` → Hostinger redirect → `https://www.repairrange.io`. The apex is NOT relied on to serve directly and was removed from GitLab Pages. Do not re-add it.
- gitlab.io URL still works forever as a fallback.
- **If the apex ever shows a cert error again: that is expected and irrelevant. Everything routes through www. Do not attempt to re-add the apex to GitLab or chase its cert — that path was abandoned deliberately after days of failure.**

### Canonical sweep — DONE (all 31 pages, this session)
- [x] Every published page's `<link rel="canonical">` and `og:url` switched from `https://repairrange.io/...` to `https://www.repairrange.io/...`. All 31 HTML pages: index, brands, fix, locations, calculator, about, privacy, terms, tools/software-stack, brands/{apple,samsung,google}, locations/newcastle, all 10 fix/ guides, all 7 repair/ model pages. Homepage schema.org `url` also updated to www.
- [x] `blog.html` was an empty "hello world" stub with no canonical (it's what aborted the original 31-file batch). Converted to a `noindex, follow` placeholder that meta-redirects to /index.html — prevents a thin page dragging the site-quality signal. SHA `6e5208f5e375cb81f01722fc513657c19a48cdb3`. (If a real blog is built later, replace it.)

### Launch sequence — mostly DONE (this session)
- [x] Regenerated `sitemap.xml` with customDomain=`https://www.repairrange.io`, pruned `blog.html` + `blog/sample-post.html` stubs, published. SHA `b9e124b515e78dba150104ba5e073004aef1f6c3`. 30 real pages.
- [x] Generated + published `robots.txt` (allows crawl, references https://www.repairrange.io/sitemap.xml). SHA `7080d5a5dc0999605665e51ac0d41baed89180f4`.
- [x] Generated + published `llms.txt` (fixed generator's doubled-https bug, removed blog stub). SHA `473190fcae17fc98cb8b47acf2c82a257aad977e`.
- [x] **Google Search Console — VERIFIED (May 2026).** Khalil added a **Domain property** for `repairrange.io` and verified it via a **DNS TXT record at Hostinger** (the HTML meta-tag method failed because the www URL redirects to the bare apex and Google's verifier wouldn't follow the hop — DNS verification sidesteps that entirely and is the robust choice given this domain's redirect layer). A `google-site-verification` meta tag was also added to index.html (SHA `c12a89129c7e9fe1f44cea0d9f916a4636f9d31c`) — now redundant under DNS verification but harmless; leave it.
- [x] **Sitemap submitted AND accepted by Google Search Console (Khalil, May 2026).** Submitted under the `repairrange.io` Domain property. It initially showed **"Couldn't fetch"** (the apex→www redirect tripping Google's sitemap fetcher, exactly as predicted) then flipped to **"Success"** — confirmed by Khalil. Google is now discovering all ~34 pages. **LAUNCH SEQUENCE FULLY COMPLETE — site is live, secure, verified, and being indexed. Nothing further blocks discovery.** Indexing of individual pages still rolls out over days–weeks (normal). **Reusable lesson for future satellite sites on this Hostinger apex→www setup: GSC sitemap submission will likely show "Couldn't fetch" first; resubmitting the explicit `https://www.<domain>/sitemap.xml` (not the bare path) and/or waiting for a retry resolves it — this is expected, not a fault.**

### Migration consideration
gitlab.io URL keeps working forever as backup. Google should see `https://www.repairrange.io` as canonical (the canonical tags now correctly say so). No GitLab-side 301s needed; the Hostinger apex→www redirect plus the canonical tags handle SEO consolidation.

---

## 12. ⚠️ Deploy bug (CI subdirectory copy) + Phase 4 — May 2026

### The deploy bug (CRITICAL history — do not repeat)
**Symptom:** every subdirectory page (all 10 `fix/` guides, all 5 `locations/` pages, all 7 `repair/` model pages, 3 `brands/` pages, `tools/`) returned **404 on the live site**, while the repo content was 100% correct and `read_site_file` showed them fine. Root pages (index, brands.html, fix.html, locations.html) worked, masking it.

**Root cause:** `.gitlab-ci.yml` only ran `cp *.html public/` + `cp -r blog public/` + txt/xml. It NEVER copied `fix/ locations/ repair/ brands/ tools/`. Those pages were committed but never deployed. This persisted across MULTIPLE sessions because PROJECT.md §9 had been (incorrectly) marked “CI publish — done, SHA 3c1a3fa6…”, and §6 still described the old broken behaviour — so every session trusted the brief instead of testing a live subdirectory URL.

**Fix:** rewrote the CI script to:
```yaml
script:
  - mkdir -p public
  - cp -r ./*.html ./*.txt ./*.xml public/ 2>/dev/null || true
  - cp -r fix locations repair brands tools blog public/ 2>/dev/null || true
```
Committed at SHA `abc580c106b8784844696c4da212fca133ad3286`. Pipeline ran; Khalil confirmed `https://www.repairrange.io/locations/sydney.html` and the troubleshooting links now load. **The folder list is explicit on purpose** (a blanket `cp -r *` would drag PROJECT.md and .gitlab-ci.yml into the public site). New top-level content folders must be added to that line.

**Tooling note:** `discard_draft`/`publish_draft` fail on `.gitlab-ci.yml` (leading-dot path bug, error `'publishedPagesMeta..gitlab-ci.yml' contains an empty field name`). Despite that error the `save_draft`+`publish_draft(forceOverwrite:true)` sequence DOES commit — always re-`read_site_file` the .yml afterward to confirm the new SHA + correct content; do not trust the error message either way.

**🔴 THIS FIX REGRESSES — IT IS NOT PERMANENT (confirmed twice, May 2026).** The CI was fixed (SHA `abc580c1`), verified live by Khalil, then **silently reverted on its own** to the broken root-only config (mystery SHA `1fdb35f8`), breaking every subdirectory page again mid-session. Re-fixed at SHA `4b4c9382`. **Khalil's hypothesis (high confidence): removing and re-adding the custom domain in GitLab Pages regenerates/resets `.gitlab-ci.yml` to GitLab's default Pages template — which is exactly the broken "copy root *.html + blog/ only" pattern.** This also explains why the broken versions were configs neither of us wrote. The HTTPS-now-working state is the same root event: a domain operation fixed the cert AND clobbered the CI.

**MANDATORY SESSION-START + POST-DOMAIN-CHANGE CHECK (do this before any Phase 2/content work, and immediately after ANY domain/DNS/GitLab-Pages change):**
1. `read_site_file('.gitlab-ci.yml')` — confirm it contains the `cp -r fix locations repair brands tools blog public/` line. If it shows the short `cp *.html` + `cp -r blog` pattern, it has regressed — re-apply the fix immediately.
2. After re-applying, confirm the pipeline ran green AND load a real subdirectory URL (`https://www.repairrange.io/locations/sydney.html`) on the live domain. Commit success ≠ deployed.
3. Treat the brief's "deploy fixed" claims as PROVISIONAL, never settled. This is the single highest-recurrence failure in the project.

**Process lesson (apply to all future deploy/infra changes):** a deploy or routing change is NOT done until an actual deep URL (not the root, not the repo, not a preview) is loaded on the live custom domain and confirmed. Never mark such a task complete on the basis of a successful commit alone. AND: infra fixes here are not durable — re-verify, don't assume.

### Phase 4 — COMPLETE (May 2026)
All 5 `/locations/` city pages built, published, and — after the CI fix — verified live.
- ✅ `locations/newcastle.html` — the backlink keystone (built earlier; features Mayfield Phone Repair). SHA `8eb0b1e3…`.
- ✅ `locations/sydney.html` — SHA `55b169fa1491424b730c4fbb2539cb27a5f7d0be`. Honest pricing, CBD-vs-suburb context, NO Mayfield push, AggregateOffer schema, calculator CTA.
- ✅ `locations/melbourne.html` — SHA `ef7ac4acebf6eff17419361c511557721f6d88db`. Inner-north value angle, teaser-rate warning.
- ✅ `locations/brisbane.html` — SHA `ede871c56b93840ac8f16185d4d605372babf5c5`. Tighter-spread + humidity/charging-port angle.
- ✅ `locations/perth.html` — SHA `c9f614e3455410ee7573172b8fb366bed102f439`. Parts-lead-time angle, slightly higher floor (freight).

**Newcastle exclusivity preserved:** the 4 non-Newcastle pages deliberately do NOT feature or link Mayfield (per §1 strategy — pushing Mayfield outside the Hunter cheapens the keystone). They point to the calculator instead.

**`locations.html` honesty fix (SHA `a41dc68550e5de785d63960fb22289b1ec7c91cc`):** the index had been making FALSE claims that the new honest city pages contradicted — fake “Verified shops: 18/15/11/8” counts, a hero promising “get matched with a verified local tech” (no such matching exists), and a methodology describing a phone-quote-gathering process that never happened. All rewritten to be truthful: real iPhone-14 ranges per city, “Local guide: Full” instead of fake counts, honest methodology with an explicit disclosure that Newcastle is the editorial exception. **If editing locations.html again, do not reintroduce “verified/vetted/matched” language — it's false and an ACCC risk.**

**Sitemap regenerated + published (SHA `fb52cde389e2a06c43433d0def71bc4fc19f8098`):** now 34 real pages incl. the 4 new city pages; `blog.html` + `blog/sample-post.html` pruned again (generate_sitemap re-adds them every run — always re-prune).

### Open international placeholders (low priority, untouched)
`locations.html` still has 4 “Coming Q2 2026” cards (London/NY/LA/Toronto) — cosmetic, harmless, no pages behind them. Leave or remove later.

---

## 13. Monetisation — paid-listing directory (designed May 2026, NOT YET BUILT)

### The model
Paid shop listings on the **non-Newcastle city pages** (Sydney, Melbourne, Brisbane, Perth) under a **prepaid pay-per-click** scheme. Newcastle is OFF-LIMITS to paid slots — it stays the editorial keystone featuring Mayfield Phone Repair (§1). Touching Newcastle's curation kills the rest of the strategy.

**Mechanic:**
1. Shop creates a listing and prepays $10 (Stripe).
2. Each billable user action against their listing deducts $1 from their balance.
3. When balance hits $0, listing auto-pauses until they top up.
4. Linear scaling: 100 paid clicks across all shops = $100 revenue. No ceiling, no extra ops cost per click once plumbing exists.

**Defensible labelling:** all paid slots labelled **"Listed shops"**, NEVER "verified", "recommended", "endorsed", or "vetted". ACCC + credibility. The page must somewhere visibly disclose that listings are paid placements.

### What counts as a billable click (one event per visitor session, deduped)
The valuable user actions — a billable click is the FIRST of these to fire in a session:
- "Call now" tap on mobile (click-to-call link)
- Phone number reveal on desktop (number hidden until tapped)
- Quote/booking form submission

Secondary impressions (just scrolling past the listing) are NOT billable — too gameable, too low-signal. Bill only on intent actions.

### Fraud protection (non-negotiable — the system fails on trust without this)
- Unique-visitor dedupe: same IP within 24h = max 1 billable click per listing.
- Bot filtering: block known bot UAs, add a basic JS challenge.
- Daily cap per listing: e.g. max 5–10 billable clicks/day to prevent runaway burn.
- Self-click exclusion: shop owner's own IP/device range never bills.
- Dispute window: shop can flag suspicious clicks within 7 days, Khalil reviews.

### Unit economics (honest read)
- $1/click at ≈20–30% lead-to-sale conversion = $3–$5 customer-acquisition cost on a $200+ screen repair job. Excellent value for the shop. Room to raise to $1.50–$2 once traffic is proven.
- $10 = only 10 clicks. For a well-ranking listing this depletes fast. **Auto-topup is essential** (Stripe saved card, "refill $50 when balance < $5") — without it, 50%+ of listings will lapse paused. Manual top-up should still be an option for shops who prefer no auto-charge.

### Hard prerequisite
**Build only AFTER city pages actually rank and pull traffic.** Selling listings on pages that don't rank = no clicks = angry shops = refunds + bad word of mouth in the AU repair-shop community (which is small and talks). Wait for measurable monthly visitors per city page before pitching anyone.

### Phased rollout (recommended — don't skip phases)

**Phase A — manual paid listings (no code).** Once 2–3 city pages rank, email 3–5 shops per city. Quote flat $30/month for a slot, paid via bank transfer. Track clicks in a Google Sheet. Goal: prove shops will pay, refine pitch, learn objections. Revenue: maybe $200–500/month. Build cost: zero. **Skipping this phase is the #1 way directory businesses die — don't.**

**Phase B — prepaid model on minimal infra.** Stripe checkout link for prepay. Cloudflare Worker (or similar) for click tracking + dedupe. Simple admin dashboard for Khalil only — no shop logins yet. Shops email Khalil to top up; he updates balances manually. Crude but proves unit economics with real money. ~1 week build.

**Phase C — full self-service.** Shop login, balance dashboard, auto-topup via saved Stripe card, dispute interface, click breakdown analytics. Build only if Phase B clears ≈$500/month consistently. ~3–4 weeks focused dev.

### Open design questions (decide at Phase B)
- Stripe vs simpler payment (manual invoice for AU shops who prefer bank transfer)?
- Refund policy on disputed clicks — case-by-case, or auto-credit any flagged click and trust the shop?
- Pricing tiers — keep $1 universal, or charge more in Sydney where intent is higher?
- One slot per city or unlimited (with rotation)? Single slot reduces competition burn rate but caps total revenue.
- Should shops be able to set their own daily cap (e.g. "max $5/day")? Probably yes — reduces refund disputes.

### What this is NOT
- NOT a replacement for the satellite-backlink purpose (§1). The primary value of RepairRange is editorial backlinks to mayfieldphonerepair.com.au. Directory revenue is a secondary upside, never the primary lever.
- NOT a lead-routing system that takes a cut of sales — too complex to track, too disputable, and would require trusting shops to self-report sales. PPC sidesteps all that.
- NOT to be confused with Mayfield's Newcastle slot, which is editorial and free.

---

## 9. Open questions / to-decide

- [x] **CI publish — ACTUALLY fixed this session (was falsely marked done before).** See §12. The earlier claim that SHA `3c1a3fa6…` deployed the subdirs was WRONG — that CI still only copied root `*.html` + `blog/`, so every subdirectory page 404'd on the live site for multiple sessions while appearing correct in the repo. Real fix committed at SHA `abc580c106b8784844696c4da212fca133ad3286`; pipeline run confirmed; subdirectory pages verified live by Khalil. Lesson: never mark a deploy fix done without loading an actual subdirectory URL on the live domain.

- [ ] Custom domain for RepairRange (when to register, which TLD)
- [ ] Whether to disclose the Mayfield Phone Repair connection on the About page (recommendation: yes, in Phase 5, once Mayfield is a featured Newcastle shop)
- [ ] Lead-gen form mechanics (Phase 4) — where do non-Newcastle leads route? Sell to other shops, or just say "we'll match you in 24h" and email Khalil?
- [ ] AdSense application timing (after 30–50 pages, so post-Phase 3)
- [ ] Amazon Associates application timing (any time, but more credible with traffic)
- [ ] Email forwarding setup for hello@repairrange.io (now that the domain is registered)
- [ ] Directory model (Phase 6/7): listing data format, submission/moderation mechanism, payment link choice — decide at Phase 6 start, not before (depends on what's cheapest to administer then)

---

## 10. Phase 2 status (in progress — do not lose context)

### ⚠️ §10 WAS STALE — corrected May 2026 against the LIVE repo (do not trust prior "done" claims here)
The previous version of this section claimed "2 model pages LIVE" and "`data/devices.json` v2026.05.2 … Published". **Both were FALSE when checked against `list_site_files`.** Same false-"done" pattern as the CI bug (§12). Verified actual state below. **Rule: trust only `list_site_files`/`read_site_file`, never this section's history.**

### What's ACTUALLY live (verified via list_site_files, May 2026)
- **NO `data/` directory exists in the repo.** `devices.json` was never committed. The calculator still uses inlined model data. Any build script lived only in the ephemeral sandbox and is gone.
- **7 model pages exist in `/repair/`:** `iphone-14.html`, `iphone-14-pro.html`, `iphone-15.html`, `iphone-15-pro.html`, `iphone-15-pro-max.html`, `pixel-8-pro.html`, `samsung-galaxy-s24-ultra.html`.
- No Python build script in repo (sandbox ephemeral). Model pages are now built by adapting the live `repair/iphone-14.html` template per model — no devices.json dependency.

### Pricing sourcing decision (Khalil, May 2026)
Khalil chose **web search for AU market pricing** for the remaining models (not bench prices, not derivation). NEVER fabricate pricing — the site's entire value is honest researched pricing. "Independent" column = reputable shop with OEM-grade/quality-aftermarket parts (NOT rock-bottom kiosk, NOT Apple authorised). Maintain internal descending-by-age coherence: older models priced a notch below newer (e.g. iPhone 13 set below the live iPhone 14's $199–$289 independent screen).

### What's NOT yet done — 13 models REMAINING
Build method: read live `repair/iphone-14.html` as the template, adapt per model with correct name/specs/pricing, web-search AU pricing per model, `save_draft` + `validate_draft` + `publish_draft` each immediately (don't batch — context-safe; ~22–31K tokens/page). **CRITICAL: after publishing repair pages, re-verify `.gitlab-ci.yml` is NOT regressed (§12) and load a real `repair/{slug}.html` URL live before calling any of it done — a repair page in a regressed deploy is invisible.**

Remaining 13 slugs (priority order, highest search volume first):
- iphone-13 (DRAFT staged this session, NOT yet published — finish first), iphone-12, iphone-13-pro-max, iphone-14-pro-max, iphone-15-plus, iphone-se-3
- samsung-galaxy-s24, samsung-galaxy-s23-ultra, samsung-galaxy-s23, samsung-galaxy-a54
- samsung-galaxy-z-fold-5, samsung-galaxy-z-flip-5 (foldables — different repair economics, search pricing carefully)
- pixel-8

### 🔴 PER-MODEL CHECKLIST — a model page is NOT done until ALL of these are committed (do them as ONE unit, never split)
The iPhone 13 "Soon" bug (May 2026) happened because the page was published but the two brand-index links still said "Soon", so visitors/Google couldn't find it. For EVERY model built, all of the following must be done together before moving on:
1. `repair/{slug}.html` — build from the live `repair/iphone-14.html` template, web-searched AU pricing, save_draft + validate_draft + publish_draft.
2. `brands.html` — in the "Popular models, A–Z" list, change that model's `<a href="calculator.html" class="ed-link text-muted ...">` to `<a href="repair/{slug}.html" class="ed-link text-ink ...">` (muted→ink = greyed→live).
3. `brands/{brand}.html` (apple.html / samsung.html / google.html) — convert that model's greyed `<div class="bg-white p-6 opacity-55">…Soon…</div>` placeholder card into the live `<a href="../repair/{slug}.html" class="card bg-white p-6 group">…` style with the arrow icon + "Screen from $X · full guide".
4. Update the brand card's "N guides live" count on `brands.html` if it changed.
5. After publishing: re-verify `.gitlab-ci.yml` not regressed (§12) and load the live `repair/{slug}.html` URL.
**"Soon"/greyed labels are accurate for un-built models — do NOT remove a "Soon" label without building the actual page; routing a fake "live" link to the calculator is dishonest and breaks the site's core value.**

### Progress log (update as each ships)
- ✅ iphone-13 — page SHA `8e509ea0503d27980834e5d49ed073f791aa10db`; brands.html link `efe65d353a9fab2f647b1bdec07869b57c2869c2`; brands/apple.html card `5c8e8a359cb07f8169b2b8b0574a9378bd8965e6`. Screen $179–$269 indie. DONE — pending Khalil live-URL confirmation.
- ✅ iphone-12 — page SHA `133f907c1557b6eca86988c1ff844d431383d611`; brands.html link+count `fef6834ffa3440ad7332f399dbb2445b14adc2e8`; brands/apple.html card `1300abccca7cdc40dfd69bca5b2009579673982a`. Screen $159–$239 indie. DONE — pending Khalil live-URL confirmation.
- ✅ iphone-13-pro-max — page SHA `55b8da4db355dbe33da61cb47423e4b517bb33e7`; brands.html link + Apple count 7→8 SHA `20cb445bfcf98923f72412547a41691f93458d0d`; brands/apple.html card SHA `b91e75a38c5b5a249cd248a503559820237e2a0b`. Screen $249–$379 indie (above std 13, 6.7" ProMotion). CI re-verified intact (`4b4c9382`). DONE — pending Khalil live-URL confirmation.
- ✅ iphone-14-pro-max — page SHA `842fa33a6c6f5736880f1e49678e7ba32bf84bb5`; brands.html link + Apple count 8→9 SHA `e3753842d894af992cbf04b404e41128ce29b740`; brands/apple.html card SHA `2afbe885dde3956ed48ca80abe3d76fcac329a59`. Screen $309–$469 indie (top of 14 line, back-glass-first chassis cheaper than 13PM). CI re-verified intact (`4b4c9382`). DONE — pending Khalil live-URL confirmation.
- ✅ iphone-15-plus — page SHA `4b0cdbffd240e4ec45bb9d045eea3bdad8fad410`; brands.html link + Apple count 9→10 SHA `154e41bebe80a2691ebed554bb909f36206592e5`; brands/apple.html card SHA `a871e820996345a9996e1843f2b570621209c2bd`. Screen $239–$329 indie (no ProMotion/Dynamic Island = cheaper than 15PM, sits above std 15). **15-series uses USB-C, not Lightning** — page reflects this in the port column header and DIY note. CI re-verified intact (`4b4c9382`). DONE — pending Khalil live-URL confirmation. The iPhone 15 line is now COMPLETE (15, 15+, 15 Pro, 15PM all live).
- ⏳ 8 remaining — ALL need pricing research. Priority: iphone-se-3 (⚠️ DIFFERENT FORM FACTOR — 4.7" LCD, Touch ID not Face ID, Lightning, Home button — template needs careful spec adjustment, NOT just pricing swap), then Samsung block (s24, s23-ultra, s23, a54), foldables (z-fold-5, z-flip-5 — search carefully, very different repair economics), pixel-8.
  - Samsung pages go in brands/samsung.html (count currently "1 guide live" — the live s24-ultra). Pixel pages in brands/google.html ("1 guide live" — the live pixel-8-pro).

### NOTE: stale .gitlab-ci.yml DRAFT exists (harmless, do not touch)
A 257-byte unpublished `.gitlab-ci.yml` draft is staged (the correct fixed content, from an earlier save_draft that couldn't be cleared due to the leading-dot discard bug). The LIVE committed CI is correct (`4b4c9382`). Do NOT try to discard it (hits the tooling bug) and do NOT publish it (unnecessary — live is already identical/correct). validate_draft will keep flagging it with spurious HTML errors — ignore. Leave it alone.

### CONTEXT BUDGET LESSON (May 2026)
A fully-checklisted model costs ~80–100K tokens (pricing search + template read + 31K page build + two ~18K brand-index reads + edits + CI verify). Realistic safe budget: **2–3 models per session**, NOT more — attempting more risks a half-built page / missed brand link / unverified deploy, which is the project's recurring buried-failure mode. Pre-researching pricing into this log (as done above for the next two) lets the next session skip the search step and do more.

### Pricing corrections already applied in v2026.05.2 (don't re-apply)
- iPhone 15 Pro Max back glass: $169–$279 (was $199–$349) — user-serviceable design
- Galaxy S24 Ultra screen floor: $299–$499 (was $349–$499) — AU indie reality

### Skipped by Khalil's choice (handle separately)
- Newcastle/Hunter main-site backlinks on model pages — will be added in a single backlink sweep after all 20 model pages are live.

### ⚠️ Current-generation models MISSING from the queue (Khalil flagged, May 2026)
The original 20-model list predates newer releases. **iPhone 17 series and Samsung Galaxy S26 series (plus likely a newer Pixel) are now out and are NOT in devices.json or the queue.** Without them the site looks dated and misses the highest-value search traffic. Requirements when adding:
- Confirm exact current lineup + model names via web search AND/OR Khalil (naming conventions may have shifted, e.g. "Air" tiers, Fold/Flip generations).
- Pricing MUST be real (Khalil's bench / AU supplier data preferred; brand-new models have volatile premium pricing that estimated multipliers get wrong and that goes stale fast).
- Build these EARLY in the next batch — newest models = highest-intent, highest-traffic queries.
- Add to devices.json first, then build pages, then they flow into sitemap automatically.

### After Phase 2 completes, before Phase 3
- Update `calculator.html` to `fetch('data/devices.json')` instead of inlined MODELS dict
- Regenerate `sitemap.xml` via Gitpage:generate_sitemap so all model pages are indexed
- Submit fresh sitemap to Google Search Console
