import { adminStore } from '$lib/stores/authStore';
import { goto } from '$app/navigation';
import { get } from 'svelte/store';
import type { LayoutLoad } from './$types';

export const load: LayoutLoad = async ({ parent }) => {
	await parent();
	const admin = get(adminStore);
	console.log('Admin in layout:', admin);

	if (!admin) {
		await goto('/admin/login');
	}
	return {};
};