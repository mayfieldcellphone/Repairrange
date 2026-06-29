import { NextResponse } from 'next/server';
import { getAIReply } from '../../../lib/ai-engine';

export async function POST(request: Request) {
    try {
        const body = await request.json();
        const { shopId, message } = body;

        if (!shopId || !message) {
            return NextResponse.json({ error: "Missing parameters" }, { status: 400 });
        }

        const aiResult = await getAIReply(shopId, message);
        return NextResponse.json(aiResult);

    } catch (error: any) {
        console.error("Chat API Error:", error);
        return NextResponse.json({ error: "Internal Server Error", details: error.message }, { status: 500 });
    }
}

export async function OPTIONS() {
    return NextResponse.json({}, {
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        }
    });
}
