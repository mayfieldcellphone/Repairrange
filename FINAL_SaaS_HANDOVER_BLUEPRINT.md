# 📑 MASTER HANDOVER: BizHub AI SaaS Ecosystem

## 1. 🔑 The Credentials Vault (SaaS Master Keys)
**Mandatory**: Use these exact names and values in your Environment Variables.

| Category | Variable Name | Value |
| :--- | :--- | :--- |
| **AI Brain** | `GEMINI_KEY` | `AQ.Ab8RN6Jiwq7Ra1uig_XBoplP2TuEtXVeliHLacwvjq5r6gbuTg` |
| **Payments** | `STRIPE_SECRET_KEY` | `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` |
| **WhatsApp** | `WHATSAPP_TOKEN` | `EAAO2W3vEH5MBRZBbABZCDyJhBXmJhsMsUO89YftZC6mOFmciQHFRiGfD8RiCMC6kfewZCJkEDsmtToRQb3u30MGmNx182VpWyy3mtat36Ac1I3XK381jltqLQfCGApqoyu63Br1W27cxM40M33XZAQgBajnsm5klQ2iVfDZBZCgfrugDg0VyQiB42PtoW0qld0hvHRXBIMUZCvJJCM6KZBNLOtZCWpcJxrUKuUqvqCwqIF4XqvvNqbZBXSDbMnsFRin4yUSi1cZCIvsZC6YuZCCjOxZAYjrc5AZD` |
| **Security** | `VERIFY_TOKEN` | `RepairHubSecret123` |
| **Auth** | `NEXTAUTH_SECRET` | `BizHubSuperSecret123` |
| **Auth** | `NEXTAUTH_URL` | `https://repairhub-whatsapp-ai-302106920849.europe-west1.run.app/` |

### 🔥 Firebase Database Config (Next.js Public)
- `NEXT_PUBLIC_FIREBASE_API_KEY`: `AIzaSyBGs5Fd1aYrVQDs_MhOgy5d8LFn5oLvXYI`
- `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN`: `repairhub-saas.firebaseapp.com`
- `NEXT_PUBLIC_FIREBASE_PROJECT_ID`: `repairhub-saas`
- `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET`: `repairhub-saas.firebasestorage.app`
- `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID`: `135356822613`
- `NEXT_PUBLIC_FIREBASE_APP_ID`: `1:135356822613:web:6220b004dc9193aaff50dc`

---

## 2. 🏗️ Technical Architecture & Constraints
- **Hosting**: Google Cloud Run (Docker Container).
- **Networking**: Listen on **Port 3000**, bind to `0.0.0.0`.
- **Framework**: Next.js 14.2 (App Router). `output: 'standalone'` in `next.config.mjs`.
- **Imports**: Use relative paths (`../../lib/...`) to avoid build errors.

## 3. 🧠 Business Logic
- **Mayfield Shop**: Lead Gen mode. Capture device model/issue.
- **SelfRepairKit**: E-commerce mode. Push sales and support DIY repairs.
- **RepairBill**: SaaS Billing mode. Verify payments and handle invoices.

## 4. 🚀 Next Steps
1. Build the **5-Step Onboarding Wizard**.
2. Create the **JavaScript Snippet Generator** for websites.
3. Integrate **Voice-to-Invoice** features as a global service.
