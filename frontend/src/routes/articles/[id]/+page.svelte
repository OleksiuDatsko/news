<script lang="ts">
    import type { PageData } from "./$types";
    import { userStore } from "$lib/stores/authStore";
    import { api } from "$lib/services/api";
    import AdCard from "$lib/components/ui/cards/AdCard.svelte";
    import CommentList from "$lib/components/comments/CommentList.svelte";
    import { error } from "@sveltejs/kit";
    import { onMount } from "svelte";

    let { data }: { data: PageData } = $props();

    let article = $state(data.article);
    let isLoadingSave = $state(false);
    let isLoadingLike = $state(false);
    let isSaved = $state(false);
    let isLiked = $state(false);
    let likesCount = $state(0);

    onMount(() => {
		if (article) {
			const key = `viewed_article_${article.id}`;
			if (!sessionStorage.getItem(key)) {
				api.post(`/articles/${article.id}/impression`, {})
					.then(() => {
						sessionStorage.setItem(key, 'true');
						console.log(`View tracked for article ${article.id}`);
					})
					.catch((err) => {
						console.error('Failed to track article view', err);
					});
			}
		}
	});

    $effect(() => {
        isSaved = article?.is_saved ?? false;
        isLiked = article?.is_liked ?? false;
        likesCount = article?.likes_count ?? 0;
    });

    const canSave = $userStore?.permissions?.save_article;
    const canLike = !!$userStore;

    function formatDate(dateString: string) {
        return new Date(dateString).toLocaleDateString("uk-UA", {
            year: "numeric",
            month: "long",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        });
    }

    async function handleToggleSave() {
        if (isLoadingSave || !article) return;
        isLoadingSave = true;

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
            isLoadingSave = false;
        }
    }

    async function handleToggleLike() {
        if (isLoadingLike || !article) return;
        isLoadingLike = true;

        const originalState = isLiked;
        isLiked = !isLiked;
        if (isLiked) {
            likesCount = likesCount + 1;
        } else {
            likesCount = Math.max(0, likesCount - 1); // Захист від < 0
        }

        try {
            const response = await api.post<{ is_liked: boolean }>(
                `/articles/${article.id}/toggle-like`,
                {},
            );
            isLiked = response.is_liked;
        } catch (error) {
            console.error("Failed to toggle like:", error);
            isLiked = originalState;
        } finally {
            isLoadingLike = false;
        }
    }
</script>

<svelte:head>
    <title>{article?.title ?? "Стаття не знайдена"}</title>
</svelte:head>

