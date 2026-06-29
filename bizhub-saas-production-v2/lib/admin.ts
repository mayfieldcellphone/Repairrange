import { db } from "./firebase";
import { collection, getDocs, updateDoc, doc } from "firebase/firestore";

export const getAllSubscribers = async () => {
    try {
        const querySnapshot = await getDocs(collection(db, "shops"));
        return querySnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    } catch (error) {
        console.error("Error fetching subscribers:", error);
        return [];
    }
};

export const setSubscriptionStatus = async (shopId: string, newStatus: 'active' | 'suspended') => {
    try {
        const shopRef = doc(db, "shops", shopId);
        await updateDoc(shopRef, {
            status: newStatus,
            updatedAt: new Date().toISOString()
        });
        return true;
    } catch (error) {
        console.error("Error updating status:", error);
        return false;
    }
};

export const getFinancialStats = async () => {
    try {
        const shops = await getAllSubscribers() as any[];
        const totalRevenue = shops.reduce((sum, shop) => {
            const rev = shop.revenue ? parseFloat(shop.revenue.replace(/[^0-9.]/g, '')) : 0;
            return sum + (isNaN(rev) ? 0 : rev);
        }, 0);
        return {
            totalRevenue: `$${totalRevenue.toLocaleString()}`,
            activeCount: shops.filter(s => s.status === 'active').length
        };
    } catch (error) {
        console.error("Error calculating stats:", error);
        return { totalRevenue: "$0", activeCount: 0 };
    }
};
