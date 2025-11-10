<script lang="ts">
  import type { IUser } from '$lib/types/user';
  import type { IAdmin } from '$lib/types/admin';
  import Button from '$lib/components/ui/Button.svelte';

  let {
    user,
    admin,
    onLogout
  }: {
    user: IUser | null;
    admin: IAdmin | null;
    onLogout: (type: 'user' | 'admin') => void;
  } = $props();
</script>

{#if user}
  <div class="bg-white p-4 rounded-lg shadow-md border border-gray-100 mb-6">
    <p class="text-sm text-gray-700 mb-3">
      Ви увійшли як:
      <strong class="font-medium text-gray-900 block text-base">{user.username}</strong>
    </p>
    <div class="flex items-center gap-3">
      <a
        href="/profile"
        class="block w-full text-center text-sm font-medium text-indigo-600 hover:text-indigo-800 transition-colors"
      >
        Мій профіль
      </a>
      <Button
        onclick={() => onLogout('user')}
        class="!w-full !py-1.5 !px-3 !bg-slate-200 !text-slate-700 hover:!bg-slate-300"
      >
        Вийти
      </Button>
    </div>
  </div>
{/if}

{#if admin}
  <div class="bg-white p-4 rounded-lg shadow-md border border-gray-100 mb-6">
    <p class="text-sm text-gray-700 mb-3">
      Адмін-панель:
      <strong class="font-medium text-gray-900 block text-base">{admin.email}</strong>
    </p>
    <div class="flex items-center gap-3">
      <a
        href="/admin/dashboard"
        class="block w-full text-center text-sm font-medium text-indigo-600 hover:text-indigo-800 transition-colors"
      >
        Dashboard
      </a>
      <Button
        onclick={() => onLogout('admin')}
        class="!w-full !py-1.5 !px-3 !bg-slate-200 !text-slate-700 hover:!bg-slate-300"
      >
        Вийти
      </Button>
    </div>
  </div>
{/if}
