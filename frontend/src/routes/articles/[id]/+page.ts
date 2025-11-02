import { api } from '$lib/services/api';
import type { IArticleFull } from '$lib/types/article';
import type { IAd } from '$lib/types/ad';
import type { PageLoad } from './$types';

type ArticlePageData = IArticleFull & {
	ads: IAd[];
};

export const load: PageLoad = async ({ params, fetch }) => {
	try {
		const { id } = params;
		const data = await api.get<ArticlePageData>(`/articles/${id}`, fetch);

		return {
			article: data,
			ads: data.ads
		};
	} catch (error) {
		console.error('Failed to load article:', error);
		return {
			article: null,
			ads: []
		};
	}
};