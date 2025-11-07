<script lang="ts">
	import ArticleCard from '$lib/components/ui/cards/ArticleCard.svelte';
	import Pagination from '$lib/components/ui/Pagination.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>
		{data.author ?
			`${data.author.first_name} ${data.author.last_name}`
			: 'Автор не знайдений'}
	</title>
	{#if data.author?.bio}
		<meta name="description" content={data.author.bio.substring(0, 150)} />
	{/if}
</svelte:head>

<div class="max-w-4xl mx-auto">
	{#if data.author}
		<div class="mb-12 p-6 bg-white rounded-lg shadow-md">
			<h1 class="text-4xl font-bold text-gray-900 mb-2">
				{data.author.first_name} {data.author.last_name}
			</h1>
			<p class="text-lg text-gray-700">
				{data.author.bio || 'Біографія автора відсутня.'}
			</p>
			<p class="text-sm text-gray-500 mt-4">
				Всього опубліковано статей (на сайті): {data.total}
			</p>
		</div>

		<h2 class="text-3xl font-bold text-gray-900 mb-8">
			Статті автора
		</h2>
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
		{:else}
			<div class="bg-white p-12 rounded-lg shadow-md text-center">
				<p class="text-gray-600 text-lg">
					У цього автора ще немає опублікованих статей.
				</p>
			</div>
		{/if}
	{:else}
		<div class="bg-white p-12 rounded-lg shadow-md text-center">
			<h1 class="text-2xl font-bold text-red-600">Помилка</h1>
			<p class="text-gray-600 mt-4">
				Не вдалося завантажити дані про автора. Можливо, його не існує.
			</p>
			<a href="/" class="text-indigo-600 hover:underline mt-4 block">
				Повернутися на головну
			</a>
		</div>
	{/if}
</div>