import { api } from '$lib/services/api';
import type { IAdmin } from '$lib/types/admin';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch }) => {
  const { id } = params;
  try {
    const admin = await api.get<IAdmin>(`/admin/admin-users/${id}`, fetch);
    return {
      admin
    };
  } catch (error) {
    console.error(`Failed to load admin ${id}:`, error);
    return {
      admin: null
    };
  }
};
