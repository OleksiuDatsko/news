<script lang="ts">
	import { adminStore, userStore } from "$lib/stores/authStore";
	import { api } from "$lib/services/api";
	import "../app.css";
	import Button from "$lib/components/ui/Button.svelte";

	let { children } = $props();

	async function logout(userType: "user" | "admin") {
		if (userType === "user") {
			await api.post("/auth/logout", {});
			userStore.set(null);
		} else if (userType === "admin") {
			await api.post("/admin/auth/logout", {});
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
