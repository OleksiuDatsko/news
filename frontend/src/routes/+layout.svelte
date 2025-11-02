<script lang="ts">
	import Footer from "$lib/components/layout/Footer.svelte";
	import Header from "$lib/components/layout/Header.svelte";
	import "../app.css";

	let { children } = $props();
</script>

<div class="flex flex-col min-h-screen bg-slate-50">
	<Header />

	<main class="container mx-auto p-4 md:p-8 flex-grow w-full">
		{@render children()}
	</main>

	<Footer />
</div>
