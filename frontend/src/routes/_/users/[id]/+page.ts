import { api } from '$lib/services/api';
import type { IUser } from '$lib/types/user';
import type { PageLoad } from './$types';

interface ISubscriptionPlan {
    id: number;
    name: string;
    price_per_month: number;
    description: string;
}

interface IUserWithSubscription extends IUser {
    current_subscription: {
        id: number;
        plan_id: number;
        plan: {
            name: string;
        };
    } | null;
}

export const load: PageLoad = async ({ params, fetch }) => {
    const { id } = params;

    try {
        const userPromise = api.get<IUserWithSubscription>(`/admin/users/${id}`, fetch);
        const plansPromise = api.get<ISubscriptionPlan[]>(`/subscriptions/`, fetch);

        const [user, plans] = await Promise.all([userPromise, plansPromise]);

        return {
            user,
            plans
        };
    } catch (error) {
        console.error(`Failed to load user ${id}:`, error);
        return {
            user: null,
            plans: []
        };
    }
};