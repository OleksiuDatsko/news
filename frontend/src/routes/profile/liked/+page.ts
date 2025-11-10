import { api } from '$lib/services/api';
import type { IArticle } from '$lib/types/article';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
  try {
    const likedArticles = await api.get<IArticle[]>('/articles/liked', fetch);
    return {
      articles: likedArticles
    };
  } catch (error) {
    console.error('Failed to load liked articles:', error);
    return {
      articles: []
    };
  }
};
