import { userStore, adminStore } from '$lib/stores/authStore';
import { categoryStore } from '$lib/stores/categoryStore';
import { api } from '$lib/services/api';
import type { LayoutLoad } from './$types';
import type { IUser } from '$lib/types/user';
import type { IAdmin } from '$lib/types/admin';
import type { ICategory } from '$lib/types/category';

export const ssr = false;

const PUBLIC_ROUTES = ['/auth/login', '/auth/register', '/admin/login'];

export const load: LayoutLoad = async ({ fetch, url }) => {
	const currentPath = url.pathname;
	const isPublicRoute = PUBLIC_ROUTES.includes(currentPath);

	const promises = [];
	if (!isPublicRoute) {
		const authPromise = (async () => {
			try {
				const { admin } = await api.get<{ admin: IAdmin }>('/admin/auth/me', fetch);
				adminStore.set(admin);
			} catch (e) {
				adminStore.set(null);
				try {
					const { user } = await api.get<{ user: IUser }>('/auth/me', fetch);
					const canSave = user?.permissions?.save_article;
					if (canSave && user) {
						const savedArticles = await api.get<number[]>(
							'/articles/saved?ids=true',
							fetch
						);
						user.savedArticles = savedArticles;
					}
					userStore.set(user);
				} catch (err) {
					userStore.set(null);
				}
			}
		})();
		promises.push(authPromise);
	} else {
		userStore.set(null);
		adminStore.set(null);
	}

	const categoryPromise = (async () => {
		try {
			const { categories } = await api.get<{ categories: ICategory[] }>(
				'/categories/',
				fetch
			);
			categoryStore.set(categories);
		} catch (e) {
			console.error('Failed to load categories', e);
			categoryStore.set([]);
		}
	})();
	promises.push(categoryPromise);

	await Promise.all(promises);
	return {};
};