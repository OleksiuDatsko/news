<script lang="ts">
  import { goto } from '$app/navigation';
  import { api } from '$lib/services/api';
  import type { ICategory } from '$lib/types/category';
  import Button from '$lib/components/ui/Button.svelte';
  import Alert from '$lib/components/ui/Alert.svelte';
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();
  let categories = $derived<ICategory[]>(data.categories);
  let error = $state('');
  let loadingAction = $state(false);

  function handleCreateNew() {
    goto('/_/categories/new');
  }

  function handleEdit(categoryId: number) {
    goto(`/_/categories/${categoryId}`);
  }

  async function handleDelete(categoryId: number) {
    if (loadingAction) return;
    if (
      !confirm('Ви впевнені, що хочете видалити цю категорію? Це неможливо, якщо у неї є статті.')
    ) {
      return;
    }

    loadingAction = true;
    error = '';
    try {
      await api.del(`/admin/categories/${categoryId}`);
      categories = categories.filter((c) => c.id !== categoryId);
    } catch (e: any) {
      error = e.message || 'Помилка видалення. Перевірте, чи у категорії немає статей.';
    } finally {
      loadingAction = false;
    }
  }
</script>

<svelte:head>
  <title>Адмін: Категорії</title>
</svelte:head>

<div class="flex justify-between items-center mb-6">
  <h1 class="text-3xl font-bold text-gray-900">Управління Категоріями</h1>
  <Button onclick={handleCreateNew} class="shadow-sm">Створити Категорію</Button>
</div>

{#if error}
  <Alert type="error">{error}</Alert>
{/if}

<div class="bg-white shadow-lg rounded-lg overflow-hidden">
  {#if categories.length > 0}
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >ID</th
            >
            <th
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >Назва</th
            >
            <th
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >Slug</th
            >
            <th
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >К-ть статей</th
            >
            <th
              class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >Дії</th
            >
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          {#each categories as category (category.id)}
            <tr class="hover:bg-gray-50 transition-colors duration-150">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{category.id}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                >{category.name}</td
              >
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{category.slug}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700"
                >{category.total_articles ?? 0}</td
              >
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                <Button
                  onclick={() => handleEdit(category.id)}
                  disabled={loadingAction}
                  class="!w-auto !py-1 !px-3 !bg-blue-600 hover:!bg-blue-700 !text-xs !font-medium"
                >
                  Редагувати
                </Button>
                <Button
                  onclick={() => handleDelete(category.id)}
                  disabled={loadingAction}
                  class="!w-auto !py-1 !px-3 !bg-red-600 hover:!bg-red-700 !text-xs !font-medium"
                >
                  Видалити
                </Button>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {:else}
    <div class="text-center p-12">
      <h3 class="mt-2 text-lg font-medium text-gray-900">Жодної категорії не знайдено</h3>
      <div class="mt-6">
        <Button onclick={handleCreateNew} class="!w-auto shadow-sm">
          Створити першу категорію
        </Button>
      </div>
    </div>
  {/if}
</div>
