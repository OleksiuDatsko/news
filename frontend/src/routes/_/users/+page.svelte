<script lang="ts">
  import { goto } from '$app/navigation';
  import { api } from '$lib/services/api';
  import Button from '$lib/components/ui/Button.svelte';
  import Alert from '$lib/components/ui/Alert.svelte';
  import Pagination from '$lib/components/ui/Pagination.svelte';
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();

  let users = $state(data.users);
  let error = $state('');
  let loadingAction = $state(false);

  function formatDate(dateString: string) {
    return new Date(dateString).toLocaleDateString('uk-UA', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }

  function handleEdit(userId: number) {
    goto(`/_/users/${userId}`);
  }

  async function handleDelete(userId: number) {
    if (loadingAction) return;
    if (!confirm('Ви впевнені, що хочете видалити цього користувача?')) {
      return;
    }

    loadingAction = true;
    error = '';
    try {
      await api.del(`/admin/users/${userId}`);
      users = users.filter((u) => u.id !== userId);
    } catch (e: any) {
      error = e.message || 'Помилка видалення користувача.';
    } finally {
      loadingAction = false;
    }
  }
</script>

<svelte:head>
  <title>Адмін: Користувачі</title>
</svelte:head>

<div class="flex justify-between items-center mb-6">
  <h1 class="text-3xl font-bold text-gray-900">Управління Користувачами</h1>
</div>

{#if error}
  <Alert type="error">{error}</Alert>
{/if}

<div class="bg-white shadow-lg rounded-lg overflow-hidden">
  {#if users.length > 0}
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
              >Ім'я (Username)</th
            >
            <th
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >Email</th
            >
            <th
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >Дата реєстрації</th
            >
            <th
              class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
              >Дії</th
            >
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          {#each users as user (user.id)}
            <tr class="hover:bg-gray-50 transition-colors duration-150">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{user.id}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                >{user.username}</td
              >
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{user.email}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700"
                >{formatDate(user.created_at)}</td
              >
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                <Button
                  onclick={() => handleEdit(user.id)}
                  disabled={loadingAction}
                  class="!w-auto !py-1 !px-3 !bg-blue-600 hover:!bg-blue-700 !text-xs !font-medium"
                >
                  Редагувати
                </Button>
                <Button
                  onclick={() => handleDelete(user.id)}
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
      <h3 class="mt-2 text-lg font-medium text-gray-900">Жодного користувача не знайдено</h3>
      <p class="mt-1 text-sm text-gray-500">Система ще не має зареєстрованих користувачів.</p>
    </div>
  {/if}
</div>
