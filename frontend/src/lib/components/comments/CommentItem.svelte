<script lang="ts">
	import type { IComment } from '$lib/types/comment';

	let { comment }: { comment: IComment } = $props();

	function formatDate(dateString: string) {
		return new Date(dateString).toLocaleDateString('uk-UA', {
			year: 'numeric',
			month: 'long',
			day: 'numeric',
			hour: '2-digit',
			minute: '2-digit'
		});
	}
</script>

<article class="p-4 bg-gray-50 rounded-lg border border-gray-200">
	<div class="flex justify-between items-center mb-2">
		<p class="font-semibold text-sm text-gray-900">
			{comment.user?.username ?? 'Анонім'}
		</p>
		<time class="text-xs text-gray-500">
			{formatDate(comment.created_at)}
		</time>
	</div>
	<p class="text-gray-700 text-base">
		{comment.text}
	</p>
</article>