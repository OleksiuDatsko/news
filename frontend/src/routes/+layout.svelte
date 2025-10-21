<script lang="ts">
	import { onMount } from 'svelte';
	import { adminStore, userStore } from '$lib/stores/authStore';
	import { api } from '$lib/services/api';
	import '../app.css';
    import type { IUser } from '$lib/types/user';
    import type { IAdmin } from '$lib/types/admin';
    import Button from '$lib/components/ui/Button.svelte';

	let { children } = $props();

	onMount(async () => {
		try {
			const { user } = await api.get<{user: IUser}>('/auth/me');
			userStore.set(user);
			console.log('User authenticated:', user);
		} catch (e) {
			try {
				const { admin } = await api.get<{admin: IAdmin}>('/admin/auth/me');
				adminStore.set(admin);
				console.log('Admin authenticated:', admin);
			} catch (err) {
				userStore.set(null);
				adminStore.set(null);
			}
		}
	});

	async function logout(userType: 'user' | 'admin') {
		if (userType === 'user') {
			await api.post('/auth/logout', {});
			userStore.set(null);
		} else if (userType === 'admin') {
			await api.post('/admin/auth/logout', {});
			adminStore.set(null);
		}
	}
</script>

<main class="container mx-auto p-4">
	{#if $userStore?.id}
		<p>Logged in as user: {$userStore?.username}</p>
		<Button onclick={() => logout("user")}>Logout</Button>
	{/if}
	{#if $adminStore?.id}
		<p>Logged in as admin: {$adminStore?.email}</p>
		<Button onclick={() => logout("admin")}>Logout</Button>
	{/if}
	{@render children()}
</main>