import { api } from '$lib/services/api';
import type { IArticle } from '$lib/types/article';
import type { PageLoad } from './$types';
import { userStore } from '$lib/stores/authStore';
import { get } from 'svelte/store';
import { goto } from '$app/navigation';

export const load: PageLoad = async ({ fetch }) => {
    const user = get(userStore);

    if (!user?.permissions?.save_article) {
        await goto('/profile');
        return { articles: [] };
    }

    try {
        const savedArticles = await api.get<IArticle[]>(
            '/articles/saved',
            fetch
        );

        return {
            articles: savedArticles
        };
    } catch (error) {
        console.error('Failed to load saved articles:', error);
        return {
            articles: []
        };
    }
};