import { api } from '$lib/services/api';
import type { ISubscriptionPlan } from '$lib/types/subscription-plan';
import type { PageLoad } from './$types';

interface PlanData {
  plans: ISubscriptionPlan[];
  total: number;
}

export const load: PageLoad = async ({ fetch }) => {
  try {
    const data = await api.get<PlanData>('/admin/subscriptions/', fetch);
    return {
      plans: data.plans,
      total: data.total
    };
  } catch (error) {
    console.error('Failed to load subscription plans:', error);
    return {
      plans: [],
      total: 0
    };
  }
};
