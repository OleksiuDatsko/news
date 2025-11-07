<script lang="ts">
	import ArticleCard from "$lib/components/ui/cards/ArticleCard.svelte";
	import Pagination from "$lib/components/ui/Pagination.svelte";
	import type { PageData } from "./$types";
	import { userStore } from "$lib/stores/authStore";
	import { api } from "$lib/services/api";
	import Button from "$lib/components/ui/Button.svelte";

	let { data }: { data: PageData } = $props();

	let isFollowing = $state(data.is_following);
	let isLoadingFollow = $state(false);

	async function handleToggleFollow() {
		if (!data.author) return;
		isLoadingFollow = true;

		try {
			const response = await api.post<{ is_following: boolean }>(
				`/authors/${data.author.id}/toggle-follow`,
				{},
			);
			isFollowing = response.is_following;
			userStore.update((user) => {
				if (!user || !data.author) return user;

				const favs = user.followed_authors || [];

				if (isFollowing) {
					if (!favs.includes(data.author.id)) {
						user.followed_authors = [...favs, data.author.id];
					}
				} else {
					user.followed_authors = favs.filter(
						(id) => id !== data.author.id,
					);
				}
				return { ...user };
			});
		} catch (e: any) {
			console.error("Помилка підписки:", e);
			isFollowing = !isFollowing;
		} finally {
			isLoadingFollow = false;
		}
	}
</script>

<svelte:head>
	<title>
		{data.author
			? `${data.author.first_name} ${data.author.last_name}`
			: "Автор не знайдений"}
	</title>
	{#if data.author?.bio}
		<meta name="description" content={data.author.bio.substring(0, 150)} />
	{/if}
</svelte:head>

<div class="max-w-4xl mx-auto">
	{#if data.author}
		<div class="mb-12 p-6 bg-white rounded-lg shadow-md">
			<div class="flex justify-between items-start">
				<div>
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
				
				{#if $userStore}
					<Button
						onclick={handleToggleFollow}
						loading={isLoadingFollow}
						class="!w-auto ml-4 {isFollowing ?
							'!bg-gray-200 !text-gray-800 hover:!bg-gray-300'
							: '!bg-green-600 hover:!bg-green-700'}"
					>
						{isFollowing ? 'Відстежується' : 'Слідкувати'}
					</Button>
				{/if}
				</div>
		</div>

		<h2 class="text-3xl font-bold text-gray-900 mb-8">Статті автора</h2>
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
