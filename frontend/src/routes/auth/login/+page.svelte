<script lang="ts">
  import { goto } from '$app/navigation';
  import { api } from '$lib/services/api';
  import { userStore } from '$lib/stores/authStore';
  import Alert from '$lib/components/ui/Alert.svelte';
  import Button from '$lib/components/ui/Button.svelte';
  import FormWrapper from '$lib/components/ui/FormWrapper.svelte';
  import Input from '$lib/components/ui/Input.svelte';
  import type { IUser } from '$lib/types/user';

  let email = $state('');
  let password = $state('');
  let error = $state('');
  let loading = $state(false);

  async function handleSubmit() {
    loading = true;
    error = '';
    try {
      const { user } = await api.post<{ user: IUser }>('/auth/login', {
        email,
        password
      });
      userStore.set(user);
      await goto('/');
    } catch (e: any) {
      error = e.message || 'Невірний email або пароль.';
    } finally {
      loading = false;
    }
  }
</script>

<FormWrapper title="Вхід у акаунт" description="Увійдіть, щоб отримати доступ до всіх можливостей.">
  <form onsubmit={handleSubmit} class="space-y-6">
    {#if error}
      <Alert type="error">{error}</Alert>
    {/if}

    <Input name="email" type="email" label="Електронна пошта" required bind:value={email} />
    <Input name="password" type="password" label="Пароль" required bind:value={password} />

    <Button type="submit" {loading} class="w-full">Увійти</Button>
  </form>
  <p class="mt-4 text-center text-sm text-gray-600">
    Немає акаунту? <a
      href="/auth/register"
      class="font-medium text-indigo-600 hover:text-indigo-500">Зареєструватися</a
    >
    <br />
    <a href="/admin/login" class="font-sm text-gray-600 hover:text-indigo-500">Увійти як адмін</a>
  </p>
</FormWrapper>
