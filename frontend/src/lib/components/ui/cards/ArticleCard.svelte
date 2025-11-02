<script lang="ts">
	import type { IArticle } from "$lib/types/article";
	import { userStore } from "$lib/stores/authStore"; // 1. Імпорт store для перевірки прав
	import { api } from "$lib/services/api"; // 2. Імпорт API для відправки запиту

	let { article }: { article: IArticle } = $props();

	const canSave = $userStore?.permissions?.save_article;

	let isSaved = $state(false);
	let isLoading = $state(false);

	$effect(() => {
		isSaved = $userStore?.savedArticles?.includes(article.id) ?? false;
	});

	function formatDate(dateString: string) {
		return new Date(dateString).toLocaleDateString("uk-UA", {
			year: "numeric",
			month: "long",
			day: "numeric",
		});
	}

	async function handleToggleSave() {
		if (isLoading) return;
		isLoading = true;

		const originalState = isSaved;
		isSaved = !isSaved;

		try {
			const response = await api.post<{ is_saved: boolean }>(
				`/articles/${article.id}/toggle-save`,
				{},
			);
			isSaved = response.is_saved;
			userStore.update((user) => {
				if (!user) return user;
				const savedArticles = user.savedArticles || [];
				if (isSaved) {
					user.savedArticles = [...savedArticles, article.id];
				} else {
					user.savedArticles = savedArticles.filter(
						(a) => a !== article.id,
					);
				}
				return user;
			});
		} catch (error) {
			console.error("Failed to toggle save:", error);
			isSaved = originalState;
		} finally {
			isLoading = false;
		}
	}

	$inspect($userStore);
</script>

<article
	class="relative bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 ease-in-out"
>
	{#if canSave}
		<button
			onclick={handleToggleSave}
			disabled={isLoading}
			class="absolute top-4 right-4 z-10 p-2 rounded-full bg-black/10 backdrop-blur-sm
                   hover:bg-black/20 transition-colors duration-200
                   disabled:opacity-50 disabled:cursor-not-allowed"
			aria-label={isSaved ? "Видалити зі збережених" : "Зберегти статтю"}
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 24 24"
				class="w-5 h-5 text-white"
			>
				<path
					d="M17.59 3.00037H6.41C5.07 3.00037 4 4.07037 4 5.41037V21.0004L12 17.0004L20 21.0004V5.41037C20 4.07037 18.93 3.00037 17.59 3.00037Z"
					stroke-width="2"
					stroke={isSaved ? "#fff" : "none"}
					fill={isSaved ? "#fff" : "none"}
					stroke-linecap="round"
					stroke-linejoin="round"
					class="transition-all"
					style={isSaved
						? "fill-opacity: 1; stroke-opacity: 1;"
						: "stroke: #fff; fill: #000; fill-opacity: 0.2;"}
				/>
			</svg>
		</button>
	{/if}

	<div class="p-6">
		<div class="flex items-center gap-2 mb-3">
			{#if article.is_breaking}
				<span
					class="text-xs font-semibold uppercase px-3 py-1 rounded-full bg-red-100 text-red-700"
				>
					Термінова новина
				</span>
			{/if}
			{#if article.is_exclusive}
				<span
					class="text-xs font-semibold uppercase px-3 py-1 rounded-full bg-indigo-100 text-indigo-700"
				>
					Ексклюзив
				</span>
			{/if}
		</div>

		<h2 class="text-2xl font-bold mb-3 text-gray-900 leading-tight">
			<a
				href="/article/{article.id}"
				class="hover:text-indigo-600 transition-colors duration-200"
			>
				{article.title}
			</a>
		</h2>

		<div
			class="text-sm text-gray-500 flex flex-wrap items-center gap-x-3 gap-y-1"
		>
			<span>{article.author.first_name} {article.author.last_name}</span>
			<span class="text-gray-300 hidden md:inline">|</span>
			<span>{formatDate(article.created_at)}</span>
			{#if article.category}
				<span class="text-gray-300 hidden md:inline">|</span>
				<a
					href="/category/{article.category.name.toLowerCase()}"
					class="font-medium text-indigo-600 hover:underline"
				>
					{article.category.name}
				</a>
			{/if}
		</div>
	</div>
</article>
