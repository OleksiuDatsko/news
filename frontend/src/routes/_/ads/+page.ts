import { api } from '$lib/services/api';
import type { PageLoad } from './$types';

export interface IAdminAd {
  id: number;
  title: string;
  ad_type: 'banner' | 'sidebar' | 'popup' | 'inline' | 'video';
  is_active: boolean;
  content: string;
  start_date: string | null;
  end_date: string | null;
  impressions_count: number;
  clicks_count: number;
  ctr: number;
  status: 'active' | 'inactive' | 'expired';
}

interface AdminAdData {
  ads: IAdminAd[];
  page: number;
  per_page: number;
  total: number;
}

export const load: PageLoad = async ({ fetch, url }) => {
  const page = url.searchParams.get('page') || '1';
  const perPage = '15';

  try {
    const data = await api.get<AdminAdData>(`/admin/ads/?page=${page}`, fetch);
    return {
      ads: data.ads,
      page: data.page,
      perPage: data.per_page,
      total: data.total
    };
  } catch (error) {
    console.error('Failed to load admin ads:', error);
    return {
      ads: [],
      page: 1,
      perPage: 15,
      total: 0
    };
  }
};
