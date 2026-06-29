# PRD: HubSpot Form Integration & Embed Guide for RepairRange.io

**Author:** RepairRange Product Manager  
**Date:** June 3, 2026  
**Status:** Ready for Implementation  
**Target Page:** `https://www.repairrange.io/list-your-shop.html`

---

## 1. Executive Summary & Objectives
To solve the "cold-start" problem of onboarding Australian mobile phone repair shops onto RepairRange.io, we need a high-converting, friction-free registration form. Since HubSpot Free CRM is our recommended tool for lead tracking and sales pipeline management, we will utilize **HubSpot Free Forms**. 

Because we do not have direct API credentials or automated access to HubSpot's secure cloud interface, this document serves as the complete **Form Specification, Mapping Plan, and Website Embedding Guide** so that you can create the form in HubSpot in 2 minutes and integrate it seamlessly into `list-your-shop.html`.

### 1.1 Success Metrics & Measurement Plan
| Metric | Target | Measurement Plan |
| :--- | :--- | :--- |
| **Form Completion Rate** | > 15% (of visitors to `/list-your-shop.html`) | HubSpot Forms Dashboard + Google Analytics 4 (GA4) custom event. |
| **CRM Contact Accuracy** | 100% of submissions automatically mapped | Audit CRM contacts after first 10 submissions. |
| **Pipeline Deal Creation** | Auto-creation of "Deal" in "Active Trial" stage | HubSpot workflow trigger (Free tier manual check or Zapier). |

---

## 2. Jobs-to-be-Done (JTBD) & User Stories
### 2.1 Job Story
* **Situation:** When I visit RepairRange's onboarding page as an interested local phone repair shop owner,
* **Motivation:** I want to submit my business details quickly without complex account registration or payment gateways,
* **Outcome:** So that I can activate my 30-day free trial listing and test the traffic with zero risk.

### 2.2 User Stories
* **Story 1 (Frictionless Onboarding):** As a busy technician & shop owner, I want the form to require only essential contact and business details, so that I can submit it in under 60 seconds on my phone or computer.
* **Story 2 (Plan Clarity):** As a cost-conscious business owner, I want to clearly select my preferred listing plan and see the pricing transparently, so that I know what happens after my 30-day free trial ends.

---

## 3. Form Specification & CRM Mapping
To ensure that all submissions flow perfectly into HubSpot without manual data entry, the form fields must be mapped directly to HubSpot **Standard Contact & Company Properties** or defined as **Custom Properties**.

### 3.1 Field Prioritization (MoSCoW Framework)
* **Must Have:** Shop Name, Contact Name, Business Email, Shop Phone, City (Australia), Preferred Plan.
* **Should Have:** Website URL, Street Address (for map listing).
* **Could Have:** Business Tagline (Featured Tier), Operating Hours.
* **Won't Have:** Credit Card details (payments are processed via Stripe billing links *after* the 30-day trial).

### 3.2 Property Mapping Table
| Form Label | Field Type | HubSpot CRM Property Name | Requirement | Options / Fallbacks |
| :--- | :--- | :--- | :--- | :--- |
| **Shop Name** | Single-line text | `company` (Company Name) | **Required** | Text input |
| **Contact Name** | Single-line text | `firstname` (First Name) | **Required** | Text input (maps to First Name) |
| **Business Email** | Email address | `email` (Email) | **Required** | Must be a valid email format |
| **Shop Phone Number** | Phone number | `phone` (Phone Number) | **Required** | Mobile or landline |
| **City** | Dropdown | `city` (City) | **Required** | Sydney, Melbourne, Brisbane, Perth, Adelaide, Hobart, Newcastle, Wollongong, Gold Coast, Canberra, Darwin, Geelong, Other |
| **Street Address** | Single-line text | `address` (Street Address) | Optional | e.g. "276 Maitland Rd, Mayfield NSW" |
| **Website URL** | URL | `website` (Website URL) | Optional | Must start with `http://` or `https://` |
| **Select Listing Plan** | Dropdown (Custom) | `listing_plan` (Custom Dropdown) | **Required** | • Starter ($29 AUD / 3 months)<br>• Verified ($49 AUD / 6 months)<br>• Featured ($89 AUD / 12 months) |
| **Shop Tagline / Notes** | Multi-line text | `message` (Message/Notes) | Optional | Textarea for custom specialties or notes |

---

## 4. Step-by-Step HubSpot Form Creation Guide
Follow these steps inside your HubSpot account to build this form:

