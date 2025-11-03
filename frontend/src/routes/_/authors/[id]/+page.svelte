<script lang="ts">
	import { goto } from '$app/navigation';
	import { api } from '$lib/services/api';
	import Button from '$lib/components/ui/Button.svelte';
	import Alert from '$lib/components/ui/Alert.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	let first_name = $state(data.author?.first_name ?? '');
	let last_name = $state(data.author?.last_name ?? '');
	let bio = $state(data.author?.bio ?? '');
	let error = $state('');
	let loading = $state(false);

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
</script>

<svelte:head>
	<title>Адмін: Редагувати {data.author?.first_name ?? 'Автор'}</title>
</svelte:head>

{#if data.author}
	<h1 class="text-3xl font-bold text-gray-900 mb-6">
		Редагувати: {data.author.first_name} {data.author.last_name}
	</h1>

	<div class="bg-white p-8 rounded-lg shadow-lg max-w-2xl">
		<form onsubmit={handleSubmit} class="space-y-6">
			{#if error}
				<Alert type="error">{error}</Alert>
			{/if}

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
{:else}
	<h1 class="text-3xl font-bold text-red-600 mb-6">Автора не знайдено</h1>
	<Alert type="error">
		Не вдалося завантажити дані. Можливо, автора було видалено.
	</Alert>
	<a href="/_/authors" class="text-indigo-600 hover:underline mt-4 inline-block">
		&larr; Повернутися до списку авторів
	</a>
{/if}