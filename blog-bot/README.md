# blog-bot

Scheduled blog generation for RepairRange, SelfRepairKit, PDFRange and Mayfield Gadgets.

---

## Read this first

**Claude cannot schedule anything.** No background execution, no persistence between
chats. If an assistant says "scheduled ✅", nothing happened — same failure mode as
Accio reporting done on work it never did.

The only things on your stack that run on a timer without a human are:

- **GitLab pipeline schedules** (RepairRange already uses one for `generate_news`)
- **Any external cron** you point at the LaunchMyStore API

So this repo is a CI job. You create the schedule in the GitLab UI. After that it runs
on its own, forever, and emails you.

---

## The honest bit about auto-publishing

You asked for auto-create **and auto-publish**. I've set `"autopublish": false` on all
four sites, and you should think hard before flipping it.

Four domains × 1–2 unreviewed AI posts a week is roughly 400 machine-written pages a
year across a network that shares an owner, a hosting pattern, and interlinks. That is
a textbook match for Google's **scaled content abuse** policy — the enforcement is
site-wide, not page-level, and it would take RepairRange down with it. RepairRange
currently has **zero backlinks** and is fighting for its first rankings. It cannot
absorb a manual action.

The setup as shipped: bot generates → validates → saves as draft → emails you the URL.
You skim and approve. Costs you five minutes a week and removes the entire risk class.

If you want auto-publish anyway, flip one flag per site in `config/sites.json`. My
suggestion: run drafts for six weeks, and if the drafts are consistently good enough to
approve unread, *then* turn it on for **one** site — PDFRange, since it has the least to
lose. Never RepairRange.

Your call. The switch is right there.

---

## What's in here

```
blog-bot/
  generate.py                     the whole engine
  notify.py                       gmail SMTP email
  config/sites.json               per-site brand, voice, guardrails, autopublish flag
  topics/<site>.txt               topic queue, consumed top-down (15 each = ~4 months)
  topics/<site>_used.txt          written automatically, your audit trail
  templates/repairrange.html      static-CSS post template
  templates/pdfrange.html         static-CSS post template
  ci/.gitlab-ci.blog-bot.yml      the CI job + schedule instructions
```

The templates ship **static CSS, no Tailwind CDN** — so every new blog post is already
on the right side of your pending RepairRange CSS fix instead of adding to the debt.

---

## Guardrails (tested, not claimed)

`generate.py` refuses to publish a draft that breaks any of these. It retries the model
up to 3× with the failures fed back, then hard-fails the job rather than shipping
something bad:

| Rule | Sites | Status |
|---|---|---|
| **No invented prices** — any `$`, `AUD`, "dollars" | RR, SRK, MG | tested, blocks |
| **No quantified CO2 / e-waste claims** | MG | tested, blocks |
| **Max one link to mayfieldphonerepair.com.au** (PBN hygiene) | all | tested, blocks |
| No AI slop phrases ("delve", "in today's world", "game-changer") | all | tested, blocks |
| 700–1600 words, meta 110–160 chars, ≥1 internal link, ≤4 total links | all | tested, blocks |
| No fabricated stats/studies/sources | all | prompt-level |

The price rule is deliberately blunt. A blog post about repair costs that never names a
price sounds constraining — it's actually your differentiator, because it forces every
cost conversation to end at the calculator, which is the page you want ranking.

---

## Setup

**1. Copy `blog-bot/` into the RepairRange repo and the PDFRange repo.**

**2. Merge `ci/.gitlab-ci.blog-bot.yml` into each repo's existing `.gitlab-ci.yml`.**
Merge, don't replace — RepairRange's `generate_news` and `pages` stages must survive.

**3. Add CI variables** (Settings → CI/CD → Variables, masked + protected):

| Variable | Value |
|---|---|
| `GEMINI_API_KEY` | already set on RepairRange; copy to PDFRange |
| `SMTP_USER` | the gmail address that sends |
| `SMTP_PASS` | gmail **app password** — Google Account → Security → 2-Step → App passwords. Not your login password. |
| `NOTIFY_TO` | `engrkhalil77@gmail.com` |
| `GITLAB_PUSH_TOKEN` | project access token, scope `write_repository` |

**4. Dry run before you schedule anything.** Build → Run pipeline → set `SITE_KEY` →
play `blog_bot_dryrun`. Read the output. If the post is rubbish, fix the `voice` line in
`config/sites.json` and run again. Do not schedule until a dry run produces something
you'd sign your name to.

**5. Create the schedules** (Build → Pipeline schedules → New schedule).
GitLab cron is **UTC**. AEST is UTC+10:

| Repo | Name | Cron (UTC) | Variable | Fires |
|---|---|---|---|---|
| RepairRange | RepairRange Tue | `0 20 * * 1` | `SITE_KEY=repairrange` | Tue 06:00 AEST |
| RepairRange | RepairRange Fri | `0 20 * * 4` | `SITE_KEY=repairrange` | Fri 06:00 AEST |
| PDFRange | PDFRange Thu | `0 20 * * 3` | `SITE_KEY=pdfrange` | Thu 06:00 AEST |

