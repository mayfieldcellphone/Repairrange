# RepairRange — Shop Directory Design Doc

> **Status:** DESIGN PHASE — no code, no live pages, no real shop signups yet. This document exists to settle the hard questions BEFORE building. Updated as decisions are made.
>
> **Scope:** the paid-listing directory system described in PROJECT.md §13. This doc is the working design; PROJECT.md §13 is the strategic frame.
>
> **NOTE: this `.md` file does NOT deploy to the live site** (per `.gitlab-ci.yml` — only `*.html / *.txt / *.xml` and content folders deploy). It lives in the repo as design reference only. Safe to commit freely.

---

## 0. Guiding principles (re-state from PROJECT.md so this doc is self-contained)

1. **Newcastle is OFF-LIMITS** to paid listings. It stays the curated editorial keystone featuring Mayfield Phone Repair, free, never paid. Paid directory exists ONLY on `locations/sydney.html`, `locations/melbourne.html`, `locations/brisbane.html`, `locations/perth.html`.
2. **Honesty over polish.** "Listed shops" not "verified" / "recommended" / "vetted". ACCC + credibility.
3. **Don't break the SEO/editorial credibility of the page.** The whole point of RepairRange is editorial backlinks to mayfieldphonerepair.com.au (PROJECT.md §1). A clunky paid-listings section that screams "ad" will tank the trust signal that makes the rest of the site work.
4. **Build only AFTER pages rank.** Selling listings on dead pages = no clicks = angry shops = refunds + reputation damage in the small AU repair community. No real shop onboarding goes live until city pages have measurable monthly visitors.
5. **Phase A (manual) before Phase B (code).** PROJECT.md §13 spells this out. Static design and prototype HTML can be built ahead of time; live signup with payment integration only happens after Phase A proves shops will pay.

---

## 1. The hard design questions (with proposed answers — revise as needed)

### Q1: What does a shop's listing look like on the city page?

**Decision (proposed):** A "Listed shops in [City]" section that appears BELOW the editorial pricing table and city-context narrative, not woven into them. Each listing is a card with:
- Business name + suburb (one line)
- One-line description (shop-written, 100 char max)
- Services offered (chips: "Screen repair", "Battery", "Water damage", etc.)
- Opening hours summary
- "Call now" button (mobile click-to-call) / phone number reveal (desktop)
- "Get a quote" button → opens shop-specific quote form
- Small "Listed shop" label on the card (NOT "verified" / "recommended")

**Why below, not woven in:** keeps the editorial pricing section uncontaminated by paid content. A reader scanning for pricing reads pricing. A reader looking for a shop scrolls to the shops section. Clear separation = defensible disclosure + better UX.

**Section header copy (proposed):** "Listed shops in Sydney" with a small explanatory line beneath: "These shops pay to appear here. We don't vet them. Listings are not endorsements — compare quotes against the pricing above."

That explanatory line is the ACCC-defensible disclosure. It's prominent, plain-English, and doesn't try to soft-pedal. Honesty as a feature.

### Q2: What data does a shop submit during signup?

**MVP signup form (required):**
- Business name
- ABN (validates legitimacy — free check via ABN Lookup API, also helps with GST treatment of payments)
- Address (suburb + state minimum; full address optional)
- Public phone number (click-to-call target)
- One-line description (100 char max, shop-written)
- Services offered (multi-select checkbox: Screen / Battery / Back glass / Water damage / Charging port / Software / Other)
- Opening hours
- Owner contact name + email (NOT publicly displayed — for our records / dispute communication)
- Acceptance of terms (separate flat doc)

**Nice-to-have (Phase C, not MVP):**
- Logo upload
- Photo of shopfront
- Warranty terms
- Average turnaround time
- Brands specialised in

**Decision rationale:** MVP captures only what's needed to render a useful card + identify a real business. Logos and photos require image hosting + moderation pipeline; not worth Phase A complexity.

### Q3: How does a shop see their listing before going live?

**Decision (proposed):** Manual approval for Phase A and Phase B; self-service approval pipeline only in Phase C.

- **Phase A (no code):** Shop emails Khalil their details → Khalil manually creates the card HTML in the city page → Khalil emails the shop a preview link (the live URL once committed). No back-and-forth iteration; if the shop wants edits, they email and Khalil edits. Crude but works for first 10 shops.
- **Phase B (light code):** A signup form on the site posts data to a private spreadsheet/database. Khalil reviews, manually publishes via a private admin page. Shop sees the preview only AFTER approval. Bottleneck is Khalil, by design.
- **Phase C (self-service):** Shop submits → auto-generates preview → shop approves → goes live. Khalil reviews flagged listings only (anything with banned keywords, ABN mismatch, etc.).

**Why manual at first:** the first 10–20 shops set the tone for the directory. One bad listing (misleading claims, sketchy looking, profanity) damages credibility for every legitimate shop that follows. Manual review for the early period is cheap insurance.

