<script lang="ts">
	import { onMount } from 'svelte';
	import { api } from '$lib/services/api';
	import type { IAuthor } from '$lib/types/author';
	import Button from '$lib/components/ui/Button.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import Alert from '$lib/components/ui/Alert.svelte';
    import { adminStore } from '$lib/stores/authStore';

	let authors: IAuthor[] = $state([]);
	let loading = $state(true);
	let error = $state('');

	let isModalOpen = $state(false);
	let modalError = $state('');
	let modalLoading = $state(false);
	
	let currentAuthor: IAuthor | null = $state(null);
	
	let formState = $state({
		first_name: '',
		last_name: '',
		bio: ''
	});

	async function loadAuthors() {
		loading = true;
		error = '';
		try {
			const data = await api.get<{ authors: IAuthor[] }>('/admin/authors/');
			authors = data.authors;
		} catch (e: any) {
			error = e.message || 'Не вдалося завантажити авторів.';
		} finally {
			loading = false;
		}
	}

	onMount(loadAuthors);

	function openCreateModal() {
		currentAuthor = null;
		formState.first_name = '';
		formState.last_name = '';
		formState.bio = '';
		modalError = '';
		isModalOpen = true;
	}

	function openEditModal(author: IAuthor) {
		currentAuthor = author;
		formState.first_name = author.first_name;
		formState.last_name = author.last_name;
		formState.bio = author.bio || ''; // Враховуємо, що bio може бути null
		modalError = '';
		isModalOpen = true;
	}

	function closeModal() {
		isModalOpen = false;
	}

	async function handleSubmit() {
		modalLoading = true;
		modalError = '';
		try {
			if (currentAuthor) {
				await api.put(`/admin/authors/${currentAuthor.id}`, formState);
			} else {
				await api.post('/admin/authors', formState);
			}
			closeModal();
			await loadAuthors();
		} catch (e: any) {
			modalError = e.message || 'Помилка збереження.';
		} finally {
			modalLoading = false;
		}
	}

	async function handleDelete(authorId: number) {
		if (!confirm('Ви впевнені, що хочете видалити цього автора?')) {
			return;
		}
		
		try {
			await api.del(`/admin/authors/${authorId}`);
			await loadAuthors();
		} catch (e: any) {
			error = e.message || 'Помилка видалення.';
		}
	}
</script>

<svelte:head>
	<title>Адмін: Автори</title>
</svelte:head>

<div class="flex justify-between items-center mb-6">
	<h1 class="text-3xl font-bold">Управління Авторами</h1>
	<Button onclick={openCreateModal}>+ Створити Автора</Button>
</div>

{JSON.stringify($adminStore)}

{#if loading}
	<p>Завантаження...</p>
{:else if error}
	<Alert type="error">{error}</Alert>
{:else}
	<div class="bg-white shadow rounded-lg overflow-x-auto">
		<table class="min-w-full divide-y divide-gray-200">
			<thead class="bg-gray-50">
				<tr>
					<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
					<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ім'я</th>
					<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Прізвище</th>
					<th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Дії</th>
				</tr>
			</thead>
			<tbody class="bg-white divide-y divide-gray-200">
				{#each authors as author (author.id)}
					<tr>
						<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{author.id}</td>
						<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{author.first_name}</td>
						<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{author.last_name}</td>
						<td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
							<Button onclick={() => openEditModal(author)} class="!w-auto !py-1 !px-3">Редагувати</Button>
							<Button onclick={() => handleDelete(author.id)} class="!w-auto !py-1 !px-3 !bg-red-600 hover:!bg-red-700">Видалити</Button>
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/if}

{#if isModalOpen}
	<div class="fixed inset-0 z-10 flex items-center justify-center bg-black bg-opacity-50">
		<div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-md">
			<h2 class="text-2xl font-bold mb-4">
				{currentAuthor ? 'Редагувати Автора' : 'Створити Автора'}
			</h2>
			
			<form onsubmit={handleSubmit} class="space-y-4">
				{#if modalError}
					<Alert type="error">{modalError}</Alert>
				{/if}
				
				<Input name="first_name" label="Ім'я" required bind:value={formState.first_name} />
				<Input name="last_name" label="Прізвище" required bind:value={formState.last_name} />
				<div>
					<label for="bio" class="block text-sm font-medium text-gray-700">Біографія</label>
					<textarea
						id="bio"
						bind:value={formState.bio}
						rows="4"
						class="appearance-none block w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:outline-none sm:text-sm border-gray-300 focus:ring-indigo-500 focus:border-indigo-500"
					></textarea>
				</div>

				<div class="flex justify-end space-x-4 mt-6">
					<Button type="button" onclick={closeModal} class="!bg-gray-300 hover:!bg-gray-400 !text-black">Скасувати</Button>
					<Button type="submit" loading={modalLoading} class="!w-auto">{currentAuthor ? 'Зберегти' : 'Створити'}</Button>
				</div>
			</form>
		</div>
	</div>
{/if}