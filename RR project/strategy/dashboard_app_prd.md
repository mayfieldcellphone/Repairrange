# Product Requirements Document (PRD)
## RepairRange Standalone Lead Sourcing & CRM Dashboard App

* **Author:** RepairRange PM
* **Date:** Thursday, June 4, 2026
* **Status:** Draft / Proposal
* **Target Environment:** Standalone Local or Hosted Web App

---

## 1. Executive Summary & Problem Statement

### The Problem
Currently, the RepairRange lead sourcing and outreach system relies on raw CLI terminal commands (`python source_leads.py [City]`, `python check_inquiries.py`, `python send_daily_batch.py`). While highly functional and robust, this CLI-first approach has several friction points for long-term independent use:
1. **Lack of Visibility:** The user must open CSV and Markdown files manually to inspect leads, view sending statuses, or see pipeline performance.
2. **Data Manipulation Friction:** Updating lead statuses (e.g., from `Pending` to `Trial` or `Paid`) requires opening a spreadsheet editor or text editor, which can introduce formatting bugs or column shifts.
3. **Execution Overhead:** Running automated scripts requires terminal access, python environment familiarity, and manual command typing.

### The Solution
Build a **standalone, lightweight, independent web dashboard** that wraps the existing Python automation engine (`source_leads.py`, `check_inquiries.py`, `send_daily_batch.py`) into a beautiful, mouse-driven user interface. This turns the local scripts into an **all-in-one private SaaS tool** that can be run locally on a laptop or deployed securely to the web with zero server costs.

---

## 2. Standalone Tech Stack Evaluation

To ensure the app can be used completely independently and easily, we evaluate three primary architectures:

| Evaluation Criteria | Option A: Streamlit (Python) | Option B: Flask + HTML/JS | Option C: React + FastAPI (Modern SaaS) |
|---|---|---|---|
| **Development Speed** | 🚀 **Very Fast (1-2 days)** - No HTML/CSS/JS required. | 🟡 **Medium (3-5 days)** - Requires templates & manual JS. | 🔴 **Slow (1-2 weeks)** - Two separate repositories & builds. |
| **Integration with Scripts** | 🟢 **Direct** - Can import functions directly from our Python scripts. | 🟢 **Direct** - Standard Python backend import. | 🟡 **Indirect** - Requires API contract mapping & JSON parsing. |
| **User Interface** | 🟢 **Modern & Clean** - Beautiful built-in charts, tables, and sidebars. | 🟡 **Customizable but basic** - Requires styling from scratch. | 🟢 **Excellent/Production** - Full UI/UX customization. |
| **Portability/Hosting** | 🟢 **Zero-Cost** - Self-host locally with `streamlit run` or deploy to Streamlit Cloud. | 🟢 **Low-Cost** - Deploy to Render, Heroku, or Hostinger VPS. | 🟡 **Complex** - Dual hosting for frontend (Vercel) and backend. |
| **Recommendation** | 🏆 **Winner: Option A (Streamlit)** | Secondary Option (Flask) | Overkill for Private/Internal tool |

**Decision:** We recommend **Streamlit** for the RepairRange Dashboard because it lets us preserve 100% of our existing Python script logic, provides a spreadsheet-like data editor out of the box, and runs entirely locally or on a free cloud hosting tier.

---

## 3. Product Goals & Success Metrics

### Business Goals
* Onboard more Australian phone repair shops to city-specific pricing pages.
* Streamline lead acquisition and email outreach into a 10-minute daily routine.
* Maintain a local-first, zero-subscription cost infrastructure.

### Success Metrics
* **Outreach Velocity:** Time to source 10 new leads and send personalized emails reduced from 30 minutes (CLI) to <3 minutes (Dashboard).
* **Data Integrity:** Zero formatting or syntax corruption issues in the underlying `outreach_schedule_june_2026.csv` from manual entry errors.
* **Adoption Rate:** 100% of pipeline tracking and batch email execution managed directly through the dashboard.

---

## 4. User Stories & Jobs-to-be-Done (JTBD)

### Jobs-to-be-Done (JTBD)
> "When I want to grow RepairRange.io's directory with local shops, I want an intuitive visual tool that sources leads, runs email outreach, and tracks deal stages in one place, so that I can focus on partner relationships instead of managing technical scripts."

### Standard User Stories
1. **As a** RepairRange owner (Khalil),
   **I want to** enter an Australian city name in a text field and click a button,
   **So that** the system automatically scrapes search results and adds qualified leads to my list without touching the terminal.

2. **As a** business operator,
   **I want to** view my lead pipeline in a visual funnel chart,
   **So that** I instantly know my sourcing-to-conversion rates and estimated MRR.

3. **As a** salesperson,
   **I want to** edit lead statuses directly in a spreadsheet-like grid,
   **So that** I can easily update trials, paid subscribers, or bounces.

4. **As an** outreach manager,
   **I want to** see which email batches are scheduled for today and click "Send Batch,"
   **So that** I can control exactly when emails go out and review them beforehand.

---

## 5. MoSCoW Prioritization

