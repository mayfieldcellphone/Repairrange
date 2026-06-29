import { GoogleGenerativeAI } from "@google/generative-ai";
import { db } from "./firebase";
import { doc, getDoc } from "firebase/firestore";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_KEY as string);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-pro" });

export const getAIReply = async (shopId: string, customerMessage: string) => {
    try {
        const shopRef = doc(db, "shops", shopId);
        const shopSnap = await getDoc(shopRef);
        
        if (!shopSnap.exists() || shopSnap.data()?.status !== 'active') {
            return {
                reply: "This service is currently unavailable. Please contact the shop owner.",
                status: "blocked"
            };
        }

        const shopData = shopSnap.data() as any;

        const prompt = `
            ROLE: Official AI Assistant for ${shopData.name}
            VOICE: ${shopData.tone || 'Professional and helpful'}
            KNOWLEDGE: ${shopData.knowledgeBase || "General repair information."}
            
            USER MESSAGE: ${customerMessage}
            
            RULES:
            - Summarize articles into 2-3 bullets.
            - If price is unknown, offer technician handoff.
            - Do not leak data from other tenants.
            - Output as JSON: { "reply": "...", "intent": "lead|sale|support" }
        `;

        const result = await model.generateContent(prompt);
        const rawText = result.response.text();
        
        const jsonMatch = rawText.match(/\{[\s\S]*\}/);
        const parsed = jsonMatch ? JSON.parse(jsonMatch[0]) : { reply: rawText };

        return {
            reply: parsed.reply,
            intent: parsed.intent || "general",
            status: "success"
        };

    } catch (error) {
        console.error("AI Engine Error:", error);
        return { reply: "I'm having trouble processing that right now.", status: "error" };
    }
};
