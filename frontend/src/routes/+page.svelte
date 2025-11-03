<script lang="ts">
    import AdCard from "$lib/components/ui/cards/AdCard.svelte";
    import ArticleCard from "$lib/components/ui/cards/ArticleCard.svelte";
    import Pagination from "$lib/components/ui/Pagination.svelte";
    import type { PageData } from "./$types";

    let { data }: { data: PageData } = $props();
</script>

<svelte:head>
    <title>Головна - Новинна Газета</title>
    <meta
        name="description"
        content="Останні новини політики, економіки, культури та спорту."
    />
</svelte:head>

<div class="p-4 md:p-8 min-h-screen">
    <div class="grid grid-cols-[1fr_auto] gap-8 max-w-7xl mx-auto">
        <div class="space-y-6">
            <h1
                class="text-4xl font-bold text-gray-900 border-b border-gray-200 pb-4"
            >
                Останні новини
            </h1>

            {#if data.articles.length > 0}
                {#each data.articles as article (article.id)}
                    <ArticleCard {article} />
                {/each}
            {:else}
                <div class="bg-white p-12 rounded-lg shadow-md text-center">
                    <p class="text-gray-600 text-lg">
                        Наразі немає опублікованих статей.
                    </p>
                </div>
            {/if}
            <Pagination 
                currentPage={data.page} 
                perPage={data.perPage} 
                totalItems={data.total}
            />
        </div>

        {#if data.ads.length > 0}
            <aside class="lg:col-span-1">
                <div class="sticky top-8 space-y-6">
                    <h2
                        class="text-2xl font-bold text-gray-900 border-b border-gray-200 pb-2"
                    >
                        Реклама
                    </h2>

                    {#each data.ads as ad (ad.id)}
                        <AdCard {ad} />
                    {/each}
                </div>
            </aside>
        {/if}
    </div>
</div>
