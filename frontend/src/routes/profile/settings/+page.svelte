<script lang="ts">
	import Button from '$lib/components/ui/Button.svelte';
	import Alert from '$lib/components/ui/Alert.svelte';

	let error = $state('');
	let loading = $state(false);
	
	// Ці значення мали б завантажуватись з $userStore.preferences
	let dailyDigest = $state(true);
	let authorNews = $state(false);
	let breakingNews = $state(true);

	function handleSubmit() {
		loading = true;
		error = 'Функціонал збереження налаштувань ще не реалізовано на бекенді.';
		loading = false;
		
		// TODO: Коли бекенд буде готовий, тут буде виклик
		// await api.put('/auth/me/preferences', { 
		//   dailyDigest, authorNews, breakingNews 
		// });
	}
</script>

<svelte:head>
	<title>Налаштування</title>
</svelte:head>

<div class="max-w-2xl mx-auto">
	<a href="/profile" class="text-indigo-600 hover:underline text-sm">&larr; Назад до профілю</a>
	<h1 class="text-3xl font-bold text-gray-900 mt-2 mb-8">
		Налаштування
	</h1>

	<div class="bg-white p-8 rounded-lg shadow-lg border border-gray-100">
		<form onsubmit={handleSubmit} class="space-y-6">
			
			<h2 class="text-lg font-semibold text-gray-800 border-b pb-2">Сповіщення</h2>
			
			{#if error}
				<Alert type="error">{error}</Alert>
			{/if}

			<div class="flex items-center justify-between">
				<label for="breakingNews" class="font-medium text-gray-700">Термінові новини</label>
				<input
					id="breakingNews"
					type="checkbox"
					bind:checked={breakingNews}
					class="h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
				/>
			</div>
			
			<div class="flex items-center justify-between">
				<label for="dailyDigest" class="font-medium text-gray-700">Щоденний дайджест</label>
				<input
					id="dailyDigest"
					type="checkbox"
					bind:checked={dailyDigest}
					class="h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
				/>
			</div>

			<div class="flex items-center justify-between">
				<label for="authorNews" class="font-medium text-gray-700">Новини від улюблених авторів</label>
				<input
					id="authorNews"
					type="checkbox"
					bind:checked={authorNews}
					class="h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
				/>
			</div>
			
			<div class="border-t pt-6">
				<Button type="submit" loading={loading} class="!w-auto">
					Зберегти зміни
				</Button>
			</div>
		</form>
	</div>
</div>