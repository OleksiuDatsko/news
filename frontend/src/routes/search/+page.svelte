<script lang="ts">
	import ArticleCard from "$lib/components/ui/cards/ArticleCard.svelte";
	import Pagination from "$lib/components/ui/Pagination.svelte";
	import type { PageData } from "./$types";

	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>Результати пошуку: {data.query}</title>
</svelte:head>

<div class="max-w-4xl mx-auto">
	<h1 class="text-3xl font-bold text-gray-900 mb-4">
		Результати пошуку
	</h1>
	
	{#if data.query}
		<p class="text-lg text-gray-600 mb-8">
			За запитом: <span class="font-semibold text-gray-800">"{data.query}"</span>
			{#if data.total > 0}
				(знайдено {data.total}
				{data.total === 1 ? 'статтю' : data.total >= 2 && data.total <= 4 ? 'статті' : 'статей'})
			{/if}
		</p>
	{/if}

	{#if data.articles.length > 0}
		<div class="space-y-6">
			{#each data.articles as article (article.id)}
				<ArticleCard {article} />
			{/each}
		</div>

		<Pagination
			currentPage={data.page}
			perPage={data.perPage}
			totalItems={data.total}
		/>
	{:else if data.query}
		<div class="bg-white p-12 rounded-lg shadow-md text-center">
			<p class="text-gray-600 text-lg">
				На жаль, за вашим запитом нічого не знайдено.
			</p>
			<p class="text-sm text-gray-500 mt-2">
				Спробуйте змінити пошуковий запит.
			</p>
		</div>
	{:else}
		<div class="bg-white p-12 rounded-lg shadow-md text-center">
			<p class="text-gray-600 text-lg">
				Будь ласка, введіть пошуковий запит у поле вище.
			</p>
		</div>
	{/if}
</div>