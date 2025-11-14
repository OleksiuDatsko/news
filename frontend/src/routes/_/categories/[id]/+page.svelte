<script lang="ts">
  import { goto } from '$app/navigation';
  import { api } from '$lib/services/api';
  import Button from '$lib/components/ui/Button.svelte';
  import Alert from '$lib/components/ui/Alert.svelte';
  import Input from '$lib/components/ui/Input.svelte';
  import type { PageData } from './$types';
  import SmallArticleCard from '$lib/components/ui/cards/SmallArticleCard.svelte';
  import Pagination from '$lib/components/ui/Pagination.svelte'; // <-- 1. Імпорт

  let { data }: { data: PageData } = $props();

  let name = $state(data.category?.name ?? '');
  let description = $state(data.category?.description ?? '');
  let error = $state('');
  let loading = $state(false);

  $effect(() => {
    name = data.category?.name ?? '';
    description = data.category?.description ?? '';
  });

  async function handleSubmit() {
    if (!data.category) return;
    loading = true;
    error = '';
    try {
      await api.put(`/admin/categories/${data.category.id}`, {
        name,
        description
      });
      await goto('/_/categories');
    } catch (e: any) {
      error = e.message || 'Помилка оновлення категорії.';
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head>
  <title>Адмін: Редагувати {data.category?.name ?? 'Категорія'}</title>
</svelte:head>

{#if data.category}
  <h1 class="text-3xl font-bold text-gray-900 mb-6">
    Редагувати: {data.category.name}
  </h1>

  {#if error}
    <Alert type="error">{error}</Alert>
  {/if}

  <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
    <div class="lg:col-span-2">
      <div class="bg-white p-8 rounded-lg shadow-lg">
        <form onsubmit={handleSubmit} class="space-y-6">
          <Input name="name" label="Назва категорії" required bind:value={name} />
          <Input name="description" label="Опис (optional)" bind:value={description} />

          <div class="flex gap-4">
            <Button type="submit" {loading} class="!w-auto">Зберегти Зміни</Button>
            <a
              href="/_/categories"
              class="inline-flex items-center justify-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              Скасувати
            </a>
          </div>
        </form>
      </div>
    </div>

    <div class="lg:col-span-1">
      <div class="bg-white p-6 rounded-lg shadow-lg">
        <h2 class="text-xl font-bold text-gray-900 mb-4">
          Статті цієї категорії ({data.total})
        </h2>
        {#if data.articles.length > 0}
          <ul class="space-y-4">
            {#each data.articles as article (article.id)}
              <li class="border-b pb-3">
                <SmallArticleCard {article} />
              </li>
            {/each}
          </ul>
          <Pagination
            currentPage={data.page}
            perPage={data.perPage}
            totalItems={data.total}
            showTotal={false}
          />
        {:else}
          <p class="text-sm text-gray-500">У цій категорії ще немає статей.</p>
        {/if}
      </div>
    </div>
  </div>
{:else}
  <h1 class="text-3xl font-bold text-red-600 mb-6">Категорію не знайдено</h1>
  <Alert type="error">Не вдалося завантажити дані. Можливо, категорію було видалено.</Alert>
  <a href="/_/categories" class="text-indigo-600 hover:underline mt-4 inline-block">
    &larr; Повернутися до списку категорій
  </a>
{/if}
