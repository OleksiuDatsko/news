import { api } from '$lib/services/api';
import type { IAuthor } from '$lib/types/author';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
    try {
        const data = await api.get<{ authors: IAuthor[] }>('/admin/authors/', fetch);
        return {
            authors: data.authors
        };
    } catch (error) {
        console.error('Failed to load authors:', error);
        return {
            authors: []
        };
    }
};