import { api } from '$lib/services/api';
import type { IArticle } from '$lib/types/article';
import type { IAd } from '$lib/types/ad';
import type { PageLoad } from './$types';

interface HomePageData {
	articles: IArticle[];
	ads: IAd[];
}

export const load: PageLoad = async ({fetch}) => {
	try {
		const data = await api.get<HomePageData>('/articles/', fetch); 

		return {
			articles: data.articles,
			ads: data.ads
		};
	} catch (error) {
		console.error('Failed to load homepage data:', error);
		return {
			articles: [],
			ads: []
		};
	}
};