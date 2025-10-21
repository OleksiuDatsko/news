<script lang="ts">
	let {
		label = '',
		name,
		type = 'text',
		required = false,
		placeholder = '',
		error = '',
		value = $bindable(''),
		...rest
	} = $props();
</script>

<div>
	<label for={name} class="block text-sm font-medium text-gray-700">
		{label}
	</label>
	<div class="mt-1">
		<input
			{name}
			{type}
			id={name}
			{required}
			{placeholder}
			bind:value
			class="appearance-none block w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:outline-none sm:text-sm"
			class:border-gray-300={!error}
			class:focus:ring-indigo-500={!error}
			class:focus:border-indigo-500={!error}
			class:border-red-500={error}
			class:focus:ring-red-500={error}
			class:focus:border-red-500={error}
			{...rest}
		/>
	</div>
	{#if error}
		<p class="mt-2 text-sm text-red-600" id="{name}-error">
			{error}
		</p>
	{/if}
</div>