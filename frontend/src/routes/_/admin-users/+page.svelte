<script lang="ts">
  import { goto } from '$app/navigation';
  import { api } from '$lib/services/api';
  import Button from '$lib/components/ui/Button.svelte';
  import Alert from '$lib/components/ui/Alert.svelte';
  import type { PageData } from './$types';
  import { adminStore } from '$lib/stores/authStore';

  let { data }: { data: PageData } = $props();
  let admins = $state(data.admins);
  let error = $state('');
  let loadingAction = $state(false);
  const currentAdminId = $derived($adminStore?.id);

  function handleCreateNew() {
    goto('/_/admin-users/new');
  }

  function handleEdit(adminId: number) {
    goto(`/_/admin-users/${adminId}`);
  }

  async function handleDelete(adminId: number) {
    if (loadingAction || adminId === currentAdminId) return;
    if (!confirm('Ви впевнені, що хочете видалити цього адміністратора?')) {
      return;
    }

    loadingAction = true;
    error = '';
    try {
      await api.del(`/admin/admin-users/${adminId}`);
      admins = admins.filter((a) => a.id !== adminId);
    } catch (e: any) {
      error = e.message || 'Помилка видалення адміністратора.';
    } finally {
      loadingAction = false;
    }
  }
</script>

<svelte:head>
  <title>Адмін: Адміністратори</title>
</svelte:head>

<div class="flex justify-between items-center mb-6">
  <h1 class="text-3xl font-bold text-gray-900">Керування Адміністраторами</h1>
  <Button onclick={handleCreateNew} class="shadow-sm">Створити Адміністратора</Button>
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
            >Email</th
          >
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >Дата створення</th
          >
          <th
            class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
            >Дії</th
          >
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        {#each admins as admin (admin.id)}
          <tr class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{admin.id}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
              >{admin.email}
              {#if admin.id === currentAdminId}
                <span class="ml-2 text-xs font-medium text-indigo-600">(Це ви)</span>
              {/if}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700"
              >{new Date(admin.created_at).toLocaleDateString('uk-UA')}</td
            >
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
              <Button
                onclick={() => handleEdit(admin.id)}
                disabled={loadingAction}
                class="!w-auto !py-1 !px-3 !bg-blue-600 hover:!bg-blue-700 !text-xs !font-medium"
              >
                Змінити пароль
              </Button>
              <Button
                onclick={() => handleDelete(admin.id)}
                disabled={loadingAction || admin.id === currentAdminId}
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
