<script lang="ts">
	import { goto } from '$app/navigation';
	import { api } from '$lib/services/api';
	import Button from '$lib/components/ui/Button.svelte';
	import Alert from '$lib/components/ui/Alert.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	let new_password = $state('');
	let error = $state('');
	let success = $state('');
	let loading = $state(false);

	async function handleSubmit() {
		if (!data.admin || !new_password) return;

		loading = true;
		error = '';
		success = '';
		try {
			await api.put(`/admin/admin-users/${data.admin.id}/change-password`, {
				new_password
			});
			success = 'Пароль успішно змінено!';
			new_password = '';
		} catch (e: any) {
			error = e.message || 'Помилка оновлення пароля.';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Адмін: Зміна пароля для {data.admin?.email}</title>
</svelte:head>

{#if data.admin}
	<h1 class="text-3xl font-bold text-gray-900 mb-6">
		Зміна пароля для: {data.admin.email}
	</h1>

	<div class="bg-white p-8 rounded-lg shadow-lg max-w-2xl mx-auto">
		<form onsubmit={handleSubmit} class="space-y-6">
			{#if error}
				<Alert type="error">{error}</Alert>
			{/if}
			{#if success}
				<Alert type="success">{success}</Alert>
			{/if}

			<Input
				name="password"
				label="Новий Пароль"
				type="password"
				required
				bind:value={new_password}
			/>

			<div class="flex gap-4">
				<Button type="submit" {loading} class="!w-auto">
					Встановити новий пароль
				</Button>
				<a
					href="/_/admin-users"
					class="inline-flex items-center justify-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
				>
					Назад
				</a>
			</div>
		</form>
	</div>
{:else}
	<h1 class="text-3xl font-bold text-red-600 mb-6">Адміністратора не знайдено</h1>
	<Alert type="error">
		Не вдалося завантажити дані. Можливо, адміністратора було видалено.
	</Alert>
{/if}