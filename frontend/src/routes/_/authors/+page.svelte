<script lang="ts">
	import { goto } from "$app/navigation";
	import { api } from "$lib/services/api";
	import type { IAuthor } from "$lib/types/author";
	import Button from "$lib/components/ui/Button.svelte";
	import Alert from "$lib/components/ui/Alert.svelte";
	import type { PageData } from "./$types";

	let { data }: { data: PageData } = $props();

	let authors = $derived(data.authors);
	let error = $state("");
	let loadingAction = $state(false);

	function handleCreateNew() {
		goto("/_/authors/new");
	}

	function handleEdit(authorId: number) {
		
		goto(`/_/authors/${authorId}`);
	}

	async function handleDelete(authorId: number) {
		if (loadingAction) return;
		if (
			!confirm(
				"Ви впевнені, що хочете видалити цього автора? Це неможливо, якщо у нього є статті.",
			)
		) {
			return;
		}

		loadingAction = true;
		error = "";
		try {
			await api.del(`/_/authors/${authorId}`);
			authors = authors.filter((a) => a.id !== authorId);
		} catch (e: any) {
			error =
				e.message ||
				"Помилка видалення автора. Можливо, у нього є статті.";
		} finally {
			loadingAction = false;
		}
	}
</script>

<svelte:head>
	<title>Адмін: Автори</title>
</svelte:head>

<div class="flex justify-between items-center mb-6">
	<h1 class="text-3xl font-bold text-gray-900">Управління Авторами</h1>
	<Button onclick={handleCreateNew} class="shadow-sm">
		<svg
			class="-ml-1 mr-2 h-5 w-5"
			xmlns="http://www.w3.org/2000/svg"
			viewBox="0 0 20 20"
			fill="currentColor"
		>
			<path
				d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 11a1 1 0 10-2 0v2h-2a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2v-2z"
			/>
		</svg>
		Створити Автора
	</Button>
</div>

{#if error}
	<Alert type="error">{error}</Alert>
{/if}

<div class="bg-white shadow-lg rounded-lg overflow-hidden">
	{#if authors.length > 0}
		<div class="overflow-x-auto">
			<table class="min-w-full divide-y divide-gray-200">
				<thead class="bg-gray-50">
					<tr>
						<th
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
							>ID</th
						>
						<th
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
							>Ім'я</th
						>
						<th
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
							>Прізвище</th
						>
						<th
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
							>К-ть статей</th
						>
						<th
							class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
							>Дії</th
						>
					</tr>
				</thead>
				<tbody class="bg-white divide-y divide-gray-200">
					{#each authors as author (author.id)}
						<tr
							class="hover:bg-gray-50 transition-colors duration-150"
						>
							<td
								class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
							>
								{author.id}
							</td>
							<td
								class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
							>
								{author.first_name}
							</td>
							<td
								class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
							>
								{author.last_name}
							</td>
							<td
								class="px-6 py-4 whitespace-nowrap text-sm text-gray-700"
							>
								{author.total_articles ?? 0}
							</td>
							<td
								class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2"
							>
								<Button
									onclick={() => handleEdit(author.id)}
									disabled={loadingAction}
									class="!w-auto !py-1 !px-3 !bg-blue-600 hover:!bg-blue-700 !text-xs !font-medium"
								>
									Редагувати
								</Button>
								<Button
									onclick={() => handleDelete(author.id)}
									disabled={loadingAction}
									class="!w-auto !py-1 !px-3 !bg-red-600 hover:!bg-red-700 !text-xs !font-medium"
								>
									Видалити
								</Button>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	{:else}
		<div class="text-center p-12">
			<svg
				class="mx-auto h-12 w-12 text-gray-400"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
				aria-hidden="true"
			>
				<path
					vector-effect="non-scaling-stroke"
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
				/>
			</svg>
			<h3 class="mt-2 text-lg font-medium text-gray-900">
				Жодного автора не знайдено
			</h3>
			<p class="mt-1 text-sm text-gray-500">
				Почніть додавати авторів, які будуть писати статті.
			</p>
			<div class="mt-6">
				<Button onclick={handleCreateNew} class="!w-auto shadow-sm">
					<svg
						class="-ml-1 mr-2 h-5 w-5"
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 20 20"
						fill="currentColor"
					>
						<path
							d="M8 9a3 3 0 100-6 3 3 0 000 6zM8 11a6 6 0 016 6H2a6 6 0 016-6zM16 11a1 1 0 10-2 0v2h-2a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2v-2z"
						/>
					</svg>
					Створити першого автора
				</Button>
			</div>
		</div>
	{/if}
</div>
