<script lang="ts">
	import { userStore } from '$lib/stores/authStore';
	import { api } from '$lib/services/api';
	import { goto } from '$app/navigation';
	import Button from '$lib/components/ui/Button.svelte';

	let error = $state('');
	let loading = $state(false);

	async function handleLogout() {
		loading = true;
		error = '';
		try {
			await api.post('/auth/logout', {});
			userStore.set(null);
			await goto('/');
		} catch (e: any) {
			error = e.message || 'Помилка виходу';
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Мій Профіль</title>
</svelte:head>

<div class="max-w-4xl mx-auto">
	<h1 class="text-3xl font-bold text-gray-900 mb-4">
		Вітаємо, {$userStore?.username}!
	</h1>
	<p class="text-lg text-gray-600 mb-8">
		Це ваш особистий кабінет. Тут ви можете керувати своїми налаштуваннями, підписками та збереженими статтями.
	</p>

	<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
		
		{#if $userStore?.permissions?.save_article}
			<a
				href="/profile/saved"
				class="group bg-white p-6 rounded-lg shadow-lg hover:shadow-xl
					   border border-gray-100 hover:border-indigo-500
					   transition-all duration-300 ease-in-out transform hover:-translate-y-1"
			>
				<h3
					class="text-lg font-semibold text-gray-900 group-hover:text-indigo-600 transition-colors duration-300"
				>
					Збережені статті
				</h3>
				<p class="mt-1 text-sm text-gray-500">
					Переглянути статті, які ви додали для читання пізніше.
				</p>
				<div
					class="mt-4 text-sm font-medium text-indigo-600 group-hover:text-indigo-700"
				>
					Перейти &rarr;
				</div>
			</a>
		{/if}

		<a
			href="/profile/subscription"
			class="group bg-white p-6 rounded-lg shadow-lg hover:shadow-xl
				   border border-gray-100 hover:border-indigo-500
				   transition-all duration-300 ease-in-out transform hover:-translate-y-1"
		>
			<h3
				class="text-lg font-semibold text-gray-900 group-hover:text-indigo-600 transition-colors duration-300"
			>
				Моя підписка
			</h3>
			<p class="mt-1 text-sm text-gray-500">
				Керувати вашим поточним планом та переглянути доступні.
			</p>
			<div
				class="mt-4 text-sm font-medium text-indigo-600 group-hover:text-indigo-700"
			>
				Перейти &rarr;
			</div>
		</a>

		<a
			href="/profile/settings"
			class="group bg-white p-6 rounded-lg shadow-lg hover:shadow-xl
				   border border-gray-100 hover:border-indigo-500
				   transition-all duration-300 ease-in-out transform hover:-translate-y-1"
		>
			<h3
				class="text-lg font-semibold text-gray-900 group-hover:text-indigo-600 transition-colors duration-300"
			>
				Налаштування
			</h3>
			<p class="mt-1 text-sm text-gray-500">
				Керувати сповіщеннями та улюбленими темами.
			</p>
			<div
				class="mt-4 text-sm font-medium text-indigo-600 group-hover:text-indigo-700"
			>
				Перейти &rarr;
			</div>
		</a>
	</div>

	<div class="bg-white p-6 rounded-lg shadow-lg border border-gray-100">
		<h2 class="text-xl font-bold text-gray-900 mb-3">Вихід з акаунту</h2>
		<p class="text-sm text-gray-600 mb-4">
			Ви увійшли як: <span class="font-medium">{$userStore?.email}</span>
		</p>
		<Button onclick={handleLogout} loading={loading} class="!w-auto !bg-red-600 hover:!bg-red-700">
			Вийти з акаунту
		</Button>
	</div>
</div>