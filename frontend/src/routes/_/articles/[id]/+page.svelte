<script lang="ts">
	import { goto } from '$app/navigation';
	import { api } from '$lib/services/api';
	import Button from '$lib/components/ui/Button.svelte';
	import Alert from '$lib/components/ui/Alert.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	let title = $state(data.article?.title ?? '');
	let content = $state(data.article?.content ?? '');
	let author_id = $state(data.article?.author.id ?? null);
	let category_id = $state(data.article?.category?.id ?? null);
	let status = $state(data.article?.status ?? 'draft');
	let is_exclusive = $state(data.article?.is_exclusive ?? false);
	let is_breaking = $state(data.article?.is_breaking ?? false);

	let error = $state('');
	let loading = $state(false);

	async function handleSubmit() {
		if (!data.article) return;
		
		loading = true;
		error = '';

		if (!author_id) {
			error = "Будь ласка, оберіть автора.";
			loading = false;
			return;
		}

		try {
			await api.put(`/admin/articles/${data.article.id}`, {
				title,
				content,
				author_id,
				category_id: category_id || undefined,
				status,
				is_exclusive,
				is_breaking
			});
			await goto('/_/articles');
		} catch (e: any) {
			error = e.message || 'Помилка оновлення статті.';
		} finally {
			loading = false;
		}
	}

	const statuses = [
		{ value: 'draft', label: 'Чернетка' },
		{ value: 'published', label: 'Опубліковано' },
		{ value: 'archived', label: 'Архівовано' }
	];
</script>

<svelte:head>
	<title>Адмін: Редагувати {data.article?.title ?? 'Стаття'}</title>
</svelte:head>

{#if data.article}
	<h1 class="text-3xl font-bold text-gray-900 mb-6">
		Редагувати: {data.article.title}
	</h1>

	<div class="bg-white p-8 rounded-lg shadow-lg max-w-4xl mx-auto">
		<form onsubmit={handleSubmit} class="space-y-6">
			{#if error}
				<Alert type="error">{error}</Alert>
			{/if}

			<Input name="title" label="Заголовок" required bind:value={title} />

			<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
				<div>
					<label for="author" class="block text-sm font-medium text-gray-700">
						Автор
					</label>
					<select
						id="author"
						name="author"
						required
						bind:value={author_id}
						class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
					>
						<option value={null} disabled>Оберіть автора...</option>
						{#each data.authors as author (author.id)}
							<option value={author.id}>
								{author.first_name} {author.last_name}
							</option>
						{/each}
					</select>
				</div>
				<div>
					<label for="category" class="block text-sm font-medium text-gray-700">
						Категорія (optional)
					</label>
					<select
						id="category"
						name="category"
						bind:value={category_id}
						class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
					>
						<option value={null}>Без категорії...</option>
						{#each data.categories as category (category.id)}
							<option value={category.id}>{category.name}</option>
						{/each}
					</select>
				</div>
			</div>

			<div>
				<label for="content" class="block text-sm font-medium text-gray-700">
					Вміст статті
				</label>
				<div class="mt-1">
					<textarea
						id="content"
						name="content"
						rows={10}
						required
						bind:value={content}
						class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
					></textarea>
				</div>
			</div>

			<div>
				<label for="status" class="block text-sm font-medium text-gray-700">
					Статус
				</label>
				<select
					id="status"
					name="status"
					bind:value={status}
					class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
				>
					{#each statuses as s (s.value)}
						<option value={s.value}>{s.label}</option>
					{/each}
				</select>
			</div>

			<div class="flex items-center gap-6">
				<div class="flex items-center">
					<input
						id="is_exclusive"
						name="is_exclusive"
						type="checkbox"
						bind:checked={is_exclusive}
						class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
					/>
					<label for="is_exclusive" class="ml-2 block text-sm text-gray-900">
						Ексклюзив
					</label>
				</div>
				<div class="flex items-center">
					<input
						id="is_breaking"
						name="is_breaking"
						type="checkbox"
						bind:checked={is_breaking}
						class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
					/>
					<label for="is_breaking" class="ml-2 block text-sm text-gray-900">
						Термінова новина
					</label>
				</div>
			</div>

			<div class="flex gap-4">
				<Button type="submit" {loading} class="!w-auto">
					Зберегти Зміни
				</Button>
				<a
					href="/_/articles"
					class="inline-flex items-center justify-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
				>
					Скасувати
				</a>
			</div>
		</form>
	</div>
{:else}
	<h1 class="text-3xl font-bold text-red-600 mb-6">Статтю не знайдено</h1>
	<Alert type="error">
		Не вдалося завантажити дані. Можливо, статтю було видалено.
	</Alert>
	<a href="/_/articles" class="text-indigo-600 hover:underline mt-4 inline-block">
		&larr; Повернутися до списку статей
	</a>
{/if}