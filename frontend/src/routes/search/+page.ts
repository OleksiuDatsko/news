import { api } from '$lib/services/api';
import type { IArticle } from '$lib/types/article';
import type { PageLoad } from './$types';

interface SearchData {
	articles: IArticle[];
	query: string;
	page: number;
	per_page: number;
	total: number;
}

export const load: PageLoad = async ({ fetch, url }) => {
	const query = url.searchParams.get('q') || '';
	const page = url.searchParams.get('page') || '1';

	if (!query) {
		return { articles: [], query, page: 1, perPage: 10, total: 0 };
	}

	try {
		const data = await api.get<SearchData>(
			`/articles/search?q=${encodeURIComponent(query)}&page=${page}`,
			fetch
		);
		return {
			articles: data.articles,
			query: data.query,
			page: data.page,
			perPage: data.per_page,
			total: data.total
		};
	} catch (error) {
		console.error('Failed to load search results:', error);
		return { articles: [], query, page: 1, perPage: 10, total: 0 };
	}
};