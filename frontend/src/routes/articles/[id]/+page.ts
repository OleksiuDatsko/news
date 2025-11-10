import { api } from '$lib/services/api';
import type { IArticle, IArticleFull } from '$lib/types/article';
import type { IAd } from '$lib/types/ad';
import type { PageLoad } from './$types';

type ArticlePageData = IArticleFull & {
	ads: IAd[];
};

interface ArticleListData {
	articles: IArticle[];
	ads: IAd[];
	page: number;
	per_page: number;
	total: number;
}

export const load: PageLoad = async ({ params, fetch }) => {
	const { id } = params;

	try {
		const articlePromise = api.get<ArticlePageData>(`/articles/${id}`, fetch);
		const recPromise = api.get<ArticleListData>(
			`/articles/recommended?page=1&per_page=3`,
			fetch
		);

		const [articleResult, recResult] = await Promise.allSettled([
			articlePromise,
			recPromise
		]);

		if (articleResult.status === 'rejected') {
			throw articleResult.reason;
		}

		const recommendations =
			recResult.status === 'fulfilled' ? recResult.value.articles : [];
		
		const articleData = articleResult.value;

		return {
			article: articleData,
			ads: articleData.ads,
			recommendations,
			error: null
		};
	} catch (error) {
		console.error('Failed to load article:', error);
		return {
			article: null,
			ads: [],
			recommendations: [],
			error: error
		};
	}
};