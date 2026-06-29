# CRM Recommendations for RepairRange.io Outreach

**Author:** RepairRange Product Manager  
**Date:** June 2, 2026  
**Status:** Completed  

This document evaluates the best free CRM platforms for RepairRange.io's cold email outreach campaign and subsequent sales pipeline management.

---

## 1. Core Requirements for RepairRange's CRM
For RepairRange to successfully onboard local mobile phone repair shops and convert them to paid listings ($29/quarter), the CRM must support:
1. **Gmail Integration:** Since outreach is sent from `support@selfrepairkit.com.au`, the CRM must automatically log sent emails, replies, and follow-ups.
2. **Email Tracking (Open & Click Alerts):** In cold outreach, knowing **who** opened your email and **who** clicked the link (`list-your-shop.html`) is vital. This reveals high-intent leads who are interested but haven't signed up yet.
3. **Visual Deal Pipeline:** Track shops as they progress through the funnel:  
   `Contacted` ➔ `Opened/Interested` ➔ `1-Month Free Trial` ➔ `Paid Quarterly Listing` ➔ `Closed Lost`.
4. **Cost:** MUST have a robust, "free forever" tier with no hidden fees for the initial setup.

---

## 2. Comparison of Top Free CRM Options

| Feature / Limit | HubSpot CRM (Free Plan) | Zoho CRM (Free Plan) | Custom Google Sheet / Local CRM |
| :--- | :--- | :--- | :--- |
| **Price** | Free Forever | Free Forever | Free Forever (Zero Cost) |
| **Contacts Limit** | Up to **1,000,000** contacts | Up to **10,000** records | Infinite |
| **Gmail Integration** | Perfect (Native 1-click Chrome Extension) | Good (SMTP/IMAP sync) | None (Manual logging) |
| **Email Tracking** | **Yes** (Real-time open & click notifications) | No (Requires paid upgrade for basic tracking) | No |
| **Deal Pipeline** | Yes (1 pipeline, highly customizable) | Yes (1 pipeline, basic customization) | Yes (Manual visual table) |
| **Ease of Use** | Extremely High (Modern, intuitive UI) | Moderate (Slightly steep learning curve) | Infinite (100% familiar) |

---

## 3. Deep-Dive Platform Analysis

### Option 1: HubSpot CRM (Free Tier) — *The Sourcing Champion*
HubSpot is widely recognized as the gold standard for free CRM software for startups and small business outreach.

* **Pros:**
  * **Gmail Chrome Extension:** Adds a sidebar directly into your Gmail inbox. You can check a box to "Track" and "Log" emails automatically.
  * **Real-time Notifications:** You get a browser popup the second a repair shop in Sydney opens your email or clicks your landing page link.
  * **Meeting Scheduler:** Includes a free scheduling link (like Calendly) that you can insert in emails so shop owners can book a short call with you.
* **Cons:**
  * Some customer-facing assets (like automated forms or chat widgets, if used) will have "HubSpot" branding. (Not an issue for cold outreach).
  * Upgrading to paid marketing tiers can be expensive (though the free tier is more than sufficient for your initial 500 contacts).

### Option 2: Zoho CRM (Free Tier)
Zoho is a highly customizable, enterprise-grade CRM that offers a solid free plan for small teams.

* **Pros:**
  * Highly customizable fields and modules.
  * Good security features and multiple user accounts (up to 3 users free).
* **Cons:**
  * Email open/click tracking is **not** included in the free tier; this is a critical disadvantage for cold outreach.
  * The user interface is clunky and takes significantly longer to set up and navigate.

### Option 3: Custom Google Sheet / Local Markdown Dashboard
A manual spreadsheet approach designed specifically for lean operations.

* **Pros:**
  * 100% private, zero external accounts needed.
  * Easy to bulk edit and integrate with Python automation scripts (such as the one we just wrote!).
* **Cons:**
  * No automatic email tracking (cannot see if they opened the email).
  * No automatic logging (must manually copy-paste replies into the spreadsheet).

---

## 4. Product Manager's Recommendation

**Recommendation: Implement a Hybrid CRM Strategy**

1. **Primary Tool: HubSpot CRM (Free Tier)**
   * **Why?** The ability to track email opens and link clicks is your **highest-leverage sales tool**. If a shop in Sydney opens your email 4 times but hasn't filled out the form, they are highly interested. This is a high-intent signal to follow up with a quick call or a personalized offer. The Gmail integration is seamless and requires zero developer time.
   
2. **Supporting Tool: Local Markdown Pipeline ([crm_dashboard.md](../leads/crm_dashboard.md))**
   * **Why?** Since our automated script runs locally and updates your CSV database, we can maintain a synchronized, text-based dashboard inside your workspace. This gives you a fast, zero-loading-time visual overview of your campaign's progress right inside your project directory.
