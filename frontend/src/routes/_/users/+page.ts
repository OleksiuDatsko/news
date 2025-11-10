import { api } from '$lib/services/api';
import type { IUser } from '$lib/types/user';
import type { PageLoad } from './$types';

interface AdminUserData {
    users: IUser[];
    page: number;
    per_page: number;
    total: number;
}

export const load: PageLoad = async ({ fetch, url }) => {
    const page = url.searchParams.get('page') || '1';
    const perPage = '15'; 

    try {
        const data = await api.get<AdminUserData>(
            `/admin/users/?page=${page}&per_page=${perPage}`,
            fetch
        );
        return {
            users: data.users,
            page: data.page,
            perPage: data.per_page,
            total: data.total
        };
    } catch (error) {
        console.error('Failed to load admin users:', error);
        return {
            users: [],
            page: 1,
            perPage: 15,
            total: 0
        };
    }
};