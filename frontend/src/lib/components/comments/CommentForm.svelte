<script lang="ts">
	import { api } from '$lib/services/api';
	import Button from '$lib/components/ui/Button.svelte';
	import Alert from '$lib/components/ui/Alert.svelte';
	import type { IComment } from '$lib/types/comment';

	let {
		articleId,
		onCommentPosted
	}: {
		articleId: number;
		onCommentPosted: (comment: IComment) => void;
	} = $props();

	let text = $state('');
	let loading = $state(false);
	let error = $state('');

	async function handleSubmit() {
		if (!text.trim()) {
			error = 'Текст коментаря не може бути порожнім.';
			return;
		}

		loading = true;
		error = '';

		try {
			// Використовуємо існуючий POST endpoint [cite: 72]
			const newComment = await api.post<IComment>(`/articles/${articleId}/comments`, { text });
			text = ''; // Очистити поле
			onCommentPosted(newComment); // Повідомити батьківський компонент про успіх
		} catch (e: any) {
			error = e.message || 'Не вдалося додати коментар.';
		} finally {
			loading = false;
		}
	}
</script>

<form onsubmit={handleSubmit} class="mt-6 space-y-4">
	{#if error}
		<Alert type="error">{error}</Alert>
	{/if}

	<div>
		<label for="comment-text" class="block text-sm font-medium text-gray-700 mb-1">
			Ваш коментар
		</label>
		<textarea
			id="comment-text"
			rows="4"
			class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
			placeholder="Напишіть щось..."
			bind:value={text}
			disabled={loading}
		></textarea>
	</div>

	<div class="flex justify-end">
		<Button type="submit" {loading} class="!w-auto">
			Відправити
		</Button>
	</div>
</form>