import { NextResponse } from 'next/server';
import { GoogleGenerativeAI } from "@google/generative-ai";
import { db } from "../../../lib/firebase";
import { doc, updateDoc } from "firebase/firestore";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_KEY as string);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-pro" });

export async function POST(request: Request) {
    try {
        const body = await request.json();
        const { instruction, shopId, currentData } = body;

        if (!instruction || !shopId) {
            return NextResponse.json({ error: "Missing instruction or shopId" }, { status: 400 });
        }

        // 1. Ask Gemini to "Translate" the instruction into a Knowledge Base update
        const prompt = `
            You are the BizHub Implementation AI. 
            User Instruction: "${instruction}"
            Current Shop Data: ${JSON.stringify(currentData)}
            
            TASK: Rewrite the shop's Knowledge Base / FAQ based on the instruction.
            RETURN ONLY THE NEW KNOWLEDGE BASE TEXT.
        `;

        const result = await model.generateContent(prompt);
        const newKnowledgeBase = result.response.text();

        // 2. Automatically "Implement" the change in Firebase
        const shopRef = doc(db, "shops", shopId);
        await updateDoc(shopRef, {
            knowledgeBase: newKnowledgeBase,
            lastUpdatedBy: "Implementation_AI",
            updatedAt: new Date().toISOString()
        });

        return NextResponse.json({ 
            success: true, 
            message: "I have successfully implemented your changes in the database.",
            newKnowledgeBase 
        });

    } catch (error: any) {
        console.error("Builder AI Error:", error);
        return NextResponse.json({ error: "Implementation failed", details: error.message }, { status: 500 });
    }
}
