<script lang="ts">
	let {
		title = 'Form Title',
		description = '',
		children
	} = $props();
</script>

<div class="min-h-full flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
	<div class="max-w-md w-full space-y-8">
		<div>
			<h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
				{title}
			</h2>
			{#if description}
				<p class="mt-2 text-center text-sm text-gray-600">
					{description}
				</p>
			{/if}
		</div>
		<div class="mt-8 space-y-6 bg-white p-8 shadow-xl rounded-lg">
			{@render children()}
		</div>
	</div>
</div>