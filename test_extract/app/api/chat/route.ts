import { NextResponse } from 'next/server';
import { getAIReply } from '@/lib/ai-engine';

export async function POST(request: Request) {
    try {
        const body = await request.json();
        const { shopId, message } = body;

        if (!shopId || !message) {
            return NextResponse.json({ error: "Missing parameters" }, { status: 400 });
        }

        const aiResult = await getAIReply(shopId, message);
        return NextResponse.json(aiResult);

    } catch (error) {
        return NextResponse.json({ error: "Internal Server Error" }, { status: 500 });
    }
}
