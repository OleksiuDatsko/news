<script lang="ts">
  import ArticleCard from '$lib/components/ui/cards/ArticleCard.svelte';
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();
</script>

<svelte:head>
  <title>Збережені статті</title>
</svelte:head>

<div class="max-w-4xl mx-auto">
  <a href="/profile" class="text-indigo-600 hover:underline text-sm">&larr; Назад до профілю</a>
  <h1 class="text-3xl font-bold text-gray-900 mt-2 mb-8">Мої збережені статті</h1>

  {#if data.articles && data.articles.length > 0}
    <div class="space-y-6">
      {#each data.articles as article (article.id)}
        <ArticleCard {article} />
      {/each}
    </div>
  {:else}
    <div class="bg-white p-12 rounded-lg shadow-md text-center">
      <p class="text-gray-600 text-lg">Ви ще не зберегли жодної статті.</p>
      <a href="/" class="text-indigo-600 hover:underline mt-4 block"> Перейти до новин </a>
    </div>
  {/if}
</div>
