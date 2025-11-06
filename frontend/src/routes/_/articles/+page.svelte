<script lang="ts">
	import { goto } from "$app/navigation";
	import { api } from "$lib/services/api";
	import type { IArticle } from "$lib/types/article";
	import Button from "$lib/components/ui/Button.svelte";
	import Alert from "$lib/components/ui/Alert.svelte";
	import type { PageData } from "./$types";
	import Pagination from "$lib/components/ui/Pagination.svelte";

	let { data }: { data: PageData } = $props();

	let articles = $derived(data.articles);
	let error = $state("");
	let loadingAction = $state(false);
	let loadingPublishId = $state<number | null>(null);

	function formatDate(dateString: string) {
		return new Date(dateString).toLocaleDateString("uk-UA", {
			year: "numeric",
			month: "long",
			day: "numeric",
		});
	}

	function handleCreateNew() {
		goto("/_/articles/new");
	}

	function handleEdit(articleId: number) {
		goto(`/_/articles/${articleId}`);
	}

	async function handleDelete(articleId: number) {
		if (loadingAction) return;
		if (!confirm("Ви впевнені, що хочете видалити цю статтю?")) {
			return;
		}

		loadingAction = true;
		error = "";
		try {
			await api.del(`/admin/articles/${articleId}`);
			articles = articles.filter((a) => a.id !== articleId);
		} catch (e: any) {
			error = e.message || "Помилка видалення статті.";
		} finally {
			loadingAction = false;
		}
	}

	function getStatusClass(status: string) {
		switch (status) {
			case "published":
				return "bg-green-100 text-green-800";
			case "draft":
				return "bg-yellow-100 text-yellow-800";
			case "archived":
				return "bg-gray-100 text-gray-600";
			default:
				return "bg-gray-100 text-gray-800";
		}
	}

	async function handlePublish(articleId: number) {
		if (loadingAction || loadingPublishId) return;

		loadingPublishId = articleId;
		error = "";
		try {
			// Використовуємо існуючий API-ендпоінт для оновлення статусу
			const updatedArticle = await api.put<IArticle>(
				`/admin/articles/${articleId}/status`,
				{
					status: "published",
				},
			);

			// Оновлюємо дані в таблиці "на льоту" без перезавантаження
			articles = articles.map((a) =>
				a.id === articleId ? updatedArticle : a,
			);
		} catch (e: any) {
			error = e.message || "Помилка публікації статті.";
		} finally {
			loadingPublishId = null;
		}
	}
</script>

<svelte:head>
	<title>Адмін: Статті</title>
</svelte:head>

<div class="flex justify-between items-center mb-6">
	<h1 class="text-3xl font-bold text-gray-900">Управління Статтями</h1>
	<Button onclick={handleCreateNew} class="shadow-sm">
		<svg
			class="-ml-1 mr-2 h-5 w-5"
			xmlns="http://www.w3.org/2000/svg"
			viewBox="0 0 20 20"
			fill="currentColor"
		>
			<path
				fill-rule="evenodd"
				d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
				clip-rule="evenodd"
			/>
		</svg>
		Створити Статтю
	</Button>
</div>

{#if error}
	<Alert type="error">{error}</Alert>
{/if}

<div class="bg-white shadow-lg rounded-lg overflow-hidden">
	{#if articles.length > 0}
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
							>Заголовок</th
						>
						<th
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
							>Автор</th
						>
						<th
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
							>Категорія</th
						>
						<th
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
							>Статус</th
						>
						<th
							class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
							>Дата</th
						>
						<th
							class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
							>Дії</th
						>
					</tr>
				</thead>
				<tbody class="bg-white divide-y divide-gray-200">
					{#each articles as article (article.id)}
						<tr
							class="hover:bg-gray-50 transition-colors duration-150"
						>
							<td
								class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
							>
								{article.id}
							</td>
							<td
								class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
							>
								{article.title}
							</td>
							<td
								class="px-6 py-4 whitespace-nowrap text-sm text-gray-700"
							>
								{article.author.first_name}
								{article.author.last_name}
							</td>
							<td
								class="px-6 py-4 whitespace-nowrap text-sm text-gray-700"
							>
								{article.category?.name ?? "N/A"}
							</td>
							<td class="px-6 py-4 whitespace-nowrap text-sm">
								<span
									class="px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full {getStatusClass(
										article.status,
									)}"
								>
									{article.status}
								</span>
							</td>
							<td
								class="px-6 py-4 whitespace-nowrap text-sm text-gray-700"
							>
								{formatDate(article.created_at)}
							</td>
							<td
								class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2"
							>
								{#if article.status === "draft"}
									<Button
										onclick={() =>
											handlePublish(article.id)}
										loading={loadingPublishId ===
											article.id}
										disabled={loadingAction ||
											loadingPublishId !== null}
										class="!w-auto !py-1 !px-3 !bg-green-600 hover:!bg-green-700 !text-xs !font-medium"
									>
										Опублікувати
									</Button>
								{/if}
								<Button
									onclick={() => handleEdit(article.id)}
									disabled={loadingAction}
									class="!w-auto !py-1 !px-3 !bg-blue-600 hover:!bg-blue-700 !text-xs !font-medium"
								>
									Редагувати
								</Button>
								<Button
									onclick={() => handleDelete(article.id)}
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
		<Pagination
			currentPage={data.page}
			perPage={data.perPage}
			totalItems={data.total}
		/>
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
					d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
				/>
			</svg>
			<h3 class="mt-2 text-lg font-medium text-gray-900">
				Жодної статті не знайдено
			</h3>
			<p class="mt-1 text-sm text-gray-500">
				Почніть наповнювати ваш сайт контентом.
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
							fill-rule="evenodd"
							d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
							clip-rule="evenodd"
						/>
					</svg>
					Створити першу статтю
				</Button>
			</div>
		</div>
	{/if}
</div>
