import { adminStore } from '$lib/stores/authStore';
import { goto } from '$app/navigation';
import { get } from 'svelte/store';
import type { LayoutLoad } from './$types';

export const load: LayoutLoad = async () => {
	const admin = get(adminStore);

	if (!admin) {
		await goto('/admin/login');
	}

	return {};
};