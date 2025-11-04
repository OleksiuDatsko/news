import { api } from '$lib/services/api';
import type { PageLoad } from './$types';

export interface ISubscriptionPlan {
    id: number;
    name: string;
    price_per_month: number;
    description: string;
	permissions: {
		no_ads: boolean;
		exclusive_content: boolean;
		save_article: boolean;
		comment: boolean;
	};
}

export interface IUserSubscription {
    id: number;
    plan_id: number;
    is_active: boolean;
	left_days: number | null;
    plan: ISubscriptionPlan;
}


export const load: PageLoad = async ({ fetch }) => {
	try {
		const plansPromise = api.get<ISubscriptionPlan[]>(
			'/subscriptions/', 
			fetch
		);
		
		const currentSubPromise = api.get<IUserSubscription>(
			'/subscriptions/me', 
			fetch
		);

		const [plans, currentSubscription] = await Promise.all([
			plansPromise,
			currentSubPromise.catch(() => null)
		]);

		return {
			plans,
			currentSubscription
		};
	} catch (error) {
		console.error('Failed to load subscription data:', error);
		return {
			plans: [],
			currentSubscription: null
		};
	}
};