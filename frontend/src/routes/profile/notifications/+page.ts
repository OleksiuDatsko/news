import { api } from '$lib/services/api';
import type { INotification } from '$lib/types/notification';
import type { PageLoad } from './$types';

interface NotificationData {
	notifications: INotification[];
	total: number;
	page: number;
	per_page: number;
}

export const load: PageLoad = async ({ fetch, url }) => {
	const page = url.searchParams.get('page') || '1';
	try {
		const data = await api.get<NotificationData>(
			`/notifications/all?page=${page}&per_page=10`,
			fetch
		);
		return {
			notifications: data.notifications,
			total: data.total,
			page: data.page,
			perPage: data.per_page
		};
	} catch (error) {
		console.error('Failed to load notifications:', error);
		return { notifications: [], total: 0, page: 1, perPage: 10 };
	}
};