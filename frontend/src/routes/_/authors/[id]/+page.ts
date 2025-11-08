import { api } from '$lib/services/api';
import type { IArticle } from '$lib/types/article';
import type { IAuthor } from '$lib/types/author';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch }) => {
    const { id } = params;
    try {
        const author = await api.get<IAuthor>(`/admin/authors/${id}`, fetch);
        const articles = await api.get<{articles: IArticle[]}>(`/admin/authors/${id}/articles`, fetch);
        return {
            author,
            articles: articles.articles
        };
    } catch (error) {
        console.error(`Failed to load author ${id}:`, error);
        return {
            author: null,
            articles: []

        };
    }
};