<script lang="ts">
	import { goto } from '$app/navigation';
	import { api } from '$lib/services/api';
	import Button from '$lib/components/ui/Button.svelte';
	import Alert from '$lib/components/ui/Alert.svelte';
	import Input from '$lib/components/ui/Input.svelte';

	let email = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);

	async function handleSubmit() {
		loading = true;
		error = '';
		try {
			
			await api.post('/admin/auth/register', {
				email,
				password
			});
			await goto('/_/admin-users');
		} catch (e: any) {
			error = e.message || 'Помилка створення адміністратора.';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Адмін: Новий Адміністратор</title>
</svelte:head>

<h1 class="text-3xl font-bold text-gray-900 mb-6">Створити Нового Адміністратора</h1>

<div class="bg-white p-8 rounded-lg shadow-lg max-w-2xl mx-auto">
	<form onsubmit={handleSubmit} class="space-y-6">
		{#if error}
			<Alert type="error">{error}</Alert>
		{/if}

		<Input name="email" label="Email" type="email" required bind:value={email} />
		<Input name="password" label="Пароль" type="password" required bind:value={password} />

		<div class="flex gap-4">
			<Button type="submit" {loading} class="!w-auto">
				Створити
			</Button>
			<a
				href="/_/admin-users"
				class="inline-flex items-center justify-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
			>
				Скасувати
			</a>
		</div>
	</form>
</div>