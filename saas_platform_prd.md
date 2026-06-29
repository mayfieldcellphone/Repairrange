# PRD: RepairHub SaaS AI Platform

## 1. Project Goal
Create a standalone, multi-tenant AI platform that allows business owners to build, train, and deploy purpose-driven WhatsApp/Web bots without writing code.

## 2. Core Features
### A. User Authentication
*   Login via GitHub/Google.
*   Persistent user sessions and profile management.

### B. The "Auto-Architect" (Internal AI Assistant)
*   **Role:** An internal AI that acts as a "Business Setup Wizard."
*   **Discovery:** Automatically scrapes a user's website to learn their "Business Nature."
*   **Modular Implementation:** Dynamically configures the Firebase environment (Leads vs. Orders vs. Finance) based on what it learns from the site or user input.
*   **Capability:** User gives information (e.g., "Here is my price list CSV"), and the AI automatically parses it and updates the specific Bot's Knowledge Base.

### C. Knowledge Management
*   GitHub Integration: Pull documentation directly from a repo.
*   File Upload: Support for .pdf, .docx, .csv, and .md.
*   URL Scraping: Automatically ingest website content.

### D. Multi-Tenant Routing
*   Each user can manage 5+ separate "Business Profiles."
*   Unique WhatsApp API keys and Webhook endpoints per user.

## 3. Technical Stack
*   **Framework:** Next.js 14 (App Router).
*   **Backend:** Node.js (Edge Functions).
*   **Database:** Supabase (Auth + DB + Vector Storage).
*   **AI Engine:** Gemini 1.5 Pro (API).

## 4. Roadmap
1. **MVP:** Login + Dashboard + Builder Bot.
2. **Beta:** WhatsApp API Integration + Multi-tenant routing.
3. **Launch:** Subscription tiers and Public API access.