### Must Have (Minimum Viable Product - MVP)
* **Pipeline Analytics Screen:** Visual conversion charts, total sourced count, sent count, trial count, and estimated MRR.
* **Interactive CRM Lead Table:** An editable data grid that loads [outreach_schedule_june_2026.csv](outreach_schedule_june_2026.csv) and saves changes instantly.
* **On-Demand Sourcing Panel:** A simple interface to run `source_leads.py` for any city on click, displaying real-time scraping progress.
* **Outreach Dispatcher:** An interface to preview and dispatch today's automated email batch (invoking `send_daily_batch.py`).

### Should Have
* **Lead Editor Drawer:** Click a lead in the table to open a detailed view where you can edit contact names, website URLs, and add custom notes.
* **Live Mailbox Sync:** A button to trigger `check_inquiries.py` to instantly pull recent signups/replies and update the dashboard.
* **Template Customizer:** An in-app editor to modify cold outreach email copy and automatically save template files.

### Could Have
* **Map View:** A geographic visualization of repair shops mapped across Australia's main cities.
* **Multi-user Authentication:** Password protection for the dashboard to allow external virtual assistants to log in.

### Won't Have (For this Phase)
* **Direct Payment Processing Integration:** We will not process listing payments directly inside the app; we keep the existing Stripe/PayPal billing links.

---

## 6. Detailed Functional Specifications & Page Layouts

The application will feature a **Sidebar Navigation Menu** with four distinct screens:

### Page 1: 📊 Pipeline Analytics (Home)
* **KPI Metric Cards:**
  * Sourced Leads (Total)
  * Active Trials (Count)
  * Paid Subscribers (Count)
  * Estimated MRR (AUD $)
* **Conversion Funnel Chart:** A bar chart showing the conversion rate at each step (Sourced -> Sent -> Trial -> Paid).
* **Activity Log Panel:** Displays the tail end of `outreach_log.txt` to show recent background actions.

### Page 2: 🗃️ CRM Lead Manager
* **Spreadsheet Grid:** Streamlit's native `st.data_editor` component displaying `outreach_schedule_june_2026.csv`.
  * Users can search, filter by city or status, sort by date, and directly edit fields.
  * Includes a "Save Changes" floating button to commit updates back to the CSV.
* **Lead Stage Transitions:** Dropdown cell editor for the `Status` column (`Pending`, `Sent`, `Trial`, `Paid`, `Bounced`, `Failed`).

### Page 3: 🛰️ Lead Sourcing Hub
* **City Sourcing Input:**
  * Text box: `Enter City Name (e.g. Newcastle, Wollongong)`
  * Button: `🔍 Start Sourcing Run`
* **Scraper Progress Console:** Displays a spinner and prints log progress outputs as it queries AOL and scans shop homepages for contact emails.
* **Results Table:** Shows newly added leads at the end of the execution.

### Page 4: ✉️ Outreach Dispatcher
* **Batch Schedulers:** Shows the count of emails scheduled for today's batch.
* **Preview Block:** Shows the exact subject line and body template that will be sent, auto-populating variables like `{Shop Name}` and `{City}` for a preview.
* **Sync Inbox:** Trigger button to run IMAP sync for `info@repairrange.io` and `info@repairbill.shop`.
* **Dispatch Button:** `🚀 Send Today's Batch Now` (invokes `send_daily_batch.py`).

---

## 7. System & Data Architecture

```text
       +------------------ User Browser (Streamlit Frontend) ------------------+
       |                                                                       |
       |  [Pipeline Analytics]  [CRM Lead Table]  [Sourcing Panel]  [Emailer]  |
       +-----------------------------------+-----------------------------------+
                                           |
                                           v
                         +-----------------+-----------------+
                         |      Streamlit Python Backend     |
                         +-----------------+-----------------+
                                           |
                    +----------------------+----------------------+
                    |                      |                      |
                    v                      v                      v
          +---------+---------+  +---------+---------+  +---------+---------+
          |  source_leads.py  |  | check_inquiries.py|  |send_daily_batch.py|
          +---------+---------+  +---------+---------+  +---------+---------+
                    |                      |                      |
                    |                      v                      |
                    +------------> [Local Lead Database] <--------+
                                   (outreach_schedule.csv)
```

---

## 8. Step-by-Step Implementation Roadmap

* **Step 1: Bootstrap App Structure** Create `app.py` with basic sidebar navigation and layout frames.
* **Step 2: Connect CRM Editor** Implement `st.data_editor` displaying our master lead CSV, including verification and saving safeguards.
* **Step 3: Integrate Sourcing Engine** Import `source_leads` functions into the sourcing screen, linking the button trigger to the live crawler.
* **Step 4: Connect Email & Sync** Import `send_daily_batch` and `check_inquiries` modules, creating button actions and live progress logs.
* **Step 5: Visual Polish & Charts** Implement Matplotlib or Altair metrics and funnel graphics on the homepage.
* **Step 6: Local Launch & Deployment** Set up a startup script (`run_dashboard.bat`) for easy double-click startup on Windows.

---

## 9. Compliance & Safety Verification
* **Local Security:** Because this dashboard runs locally or via private Streamlit instances, sensitive mailbox credentials remain safe in the local `.env` file and are never exposed.
* **User Data:** The database remains local-first, preventing external leaks or GDPR/ACCC violations.
