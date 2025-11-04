import { api } from '$lib/services/api';
import type { IArticle } from '$lib/types/article';
import type { PageLoad } from './$types';

interface SearchData {
	articles: IArticle[];
	query: string;
	page: number;
	per_page: number;
	total: number;
	date_from?: string;
	date_to?: string;
}

export const load: PageLoad = async ({ fetch, url }) => {
	const query = url.searchParams.get('q') || '';
	const page = url.searchParams.get('page') || '1';
	const date_from = url.searchParams.get('date_from') || '';
	const date_to = url.searchParams.get('date_to') || '';

	if (!query) {
		return { articles: [], query, page: 1, perPage: 10, total: 0, date_from: '', date_to: '' };
	}

	try {
		const params = new URLSearchParams({
			q: query,
			page: page,
			date_from: date_from,
			date_to: date_to
		});

		const data = await api.get<SearchData>(
			`/articles/search?${params.toString()}`,
			fetch
		);

		return {
			articles: data.articles,
			query: data.query,
			page: data.page,
			perPage: data.per_page,
			total: data.total,
			date_from: data.date_from || '',
			date_to: data.date_to || ''
		};
	} catch (error) {
		console.error('Failed to load search results:', error);
		return { articles: [], query, page: 1, perPage: 10, total: 0, date_from: date_from, date_to: date_to };
	}
};