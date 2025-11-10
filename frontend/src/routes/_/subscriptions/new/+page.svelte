<script lang="ts">
  import { goto } from '$app/navigation';
  import { api } from '$lib/services/api';
  import Button from '$lib/components/ui/Button.svelte';
  import Alert from '$lib/components/ui/Alert.svelte';
  import Input from '$lib/components/ui/Input.svelte';

  let name = $state('');
  let description = $state('');
  let price_per_month = $state(0);
  let no_ads = $state(false);
  let exclusive_content = $state(false);
  let save_article = $state(false);
  let comment = $state(false);

  let error = $state('');
  let loading = $state(false);

  async function handleSubmit() {
    loading = true;
    error = '';
    try {
      const payload = {
        name,
        description,
        price_per_month,
        permissions: {
          no_ads,
          exclusive_content,
          save_article,
          comment
        }
      };
      await api.post('/admin/subscriptions/', payload);
      await goto('/_/subscriptions');
    } catch (e: any) {
      error = e.message || 'Помилка створення плану.';
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head>
  <title>Адмін: Новий План Підписки</title>
</svelte:head>

<h1 class="text-3xl font-bold text-gray-900 mb-6">Створити План Підписки</h1>

<div class="bg-white p-8 rounded-lg shadow-lg max-w-2xl mx-auto">
  <form onsubmit={handleSubmit} class="space-y-6">
    {#if error}
      <Alert type="error">{error}</Alert>
    {/if}

    <Input name="name" label="Назва Плану" required bind:value={name} />
    <Input
      name="price"
      label="Ціна (грн/міс)"
      type="number"
      required
      bind:value={price_per_month}
    />
    <Input name="description" label="Опис" bind:value={description} />

    <fieldset class="space-y-3 pt-4">
      <legend class="text-lg font-semibold text-gray-800 border-b pb-2">Дозволи</legend>
      <div class="grid grid-cols-2 gap-4">
        <div class="flex items-center">
          <input id="no_ads" type="checkbox" bind:checked={no_ads} class="h-4 w-4" />
          <label for="no_ads" class="ml-2 block text-sm text-gray-700">Без реклами</label>
        </div>
        <div class="flex items-center">
          <input
            id="exclusive_content"
            type="checkbox"
            bind:checked={exclusive_content}
            class="h-4 w-4"
          />
          <label for="exclusive_content" class="ml-2 block text-sm text-gray-700"
            >Ексклюзивний контент</label
          >
        </div>
        <div class="flex items-center">
          <input id="save_article" type="checkbox" bind:checked={save_article} class="h-4 w-4" />
          <label for="save_article" class="ml-2 block text-sm text-gray-700"
            >Збереження статей</label
          >
        </div>
        <div class="flex items-center">
          <input id="comment" type="checkbox" bind:checked={comment} class="h-4 w-4" />
          <label for="comment" class="ml-2 block text-sm text-gray-700">Коментарі</label>
        </div>
      </div>
    </fieldset>

    <div class="flex gap-4">
      <Button type="submit" {loading} class="!w-auto">Створити План</Button>
      <a
        href="/_/subscriptions"
        class="inline-flex items-center justify-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
      >
        Скасувати
      </a>
    </div>
  </form>
</div>
