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

export const load: PageLoad = async ({ params, fetch, url }) => {
  const { id } = params;
  const page = url.searchParams.get('page') || '1';

  try {
    const author = await api.get<IAuthor>(`/admin/authors/${id}`, fetch);
    const articlesData = await api.get<AuthorArticleData>(
      `/admin/authors/${id}/articles?page=${page}&per_page=5`,
      fetch
    );
    return {
      author,
      articles: articlesData.articles,
      page: articlesData.page,
      perPage: articlesData.per_page,
      total: articlesData.total
    };
  } catch (error) {
    console.error(`Failed to load author ${id}:`, error);
    return {
      author: null,
      articles: [],
      page: 1,
      perPage: 5,
      total: 0
    };
  }
};
