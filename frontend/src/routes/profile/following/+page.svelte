<script lang="ts">
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();
</script>

<svelte:head>
  <title>Ваші підписки на авторів</title>
</svelte:head>

<div class="max-w-4xl mx-auto">
  <a href="/profile" class="text-indigo-600 hover:underline text-sm">&larr; Назад до профілю</a>
  <h1 class="text-3xl font-bold text-gray-900 mt-2 mb-8">Автори, яких ви відстежуєте</h1>

  {#if data.authors && data.authors.length > 0}
    <div class="bg-white shadow-lg rounded-lg overflow-hidden">
      <ul class="divide-y divide-gray-200">
        {#each data.authors as author (author.id)}
          <li class="p-4 hover:bg-gray-50 transition-colors">
            <a href="/authors/{author.id}" class="flex justify-between items-center">
              <div>
                <p class="text-lg font-medium text-indigo-700">
                  {author.first_name}
                  {author.last_name}
                </p>
                <p class="text-sm text-gray-600 truncate max-w-md">
                  {author.bio ?? 'Біографія відсутня'}
                </p>
              </div>
              <span class="text-sm text-gray-500 hover:underline ml-4 flex-shrink-0">
                Переглянути &rarr;
              </span>
            </a>
          </li>
        {/each}
      </ul>
    </div>
  {:else}
    <div class="bg-white p-12 rounded-lg shadow-md text-center">
      <p class="text-gray-600 text-lg">Ви ще не підписані на жодного автора.</p>
      <a href="/" class="text-indigo-600 hover:underline mt-4 block"> Перейти до новин </a>
    </div>
  {/if}
</div>
