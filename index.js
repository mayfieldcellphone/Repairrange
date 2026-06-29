const express = require('express');
const axios = require('axios');
const { GoogleGenerativeAI } = require("@google/generative-ai");

const app = express();
app.use(express.json());

// Load AI Training
const genAI = new GoogleGenerativeAI(process.env.GEMINI_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-pro" });

// Health Check for Cloud Run
app.get('/', (req, res) => {
    res.status(200).send('RepairHub AI Webhook is running!');
});

// 1. WEBHOOK VERIFICATION (For Meta Setup)
app.get('/webhook', (req, res) => {
    const verify_token = process.env.VERIFY_TOKEN;
    const mode = req.query['hub.mode'];
    const token = req.query['hub.verify_token'];
    const challenge = req.query['hub.challenge'];

    if (mode && token === verify_token) {
        res.status(200).send(challenge);
    } else {
        res.sendStatus(403);
    }
});

// 2. MESSAGE HANDLER (SaaS-Grade Multi-Tenant Engine)
app.post('/webhook', async (req, res) => {
    try {
        const body = req.body;
        if (body.object === 'whatsapp_business_account') {
            const entry = body.entry[0];
            const changes = entry.changes[0].value;

            if (changes.messages) {
                const msg = changes.messages[0];
                const from = msg.from; 
                const text = msg.text.body;
                const phone_number_id = changes.metadata.phone_number_id;

                // SAAS ROUTING LOGIC: Identify which business is being messaged
                let businessProfile = "GENERAL_ASSISTANT";
                let brandName = "RepairHub";

                // Map your WhatsApp IDs to specific Business Profiles
                if (phone_number_id === "1194675237059356") {
                    // Check if it's the Shop number or the Kit number (Example IDs)
                    brandName = "Mayfield Cell Phone Repairs";
                    businessProfile = "LOCAL_SERVICE_EXPERT";
                }

                // Call Gemini with the Multi-Tenant System Prompt
                const fullPrompt = `
                SYSTEM_MODE: SAAS_MULTI_TENANT
                TENANT_BRAND: ${brandName}
                TENANT_PROFILE: ${businessProfile}
                
                USER_MESSAGE: ${text}
                
                INSTRUCTIONS:
                1. Identify intent (Lead, Sale, or Support).
                2. Use the specific brand voice for ${brandName}.
                3. Do NOT leak data from other tenants.
                4. Output your reply in the following JSON format:
                {
                  "reply": "Your customer-facing text",
                  "intent": "sale|lead|support",
                  "confidence": 0.95
                }`;

                const result = await model.generateContent(fullPrompt);
                const rawResponse = result.response.text();
                
                // Parse the AI's structured response
                let parsed;
                try {
                    parsed = JSON.parse(rawResponse.replace(/```json|```/g, ""));
                } catch (e) {
                    parsed = { reply: rawResponse }; // Fallback to raw text
                }

                // Send the reply back to WhatsApp
                await axios.post(`https://graph.facebook.com/v18.0/${phone_number_id}/messages`, {
                    messaging_product: "whatsapp",
                    to: from,
                    text: { body: parsed.reply }
                }, {
                    headers: { 'Authorization': `Bearer ${process.env.WHATSAPP_TOKEN}` }
                });

                // LOGGING FOR SAAS DASHBOARD (Future CRM use)
                console.log(`[DASHBOARD_DATA] Brand: ${brandName} | Intent: ${parsed.intent}`);
            }
            res.sendStatus(200);
        }
    } catch (error) {
        console.error("Webhook Error:", error);
        res.sendStatus(500);
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => console.log(`RepairHub AI Webhook active on port ${PORT}`));
