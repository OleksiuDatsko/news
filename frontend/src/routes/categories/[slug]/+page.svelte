<script lang="ts">
  import type { PageData } from './$types';
  import ArticleCard from '$lib/components/ui/cards/ArticleCard.svelte';
  import AdCard from '$lib/components/ui/cards/AdCard.svelte';
  import Pagination from '$lib/components/ui/Pagination.svelte';

  let { data }: { data: PageData } = $props();

  let categoryName = $state('Категорія не знайдена');
  let categoryDescription = $state('');
  $effect(() => {
    categoryName = data.category?.name ?? 'Категорія не знайдена';
    categoryDescription = data.category?.description ?? '';
  });
</script>

<svelte:head>
  <title>{categoryName} - Новинна Газета</title>
  <meta name="description" content="Останні новини в категорії {categoryName}." />
</svelte:head>

<div class="p-4 md:p-8 min-h-screen">
  <div class="grid grid-cols-[1fr_auto] gap-8 max-w-7xl mx-auto">
    <div class="space-y-6">
      <h1 class="text-4xl font-bold text-gray-900 border-b border-gray-200 pb-4">
        Категорія: {categoryName}
      </h1>

      {#if categoryDescription}
        <p class="text-lg text-gray-600">{categoryDescription}</p>
      {/if}

      {#if data.articles && data.articles.length > 0}
        {#each data.articles as article (article.id)}
          <ArticleCard {article} />
        {/each}

        <Pagination
          currentPage={data.page}
          perPage={data.perPage}
          totalItems={data.total}
        />
      {:else}
        <div class="bg-white p-12 rounded-lg shadow-md text-center">
          <p class="text-gray-600 text-lg">Наразі немає опублікованих статей у цій категорії.</p>
        </div>
      {/if}
    </div>

    {#if data.ads.length > 0}
      <aside class="lg:col-span-1">
        <div class="sticky top-8 space-y-6">
          <h2 class="text-2xl font-bold text-gray-900 border-b border-gray-200 pb-2">Реклама</h2>

          {#each data.ads as ad (ad.id)}
            <AdCard {ad} />
          {/each}
        </div>
      </aside>
    {/if}
  </div>
</div>
