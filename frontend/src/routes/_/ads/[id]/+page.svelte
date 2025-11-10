<script lang="ts">
  import { goto } from '$app/navigation';
  import { api } from '$lib/services/api';
  import Alert from '$lib/components/ui/Alert.svelte';
  import AdForm from '../_AdForm.svelte';
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();

  let error = $state('');
  let loading = $state(false);

  function formatDate(dateString: string | null) {
    if (!dateString) return 'Не вказано';
    return new Date(dateString).toLocaleDateString('uk-UA', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }
</script>

<svelte:head>
  <title>Адмін: Редагувати {data.ad?.title ?? 'Оголошення'}</title>
</svelte:head>

{#if data.ad}
  <h1 class="text-3xl font-bold text-gray-900 mb-6">
    Редагувати: {data.ad.title}
  </h1>

  <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
    <div class="lg:col-span-2 bg-white p-8 rounded-lg shadow-lg">
      <AdForm
        ad={data.ad}
        bind:error
        bind:loading
        onSubmit={async (payload) => {
          await api.put(`/admin/ads/${data.ad?.id}`, payload);
          await goto('/_/ads');
        }}
      />
    </div>

    <div class="lg:col-span-1">
      <div class="bg-white p-6 rounded-lg shadow-lg sticky top-24">
        <h2 class="text-xl font-bold text-gray-900 mb-4 border-b pb-2">Статистика</h2>
        <ul class="space-y-3">
          <li class="flex justify-between text-sm">
            <span class="text-gray-600">Статус:</span>
            <span class="font-medium text-gray-900">{data.ad.status}</span>
          </li>
          <li class="flex justify-between text-sm">
            <span class="text-gray-600">Всього Показів:</span>
            <span class="font-medium text-gray-900">{data.ad.impressions_count}</span>
          </li>
          <li class="flex justify-between text-sm">
            <span class="text-gray-600">Всього Кліків:</span>
            <span class="font-medium text-gray-900">{data.ad.clicks_count}</span>
          </li>
          <li class="flex justify-between text-sm">
            <span class="text-gray-600">CTR:</span>
            <span class="font-medium text-gray-900">{data.ad.ctr} %</span>
          </li>
          <li class="flex justify-between text-sm border-t pt-3 mt-3">
            <span class="text-gray-600">Дата Початку:</span>
            <span class="font-medium text-gray-900">{formatDate(data.ad.start_date)}</span>
          </li>
          <li class="flex justify-between text-sm">
            <span class="text-gray-600">Дата Закінчення:</span>
            <span class="font-medium text-gray-900">{formatDate(data.ad.end_date)}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
{:else}
  <h1 class="text-3xl font-bold text-red-600 mb-6">Оголошення не знайдено</h1>
  <Alert type="error">Не вдалося завантажити дані. Можливо, оголошення було видалено.</Alert>
  <a href="/_/ads" class="text-indigo-600 hover:underline mt-4 inline-block">
    &larr; Повернутися до списку
  </a>
{/if}