{#if article}
    <div
        class={`grid ${data.ads && data.ads.length > 0 ? "grid-cols-[2fr_1fr] gap-8" : ""}`}
    >
        <div class="bg-white rounded-lg shadow-lg p-6 md:p-10">
            <header class="border-b border-gray-200 pb-6 mb-6">
                <div class="flex flex-row items-center justify-between">
                    {#if article.category}
                        <a
                            href="/categories/{article.category.slug}"
                            class="font-semibold text-indigo-600 hover:underline uppercase text-sm"
                        >
                            {article.category.name}
                        </a>
                    {/if}
                    <div>
                        {#if article.is_breaking}
                            <span
                                class="ml-4 inline-block bg-red-100 text-red-800 text-xs font-semibold px-2 py-1 rounded-full"
                            >
                                Терміново
                            </span>
                        {/if}
                        {#if article.is_exclusive}
                            <span
                                class="ml-2 inline-block bg-indigo-100 text-indigo-800 text-xs font-semibold px-2 py-1 rounded-full"
                            >
                                Ексклюзив
                            </span>
                        {/if}
                    </div>
                </div>

                <div class="flex justify-between items-start gap-4 mt-3 mb-5">
                    <h1 class="text-3xl md:text-5xl font-bold text-gray-900">
                        {article.title}
                    </h1>
                    {#if canSave}
                        <button
                            onclick={handleToggleSave}
                            disabled={isLoadingSave}
                            class="hidden lg:flex items-center gap-2 px-4 py-2
                                   rounded-md font-medium shadow-sm transition-colors
                                   disabled:opacity-60 ml-6 shrink-0
                                   {isSaved
                                ? 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                                : 'bg-indigo-600 text-white hover:bg-indigo-700'}"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 24 24"
                                class="w-5 h-5"
                            >
                                <path
                                    d="M17.59 3.00037H6.41C5.07 3.00037 4 4.07037 4 5.41037V21.0004L12 17.0004L20 21.0004V5.41037C20 4.07037 18.93 3.00037 17.59 3.00037Z"
                                    fill="currentColor"
                                />
                            </svg>
                            {isSaved ? "Збережено" : "Зберегти"}
                        </button>
                    {/if}
                </div>

                <div
                    class="flex flex-wrap items-center justify-between gap-x-4 gap-y-2 text-sm text-gray-600"
                >
                    <div class="flex flex-wrap items-center gap-x-4 gap-y-2">
                        <span>
                            Автор:
                            <a
                                href="/authors/{article.author.id}"
                                class="font-medium text-gray-900 hover:underline"
                            >
                                {article.author.first_name}
                                {article.author.last_name}
                            </a>
                        </span>
                        <span class="text-gray-400 hidden md:inline">|</span>
                        <span>{formatDate(article.created_at)}</span>
                        <span class="flex items-center gap-1">
                            Переглядів:
                            {article.views_count}
                        </span>
                    </div>
                    {#if canLike}
                        <button
                            onclick={handleToggleLike}
                            disabled={isLoadingLike}
                            class="flex items-center gap-2 px-4 py-2 rounded-md font-medium shadow-sm transition-colors
                                       disabled:opacity-60
                                       {isLiked
                                ? 'bg-red-50 text-red-600 hover:bg-red-100'
                                : 'bg-gray-100 text-gray-800 hover:bg-gray-200'}"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 24 24"
                                class="w-5 h-5"
                                fill="currentColor"
                            >
                                <path
                                    d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
                                    class:opacity-30={!isLiked}
                                />
                            </svg>
                            {isLiked ? "Вподобано" : "Лайк"}
                            <span class="font-semibold">{likesCount}</span>
                        </button>
                    {:else}
                        <div
                            class="rounded-md font-medium shadow-sm transition-colors bg-red-50 text-red-600 hover:bg-red-100 p-2 text-center"
                        >
                            <span class="font-semibold"
                                >Вподобайки {likesCount}</span
                            >
                        </div>
                    {/if}
                    {#if canSave}
                        <button
                            onclick={handleToggleSave}
                            disabled={isLoadingSave}
                            class="flex lg:hidden items-center justify-center w-full mt-4 gap-2 px-4 py-3
                                   rounded-md font-medium text-white shadow-sm transition-colors
                                   disabled:opacity-60
                                   {isSaved
                                ? 'bg-gray-700 hover:bg-gray-800'
                                : 'bg-indigo-600 hover:bg-indigo-700'}"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 24 24"
                                class="w-5 h-5"
                            >
                                <path
                                    d="M17.59 3.00037H6.41C5.07 3.00037 4 4.07037 4 5.41037V21.0004L12 17.0004L20 21.0004V5.41037C20 4.07037 18.93 3.00037 17.59 3.00037Z"
                                    fill="currentColor"
                                />
                            </svg>
                            {isSaved ? "Збережено" : "Зберегти статтю"}
                        </button>
                    {/if}
                </div>
            </header>

            <div class="prose prose-lg max-w-none text-gray-800">
                {@html article.content}
            </div>

            {#if article}
                <CommentList articleId={article.id} />
            {/if}
        </div>

        {#if data.ads && data.ads.length > 0}
            <aside class="m-4">
                <div class="sticky top-24 space-y-6">
                    <h3 class="text-xl font-bold text-gray-900 border-b pb-2">
                        Реклама
                    </h3>
                    {#each data.ads as ad (ad.id)}
                        <AdCard {ad} />
                    {/each}
                </div>
            </aside>
        {/if}
    </div>
{:else if data.error?.status == 403}
    <div class="bg-white p-12 rounded-lg shadow-md text-center">
        <h1 class="text-2xl font-bold text-red-600">Помилка</h1>
        <p class="text-gray-600 mt-4">
            Якщо хочете переглянути статтю, оформіть вищий рівень підписки.
        </p>
        <a href="/" class="text-indigo-600 hover:underline mt-4 block"
            >Повернутися на головну</a
        >
    </div>
{:else}
    <div class="bg-white p-12 rounded-lg shadow-md text-center">
        <h1 class="text-2xl font-bold text-red-600">Помилка</h1>
        <p class="text-gray-600 mt-4">
            Не вдалося завантажити статтю. Можливо, її не існує.
        </p>
        <a href="/" class="text-indigo-600 hover:underline mt-4 block"
            >Повернутися на головну</a
        >
    </div>
{/if}
