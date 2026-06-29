import { NextResponse } from 'next/server';
import { stripe } from '../../../../lib/stripe';
import { headers } from 'next/headers';
import { db } from '../../../../lib/firebase';
import { doc, updateDoc, query, collection, where, getDocs } from 'firebase/firestore';

const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;

export async function POST(req: Request) {
    const body = await req.text();
    const sig = headers().get('stripe-signature') as string;

    let event;

    try {
        event = stripe.webhooks.constructEvent(body, sig, endpointSecret!);
    } catch (err: any) {
        return NextResponse.json({ error: `Webhook Error: ${err.message}` }, { status: 400 });
    }

    // HANDLE THE REVENUE EVENTS
    switch (event.type) {
        case 'checkout.session.completed':
            const session = event.data.object as any;
            const shopId = session.metadata.shopId; // We pass this during checkout
            
            // ACTIVATE THE SHOP IN FIREBASE
            const shopRef = doc(db, "shops", shopId);
            await updateDoc(shopRef, {
                status: 'active',
                stripeCustomerId: session.customer,
                plan: 'Pro'
            });
            console.log(`✅ Shop ${shopId} activated via Stripe.`);
            break;

        case 'customer.subscription.deleted':
            const subscription = event.data.object as any;
            // Find the shop with this customer ID
            const q = query(collection(db, "shops"), where("stripeCustomerId", "==", subscription.customer));
            const querySnapshot = await getDocs(q);
            
            querySnapshot.forEach(async (shopDoc) => {
                await updateDoc(doc(db, "shops", shopDoc.id), {
                    status: 'suspended'
                });
                console.log(`❌ Shop ${shopDoc.id} suspended - Subscription ended.`);
            });
            break;
    }

    return NextResponse.json({ received: true });
}
