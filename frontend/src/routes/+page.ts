import { api } from '$lib/services/api';
import { userStore } from '$lib/stores/authStore';
import type { IAd } from '$lib/types/ad';
import type { IArticle } from '$lib/types/article';
import { get } from 'svelte/store';
import type { PageLoad } from './$types';

interface ArticleData {
	articles: IArticle[];
	ads: IAd[];
	page: number;
	per_page: number;
	total: number;
}

export const load: PageLoad = async ({ fetch, url }) => {	const page = url.searchParams.get('page') || '1';
	try {
		let data;
		if (get(userStore)?.id) {
			data = await api.get<ArticleData>(`/articles/recommended?page=${page}`, fetch); 
		} else {
			data = await api.get<ArticleData>(`/articles/?page=${page}`, fetch);
		}
		return {
			articles: data.articles,
			ads: data.ads,
			page: data.page,
			perPage: data.per_page,
			total: data.total
		};
	} catch (error) {
		console.error('Failed to load admin articles:', error);
		return {
			articles: [],
			ads: [],
			page: 1,
			perPage: 10,
			total: 0
		};
	}
};