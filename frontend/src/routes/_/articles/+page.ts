import { api } from '$lib/services/api';
import type { IArticle } from '$lib/types/article';
import type { PageLoad } from './$types';

interface AdminArticleData {
	articles: IArticle[];
	page: number;
	per_page: number;
}

export const load: PageLoad = async ({ fetch }) => {
	try {
		const data = await api.get<AdminArticleData>('/admin/articles/', fetch);

		return {
			articles: data.articles
		};
	} catch (error) {
		console.error('Failed to load admin articles:', error);
		return {
			articles: []
		};
	}
};