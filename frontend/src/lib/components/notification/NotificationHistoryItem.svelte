<script lang="ts">
  import type { INotification } from '$lib/types/notification';
  import { goto } from '$app/navigation';

  let { notification }: { notification: INotification } = $props();

  function formatDate(dateString: string) {
    return new Date(dateString).toLocaleString('uk-UA', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  const isLink = $derived(!!notification.article_id);

  function handleClick() {
    if (isLink) {
      goto(`/articles/${notification.article_id}`);
    }
  }
</script>

<li
  class="list-none p-4 rounded-lg border transition-colors"
  class:bg-white={notification.is_read}
  class:bg-indigo-50={!notification.is_read}
  class:border-gray-200={notification.is_read}
  class:border-indigo-200={!notification.is_read}
  class:hover:bg-gray-50={isLink && notification.is_read}
  class:hover:bg-indigo-100={isLink && !notification.is_read}
>
  <button
    onclick={handleClick}
    disabled={!isLink}
    class="w-full text-left"
    class:cursor-pointer={isLink}
    class:cursor-default={!isLink}
  >
    <div class="flex justify-between items-start">
      <div class="flex-1">
        <span class="block font-semibold text-gray-900">
          {notification.title ?? 'Сповіщення'}
        </span>
        <span class="block text-sm text-gray-600">
          {notification.message ?? '...'}
        </span>
      </div>
      {#if !notification.is_read}
        <span
          class="ml-4 flex-shrink-0 inline-block h-2 w-2 mt-1.5 rounded-full bg-indigo-500"
          title="Непрочитане"
        ></span>
      {/if}
    </div>
    <time class="text-xs text-gray-500 mt-2 block">
      {formatDate(notification.created_at)}
    </time>
  </button>
</li>
