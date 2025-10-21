<script lang="ts">
	type AlertType = 'error' | 'success';

	let {
		type = 'error', // 'error' | 'success'
		children
	}: { type?: AlertType; children?: any } = $props();

	const baseClasses = 'border px-4 py-3 rounded relative';
	const typeClasses: Record<AlertType, string> = {
		error: 'bg-red-100 border-red-400 text-red-700',
		success: 'bg-green-100 border-green-400 text-green-700'
	};
</script>

<div class="{baseClasses} {typeClasses[type]}" role="alert">
	<span class="block sm:inline">{@render children()}</span>
</div>