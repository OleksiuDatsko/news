<script lang="ts">
  import { goto } from '$app/navigation';
  import { api } from '$lib/services/api';
  import Button from '$lib/components/ui/Button.svelte';
  import Alert from '$lib/components/ui/Alert.svelte';
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();
  let plans = $state(data.plans);
  let error = $state('');
  let loadingAction = $state(false);

  function handleCreateNew() {
    goto('/_/subscriptions/new');
  }

  function handleEdit(planId: number) {
    goto(`/_/subscriptions/${planId}`);
  }

  async function handleDelete(planId: number) {
    if (loadingAction) return;
    if (!confirm('Ви впевнені, що хочете видалити цей план? Це може вплинути на користувачів.')) {
      return;
    }

    loadingAction = true;
    error = '';
    try {
      await api.del(`/admin/subscriptions/${planId}`);
      plans = plans.filter((p) => p.id !== planId);
    } catch (e: any) {
      error = e.message || 'Помилка видалення плану.';
    } finally {
      loadingAction = false;
    }
  }
</script>

<svelte:head>
  <title>Адмін: Плани Підписок</title>
</svelte:head>

<div class="flex justify-between items-center mb-6">
  <h1 class="text-3xl font-bold text-gray-900">Керування Планами Підписок</h1>
  <Button onclick={handleCreateNew} class="shadow-sm">Створити План</Button>
</div>

{#if error}
  <Alert type="error" additionalClass="mb-4">{error}</Alert>
{/if}

<div class="bg-white shadow-lg rounded-lg overflow-hidden">
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >ID</th
          >
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >Назва Плану</th
          >
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >Ціна (грн/міс)</th
          >
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >Дозволи</th
          >
          <th
            class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
            >Дії</th
          >
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        {#each plans as plan (plan.id)}
          <tr class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{plan.id}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
              >{plan.name}</td
            >
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700"
              >{Math.round(plan.price_per_month)}</td
            >
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700 flex flex-wrap gap-1">
              {#if plan.permissions.no_ads}
                <span class="text-xs font-medium bg-blue-100 text-blue-800 px-2 py-0.5 rounded"
                  >Без реклами</span
                >
              {/if}
              {#if plan.permissions.exclusive_content}
                <span
                  class="ml-1 text-xs font-medium bg-purple-100 text-purple-800 px-2 py-0.5 rounded"
                  >Ексклюзив</span
                >
              {/if}
              {#if plan.permissions.comment}
                <span
                  class="ml-1 text-xs font-medium bg-green-100 text-green-800 px-2 py-0.5 rounded"
                  >Коментарі</span
                >
              {/if}
              {#if plan.permissions.save_article}
                <span
                  class="ml-1 text-xs font-medium bg-orange-100 text-orange-800 px-2 py-0.5 rounded"
                  >Зберігати статті</span
                >
              {/if}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
              <Button
                onclick={() => handleEdit(plan.id)}
                disabled={loadingAction}
                class="!w-auto !py-1 !px-3 !bg-blue-600 hover:!bg-blue-700 !text-xs !font-medium"
              >
                Редагувати
              </Button>
              <Button
                onclick={() => handleDelete(plan.id)}
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
</div>
