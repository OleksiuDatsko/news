import { writable } from 'svelte/store';
import { api } from '$lib/services/api';
import type { INotification } from '$lib/types/notification';

type FetchFn = typeof fetch;

type NotificationStore = {
	notifications: INotification[];
	unread_count: number;
	loaded: boolean;
};

export const notificationStore = writable<NotificationStore>({
	notifications: [],
	unread_count: 0,
	loaded: false
});

export async function loadNotifications(customFetch?: FetchFn) {
	try {
		const data = await api.get<{
			notifications: INotification[];
			unread_count: number;
		}>('/notifications/', customFetch);

		notificationStore.set({
			notifications: data.notifications,
			unread_count: data.unread_count,
			loaded: true
		});
	} catch (error) {
		console.error('Failed to load notifications:', error);
		notificationStore.set({
			notifications: [],
			unread_count: 0,
			loaded: true
		});
	}
}

export function markOneAsRead(notificationId: number) {
	notificationStore.update((store) => {
		return {
			...store,
			notifications: store.notifications.filter((n) => n.id !== notificationId),
			unread_count: Math.max(0, store.unread_count - 1)
		};
	});
}

export function markAllAsRead() {
	notificationStore.update((store) => {
		return {
			...store,
			notifications: [],
			unread_count: 0
		};
	});
}