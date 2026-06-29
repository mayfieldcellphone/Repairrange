# HubSpot Free CRM Setup & Gmail Tracking Integration Guide

Follow this step-by-step guide to set up your HubSpot Free CRM account, connect your Gmail account (`support@selfrepairkit.com.au`), and enable real-time tracking for email opens and link clicks.

---

## Step 1: Create Your HubSpot Account
1. Visit [HubSpot Free CRM Registration](https://www.hubspot.com/products/crm) and click **"Get started free"**.
2. Create an account using your email or Google Auth for **`support@selfrepairkit.com.au`**.
3. Select your industry as **"Consumer Services"** or **"Retail"** (representing local repair services).
4. Name your company/account **"RepairRange"**.

---

## Step 2: Connect Your Gmail Inbox to HubSpot
Connecting your personal inbox allows HubSpot to automatically log outreach emails, track replies, and schedule meetings.

1. Inside HubSpot, click the **Settings Gear Icon ⚙️** in the top navigation bar.
2. In the left-hand sidebar, navigate to **CRM** ➔ **Meetings & Emails** ➔ **Email Integrations**.
3. Click the **"Connect personal inbox"** button.
4. Select **Gmail** as your provider.
5. Grant permissions for HubSpot to integrate with **`support@selfrepairkit.com.au`**.
6. Check the box to enable **"Inbox Automation"** (this automatically logs replies from repair shops).

---

## Step 3: Install the HubSpot Sales Chrome Extension
The HubSpot Sales Chrome Extension integrates directly inside your browser Gmail compose screen, giving you real-time pop-up notifications when an email is opened.

1. Go to the **Chrome Web Store** and search for **"HubSpot Sales"**.
2. Click **"Add to Chrome"** to install the extension.
3. Open Gmail (`mail.google.com`) and log in.
4. Click the HubSpot Extension icon in your extensions toolbar and log into your newly created HubSpot account.
5. In Gmail, when you click "Compose", you will now see two new checkboxes at the bottom:
   * **[x] Log:** Automatically saves a copy of the email in the CRM contact record.
   * **[x] Track:** Automatically tracks when they open the email or click a link.

---

## Step 4: Import Your RepairRange Leads
You can import all 25 verified Sydney and Melbourne leads directly into HubSpot.

1. Go to your local workspace directory and locate [outreach_schedule_june_2026.csv](../leads/outreach_schedule_june_2026.csv).
2. In HubSpot, navigate to the top bar: **CRM** ➔ **Contacts**.
3. In the upper right, click **"Import"** ➔ **"Start an import"** ➔ **"File from computer"** ➔ **"One file"** ➔ **"One object"** ➔ **"Contacts"**.
4. Upload your `outreach_schedule_june_2026.csv`.
5. Map the CSV columns to HubSpot properties:
   * `Shop Name` ➔ Map to **Company Name** (or Contact First Name/Last Name as default).
   * `City` ➔ Map to **City**.
   * `Email` ➔ Map to **Email**.
   * `Scheduled Date` ➔ Create a custom field (or ignore, as HubSpot tracks real-time dates).
6. Click **Finish Import**.

---

## Step 5: Customize Your Directory Sales Pipeline
HubSpot provides a visual Kanban board to track leads from cold outreach to paying listing subscribers.

1. In HubSpot, navigate to **Sales** ➔ **Deals**.
2. Click **"Board"** view.
3. Click the gear settings or pipeline editor to rename your stages as follows:
   * **Stage 1: Contacted (Cold Outreach)** - Leads that have been emailed.
   * **Stage 2: Engaged (Email Opened / Clicked)** - High-intent leads who opened your email or visited your landing page but haven't signed up.
   * **Stage 3: Active Trial (Month 1 - Free)** - Shops that successfully signed up on `list-your-shop.html`.
   * **Stage 4: Active Subscriber ($29/quarter)** - Shops that converted to paid listings.
   * **Stage 5: Closed Lost** - Shops that opted out or didn't respond.

---

## 📈 Leveraging Email Tracking for Sales Conversion
Once you connect Gmail and install the extension, HubSpot will notify you in real-time when an email is opened.

* **Trigger Signal:** A shop owner in Sydney opens your email 3-4 times over 2 days.
* **Interpretation:** They are highly interested and likely discussing listing with their technicians or looking at the budget, but are hesitating.
* **Actionable Play:** Send a highly personalized, friendly follow-up email (or give them a quick call if they listed a phone number on their site) offering to help them upload their listing manually. This high-touch, peer-to-peer approach is how you secure your first 15-20 trial customers!
