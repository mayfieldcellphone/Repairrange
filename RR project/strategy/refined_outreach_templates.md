# RepairRange Email Outreach Templates & Personalization Strategy

This document outlines the refined outreach email templates and the personalization mapping logic for the RepairRange.io campaign. It details how to handle missing data fields (such as first names) and provides variants for A/B testing.

---

## 1. Personalization & Fallback Logic

Since our lead database (`outreach_database_june.csv`) contains `Shop Name` and `City` but does **not** contain a `First Name` column, we must use a dynamic fallback strategy for the greeting to ensure a professional and natural tone.

| Field in Template | Source CSV Column | Fallback Value if Blank/Missing | Description |
| :--- | :--- | :--- | :--- |
| `[Shop Name]` | `Shop Name` | *Required field* (Skip lead if missing) | The name of the repair shop. |
| `[City]` | `City` | *Required field* (Skip lead if missing) | The localized city (e.g., Sydney, Melbourne). |
| `[First Name]` | *(None)* | **`[Shop Name] Team`** or **`there`** | Since first names are missing, we use **"Hi [Shop Name] Team,"** as it is polite, business-specific, and highly professional. |

---

## 2. Refined Email Templates (A/B Testing Variants)

Here are three high-converting email templates optimized for the mobile phone repair industry.

### Variant A: The Refined Original (Recommended Default)
*This is an optimized version of your original template. It uses the `[Shop Name] Team` fallback for personalization and sharpens the value proposition.*

- **Subject:** Free listing on RepairRange.io — [City] repair pricing guide
- **Body:**
  ```text
  Hi [Shop Name] Team,

  I run RepairRange.io — an independent phone repair pricing guide covering [City]. We're currently adding verified local shop listings, and I'd love to include [Shop Name].

  Your first month is completely free — you can view our plans and apply directly here:
  👉 https://www.repairrange.io/list-your-shop.html

  What you get: Your shop featured prominently on our [City] pricing page, putting you directly in front of local customers actively searching for repair costs. There are no commissions and no per-click charges — just a simple, flat listing fee starting at $29/quarter.

  Best regards,

  Khalil
  RepairRange / Mayfield Phone Repair, Newcastle
  ```

---

### Variant B: Peer-to-Peer Connection (High Trust)
*This variant leverages the fact that you also run a physical shop (Mayfield Phone Repair). Repairers trust other repairers more than anonymous tech platforms. This angle establishes instant credibility.*

- **Subject:** Peer invitation: Listing [Shop Name] on RepairRange ([City])
- **Body:**
  ```text
  Hi [Shop Name] Team,

  My name is Khalil, and I run Mayfield Phone Repair in Newcastle. Like you, I know how hard it is to get local repair customers without paying crazy per-click ad costs or high lead-gen commissions.

  To solve this, I built RepairRange.io — an independent phone repair pricing guide for [City]. We help local customers estimate repair costs and connect them directly with verified shops like yours.

  I'd like to invite [Shop Name] to join as a verified partner. Your first month is free, and we don't charge commissions or click fees. If you like the results, it's just a flat $29/quarter to stay listed.

  You can check out our listings and secure your spot here:
  👉 https://www.repairrange.io/list-your-shop.html

  Let me know if you have any questions — from one shop owner to another!

  Cheers,

  Khalil
  RepairRange / Mayfield Phone Repair, Newcastle
  ```

---

### Variant C: ROI & Lead Acquisition Focus (Direct & Business-Centric)
*This variant focuses heavily on business value, search intent, and the flat pricing model. Best for highly competitive shops in central business districts.*

- **Subject:** Get [City] repair customers on RepairRange.io — Free month for [Shop Name]
- **Body:**
  ```text
  Hi [Shop Name] Team,

  When customers in [City] search for phone repair prices, where do they go? 

  We built RepairRange.io to capture that search traffic and send high-intent customers straight to verified local shops. We're currently expanding our [City] coverage and would love to list [Shop Name].

  We are offering you a 1-month free trial to test the platform. There are no setup fees, no commissions, and no pay-per-click charges. After your free month, listings are a flat $29/quarter.

  See how it works and claim your free listing here:
  👉 https://www.repairrange.io/list-your-shop.html

  Position your shop in front of customers who are ready to book a repair today.

  Best regards,

  Khalil
  RepairRange / Mayfield Phone Repair, Newcastle
  ```

---

## 3. Analysis of Copywriting Tweaks & Why They Work

1. **"Hi [Shop Name] Team" over "Hi [First Name]"**: Addresses the entire shop professionally without risking incorrect name-guessing or sounding weirdly generic (like "Hi Friend").
2. **"completely free" / "no commissions"**: Emphasizes that there is zero risk to try.
3. **PEER-TO-PEER CREDIBILITY**: Mentioning Mayfield Phone Repair is your strongest asset. It removes the "spamy software salesperson" vibe and replaces it with "fellow local business owner building a practical utility."
4. **Transparent $29/quarter fee**: Mobile shops are heavily burned by ad agencies charging hundreds of dollars. Laying out a flat, ultra-low price ($29/quarter, which is less than $10/month) reduces skepticism immediately.
