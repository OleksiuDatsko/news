import { api } from '$lib/services/api';
import type { IAuthor } from '$lib/types/author';
import type { ICategory } from '$lib/types/category';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
  try {
    const authorsData = api.get<{ authors: IAuthor[] }>('/admin/authors/', fetch);
    const categoriesData = api.get<{ categories: ICategory[] }>('/admin/categories/', fetch);

    const [authorsResult, categoriesResult] = await Promise.all([authorsData, categoriesData]);

    return {
      authors: authorsResult.authors,
      categories: categoriesResult.categories
    };
  } catch (error) {
    console.error('Failed to load data for new article:', error);
    return {
      authors: [],
      categories: []
    };
  }
};
