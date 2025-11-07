import { api } from '$lib/services/api';
import type { IArticle } from '$lib/types/article';
import type { IAuthor } from '$lib/types/author';
import type { PageLoad } from './$types';

interface AuthorArticleData {
	articles: IArticle[];
	page: number;
	per_page: number;
	total: number;
}

export const load: PageLoad = async ({ fetch, params, url }) => {
	const { id } = params;
	const page = url.searchParams.get('page') || '1';

	try {
		const authorPromise = api.get<IAuthor>(`/authors/${id}`, fetch);
		const articlesPromise = api.get<AuthorArticleData>(
			`/authors/${id}/articles?page=${page}`,
			fetch
		);

		const [author, articleData] = await Promise.all([
			authorPromise,
			articlesPromise
		]);

		return {
			author,
			articles: articleData.articles,
			page: articleData.page,
			perPage: articleData.per_page,
			total: articleData.total
		};
	} catch (error) {
		console.error(`Failed to load author ${id} data:`, error);
		return {
			author: null,
			articles: [],
			page: 1,
			perPage: 10,
			total: 0
		};
	}
};