import { api } from '$lib/services/api';
import type { ICategory } from '$lib/types/category';
import type { PageLoad } from './$types';

type ICategoryAdmin = ICategory & {
	articles_count: number;
};

export const load: PageLoad = async ({ fetch }) => {
	try {
		const data = await api.get<{ categories: ICategoryAdmin[] }>('/admin/categories/', fetch);
		return {
			categories: data.categories
		};
	} catch (error) {
		console.error('Failed to load categories:', error);
		return {
			categories: []
		};
	}
};