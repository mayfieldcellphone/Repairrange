# Product Requirements Document (PRD): RepairRange Shop Outreach Campaign

**Author:** RepairRange Product Manager  
**Date:** June 2, 2026  
**Status:** Ready for Review  
**Target Launch:** August 2026 (Sydney & Melbourne Pilot)

---

## 1. Problem Statement & Executive Summary

### 1.1 The Problem
For a directory and pricing guide like **RepairRange.io** to be valuable to end consumers, it must feature a robust list of verified, highly-rated local mobile phone repair shops. However, as a new platform, RepairRange faces a cold-start problem:
1. **Shops** do not know about RepairRange and are skeptical of advertising/directory spam.
2. **Shops** are highly price-sensitive and frequently burned by complex CPC (cost-per-click) or commission-based advertising models.
3. **RepairRange** needs to onboard its first 20-50 high-quality shops in Sydney and Melbourne to validate the directory product and prove consumer referral value.

### 1.2 The Solution
Launch a highly personalized, cold email outreach campaign targeting 4.5+ star rated shops in Sydney and Melbourne. By leveraging a **peer-to-peer (shop-owner to shop-owner)** connection, a **1-month free trial**, and an ultra-low, flat-rate **$29/quarter listing fee**, we can bypass traditional B2B sales skepticism and accelerate onboarding.

---

## 2. Goals & Success Metrics

### 2.1 Primary Business Goals
- Onboard **10-15%** of contacted verified shops to the 1-month free trial.
- Convert **30-50%** of trial shops into paying subscribers ($29/quarter) after Month 1.
- Establish a scalable outreach playbook for Tier 2 cities in Australia.

### 2.2 Key Performance Indicators (KPIs) & Success Metrics

| Metric | Target | Measurement Plan |
| :--- | :--- | :--- |
| **Email Deliverability (Deliverability Rate)** | > 97% | Track bounces using Gmail/mailer-daemon notifications. |
| **Open Rate** | > 45% | Subject line effectiveness. Tracked via unique clicks / replies. |
| **Click-Through Rate (CTR) to landing page** | > 15% | Percentage of opened emails that click the link. |
| **Conversion Rate (Trial Sign-Up)** | > 5% of total sent | Form submissions on `list-your-shop.html`. |
| **Paid Conversion Rate (Post-Trial)** | > 30% | Number of trials converting to paid billing at Day 30. |

---

## 3. User & Job Stories

We use the **Jobs-to-be-Done (JTBD)** and **User Story** frameworks to understand our target users (repair shop owners).

### 3.1 Job Stories (JTBD)
- **Situation:** When my repair shop has quiet weekdays and unused technician capacity,
- **Motivation:** I want to find low-risk, high-intent local customer lead channels,
- **Outcome:** So that I can increase booking volume and grow revenue without wasting money on expensive Google Ads.

### 3.2 User Stories

#### Story 1: Peer Trust & Simplicity
> **As a** highly-rated phone repair shop owner,  
> **I want** to hear from fellow industry peers who understand my daily business struggles,  
> **So that** I don't feel like I'm being sold a useless, overpriced marketing package by a generic agency.

#### Story 2: Low-Risk Testing
> **As a** budget-conscious local business owner,  
> **I want** a friction-free, risk-free trial listing with no commissions or complex click charges,  
> **So that** I can test the listing's real-world ROI before committing any marketing spend.

#### Story 3: Transparent, Flat-Rate Pricing
> **As a** repair shop owner who hates fluctuating monthly costs,  
> **I want** a simple, predictable, flat quarterly fee ($29/quarter),  
> **So that** I can easily calculate my customer acquisition cost and keep overhead low.

---

## 4. MoSCoW Prioritization of Campaign Features

To execute a lean and effective outreach pilot, we prioritize campaign elements as follows:

### 4.1 Must Have (Minimum Viable Campaign)
- **Local personalization fallbacks:** Dynamically substitute `[City]` and `[Shop Name]` (with `[Shop Name] Team` as the greeting fallback).
- **Direct Link to Landing Page:** Explicit inclusion of `https://www.repairrange.io/list-your-shop.html`.
- **Peer-to-Peer Positioning:** Highlighting the sender's industry background ("Mayfield Phone Repair, Newcastle").
- **Delivery Status Verification:** Immediate automated tracking of bounced emails to maintain sender domain health.
- **Trial Offer:** Clear terms of the 1-month free trial followed by the transparent $29/quarter flat fee.

### 4.2 Should Have (Enhancements for Conversion)
- **A/B Testing (Subject & Body):** Ability to rotate between Variant A (Original Optimized) and Variant B (Peer Connection) to optimize open and click rates.
- **Pre-outreach Lead Verification:** Manual verification of lead emails to ensure we do not send to generic form/incomplete addresses (already filtered in `outreach_database_june.csv`).
- **Follow-up Sequence Plan:** A secondary follow-up email sent 5 days later to non-responders.

### 4.3 Could Have (Nice to Have)
- **Direct Booking Link Integration:** Enabling shops to embed their own booking link directly on their listing card.
- **Specific Suburb Localization:** Mentioning their actual suburb/street instead of just the broad `[City]` (e.g., "Bondi Junction" or "CBD").

### 4.4 Won't Have (Deferred for Future Phases)
- **Automated CRM Integration:** Full automation with Salesforce/HubSpot (manual Google Sheets/CSV tracking is sufficient for pilot).
- **Affiliate/Referral Payouts:** Referral discounts for shops referring other shops.

---

## 5. Strategic Trade-offs & Risk Mitigation

### Trade-off 1: Broad Scale vs. Highly Localized Credibility
* **Option 1:** Mass-emailing 500+ shops nationwide using generic templates. (Low effort, high volume, low trust).
* **Option 2:** Hyper-targeted outreach to verified 4.5+ star shops, localized by city, written as peer-to-peer emails. (Higher upfront research, lower volume, **significantly higher conversion and trust**).
* **Recommendation:** **Option 2**. Local shops receive dozens of spam emails daily. A highly tailored, peer-to-peer tone is the only way to break through the noise.

### Risks and Mitigation Plans

| Risk | Impact | Mitigation Plan |
| :--- | :--- | :--- |
| **Domain Spam Flagging** | High | 1. Limit daily sends to **<30 emails per day** from the Gmail account.<br>2. Use a natural, plain-text email format (no heavy HTML or tracking pixels).<br>3. Verify all emails prior to sending to keep bounce rates under 3%. |
| **Low Conversion to Paid** | Medium | 1. Implement automatic 20-day check-in emails showing them traffic data or interest on their pricing page.<br>2. Ensure the listing sign-up landing page is frictionless and professional. |
| **Missing "First Name" Data** | Medium | Use the highly natural `[Shop Name] Team` greeting, which reads as an intentional B2B outreach rather than a broken template. |

---

## 6. Implementation & Operational Roadmap

1. **Phase 1: Database Verification (Completed)** - Filter out "Form only" and "Incomplete" leads (e.g., uBreakiFix Sydney). Maintain list of 26 verified high-quality leads in Sydney/Melbourne.
2. **Phase 2: Template Selection (Current)** - Select preferred variant or approve A/B test split.
3. **Phase 3: Automated Personalization & Draft Generation** - Generate customized subjects and bodies for the 26 verified leads.
4. **Phase 4: Pilot Launch & Monitoring (August)** - Send personalized emails via Gmail. Check delivery status 5 seconds after sending.
5. **Phase 5: Evaluation & Expansion (September)** - Measure CTR and trial sign-ups. Roll out to Brisbane and Gold Coast.
