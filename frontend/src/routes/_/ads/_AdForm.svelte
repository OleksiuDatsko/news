<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
	import Alert from '$lib/components/ui/Alert.svelte';
	import Input from '$lib/components/ui/Input.svelte';
	import type { IAdminAd } from './+page.ts';

	let {
		ad = null, // Передаємо дані для режиму редагування
		onSubmit, // Функція, яку компонент викликає при сабміті
		error = $bindable(''),
		loading = $bindable(false)
	}: {
		ad?: IAdminAd | null;
		onSubmit: (payload: any) => Promise<void>;
		error?: string;
		loading?: boolean;
	} = $props();

	let title = $state(ad?.title ?? '');
	let content = $state(ad?.content ?? '');
	let ad_type = $state(ad?.ad_type ?? 'banner');
	let is_active = $state(ad?.is_active ?? true);
	// <input type="date"> вимагає формат YYYY-MM-DD
	let start_date = $state(ad?.start_date ? new Date(ad.start_date).toISOString().split('T')[0] : '');
	let end_date = $state(ad?.end_date ? new Date(ad.end_date).toISOString().split('T')[0] : '');

	const adTypes = ['banner', 'sidebar', 'popup', 'inline', 'video'];

	async function handleSubmit() {
		loading = true;
		error = '';

		// Конвертуємо дати в ISO формат, або null, якщо поле порожнє
		// Бекенд очікує дати в ISO (або null) [cite: 99, 101, 111, 112]
		const payload = {
			title,
			content,
			ad_type,
			is_active,
			start_date: start_date ? new Date(start_date).toISOString() : null,
			end_date: end_date ? new Date(end_date).toISOString() : null
		};

		try {
			await onSubmit(payload);
		} catch (e: any) {
			error = e.message || 'Помилка збереження оголошення.';
		} finally {
			loading = false;
		}
	}
</script>

<form onsubmit={handleSubmit} class="space-y-6">
	{#if error}
		<Alert type="error">{error}</Alert>
	{/if}

	<Input name="title" label="Заголовок" required bind:value={title} />

	<div>
		<label for="ad_type" class="block text-sm font-medium text-gray-700">
			Тип Оголошення
		</label>
		<select
			id="ad_type"
			name="ad_type"
			required
			bind:value={ad_type}
			class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
		>
			{#each adTypes as type (type)}
				<option value={type}>{type}</option>
			{/each}
		</select>
	</div>

	<div>
		<label for="content" class="block text-sm font-medium text-gray-700">
			Вміст (Текст/HTML)
		</label>
		<textarea
			id="content"
			name="content"
			rows={5}
			bind:value={content}
			class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
		></textarea>
	</div>

	<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
		<Input name="start_date" label="Дата Початку (optional)" type="date" bind:value={start_date} />
		<Input name="end_date" label="Дата Закінчення (optional)" type="date" bind:value={end_date} />
	</div>

	<div class="flex items-center">
		<input
			id="is_active"
			name="is_active"
			type="checkbox"
			bind:checked={is_active}
			class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
		/>
		<label for="is_active" class="ml-2 block text-sm text-gray-900">
			Активне (показувати оголошення)
		</label>
	</div>

	<div class="flex gap-4">
		<Button type="submit" {loading} class="!w-auto">
			{ad ? 'Зберегти Зміни' : 'Створити Оголошення'}
		</Button>
		<a
			href="/_/ads"
			class="inline-flex items-center justify-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
		>
			Скасувати
		</a>
	</div>
</form>