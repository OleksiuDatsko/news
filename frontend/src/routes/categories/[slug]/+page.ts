import { api } from '$lib/services/api';
import type { IArticle } from '$lib/types/article';
import type { IAd } from '$lib/types/ad';
import type { ICategory } from '$lib/types/category';
import type { PageLoad } from './$types';

interface CategoryPageData {
  articles: IArticle[];
  ads: IAd[];
  page: number;
  per_page: number;
  total: number;
}

export const load: PageLoad = async ({ params, fetch, url }) => {
  const { slug } = params;
  const page = url.searchParams.get('page') || '1';

  try {
    const data = await api.get<CategoryPageData>(
      `/articles/?category_slug=${slug}&page=${page}`,
      fetch
    );
    const categoryData = await api.get<ICategory>(`/categories/slug/${slug}`, fetch);

    return {
      articles: data.articles,
      ads: data.ads,
      category: categoryData,
      page: data.page,
      perPage: data.per_page,
      total: data.total
    };
  } catch (error) {
    console.error('Failed to load category data:', error);
    return {
      articles: null,
      ads: [],
      category: null,
      page: 1,
      perPage: 10,
      total: 0
    };
  }
};
