<script lang="ts">
  import Footer from '$lib/components/layout/Footer.svelte';
  import Header from '$lib/components/layout/Header.svelte';
  import { onMount } from 'svelte';
  import '../app.css';

  let { children } = $props();
  onMount(() => {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker
        .register('/service-worker.js')
        .then((registration) => {
          console.log('✅ Service Worker зареєстрований, scope:', registration.scope);
        })
        .catch((err) => {
          console.error('❌ Помилка реєстрації Service Worker:', err);
        });
    }
  });
</script>

<div class="flex flex-col min-h-screen bg-slate-50">
  <Header />

  <main class="container mx-auto p-4 md:p-8 flex-grow w-full">
    {@render children()}
  </main>

  <Footer />
</div>
