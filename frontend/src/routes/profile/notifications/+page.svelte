<script lang="ts">
	import type { PageData } from './$types';
	import Pagination from '$lib/components/ui/Pagination.svelte';
    import NotificationHistoryItem from '$lib/components/notification/NotificationHistoryItem.svelte';

	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>Історія сповіщень</title>
</svelte:head>

<div class="max-w-3xl mx-auto">
	<a href="/profile" class="text-indigo-600 hover:underline text-sm">&larr; Назад до профілю</a>
	<h1 class="text-3xl font-bold text-gray-900 mt-2 mb-8">
		Історія сповіщень
	</h1>

	{#if data.notifications && data.notifications.length > 0}
		<ul class="space-y-4">
			{#each data.notifications as notification (notification.id)}
				<NotificationHistoryItem {notification} />
			{/each}
		</ul>

		<Pagination
			currentPage={data.page}
			perPage={data.perPage}
			totalItems={data.total}
		/>
	{:else}
		<div class="bg-white p-12 rounded-lg shadow-md text-center">
			<p class="text-gray-600 text-lg">
				У вас ще немає жодних сповіщень.
			</p>
		</div>
	{/if}
</div>