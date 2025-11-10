import { api } from '$lib/services/api';
import type { IArticle } from '$lib/types/article';
import type { PageLoad } from './$types';

interface AdminArticleData {
  articles: IArticle[];
  page: number;
  per_page: number;
  total: number;
}

export const load: PageLoad = async ({ fetch, url }) => {
  const page = url.searchParams.get('page') || '1';
  try {
    const data = await api.get<AdminArticleData>(
      `/admin/articles/?page=${page}&per_page=10`,
      fetch
    );
    return {
      articles: data.articles,
      page: data.page,
      perPage: data.per_page,
      total: data.total
    };
  } catch (error) {
    console.error('Failed to load admin articles:', error);
    return {
      articles: [],
      page: 1,
      perPage: 10,
      total: 0
    };
  }
};
