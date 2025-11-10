<script lang="ts">
  import { goto } from '$app/navigation';
  import { api } from '$lib/services/api';
  import Button from '$lib/components/ui/Button.svelte';
  import Alert from '$lib/components/ui/Alert.svelte';
  import Input from '$lib/components/ui/Input.svelte';
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();

  let username = $state(data.user?.username ?? '');
  let email = $state(data.user?.email ?? '');
  let profileError = $state('');
  let profileLoading = $state(false);

  let selectedPlanId = $state(data.user?.current_subscription?.plan_id ?? '');
  let subscriptionError = $state('');
  let subscriptionLoading = $state(false);

  let currentPlanName = $derived(data.user?.current_subscription?.plan.name ?? 'Відсутня');

  async function handleProfileSubmit() {
    if (!data.user) return;
    profileLoading = true;
    profileError = '';

    try {
      await api.put(`/admin/users/${data.user.id}`, {
        username,
        email
      });
    } catch (e: any) {
      profileError = e.message || 'Помилка оновлення профілю.';
    } finally {
      profileLoading = false;
    }
  }

  async function handleSubscriptionSubmit() {
    if (!data.user || !selectedPlanId) return;
    subscriptionLoading = true;
    subscriptionError = '';

    try {
      const response = await api.put<{ subscription: any }>(
        `/admin/users/${data.user.id}/subscription`,
        {
          plan_id: selectedPlanId
        }
      );
      if (data.user) {
        data.user.current_subscription = response.subscription;
      }
    } catch (e: any) {
      subscriptionError = e.message || 'Помилка зміни підписки.';
    } finally {
      subscriptionLoading = false;
    }
  }
</script>

<svelte:head>
  <title>Адмін: Редагувати {data.user?.username ?? 'Користувач'}</title>
</svelte:head>

{#if data.user}
  <h1 class="text-3xl font-bold text-gray-900 mb-6">
    Редагувати: {data.user.username}
  </h1>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
    <div class="bg-white p-8 rounded-lg shadow-lg">
      <h2 class="text-xl font-bold text-gray-900 mb-4">Дані Користувача</h2>
      <form onsubmit={handleProfileSubmit} class="space-y-6">
        {#if profileError}
          <Alert type="error">{profileError}</Alert>
        {/if}

        <Input name="username" label="Ім'я (Username)" required bind:value={username} />
        <Input name="email" type="email" label="Email" required bind:value={email} />

        <Button type="submit" loading={profileLoading} class="!w-auto">Зберегти Зміни</Button>
      </form>
    </div>

    <div class="bg-white p-8 rounded-lg shadow-lg">
      <h2 class="text-xl font-bold text-gray-900 mb-4">Керування Підпискою</h2>
      <p class="text-sm text-gray-600 mb-4">
        Поточний план: <strong class="text-gray-900">{currentPlanName}</strong>
      </p>

      <form onsubmit={handleSubscriptionSubmit} class="space-y-6">
        {#if subscriptionError}
          <Alert type="error">{subscriptionError}</Alert>
        {/if}

        <div>
          <label for="plan" class="block text-sm font-medium text-gray-700"> Змінити план </label>
          <select
            id="plan"
            name="plan"
            required
            bind:value={selectedPlanId}
            class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
          >
            <option value="" disabled>Оберіть новий план...</option>
            {#each data.plans as plan (plan.id)}
              <option value={plan.id}>
                {plan.name} ({Math.round(plan.price_per_month)} грн/міс)
              </option>
            {/each}
          </select>
        </div>

        <Button type="submit" loading={subscriptionLoading} class="!w-auto">
          Змінити Підписку
        </Button>
      </form>
    </div>
  </div>
{:else}
  <h1 class="text-3xl font-bold text-red-600 mb-6">Користувача не знайдено</h1>
  <Alert type="error">Не вдалося завантажити дані. Можливо, користувача було видалено.</Alert>
  <a href="/_/users" class="text-indigo-600 hover:underline mt-4 inline-block">
    &larr; Повернутися до списку користувачів
  </a>
{/if}
