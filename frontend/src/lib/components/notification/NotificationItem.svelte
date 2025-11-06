<script lang="ts">
	import type { INotification } from '$lib/types/notification';
	import { api } from '$lib/services/api';
	import { markOneAsRead } from '$lib/stores/notificationStore';
	import { goto } from '$app/navigation';

	let { notification }: { notification: INotification } = $props();

	let loading = $state(false);

	async function handleClick() {
		if (loading) return;
		loading = true;

		try {
			await api.post(`/notifications/${notification.id}/read`, {});
			markOneAsRead(notification.id);
			if (notification.article_id) {
				await goto(`/articles/${notification.article_id}`);
			}
		} catch (e) {
			console.error('Failed to mark notification as read', e);
			loading = false;
		}
	}
</script>

<button
	onclick={handleClick}
	disabled={loading}
	class="block w-full text-left px-4 py-3 text-sm text-gray-700 hover:bg-gray-100
		   transition-colors duration-150 disabled:opacity-50 border-b border-gray-100 last:border-b-0"
>
	<span class="font-semibold block text-gray-800">{@html notification.title ?? 'Нове сповіщення'}</span>
	<span class="text-xs text-gray-500">{@html notification.message ?? '...'}</span>
</button>