<script lang="ts">
  import { goto } from '$app/navigation';
  import { api } from '$lib/services/api';
  import Button from '$lib/components/ui/Button.svelte';
  import Alert from '$lib/components/ui/Alert.svelte';
  import Input from '$lib/components/ui/Input.svelte';

  let name = $state('');
  let description = $state('');
  let is_searchable = $state(true);

  let error = $state('');
  let loading = $state(false);

  async function handleSubmit() {
    loading = true;
    error = '';
    try {
      await api.post('/admin/categories/', {
        name,
        description,
        is_searchable
      });
      await goto('/_/categories');
    } catch (e: any) {
      error = e.message || 'Помилка створення. Можливо, така назва вже існує.';
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head>
  <title>Адмін: Нова Категорія</title>
</svelte:head>

<h1 class="text-3xl font-bold text-gray-900 mb-6">Створити Нову Категорію</h1>

<div class="bg-white p-8 rounded-lg shadow-lg max-w-2xl mx-auto">
  <form onsubmit={handleSubmit} class="space-y-6">
    {#if error}
      <Alert type="error">{error}</Alert>
    {/if}

    <Input name="name" label="Назва Категорії" required bind:value={name} />

    <div>
      <label for="description" class="block text-sm font-medium text-gray-700">
        Опис (optional)
      </label>
      <div class="mt-1">
        <textarea
          id="description"
          name="description"
          rows={4}
          bind:value={description}
          class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        ></textarea>
      </div>
    </div>

    <div class="flex items-center">
      <input
        id="is_searchable"
        name="is_searchable"
        type="checkbox"
        bind:checked={is_searchable}
        class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
      />
      <label for="is_searchable" class="ml-2 block text-sm text-gray-900">
        Дозволити для пошуку
      </label>
    </div>

    <div class="flex gap-4">
      <Button type="submit" {loading} class="!w-auto">Створити Категорію</Button>
      <a
        href="/_/categories"
        class="inline-flex items-center justify-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
      >
        Скасувати
      </a>
    </div>
  </form>
</div>
