import { userStore, adminStore } from '$lib/stores/authStore';
import { api } from '$lib/services/api';
import type { LayoutLoad } from './$types';
import type { IUser } from '$lib/types/user';
import type { IAdmin } from '$lib/types/admin';
import type { IArticle } from '$lib/types/article';

export const ssr = false;

export const load: LayoutLoad = async ({fetch}) => {
	try {
		const { admin } = await api.get<{ admin: IAdmin }>('/admin/auth/me', fetch);
		adminStore.set(admin);
	} catch (e) {
		adminStore.set(null); // Важливо скинути старе значення
		try {
			const { user } = await api.get<{ user: IUser }>('/auth/me', fetch);
			const canSave = user?.permissions?.save_article;
			if (canSave) {
				console.log('Fetching saved articles for user...');
				const savedArticles = await api.get<number[]>('/articles/saved?ids=true', fetch);
				user.savedArticles = savedArticles;
			}
			userStore.set(user);

		} catch (err) {
			userStore.set(null);
		}
	}
	
	return {};
};