<script lang="ts">
	import { goto } from '$app/navigation';
	import { api } from '$lib/services/api';
	import { userStore } from '$lib/stores/authStore';
	import Alert from '$lib/components/ui/Alert.svelte';
	import Button from '$lib/components/ui/Button.svelte';
	import FormWrapper from '$lib/components/ui/FormWrapper.svelte';
	import Input from '$lib/components/ui/Input.svelte';
    import type { IUser } from '$lib/types/user';

	let username = $state('');
	let email = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);

	async function handleSubmit() {
		loading = true;
		error = '';
		try {
			const { data: user  } = await api.post<{data: IUser}>('/auth/register', { username, email, password });
			userStore.set(user);
			await goto('/');
		} catch (e: any) {
			error = e.message || 'Помилка реєстрації.';
		} finally {
			loading = false;
		}
	}
</script>

<FormWrapper title="Створити акаунт" description="Приєднуйтесь до нашої спільноти читачів.">
	<form onsubmit={handleSubmit} class="space-y-6">
		{#if error}
			<Alert type="error">{error}</Alert>
		{/if}

		<Input name="username" label="Ім'я користувача" required bind:value={username} />
		<Input name="email" type="email" label="Електронна пошта" required bind:value={email} />
		<Input name="password" type="password" label="Пароль" required bind:value={password} />

		<Button type="submit" {loading} class="w-full">Зареєструватися</Button>
	</form>
	<p class="mt-4 text-center text-sm text-gray-600">
		Вже маєте акаунт? <a href="/auth/login" class="font-medium text-indigo-600 hover:text-indigo-500">Увійти</a>
	</p>
</FormWrapper>