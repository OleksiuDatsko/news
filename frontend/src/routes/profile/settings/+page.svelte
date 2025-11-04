<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
	import Alert from '$lib/components/ui/Alert.svelte';
	import { api } from '$lib/services/api';
	import { userStore } from '$lib/stores/authStore';
	import { categoryStore } from '$lib/stores/categoryStore';
	import type { IUser } from '$lib/types/user';

	let allCategories = $derived($categoryStore);

	let dailyDigest = $state($userStore?.preferences?.dailyDigest ?? true);
	let authorNews = $state($userStore?.preferences?.authorNews ?? false);
	let breakingNews = $state($userStore?.preferences?.breakingNews ?? true);
	let favorite_categories = $state($userStore?.preferences?.favorite_categories ?? []);

	let error = $state('');
	let success = $state('');
	let loading = $state(false);

	async function handleSubmit() {
		loading = true;
		error = '';
		success = '';

		const newPreferences = {
			dailyDigest,
			authorNews,
			breakingNews,
			favorite_categories
		};

		try {
			const { user } = await api.put<{ user: IUser }>('/auth/me/preferences', newPreferences);

			userStore.update((currentUser) => {
				if (!currentUser) return null;
				currentUser.preferences = user.preferences;
				return { ...currentUser };
			});

			success = 'Налаштування успішно збережено!';
		} catch (e: any) {
			error = e.message || 'Не вдалося зберегти налаштування.';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Налаштування</title>
</svelte:head>

<div class="max-w-2xl mx-auto">
	<a href="/profile" class="text-indigo-600 hover:underline text-sm">&larr; Назад до профілю</a>
	<h1 class="text-3xl font-bold text-gray-900 mt-2 mb-8">
		Налаштування
	</h1>

	<div class="bg-white p-8 rounded-lg shadow-lg border border-gray-100">
		<form onsubmit={handleSubmit} class="space-y-6">
			{#if error}
				<Alert type="error">{error}</Alert>
			{/if}
			{#if success}
				<Alert type="success">{success}</Alert>
			{/if}

			<fieldset class="space-y-4">
				<legend class="text-lg font-semibold text-gray-800 border-b pb-2">Сповіщення</legend>

				<div class="flex items-center justify-between">
					<label for="breakingNews" class="font-medium text-gray-700">Термінові новини</label>
					<input
						id="breakingNews"
						type="checkbox"
						bind:checked={breakingNews}
						class="h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
					/>
				</div>

				<div class="flex items-center justify-between">
					<label for="dailyDigest" class="font-medium text-gray-700">Щоденний дайджест</label>
					<input
						id="dailyDigest"
						type="checkbox"
						bind:checked={dailyDigest}
						class="h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
					/>
				</div>

				<div class="flex items-center justify-between">
					<label for="authorNews" class="font-medium text-gray-700">
						Новини від улюблених авторів (незабаром)
					</label>
					<input
						id="authorNews"
						type="checkbox"
						bind:checked={authorNews}
						disabled
						class="h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded disabled:bg-gray-200"
					/>
				</div>
			</fieldset>

			<fieldset class="space-y-3 pt-4">
				<legend class="text-lg font-semibold text-gray-800 border-b pb-2">
					Улюблені рубрики (для рекомендацій)
				</legend>
				<div class="grid grid-cols-2 gap-x-4 gap-y-2">
					{#if allCategories.length > 0}
						{#each allCategories as category (category.id)}
							<div class="flex items-center">
								<input
									id="cat-{category.id}"
									type="checkbox"
									value={category.slug}
									bind:group={favorite_categories}
									class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
								/>
								<label for="cat-{category.id}" class="ml-2 block text-sm text-gray-700">
									{category.name}
								</label>
							</div>
						{/each}
					{:else}
						<p class="text-sm text-gray-500">Завантаження категорій...</p>
					{/if}
				</div>
			</fieldset>

			<div class="border-t pt-6">
				<Button type="submit" loading={loading} class="!w-auto">
					Зберегти зміни
				</Button>
			</div>
		</form>
	</div>
</div>