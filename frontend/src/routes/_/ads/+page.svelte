<script lang="ts">
  import { goto } from '$app/navigation';
  import { api } from '$lib/services/api';
  import Button from '$lib/components/ui/Button.svelte';
  import Alert from '$lib/components/ui/Alert.svelte';
  import Pagination from '$lib/components/ui/Pagination.svelte';
  import type { PageData } from './$types';
  import type { IAdminAd } from './+page.ts';

  let { data }: { data: PageData } = $props();

  let ads = $derived<IAdminAd[]>(data.ads);
  let error = $state('');
  let loadingAction = $state(false);

  function handleCreateNew() {
    goto('/_/ads/new');
  }

  function handleEdit(adId: number) {
    goto(`/_/ads/${adId}`);
  }

  async function handleDelete(adId: number) {
    if (loadingAction) return;
    if (!confirm('Ви впевнені, що хочете видалити це оголошення?')) {
      return;
    }

    loadingAction = true;
    error = '';
    try {
      await api.del(`/admin/ads/${adId}`);
      ads = ads.filter((a) => a.id !== adId);
    } catch (e: any) {
      error = e.message || 'Помилка видалення оголошення.';
    } finally {
      loadingAction = false;
    }
  }

  function getStatusClass(status: string) {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'inactive':
        return 'bg-yellow-100 text-yellow-800';
      case 'expired':
        return 'bg-gray-100 text-gray-600';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  }
</script>

<svelte:head>
  <title>Адмін: Реклама</title>
</svelte:head>

<div class="flex justify-between items-center mb-6">
  <h1 class="text-3xl font-bold text-gray-900">Управління Рекламою</h1>
  <Button onclick={handleCreateNew} class="shadow-sm">Створити Оголошення</Button>
</div>

{#if error}
  <Alert type="error">{error}</Alert>
{/if}

<div class="bg-white shadow-lg rounded-lg overflow-hidden">
  {#if ads.length > 0}
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase"
              >Заголовок</th
            >
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Тип</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Статус</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Покази</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Кліки</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">CTR (%)</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Дії</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          {#each ads as ad (ad.id)}
            <tr class="hover:bg-gray-50">
              <td class="px-6 py-4 text-sm text-gray-500">{ad.id}</td>
              <td class="px-6 py-4 text-sm font-medium text-gray-900">{ad.title}</td>
              <td class="px-6 py-4 text-sm text-gray-700">{ad.ad_type}</td>
              <td class="px-6 py-4 text-sm">
                <span
                  class="px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full {getStatusClass(
                    ad.status
                  )}"
                >
                  {ad.status}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-gray-700">{ad.impressions_count}</td>
              <td class="px-6 py-4 text-sm text-gray-700">{ad.clicks_count}</td>
              <td class="px-6 py-4 text-sm text-gray-700">{ad.ctr}</td>
              <td class="px-6 py-4 text-right text-sm font-medium space-x-2">
                <Button
                  onclick={() => handleEdit(ad.id)}
                  disabled={loadingAction}
                  class="!w-auto !py-1 !px-3 !bg-blue-600 hover:!bg-blue-700 !text-xs !font-medium"
                >
                  Редагувати
                </Button>
                <Button
                  onclick={() => handleDelete(ad.id)}
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
    <Pagination currentPage={data.page} perPage={data.perPage} totalItems={data.total} />
  {:else}
    <div class="text-center p-12">
      <h3 class="mt-2 text-lg font-medium text-gray-900">Жодного оголошення не знайдено</h3>
      <p class="mt-1 text-sm text-gray-500">Почніть створювати рекламні кампанії.</p>
      <div class="mt-6">
        <Button onclick={handleCreateNew} class="!w-auto shadow-sm">
          Створити перше оголошення
        </Button>
      </div>
    </div>
  {/if}
</div>
