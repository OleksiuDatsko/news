<script lang="ts">
  import { goto } from '$app/navigation';
  import { api } from '$lib/services/api';
  import Button from '$lib/components/ui/Button.svelte';
  import Alert from '$lib/components/ui/Alert.svelte';
  import Input from '$lib/components/ui/Input.svelte';
  import type { PageData } from './$types';
  import SmallArticleCard from '$lib/components/ui/cards/SmallArticleCard.svelte';

  let { data }: { data: PageData } = $props();

  let name = $state(data.category?.name ?? '');
  let description = $state(data.category?.description ?? '');
  let is_searchable = $state(data.category?.is_searchable ?? true);

  let error = $state('');
  let loading = $state(false);

  async function handleSubmit() {
    if (!data.category) return;

    loading = true;
    error = '';
    try {
      await api.put(`/admin/categories/${data.category.id}`, {
        name,
        description,
        is_searchable
      });
      await goto('/_/categories');
    } catch (e: any) {
      error = e.message || 'Помилка оновлення.';
    } finally {
      loading = false;
    }
  }

  async function handleDelete() {
    if (!data.category) return;
    if (
      !confirm('Ви впевнені, що хочете видалити цю категорію? Це неможливо, якщо у неї є статті.')
    ) {
      return;
    }

    loading = true;
    error = '';
    try {
      await api.del(`/admin/categories/${data.category.id}`);
      await goto('/_/categories');
    } catch (e: any) {
      error = e.message || 'Помилка видалення. Перевірте, чи у категорії немає статей.';
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
          <Input name="name" label="Назва Категорії" required bind:value={name} />

          <Input
            name="slug"
            label="Slug (генерується автоматично)"
            value={data.category.slug}
            disabled
            class="bg-gray-100"
          />

          <div>
            <label for="description" class="block text-sm font-medium text-gray-700"> Опис </label>
            <div class="mt-1">
              <textarea
                id="description"
                name="description"
                rows={4}
                bind:value={description}
                class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              ></textarea>
            </div>
          </div>

          <div class="flex items-center">
            <input
              id="is_searchable"
              name="is_searchable"
              type="checkbox"
              bind:checked={is_searchable}
              class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
            />
            <label for="is_searchable" class="ml-2 block text-sm text-gray-900">
              Дозволити для пошуку
            </label>
          </div>

          <div class="flex flex-wrap gap-4 items-center justify-between">
            <div class="flex gap-4">
              <Button type="submit" {loading} class="!w-auto">Зберегти Зміни</Button>
              <a
                href="/_/categories"
                class="inline-flex items-center justify-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Скасувати
              </a>
            </div>
            <Button
              type="button"
              onclick={handleDelete}
              disabled={loading}
              class="!w-auto !bg-red-600 hover:!bg-red-700"
            >
              Видалити Категорію
            </Button>
          </div>
        </form>
      </div>
    </div>

    <div class="lg:col-span-1">
      <div class="bg-white p-6 rounded-lg shadow-lg">
        <h2 class="text-xl font-bold text-gray-900 mb-4">
          Статті в цій категорії ({data.articles.length})
        </h2>
        {#if data.articles.length > 0}
          <ul class="space-y-4">
            {#each data.articles as article (article.id)}
              <li class="border-b pb-3">
                <SmallArticleCard {article} />
              </li>
            {/each}
          </ul>
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
