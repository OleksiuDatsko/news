import { api } from '$lib/services/api';
import type { IArticle } from '$lib/types/article';
import type { IAd } from '$lib/types/ad';
import type { ICategory } from '$lib/types/categories';
import type { PageLoad } from './$types';

interface CategoryPageData {
  articles: IArticle[];
  ads: IAd[];
}

export const load: PageLoad = async ({ params, fetch }) => {
  const { slug } = params;
  try {
    const data = await api.get<CategoryPageData>(`/articles/?category_slug=${slug}`, fetch);
    const categoryData = await api.get<ICategory>(`/categories/slug/${slug}`, fetch);

    return {
      articles: data.articles,
      ads: data.ads,
      category: categoryData
    };
  } catch (error) {
    console.error('Failed to load category data:', error);
    return {
      articles: null,
      ads: [],
      category: null
    };
  }
};