### Q4: What happens at signup if there's no payment infrastructure yet?

**Decision (proposed) — Phase A path:**
1. Shop fills out the signup form (which we can build as static HTML now, posting to Formspree / a similar no-code endpoint).
2. Confirmation page: "Thanks. Listings launch [date]. We'll email you to confirm details and arrange the $10 starter balance via bank transfer."
3. Khalil emails the shop within 48hrs with bank details + asks for any missing fields.
4. On receipt of $10: Khalil creates the listing card on the live page, emails shop the URL, starts a Google Sheet tracking their balance / clicks.

**Trade-off accepted:** this is slow and manual. That's the point. It forces Khalil to actually speak to the first 10 shops, learn their objections, refine the pitch, and prove the unit economics with real money before writing a single line of payment integration code. Per PROJECT.md §13's "skipping Phase A is the #1 way directory businesses die."

### Q5: How is the click event designed in the HTML from day one?

**Decision (proposed):** Every billable action element on a shop's card gets these data attributes from the start, even before any tracking script exists:

```html
<a href="tel:+61245491735"
   class="shop-cta shop-cta-call"
   data-shop-id="SYD-0001"
   data-shop-action="call">Call now</a>

<button class="shop-cta shop-cta-quote"
        data-shop-id="SYD-0001"
        data-shop-action="quote-open">Get a quote</button>
```

The `data-shop-id` and `data-shop-action` attributes are dormant in Phase A (no JS reads them), but the moment a tracking script is added in Phase B, every listing already speaks the right protocol. **Retrofitting this later across dozens of listings = pain. Designing it in from day one = free.**

**Click-event spec (for the tracking script we'll write in Phase B):**
- Fire on: `click` of any element with `data-shop-action` attribute.
- Send: `{ shopId, action, ts, sessionId, ipHash, userAgentHash }` to the tracking endpoint.
- Dedupe at endpoint: same `shopId` + same `ipHash` within 24h = ignored.
- Daily cap: max N billable events per `shopId` per day (default 10, configurable per-shop).

### Q6: What does the shop dashboard show? (sketch, not built)

Even sketched, this clarifies what to TRACK from day one:

- **Balance** (current $ remaining)
- **Clicks this week** (billable + non-billable broken out)
- **Clicks this month**
- **Last 20 clicks** (timestamp + action type only — no PII, no IPs to the shop)
- **Conversion estimate** ("of your 47 clicks, 12 were 'call' clicks → likely 3–4 real leads")
- **Top-up button** ($25 / $50 / $100 / custom)
- **Pause listing toggle** (for shops temporarily closed)
- **Edit listing** (re-opens signup form, changes go through review again)
- **Dispute a click** (button next to each click in the log)

**Key implication for Phase A:** the Google Sheet tracking each shop's balance needs columns matching this. So when Phase B ports it to a real DB, the data model is already proven.

### Q7: Anti-fraud at design time

Decisions baked into the click-event spec above plus:

1. **Exclude Khalil's IP / device entirely** — every click from Khalil's known IPs is a non-event, period.
2. **Exclude shop owner's IP** — captured at signup (last login IP for the shop's email used in the form), all clicks from that IP excluded for that shop's listing.
3. **Bot UA blocklist** — known bot user-agents (Googlebot, Bingbot, AhrefsBot, etc.) never fire a billable event. Their clicks ARE logged separately for analytics but don't deduct balance.
4. **24h dedupe per IP+shop** — same IP clicking same shop within 24h = max 1 billable event.
5. **Daily cap per shop** — configurable, default 10/day. Stops a single bad actor or referrer storm draining a balance.
6. **Dispute window** — 7 days. Shop flags suspicious clicks via dashboard; Khalil reviews logs + IPs + UAs, credits back if legit.

### Q8: Disclosure language placement

**Decision (proposed):** Three layers, descending prominence:

1. **Above the "Listed shops" section header on each city page:** one line, plain English. "These shops pay to appear here. We don't vet them. Listings are not endorsements." Always visible, no scroll-to-read.
2. **On each shop card:** small "Listed shop" label (NOT verified / recommended / sponsored — those terms either over-claim or under-disclose).
3. **In the global footer disclosure** (already exists for affiliates): extend to mention paid listings. "RepairRange features both editorial content and paid shop listings; paid listings are clearly labelled and we don't vet them."

This is over-disclosure on purpose. Under-disclosure is the ACCC risk; over-disclosure costs nothing.

### Q9: Shop exit path

