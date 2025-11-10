import { api } from '$lib/services/api';
import type { PageLoad } from './$types';
import type { IAdminAd } from '../+page.ts';

export const load: PageLoad = async ({ params, fetch }) => {
  const { id } = params;

  try {
    const ad = await api.get<IAdminAd>(`/admin/ads/${id}`, fetch);
    return {
      ad
    };
  } catch (error) {
    console.error(`Failed to load ad ${id}:`, error);
    return {
      ad: null
    };
  }
};
