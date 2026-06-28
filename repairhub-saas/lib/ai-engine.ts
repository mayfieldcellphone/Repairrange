import { GoogleGenerativeAI } from "@google/generative-ai";
import { db } from "./firebase";
import { doc, getDoc, collection, addDoc } from "firebase/firestore";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_KEY as string);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-pro" });

// 1. SAVE LEAD TO FIREBASE
export const saveLead = async (shopId: string, leadData: any) => {
    try {
        if (!db) return false;
        const leadsRef = collection(db, "shops", shopId, "leads");
        await addDoc(leadsRef, {
            ...leadData,
            createdAt: new Date().toISOString(),
            status: 'new'
        });
        return true;
    } catch (error) {
        console.error("Error saving lead:", error);
        return false;
    }
};

export const getAIReply = async (shopId: string, customerMessage: string, customerPhone: string = "WhatsApp") => {
    try {
        const shopRef = doc(db, "shops", shopId);
        const shopSnap = await getDoc(shopRef);
        
        if (!shopSnap.exists() || shopSnap.data()?.status !== 'active') {
            return { reply: "Service unavailable.", status: "blocked" };
        }

        const shopData = shopSnap.data() as any;
        const knowledgeBase = shopData.knowledgeBase || "General business information.";

        // 2. RUN AI WITH LEAD CAPTURE LOGIC
        const prompt = `
            ROLE: Assistant for ${shopData.name} (Plan: ${shopData.plan})
            KNOWLEDGE: ${knowledgeBase}
            
            USER MESSAGE: ${customerMessage}
            
            TASK: 
            1. If the user provides contact details or a specific problem, extract them.
            2. Reply naturally to the customer.
            3. If this is a SALES LEAD, output the lead data in the JSON response.
            
            OUTPUT FORMAT:
            {
              "reply": "Your friendly message here",
              "lead": { "name": "...", "email": "...", "phone": "${customerPhone}", "notes": "..." },
              "intent": "sale|support|general"
            }
        `;

        const result = await model.generateContent(prompt);
        const rawText = result.response.text();
        const jsonMatch = rawText.match(/\{[\s\S]*\}/);
        const parsed = jsonMatch ? JSON.parse(jsonMatch[0]) : { reply: rawText };

        // 3. AUTO-SAVE IF PLAN IS PRO/ENTERPRISE
        if (parsed.lead && shopData.plan !== 'Basic') {
            await saveLead(shopId, parsed.lead);
        }

        return {
            reply: parsed.reply,
            intent: parsed.intent || "general",
            status: "success"
        };

    } catch (error) {
        console.error("AI Engine Error:", error);
        return { reply: "Error processing request.", status: "error" };
    }
};
