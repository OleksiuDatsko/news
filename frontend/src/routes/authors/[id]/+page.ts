import { api } from '$lib/services/api';
import type { IArticle } from '$lib/types/article';
import type { IAuthor } from '$lib/types/author';
import type { PageLoad } from './$types';
import { userStore } from '$lib/stores/authStore';
import { get } from 'svelte/store';

interface AuthorArticleData {
  articles: IArticle[];
  page: number;
  per_page: number;
  total: number;
}

export const load: PageLoad = async ({ fetch, params, url }) => {
  const { id } = params;
  const page = url.searchParams.get('page') || '1';

  const user = get(userStore);
  const followed_authors = user?.followed_authors || [];
  const is_following = followed_authors.includes(Number(id));

  try {
    const authorPromise = api.get<IAuthor>(`/authors/${id}`, fetch);
    const articlesPromise = api.get<AuthorArticleData>(
      `/authors/${id}/articles?page=${page}`,
      fetch
    );

    const [author, articleData] = await Promise.all([authorPromise, articlesPromise]);

    return {
      author,
      articles: articleData.articles,
      page: articleData.page,
      perPage: articleData.per_page,
      total: articleData.total,
      is_following
    };
  } catch (error) {
    console.error(`Failed to load author ${id} data:`, error);
    return {
      author: null,
      articles: [],
      page: 1,
      perPage: 10,
      total: 0,
      is_following: false
    };
  }
};