**6. Verify the first run in Gitpage.** These repos are Gitpage-synced and direct GitLab
pushes have caused sync conflicts before. Confirm post #1 renders live before you trust
the schedule. And remember `generate_sitemap` / `robots_txt` / `llms_txt` **overwrite**
CI output — don't run them casually.

---

## The two LaunchMyStore sites — the open blocker

SelfRepairKit and Mayfield Gadgets are **not git repos**, so there's no CI to hang a
schedule on. `publish_lms()` is written and ready, but it needs an `LMS_API_TOKEN` —
a standing REST token, not the MCP one (MCP binds its token at auth time, which is
useless to a cron).

Three ways forward, pick one:

1. **Get a LaunchMyStore API token.** Then run `blog-bot` from any scheduler that can
   hit the internet — a GitLab schedule in the RepairRange repo works fine, it doesn't
   care that the target is a different platform. Add `SITE_KEY=selfrepairkit`. Done.
   *You should confirm the endpoint — I've assumed `POST /v1/blogs`, which may be wrong.*
2. **Cheap hack:** put the two stores' posts on a GitLab schedule that generates the
   HTML and emails it to you, and you paste into LaunchMyStore. Ugly, 3 min/week.
3. **Sessions with me.** I can write and post them via MCP whenever you open a chat.
   Not scheduled — you'd be the scheduler.

Option 1 is the real answer. Everything else is you doing a robot's job.

---

## SEO plan per site

The automation is plumbing. This is the actual strategy.

### RepairRange.io — 2/week (Tue, Fri)
Editorial only. Tech news stays on `tech-news.html`.
**Job of the blog:** capture the decision-stage queries your model and city pages can't
— "should I repair or replace", "why is my quote different", "will third-party repair
void my warranty". Every post funnels to `calculator.html` or `compare.html`.
**Reality check:** blogs will not fix RepairRange. Zero backlinks is the binding
constraint. 100 posts × 0 links = 0 rankings. The blog's real job here is being
*linkable* — that's why the topics are opinion-led ("The hidden cost of a cheap screen
repair") rather than another how-to nobody cites. Publishing without a link-building
push in parallel is motion, not progress.

### SelfRepairKit.com.au — 1/week (Wed)
**Job:** bottom-funnel capture. "iPhone 13 battery replacement guide" ranks, converts to
a kit sale on the same page. 297 products means 297 potential guides — this queue is
seeded with the highest-volume ones.
**Do first:** the malformed iPhone 13 Battery record and the 22 quarantined Samsung
S-series products. A guide that links to a broken or missing product page is a wasted
post. Fix the catalogue, then start the schedule.

### PDFRange.com — 1/week (Thu)
**Job:** feed the ebook funnel. Every post ends at the lead magnet or `library.html`,
Omnisend picks them up from there. This is the only site where the blog is a genuine
acquisition channel rather than a support act, because "is X safe to upload" is a real
query with real intent and almost no good answers.
**The only site I'd consider auto-publishing on** once the drafts prove out.

### MayfieldGadgets.com.au — 1/week (Mon)
**Job:** comparison and reassurance content for people who are 80% sold on refurbished
and want permission. "iPhone 13 or 14 in 2026", "what Grade A actually means".
**Hard constraint baked in:** no quantified environmental claims, ever. You already
pulled the homepage sustainability block over a CO2 claim — the validator now makes that
mistake structurally impossible rather than relying on someone remembering.
**Do first:** the duplicate iPhone 13 records and the +$15/+$45 battery upsell text
across 44 CrazyParts products. Same logic as SelfRepairKit — don't drive traffic at a
catalogue that's still wrong.

### Sequencing, if you want my honest read
Start **PDFRange only**. One site, one schedule, four weeks. It has the cleanest
catalogue (no products to break), the clearest funnel, and the least to lose if the
output is mediocre. Get that loop working end to end — generate, email, approve, publish,
watch Search Console — then clone the pattern outward. Turning on four schedules at once
across two platforms with two unfixed catalogues is how you end up with 30 draft emails
you never read and four sites of mediocre content.

---

## Running it locally

```bash
export GEMINI_API_KEY=...
python blog-bot/generate.py --site repairrange --dry-run
```

Exit codes: `0` ok · `1` config/topic error · `2` failed validation 3× · `3` publish failed.
A non-zero exit means **nothing was published** — the job fails loudly rather than
shipping something that broke a rule.

## Refilling topics

When `topics/<site>.txt` runs dry the job exits 1 and emails nothing. Each queue holds
~15 topics = ~4 months at 1/week. Set a calendar reminder, or ask me to generate the
next batch from Search Console data once you have ranking data to work from.
