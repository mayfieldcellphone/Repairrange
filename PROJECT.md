# RepairRange — Project Brief & Working Document

> **Canonical source of truth** for the RepairRange satellite site. Lives in this repo so it persists across Claude sessions and is version-controlled with the code. Not deployed publicly (CI only copies `*.html`, `*.txt`, `*.xml`).
>
> **Last updated:** May 2026 · Phase 1 complete, Phase 2 in progress

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
| **Live URL** | https://mayfield276.gitlab.io/blank-site-2026-05-06-6rrng (will move to repairrange.io once DNS is live) |
| **Gitpage pageId** | `69fb1fc8a84e148d906285c4` |
| **Repo** | `blank-site-2026-05-06-6rrng` on gitlab.com/mayfield276 |
| **Custom domain** | **`repairrange.io`** (registered May 2026, 3-year term) |
| **Contact email (planned)** | hello@repairrange.com |

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

### Phase 3 — 10 troubleshooting guides
Build `/fix/{slug}.html` for the 10 guides linked from `fix.html`:
- `black-screen.html` · `green-lines.html` · `ghost-touch.html` · `cracked-screen-still-works.html`
- `battery-drains-fast.html` · `charging-port.html` · `wont-turn-on.html` · `overheating.html`
- `water-damage.html` · `dropped-and-broken.html`

