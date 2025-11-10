<script lang="ts">
  import { goto } from '$app/navigation';
  import { api } from '$lib/services/api';
  import { adminStore, userStore } from '$lib/stores/authStore';
  import Alert from '$lib/components/ui/Alert.svelte';
  import Button from '$lib/components/ui/Button.svelte';
  import FormWrapper from '$lib/components/ui/FormWrapper.svelte';
  import Input from '$lib/components/ui/Input.svelte';
  import type { IUser } from '$lib/types/user';
  import type { IAdmin } from '$lib/types/admin';

  let email = $state('');
  let password = $state('');
  let error = $state('');
  let loading = $state(false);

  async function handleSubmit() {
    loading = true;
    error = '';
    try {
      const { admin } = await api.post<{ admin: IAdmin }>('/admin/auth/login', { email, password });
      adminStore.set(admin);
      await goto('/');
    } catch (e: any) {
      error = e.message || 'Невірний email або пароль.';
    } finally {
      loading = false;
    }
  }
</script>

<FormWrapper title="Вхід у акаунт" description="Увійдіть.">
  <form onsubmit={handleSubmit} class="space-y-6">
    {#if error}
      <Alert type="error">{error}</Alert>
    {/if}

    <Input name="email" type="email" label="Електронна пошта" required bind:value={email} />
    <Input name="password" type="password" label="Пароль" required bind:value={password} />

    <Button type="submit" {loading} class="w-full">Увійти</Button>
  </form>
</FormWrapper>
