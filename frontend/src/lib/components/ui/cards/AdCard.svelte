<script lang="ts">
	import type { IAd } from '$lib/types/ad';

	let { ad }: { ad: IAd } = $props();
	const adLink = '#'; // Ваше посилання для відстеження кліку
</script>

<div
	class="relative flex flex-col bg-white rounded-lg shadow-md overflow-hidden border border-gray-100 max-w-sm"
>
	<span class="absolute top-2 right-2 text-xs font-semibold text-gray-400 bg-gray-50 px-2 py-0.5 rounded">
		Реклама
	</span>

	<div class="p-6 pt-8 flex-grow">
		<h3 class="font-bold text-gray-900 text-lg mb-2">
			{ad.title}
		</h3>

		{#if ad.content}
			<p class="text-sm text-gray-600">
				{ad.content}
			</p>
		{/if}
	</div>

	<div class="px-6 pb-6 pt-2">
		<a
			href={adLink}
			class="block w-full text-center text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded-md shadow-sm transition-colors"
			target="_blank"
			rel="noopener sponsored"
		>
			Дізнатися більше
		</a>
	</div>
</div>