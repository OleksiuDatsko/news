import { api } from '$lib/services/api';
import type { IArticleFull } from '$lib/types/article';
import type { IAuthor } from '$lib/types/author';
import type { ICategory } from '$lib/types/category';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch }) => {
  const { id } = params;
  try {
    const articleData = api.get<IArticleFull>(`/admin/articles/${id}`, fetch);
    const authorsData = api.get<{ authors: IAuthor[] }>('/admin/authors/', fetch);
    const categoriesData = api.get<{ categories: ICategory[] }>('/admin/categories/', fetch);

    const [article, authorsResult, categoriesResult] = await Promise.all([
      articleData,
      authorsData,
      categoriesData
    ]);

    return {
      article,
      authors: authorsResult.authors,
      categories: categoriesResult.categories
    };
  } catch (error) {
    console.error(`Failed to load article ${id}:`, error);
    return {
      article: null,
      authors: [],
      categories: []
    };
  }
};