**Decision (proposed):**
- **Edit listing:** anytime, goes through re-approval (Phase A: email Khalil; Phase B: form → admin review; Phase C: self-service).
- **Pause listing:** anytime, takes effect immediately, balance preserved.
- **Remove listing:** anytime. Remaining balance refunded to original payment method minus a $5 admin fee (covers Stripe fees + Khalil's time on Phase A bank-transfer reversal).
- **No refund on consumed clicks** — that's the deal, baked into terms.
- **Dispute log retained** for 12 months after exit (in case of follow-up complaints).

### Q10: How does a consumer know listings are paid?

Answered by Q8's three-layer disclosure. Worth restating: the *consumer-facing* disclosure is the line above the "Listed shops" section, in plain English. A reader doesn't need to read terms or hover a tooltip to learn the listings are paid — it's stated right there before they see any listing.

---

## 2. What we build, in what order

### Step 1 (this session or next — no live impact, safe)
- [x] This design doc, committed to repo (this file)
- [ ] A `/admin/` folder design — placeholder for future admin pages. Not deployed yet (folder won't deploy unless added to `.gitlab-ci.yml` — DO NOT add it). Empty folder reserved.
- [ ] Add `data-shop-id` / `data-shop-action` attribute spec to this doc (DONE above in Q5)

### Step 2 (build static prototype — next session, ~1–2 hrs)
- [ ] `directory/signup.html` — the shop signup form. Posts to a Formspree-style endpoint. Captures all MVP fields from Q2. Lives in a new `directory/` folder that will need adding to the CI script when ready to deploy.
- [ ] `directory/thanks.html` — confirmation page from Q4.
- [ ] `directory/terms.html` — shop terms (separate from site Terms of Use): pay-per-click model, daily cap, dispute window, refund policy, our right to remove listings.
- [ ] A sample shop card component (just visual, on `directory/signup.html` as a "this is how your listing will look") so a shop signing up can see what they're getting.
- [ ] Add `directory/` folder to `.gitlab-ci.yml` ONLY when the signup form is genuinely ready to receive submissions.

### Step 3 (city pages get a "Listed shops" section — next session after Step 2)
- [ ] Add the section to `locations/sydney.html` first, as a single empty placeholder reading "Listed shops launching soon. Are you a Sydney phone repair shop? [Get listed]" with a link to `directory/signup.html`. Use it to drive early signups.
- [ ] Replicate to Melbourne, Brisbane, Perth — same placeholder pattern.
- [ ] **Newcastle gets NONE of this.**

### Step 4 (Phase A goes live — only when Step 3's pages have measurable traffic)
- [ ] First shop emails Khalil. Khalil collects $10 via bank transfer. Manually creates a real shop card on the city page. Tracks clicks in Google Sheet.
- [ ] Repeat for 5–10 shops. Refine signup form based on what they ask.

### Step 5 (Phase B — code, only after Step 4 has earned real money)
Detailed plan deferred to when we get there. Per PROJECT.md §13.

---

## 3. Open questions / decisions deferred

These are flagged for future revision, not for this session:

1. **Pricing variation per city?** $1/click universal vs higher in Sydney (more traffic, more competition). DEFER until Phase B; flat $1 launches simpler.
2. **One slot per city vs unlimited?** Single featured slot = less revenue but cleaner UX + less internal competition between paying shops. Unlimited = more revenue, risk of cluttered section. **Tentative: unlimited (up to 6 visible cards initially), with rotation if more sign up than fit.** Revisit when there are >6 signups in any city.
3. **Stripe vs simpler payment.** For Phase A: bank transfer. For Phase B: Stripe with saved-card auto-topup. AU shops sometimes prefer EFT — keep that option open.
4. **GST treatment.** If Khalil's affiliate + directory revenue crosses the $75k AU GST threshold, GST applies to listing fees. Worth flagging to an accountant when revenue starts. Not relevant at launch.
5. **What if a shop the directory featured turns out bad (negative reviews / complaints from real customers)?** Drafted terms should reserve the right to remove a listing without refund on conduct grounds. Specifically: documented customer complaints, ABN cancellation, or evidence of fraud.
6. **Anti-competition concern (Mayfield-related):** can shops in NEWCASTLE buy a listing on the Sydney page? Technically yes, the city page is geographic. But shops outside the city look weird in a "Listed shops in Sydney" section. **Decision: ABN address must match the state of the city page** (NSW shops in Sydney section, VIC in Melbourne, etc.). Newcastle shops can't game by listing in Sydney.

---

## 4. What this doc explicitly does NOT cover (yet)

- Detailed Phase C self-service dashboard UX (deferred until Phase B earns enough to justify)
- Click-tracking endpoint implementation (Cloudflare Worker? Netlify Function? deferred to Phase B planning)
- Dispute review workflow specifics (deferred — define after first real dispute happens, not in advance)
- Shop login system (Phase C only)
- Email notifications (low-balance warnings, weekly click reports, etc.) — Phase C
- Analytics for Khalil (revenue dashboards, top-converting city/shop, etc.) — Phase B-minus

---

## 5. Change log

- **2026-05-XX (initial):** doc created in design phase. Decisions in §1 are proposed, not final — revise as Khalil reacts to each.
