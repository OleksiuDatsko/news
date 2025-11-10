<script lang="ts">
  import { goto } from '$app/navigation';
  import { api } from '$lib/services/api';
  import AdForm from '../_AdForm.svelte';

  let error = $state('');
  let loading = $state(false);
</script>

<svelte:head>
  <title>Адмін: Нове Оголошення</title>
</svelte:head>

<h1 class="text-3xl font-bold text-gray-900 mb-6">Створити Нове Оголошення</h1>

<div class="bg-white p-8 rounded-lg shadow-lg max-w-4xl mx-auto">
  <AdForm
    bind:error
    bind:loading
    onSubmit={async (payload) => {
      await api.post('/admin/ads/', payload);
      await goto('/_/ads');
    }}
  />
</div>
