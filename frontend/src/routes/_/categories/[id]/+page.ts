import { api } from '$lib/services/api';
import type { ICategory } from '$lib/types/category';
import type { IArticle } from '$lib/types/article';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch }) => {
	const { id } = params;

	try {
		const categoryData = await api.get<ICategory>(`/admin/categories/${id}`, fetch);

		const articlesData = await api.get<{ articles: IArticle[] }>(
			`/admin/categories/${id}/articles`,
			fetch
		);

		return {
			category: categoryData,
			articles: articlesData.articles
		};
	} catch (error) {
		console.error(`Failed to load category ${id}:`, error);
		return {
			category: null,
			articles: []
		};
	}
};