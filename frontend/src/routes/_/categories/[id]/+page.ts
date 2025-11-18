import { api } from '$lib/services/api';
import type { ICategory } from '$lib/types/category';
import type { IArticle } from '$lib/types/article';
import type { PageLoad } from './$types';

// Визначаємо інтерфейс для відповіді API
interface CategoryArticleData {
  articles: IArticle[];
  page: number;
  per_page: number;
  total: number;
  category_name: string;
}

export const load: PageLoad = async ({ params, fetch, url }) => {
  const { id } = params;
  const page = url.searchParams.get('page') || '1';

  try {
    const categoryData = await api.get<ICategory>(`/admin/categories/${id}`, fetch);
    const articlesData = await api.get<CategoryArticleData>(
      `/articles/?category=${id}&page=${page}&per_page=3`,
      fetch
    );

    return {
      category: categoryData,
      articles: articlesData.articles,
      page: articlesData.page,
      perPage: articlesData.per_page,
      total: articlesData.total
    };
  } catch (error) {
    console.error(`Failed to load category ${id}:`, error);
    return {
      category: null,
      articles: [],
      page: 1,
      perPage: 5,
      total: 0
    };
  }
};
