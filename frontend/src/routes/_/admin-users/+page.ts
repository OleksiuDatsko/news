import { api } from '$lib/services/api';
import type { IAdmin } from '$lib/types/admin';
import type { PageLoad } from './$types';

interface AdminData {
	admin_users: IAdmin[];
	total: number;
}

export const load: PageLoad = async ({ fetch }) => {
	try {
		const data = await api.get<AdminData>('/admin/admin-users/', fetch);
		return {
			admins: data.admin_users,
			total: data.total
		};
	} catch (error) {
		console.error('Failed to load admin users:', error);
		return {
			admins: [],
			total: 0
		};
	}
};