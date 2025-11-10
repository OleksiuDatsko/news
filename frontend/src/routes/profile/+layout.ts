import { userStore } from '$lib/stores/authStore';
import { goto } from '$app/navigation';
import { get } from 'svelte/store';
import type { LayoutLoad } from './$types';

export const load: LayoutLoad = async ({ parent }) => {
  await parent();

  const user = get(userStore);

  if (!user) {
    await goto('/auth/login');
  }
  return {};
};