Each 800–1500 words, written from genuine repair experience (Khalil's actual work). These are the **AdSense + E-E-A-T anchors** — Google looks for real expertise here.

**Backlink opportunity:** every guide should have a "Need this fixed in Newcastle?" callout linking to mayfieldphonerepair.com.au.

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
- **`.gitlab-ci.yml` deploys what?** Root `*.html`, `blog/` dir, `*.txt`, `*.xml`. Markdown files (like this one) live in repo but don't deploy.
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

## 11. Custom domain rollout — repairrange.io (in progress)

### Registrar setup (Khalil's task)
- [ ] Add A records for apex: `35.185.44.232`, `35.190.65.110`, `35.227.220.34`, `35.232.218.50`
- [ ] Add CNAME for `www`: `mayfield276.gitlab.io`
- [ ] Enable WHOIS privacy
- [ ] Verify auto-renew is off (paid 3 yr upfront)

### GitLab Pages verification (Khalil's task)
URL: https://gitlab.com/mayfield276/blank-site-2026-05-06-6rrng/-/pages
- [ ] Add domain `repairrange.io` in GitLab Pages settings
- [ ] Copy the TXT verification record GitLab provides
- [ ] Add the TXT record at the registrar
- [ ] Click "Verify ownership" in GitLab
- [ ] Repeat for `www.repairrange.io`
- [ ] Wait for Let's Encrypt SSL cert to auto-issue (5–30 min after verification)

### Site updates after DNS propagates (Claude's task)
- [x] Update all internal absolute URLs (none — all internal links are relative)
- [x] Add `<link rel="canonical">` to every published page → all 16 live pages done (9 Phase 1 + 7 model pages), all point to https://repairrange.io/...
- [x] Add `og:url` to every published page → done in same sweep
- [x] Fixed critical bug: homepage schema.org url was `repairrange.com` (a domain we don't own) → corrected to `repairrange.io`
- [x] `sitemap.xml` generated via generate_sitemap with customDomain=https://repairrange.io (STAGED AS DRAFT — not yet published; publish once HTTPS confirmed)
- [ ] Generate `robots.txt` via Gitpage:generate_robots_txt (do after sitemap published)
- [ ] Generate `llms.txt` via Gitpage:generate_llms_txt
- [ ] Publish sitemap.xml draft (waiting on HTTPS confirmation so URLs resolve)
- [ ] Verify ownership of repairrange.io in Google Search Console
- [ ] Submit sitemap.xml to Google Search Console

### SSL / HTTPS status (as of last session)
- DNS: confirmed resolving correctly at Hostinger (4 A records + www CNAME)
- Errors progressed ERR_EMPTY_RESPONSE → 404 → ERR_CONNECTION_CLOSED → (turned Force HTTPS OFF) → http://repairrange.io/index.html now SERVES the site
- **Root cause of the fluctuating errors:** Let's Encrypt SSL cert still provisioning. Turning Force HTTPS off let the site serve over HTTP, which is what lets Let's Encrypt complete its domain-validation challenge.
- **NEXT:** Khalil to watch GitLab Pages settings (https://gitlab.com/mayfield276/blank-site-2026-05-06-6rrng/-/settings/pages) for the Certificate status. When it shows Active/Issued → turn Force HTTPS back ON → test https://repairrange.io/ → tell Claude "HTTPS is live" → Claude publishes sitemap.xml, generates robots.txt + llms.txt, guides GSC submission.
- **Open question to verify:** does http://repairrange.io/ (root, no /index.html) load? If only /index.html works, a default-document fix may be needed in CI.

### Migration consideration
The gitlab.io URL will keep working forever (GitLab doesn't shut it down). Once `repairrange.io` is live, the gitlab.io URL stays as a backup but Google should see `repairrange.io` as canonical. No 301 redirects needed at the GitLab side; the canonical tags handle the SEO consolidation.

---

## 9. Open questions / to-decide

- [x] **CI publish.** `.gitlab-ci.yml` updated and published — deploys tools/, repair/, fix/, locations/, brands/, data/ subdirs. SHA `3c1a3fa69883c12e85874a46047a3ddc70bae6e3`.

- [ ] Custom domain for RepairRange (when to register, which TLD)
- [ ] Whether to disclose the Mayfield Phone Repair connection on the About page (recommendation: yes, in Phase 5, once Mayfield is a featured Newcastle shop)
- [ ] Lead-gen form mechanics (Phase 4) — where do non-Newcastle leads route? Sell to other shops, or just say "we'll match you in 24h" and email Khalil?
- [ ] AdSense application timing (after 30–50 pages, so post-Phase 3)
- [ ] Amazon Associates application timing (any time, but more credible with traffic)
- [ ] Email forwarding setup for hello@repairrange.io (now that the domain is registered)

---

## 10. Phase 2 status (in progress — do not lose context)

### What's done
- `data/devices.json` v2026.05.2 with 20 devices and full pricing data. Published.
- `build_model_page.py` — Python template that reads devices.json and renders /repair/{slug}.html. Lives on Claude's sandbox during sessions; rebuild from devices.json schema if missing.
- 2 model pages LIVE: `repair/iphone-14.html` and `repair/iphone-15-pro-max.html`.

### What's NOT yet done (FINISH IN NEXT SESSION)
Publish the remaining 18 model pages. Sandbox files are ephemeral; regenerate via:
```
cd /home/claude/repairrange && python3 build_all_model_pages.py
```
Then loop `save_draft` + `publish_draft` for each slug. **Important:** save_draft is token-heavy at ~22K tokens per page — next session can budget ~12 pages max per session.

Remaining 18 slugs:
- iphone-15-pro, iphone-15-plus, iphone-15
- iphone-14-pro-max, iphone-14-pro
- iphone-13-pro-max, iphone-13, iphone-12, iphone-se-3
- samsung-galaxy-s24-ultra, samsung-galaxy-s24, samsung-galaxy-s23-ultra, samsung-galaxy-s23
- samsung-galaxy-z-fold-5, samsung-galaxy-z-flip-5, samsung-galaxy-a54
- pixel-8-pro, pixel-8

### Pricing corrections already applied in v2026.05.2 (don't re-apply)
- iPhone 15 Pro Max back glass: $169–$279 (was $199–$349) — user-serviceable design
- Galaxy S24 Ultra screen floor: $299–$499 (was $349–$499) — AU indie reality

### Skipped by Khalil's choice (handle separately)
- Newcastle/Hunter main-site backlinks on model pages — will be added in a single backlink sweep after all 20 model pages are live.

### After Phase 2 completes, before Phase 3
- Update `calculator.html` to `fetch('data/devices.json')` instead of inlined MODELS dict
- Regenerate `sitemap.xml` via Gitpage:generate_sitemap so all model pages are indexed
- Submit fresh sitemap to Google Search Console