1. **Log in to HubSpot:** Go to [HubSpot Portal](https://app.hubspot.com/).
2. **Navigate to Forms:** In the top navigation bar, go to **Marketing** ➔ **Lead Capture** ➔ **Forms**.
3. **Create Form:** Click the **"Create form"** button (top right).
4. **Select Type:** Choose **"Embedded form"** and click **Next**.
5. **Start Blank:** Choose **"Blank template"** (this allows us to style it using CSS on RepairRange.io) and click **Start**.
6. **Drag & Drop Fields:**
   * Drag standard HubSpot fields into the builder: `First Name` (rename label to *Contact Name*), `Email`, `Phone Number`, `Company Name` (rename label to *Shop Name*), `City`, `Street Address`, `Website URL`, and `Message` (rename label to *Shop Tagline / Special Requests*).
   * **Create Custom Field for Plan Selection:**
     * Click **"Create new field"** at the bottom left.
     * Object type: **Contact**.
     * Field type: **Dropdown select**.
     * Label: **Preferred Plan**.
     * Internal name: `listing_plan`.
     * Add three options:
       * `Starter ($29 AUD / 3 months after trial)`
       * `Verified ($49 AUD / 6 months after trial)`
       * `Featured ($89 AUD / 12 months after trial)`
     * Click **Save** and drag it onto the form.
7. **Configure Form Options:**
   * Go to the **Options** tab at the top.
   * **What should happen after a visitor submits this form?**
     * Select **"Display a thank you message"** or **"Redirect to another page"** (recommended redirect to `https://www.repairrange.io/thank-you.html`).
   * **Pre-populate fields with known values:** Set to **Enabled** (makes it easier for return visitors).
8. **Style & Preview:**
   * Go to **Style & Preview**. Keep styles "Unstyled" or "Raw" so your site's custom stylesheet handles colors, fonts, and buttons.
9. **Publish & Grab Embed Code:**
   * Click the **"Publish"** button in the top right.
   * A modal will pop up with your unique **Javascript Embed Code**. Copy this code (it will look like the code block in Section 5).

---

## 5. Website Embedding Code Template
Once you publish your form, HubSpot provides a JavaScript snippet. Below is the styled embedding template. Place this code directly into your `list-your-shop.html` file inside the form container element:

```html
<!-- HubSpot Form Container -->
<div class="repairrange-form-wrapper">
  <!-- Customize the header to match RepairRange branding -->
  <h2 class="form-title">List Your Shop & Claim Your 30-Day Free Trial</h2>
  <p class="form-subtitle">Join Australia's peer-to-peer independent repair pricing guide. No commissions, no risk.</p>

  <!-- HubSpot Javascript Embed Code -->
  <!-- Note: Replace YOUR_PORTAL_ID and YOUR_FORM_ID with the exact values from your HubSpot dashboard -->
  <script charset="utf-8" type="text/javascript" src="//js.hsforms.net/forms/embed/v2.js"></script>
  <script>
    hbspt.forms.create({
      region: "na1",
      portalId: "YOUR_PORTAL_ID", // Replace with your actual Portal ID
      formId: "YOUR_FORM_ID",     // Replace with your actual Form ID
      target: "#hubspot-form-target", // CSS Selector where the form will render
      css: "" // Keeps it unstyled so our CSS below takes effect
    });
  </script>
  
  <div id="hubspot-form-target"></div>
</div>

<!-- Styling to match RepairRange Brand Guidelines (Teal & Amber) -->
<style>
  .repairrange-form-wrapper {
    background-color: #0F766E; /* Brand Teal */
    color: #FFFFFF;
    padding: 40px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    max-width: 600px;
    margin: 40px auto;
    font-family: 'Helvetica Neue', Arial, sans-serif;
  }
  .form-title {
    color: #F59E0B; /* Brand Amber */
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 10px;
    text-align: center;
  }
  .form-subtitle {
    font-size: 15px;
    line-height: 1.5;
    margin-bottom: 30px;
    text-align: center;
    color: #E2E8F0;
  }
  /* HubSpot Iframe Overrides (applied when HubSpot CSS is loaded) */
  #hubspot-form-target iframe {
    width: 100% !important;
    border: none !important;
  }
</style>
```

---

## 6. Post-Submission Pipeline Strategy
To maximize trial-to-paid conversions and build peer-to-peer relationships with new signups, we recommend establishing this automated sequence:

1. **Auto-Create Contact & Deal:** 
   * When the form is submitted, HubSpot automatically creates a Contact record.
   * If using HubSpot Starter/Professional, set up an automatic workflow to create a Deal in the **Active Trial (Month 1 - Free)** pipeline stage.
   * *If using HubSpot Free:* Check your HubSpot Forms inbox once a day and manually create the Deal to keep your [crm_dashboard.md](../leads/crm_dashboard.md) synchronized.
2. **First Touch-point (Email at Day 1):**
   * Send a manual, friendly thank-you email from `info@repairrange.io` confirming their listing is being prepared. 
   * "Hi [First Name], Khalil here from RepairRange. I just saw your submission for [Shop Name] in [City]. I'm setting up your city-page card right now and will email you the link once it's live."
3. **Mid-Trial Check-in (Day 15):**
   * Email them to share their current page impressions and click stats.
4. **Billing Transition (Day 25):**
   * Send the Stripe payment link for their selected plan (`Starter: $29/3m`, `Verified: $49/6m`, `Featured: $89/12m`).
   * "If you've loved the visibility, click here to transition to our flat-rate plan and keep your spot active."
