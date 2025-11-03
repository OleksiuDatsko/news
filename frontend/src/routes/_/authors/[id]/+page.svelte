<script lang="ts">
	import { goto } from '$app/navigation';
	import { api } from '$lib/services/api';
	import Button from '$lib/components/ui/Button.svelte';
	import Alert from '$lib/components/ui/Alert.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import type { PageData } from './$types'; 
    import SmallArticleCard from '$lib/components/ui/cards/SmallArticleCard.svelte';

	let { data }: { data: PageData } = $props();

	// Логіка форми з оригінального файлу 
	let first_name = $state(data.author?.first_name ?? '');
	let last_name = $state(data.author?.last_name ?? '');
	let bio = $state(data.author?.bio ?? '');
	let error = $state('');
	let loading = $state(false);

	// Додаємо $effect для синхронізації, якщо дані оновляться
	$effect(() => {
		first_name = data.author?.first_name ?? '';
		last_name = data.author?.last_name ?? '';
		bio = data.author?.bio ?? '';
	});

	async function handleSubmit() { 
		if (!data.author) return;
		loading = true;
		error = '';
		try {
			await api.put(`/admin/authors/${data.author.id}`, {
				first_name,
				last_name,
				bio
			});
			await goto('/_/authors');
		} catch (e: any) {
			error = e.message || 'Помилка оновлення автора.';
		} finally {
			loading = false;
		} 
	}

	// Функція для форматування дати (з іншої сторінки) 
	function formatDate(dateString: string) {
		return new Date(dateString).toLocaleDateString('uk-UA', {
			year: 'numeric',
			month: 'long',
			day: 'numeric'
		});
	}
</script>

<svelte:head>
	<title>Адмін: Редагувати {data.author?.first_name ?? 'Автор'}</title> 
</svelte:head>

{#if data.author}
	<h1 class="text-3xl font-bold text-gray-900 mb-6">
		Редагувати: {data.author.first_name} {data.author.last_name}
	</h1>

	{#if error}
		<Alert type="error">{error}</Alert>
	{/if}

	<div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
		<div class="lg:col-span-2">
			<div class="bg-white p-8 rounded-lg shadow-lg">
				<form onsubmit={handleSubmit} class="space-y-6">
					<Input name="first_name" label="Ім'я" required bind:value={first_name} />
					<Input name="last_name" label="Прізвище" required bind:value={last_name} />

					<div>
						<label for="bio" class="block text-sm font-medium text-gray-700">
							Біографія (optional)
						</label>
						<div class="mt-1">
							<textarea
								id="bio"
								name="bio"
								rows={4}
								bind:value={bio}
								class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
							></textarea>
						</div>
					</div>

					<div class="flex gap-4">
						<Button type="submit" {loading} class="!w-auto">
							Зберегти Зміни
						</Button>
						<a
							href="/_/authors"
							class="inline-flex items-center justify-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
						>
							Скасувати
						</a>
					</div>
				</form>
			</div>
		</div>

		<div class="lg:col-span-1">
			<div class="bg-white p-6 rounded-lg shadow-lg">
				<h2 class="text-xl font-bold text-gray-900 mb-4">
					Статті цього автора ({data.articles.length})
				</h2>
				{#if data.articles.length > 0}
					<ul class="space-y-4">
						{#each data.articles as article (article.id)}
							<li class="border-b pb-3">
                            <SmallArticleCard {article} />
							</li>
						{/each}
					</ul>
				{:else}
					<p class="text-sm text-gray-500">
						У цього автора ще немає статей.
					</p>
				{/if}
			</div>
		</div>
	</div>
	{:else}
	<h1 class="text-3xl font-bold text-red-600 mb-6">Автора не знайдено</h1>
	<Alert type="error">
		Не вдалося завантажити дані. Можливо, автора було видалено.
	</Alert>
	<a href="/_/authors" class="text-indigo-600 hover:underline mt-4 inline-block">
		&larr; Повернутися до списку авторів
	</a>
{/if}