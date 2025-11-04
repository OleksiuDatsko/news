<script lang="ts">
	import { adminStore, userStore } from "$lib/stores/authStore";
	import { categoryStore } from "$lib/stores/categoryStore";
	import { goto } from "$app/navigation";

	let topCategories = $derived($categoryStore.slice(0, 3));

	let searchTerm = $state("");

	function handleSearch(event: Event) {
		event.preventDefault();
		if (searchTerm.trim()) {
			goto(`/search?q=${encodeURIComponent(searchTerm.trim())}`);
			searchTerm = "";
		}
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
					<a
						href="/"
						class="text-sm font-medium text-gray-700 hover:text-indigo-600"
					>
						Головна
					</a>
					{#if topCategories.length > 0}
						{#each topCategories as category (category.id)}
							<a
								href="/categories/{category.slug}"
								class="text-sm font-medium text-gray-700 hover:text-indigo-600"
							>
								{category.name}
							</a>
						{/each}
					{/if}
				</div>
			</div>
			<div class="flex-1 px-4 max-w-lg mx-auto">
				<form onsubmit={handleSearch} class="w-full">
					<input
						type="search"
						bind:value={searchTerm}
						placeholder="Пошук за ключовим словом, автором..."
						class="block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm
						   focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
					/>
				</form>
			</div>
			<div class="flex items-center gap-4">
				{#if $userStore}
					<span class="text-sm text-gray-600 hidden sm:block">
						Вітаємо,
						<a
							href="/profile"
							class="font-medium text-gray-900 hover:underline"
						>
							{$userStore.username}
						</a>
					</span>
				{:else if $adminStore}
					<span class="text-sm text-gray-600 hidden sm:block">
						Admin:
						<a
							href="/_/dashboard"
							class="font-medium text-gray-900 hover:underline"
						>
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
