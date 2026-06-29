# WhatsApp Automation Plan: RepairHub

This plan outlines the automation strategy for **selfrepairkit.com.au**, **repairbill.shop**, and **repairrange.io** using the Meta WhatsApp Cloud API and Google Cloud Run.

## 1. Automation Scenarios

### selfrepairkit.com.au (E-commerce)
*   **Goal:** Improve customer trust and reduce support queries.
*   **Trigger:** New Order / Shipment.
*   **Template:** "Hi {{1}}, your DIY Repair Kit for {{2}} is on its way! Track it here: {{3}}"

### repairbill.shop (Invoicing)
*   **Goal:** Speed up payment collection.
*   **Trigger:** Invoice Created / Overdue.
*   **Template:** "Hello {{1}}, your invoice {{2}} for ${{3}} is ready. Pay securely at: {{4}}"

### repairrange.io (Service Management)
*   **Goal:** Streamline repair lifecycle.
*   **Trigger:** Status Change (Received -> Repairing -> Ready).
*   **Template:** "Good news {{1}}! Your device repair is complete and ready for pickup at our Mayfield branch."

## 2. Technical Implementation (Google Cloud Run)

### Recommended Architecture
Create a central **Messaging Microservice** on Cloud Run.

### Node.js Core Logic
```javascript
const axios = require('axios');

async function sendWhatsApp(to, templateName, components) {
  const url = `https://graph.facebook.com/v18.0/${process.env.WHATSAPP_PHONE_NUMBER_ID}/messages`;
  
  const payload = {
    messaging_product: "whatsapp",
    to: to,
    type: "template",
    template: {
      name: templateName,
      language: { code: "en_US" },
      components: [
        {
          type: "body",
          parameters: components // Array of { type: "text", text: "..." }
        }
      ]
    }
  };

  return axios.post(url, payload, {
    headers: { 'Authorization': `Bearer ${process.env.WHATSAPP_TOKEN}` }
  });
}
```

## 3. Security & Scaling
*   **Environment Variables:** Store `WHATSAPP_TOKEN` and `PHONE_NUMBER_ID` in **Google Secret Manager**.
*   **Webhooks:** Set up a Cloud Run endpoint to receive "Delivery Receipts" and "User Replies" from Meta.

## 4. Next Steps
1. Create official Message Templates in Meta Business Manager.
2. Generate a **Permanent Access Token** (Temporary ones expire in 24 hours).
3. Connect Cloud Run to your ERP database.
