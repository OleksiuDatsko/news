<script lang="ts">
	import { adminStore, userStore } from '$lib/stores/authStore';
	import { api } from '$lib/services/api';
	import { goto } from '$app/navigation';

	async function handleLogout() {
		if ($userStore) {
			await api.post('/auth/logout', {});
			userStore.set(null);
		} else if ($adminStore) {
			await api.post('/admin/auth/logout', {});
			adminStore.set(null);
		}
		await goto('/');
	}
</script>

<header class="bg-white shadow-sm sticky top-0 z-50 border-b border-gray-200">
	<nav class="container mx-auto px-4">
		<div class="flex justify-between items-center h-16">
			<div class="flex items-center gap-6">
				<a href="/" class="text-2xl font-bold text-indigo-600">
					NewsApp
				</a>

				<div class="hidden md:flex gap-5">
					<a href="/" class="text-sm font-medium text-gray-700 hover:text-indigo-600">
						Головна
					</a>
					<a
						href="/category/politics"
						class="text-sm font-medium text-gray-700 hover:text-indigo-600"
					>
						Політика
					</a>
					<a
						href="/category/sport"
						class="text-sm font-medium text-gray-700 hover:text-indigo-600"
					>
						Спорт
					</a>
					<a
						href="/category/tech"
						class="text-sm font-medium text-gray-700 hover:text-indigo-600"
					>
						Технології
					</a>
				</div>
			</div>

			<div class="flex items-center gap-4">
				{#if $userStore}
					<span class="text-sm text-gray-600 hidden sm:block">
						Вітаємо,
						<a href="/profile" class="font-medium text-gray-900 hover:underline">
							{$userStore.username}
						</a>
					</span>
					<button
						onclick={handleLogout}
						class="text-sm font-medium text-gray-700 hover:text-indigo-600"
					>
						Вийти
					</button>
				{:else if $adminStore}
					<span class="text-sm text-gray-600 hidden sm:block">
						Admin:
						<a href="/_/dashboard" class="font-medium text-gray-900 hover:underline">
							Dashboard
						</a>
					</span>
					<button
						onclick={handleLogout}
						class="text-sm font-medium text-gray-700 hover:text-indigo-600"
					>
						Вийти
					</button>
				{:else}
					<a
						href="/auth/login"
						class="text-sm font-medium text-gray-700 hover:text-indigo-600"
					>
						Увійти
					</a>
					<a
						href="/auth/register"
						class="text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded-md transition-colors shadow-sm"
					>
						Реєстрація
					</a>
				{/if}
			</div>
		</div>
	</nav>
</header>