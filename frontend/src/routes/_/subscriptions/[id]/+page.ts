import { api } from '$lib/services/api';
import type { ISubscriptionPlan } from '$lib/types/subscription-plan';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch }) => {
	const { id } = params;
	try {
		const plan = await api.get<ISubscriptionPlan>(`/admin/subscriptions/${id}`, fetch);
		return {
			plan
		};
	} catch (error) {
		console.error(`Failed to load plan ${id}:`, error);
		return {
			plan: null
		};
	}
};