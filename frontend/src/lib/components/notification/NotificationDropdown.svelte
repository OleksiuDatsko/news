<script lang="ts">
  import { notificationStore, markAllAsRead } from '$lib/stores/notificationStore';
  import NotificationItem from './NotificationItem.svelte';
  import { api } from '$lib/services/api';
  import { fly } from 'svelte/transition';

  let loading = $state(false);

  async function handleMarkAllRead() {
    if (loading) return;
    loading = true;
    try {
      await api.post('/notifications/read-all', {});
      markAllAsRead();
    } catch (e) {
      console.error('Failed to mark all as read', e);
    } finally {
      loading = false;
    }
  }
</script>

<div
  transition:fly={{ y: -10, duration: 200 }}
  class="absolute right-0 top-full mt-2 w-80 max-w-sm
		   bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5
		   overflow-hidden z-50"
>
  <div class="flex justify-between items-center px-4 py-3 bg-gray-50 border-b border-gray-200">
    <h3 class="text-sm font-medium text-gray-700">Сповіщення</h3>
    {#if $notificationStore.unread_count > 0}
      <button
        onclick={handleMarkAllRead}
        disabled={loading}
        class="text-xs font-medium text-indigo-600 hover:underline disabled:opacity-50"
      >
        {loading ? '...' : 'Позначити всі як прочитані'}
      </button>
    {/if}
  </div>

  <div class="max-h-96 overflow-y-auto">
    {#if $notificationStore.notifications.length > 0}
      {#each $notificationStore.notifications as notification (notification.id)}
        <NotificationItem {notification} />
      {/each}
    {:else if !$notificationStore.loaded}
      <p class="p-4 text-sm text-gray-500">Завантаження...</p>
    {:else}
      <p class="p-4 text-sm text-gray-500">У вас немає нових сповіщень.</p>
    {/if}
  </div>
</div>
