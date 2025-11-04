<script lang="ts">
	import ArticleCard from "$lib/components/ui/cards/ArticleCard.svelte";
	import Pagination from "$lib/components/ui/Pagination.svelte";
	import type { PageData } from "./$types";
	import { goto } from '$app/navigation';
	import Button from '$lib/components/ui/Button.svelte';
	import Input from '$lib/components/ui/Input.svelte';

	let { data }: { data: PageData } = $props();

	let query = $state(data.query || '');
	let date_from = $state(data.date_from || '');
	let date_to = $state(data.date_to || '');

	let articles = $derived(data.articles)
	$inspect(articles, data)

	function handleFilterSubmit() {
		const params = new URLSearchParams();
		if (query) params.set('q', query);
		if (date_from) params.set('date_from', date_from);
		if (date_to) params.set('date_to', date_to);
		params.set('page', '1');
		
		goto(`?${params.toString()}`);
	}
</script>

<svelte:head>
	<title>Результати пошуку: {data.query}</title>
</svelte:head>

<div class="max-w-4xl mx-auto">
	<h1 class="text-3xl font-bold text-gray-900 mb-4">
		Результати пошуку
	</h1>
	
	<form onsubmit={handleFilterSubmit} class="bg-white p-6 rounded-lg shadow-md mb-8 space-y-4">
		<Input name="q" label="Пошуковий запит" bind:value={query} />
		<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
			<Input name="date_from" label="Дата (від)" type="date" bind:value={date_from} />
			<Input name="date_to" label="Дата (до)" type="date" bind:value={date_to} />
		</div>
		<Button type="submit" class="!w-auto">
			Застосувати фільтри
		</Button>
	</form>
	{#if data.total > 0}
		<p class="text-lg text-gray-600 mb-8">
			За запитом: <span class="font-semibold text-gray-800">"{data.query}"</span>
			(знайдено {data.total}
			{data.total === 1 ? 'статтю' : data.total >= 2 && data.total <= 4 ? 'статті' : 'статей'})
		</p>
	{/if}

	{#if articles.length > 0}
		<div class="space-y-6">
			{#each articles as article (article.id)}
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
				Спробуйте змінити пошуковий запит або очистити фільтри дати.
			</p>
		</div>
	{:else}
		<div class="bg-white p-12 rounded-lg shadow-md text-center">
			<p class="text-gray-600 text-lg">
				Будь ласка, введіть пошуковий запит, щоб почати.
			</p>
		</div>
	{/if}
</div>