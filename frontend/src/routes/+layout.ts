import { userStore, adminStore } from '$lib/stores/authStore';
import { api } from '$lib/services/api';
import type { LayoutLoad } from './$types';
import type { IUser } from '$lib/types/user';
import type { IAdmin } from '$lib/types/admin';

export const ssr = false;

export const load: LayoutLoad = async () => {
	try {
		const { admin } = await api.get<{ admin: IAdmin }>('/admin/auth/me');
		adminStore.set(admin);
	} catch (e) {
		adminStore.set(null); // Важливо скинути старе значення
		try {
			const { user } = await api.get<{ user: IUser }>('/auth/me');
			userStore.set(user);
		} catch (err) {
			userStore.set(null);
		}
	}
	
	return {};
};