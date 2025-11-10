<script lang="ts">
  import { adminStore, userStore } from '$lib/stores/authStore';
  import { categoryStore } from '$lib/stores/categoryStore';
  import { goto } from '$app/navigation';
  import { api } from '$lib/services/api';
  import { notificationStore } from '$lib/stores/notificationStore';
  import NotificationDropdown from '../notification/NotificationDropdown.svelte';
  import { page } from '$app/state';

  let topCategories = $derived($categoryStore.slice(0, 3));

  let searchTerm = $state('');
  let showNotifications = $state(false);
  const editablePages = ['articles', 'authors'];

  function handleDocumentClick(event: MouseEvent) {
    const target = event.target as HTMLElement;
    if (showNotifications && !target.closest('.notification-toggle')) {
      showNotifications = false;
    }
  }

  function handleSearch(event: Event) {
    event.preventDefault();
    if (searchTerm.trim()) {
      goto(`/search?q=${encodeURIComponent(searchTerm.trim())}`);
      searchTerm = '';
    }
  }

  async function handleLogout() {
    if ($userStore) {
      await api.post('/auth/logout', {});
      userStore.set(null);
    } else if ($adminStore) {
      await api.post('/admin/auth/logout', {});
      adminStore.set(null);
    }
    await goto('/');
  }
</script>

<svelte:body on:click={handleDocumentClick} />

<header class="bg-white shadow-sm sticky top-0 z-50 border-b border-gray-200">
  <nav class="container mx-auto px-4">
    <div class="flex justify-between items-center h-16">
      <div class="flex items-center gap-6">
        <a href="/" class="text-2xl font-bold text-indigo-600"> NewsApp </a>
        <div class="hidden md:flex gap-5">
          <a href="/" class="text-sm font-medium text-gray-700 hover:text-indigo-600"> Головна </a>
          {#if topCategories.length > 0}
            {#each topCategories as category (category.id)}
              <a
                href="/categories/{category.slug}"
                class="text-sm font-medium text-gray-700 hover:text-indigo-600"
              >
                {category.name}
              </a>
            {/each}
          {/if}
        </div>
      </div>
      <div class="flex-1 px-4 max-w-lg mx-auto">
        <form onsubmit={handleSearch} class="w-full">
          <input
            type="search"
            bind:value={searchTerm}
            placeholder="Пошук за ключовим словом, автором..."
            class="block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm
						   focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </form>
      </div>
      <div class="flex items-center gap-4">
        <div class="flex items-center gap-4">
          {#if $userStore}
            <div class="relative">
              <button
                onclick={() => (showNotifications = !showNotifications)}
                class="relative p-2 rounded-full text-gray-500 hover:text-gray-700
								   hover:bg-gray-100 focus:outline-none focus:ring-2
								   focus:ring-offset-2 focus:ring-indigo-500
								   notification-toggle"
              >
                <svg
                  class="h-6 w-6"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"
                  />
                </svg>
                {#if $notificationStore.unread_count > 0}
                  <span
                    class="absolute -top-1 -right-1 flex h-4 w-4 items-center
										   justify-center rounded-full bg-red-500 text-xs
										   font-bold text-white ring-2 ring-white"
                  >
                    {$notificationStore.unread_count}
                  </span>
                {/if}
              </button>

              {#if showNotifications}
                <NotificationDropdown />
              {/if}
            </div>
            <span class="text-sm text-gray-600 hidden sm:block">
              Вітаємо,
              <a href="/profile" class="font-medium text-gray-900 hover:underline">
                {$userStore.username}
              </a>
            </span>
          {:else if $adminStore}
            {#if editablePages.find((p) => p == page.url.pathname.split('/')[1])}
              <span class="text-sm text-gray-600 hidden sm:block">
                <a
                  href={`/_${page.url.pathname}`}
                  class="font-medium text-gray-900 hover:underline"
                >
                  Редагувати
                </a>
              </span>
            {/if}
            <span class="text-sm text-gray-600 hidden sm:block">
              Admin:
              <a href="/_/dashboard" class="font-medium text-gray-900 hover:underline">
                Dashboard
              </a>
            </span>
            <button
              onclick={handleLogout}
              class="text-sm font-medium text-gray-700 hover:text-indigo-600"
            >
              Вийти
            </button>
          {:else}
            <a href="/auth/login" class="text-sm font-medium text-gray-700 hover:text-indigo-600">
              Увійти
            </a>
            <a
              href="/auth/register"
              class="text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded-md transition-colors shadow-sm"
            >
              Реєстрація
            </a>
          {/if}
        </div>
      </div>
    </div>
  </nav>
</header>
