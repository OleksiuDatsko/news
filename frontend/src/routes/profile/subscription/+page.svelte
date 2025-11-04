<script lang="ts">
	import { api } from '$lib/services/api';
	import type { PageData } from './$types';
	import Button from '$lib/components/ui/Button.svelte';
	import Alert from '$lib/components/ui/Alert.svelte';
	import { userStore } from '$lib/stores/authStore';

	let { data }: { data: PageData } = $props();

	let currentSubscription = $state(data.currentSubscription);
	let loadingPlanId = $state<number | null>(null);
	let error = $state('');
	let success = $state('');

	async function handleSubscribe(planId: number) {
		if (loadingPlanId) return;
		loadingPlanId = planId;
		error = '';
		success = '';

		try {
			const newSubscription = await api.post<any>(
				'/subscriptions/subscribe',
				{ plan_id: planId }
			);
			currentSubscription = newSubscription;
			
			userStore.update(user => {
				if (user) {
					user.permissions = newSubscription.plan.permissions;
				}
				return user;
			});

			success = `Ви успішно підписалися на план "${newSubscription.plan.name}"!`;

		} catch (e: any) {
			error = e.message || 'Не вдалося оновити підписку.';
		} finally {
			loadingPlanId = null;
		}
	}
	
	function getPlanFeatures(permissions: any) {
		const features = [];
		if (permissions.exclusive_content) features.push("Доступ до ексклюзивних статей");
		if (permissions.comment) features.push("Можливість коментувати");
		if (permissions.save_article) features.push("Збереження статей");
		if (permissions.no_ads) features.push("Відсутність реклами");
		
		return features;
	}
</script>

<svelte:head>
	<title>Моя підписка</title>
</svelte:head>

<div class="max-w-4xl mx-auto">
	<a href="/profile" class="text-indigo-600 hover:underline text-sm">&larr; Назад до профілю</a>
	<h1 class="text-3xl font-bold text-gray-900 mt-2 mb-8">
		Керування підпискою
	</h1>

	{#if error}
		<Alert type="error" additionalClass="mb-6">{error}</Alert>
	{/if}
	{#if success}
		<Alert type="success" additionalClass="mb-6">{success}</Alert>
	{/if}

	<div class="bg-white p-6 rounded-lg shadow-lg border border-gray-100 mb-8">
		<h2 class="text-xl font-bold text-gray-900 mb-3">Ваш поточний план</h2>
		{#if currentSubscription && currentSubscription.is_active}
			<p class="text-lg font-semibold text-indigo-600">
				{currentSubscription.plan.name}
			</p>
			{#if currentSubscription.left_days}
			<p class="text-sm text-gray-600">
				Залишилось днів: {currentSubscription.left_days}
			</p>
			{/if}
			<ul class="mt-4 space-y-2 text-sm text-gray-700">
				{#each getPlanFeatures(currentSubscription.plan.permissions) as feature}
					<li class="flex items-center gap-2">
						<span class="text-green-500">✔</span> {feature}
					</li>
				{/each}
			</ul>
		{:else}
			<p class="text-gray-600">
				У вас немає активної підписки.
			</p>
		{/if}
	</div>

	<div>
		<h2 class="text-2xl font-bold text-gray-900 mb-6">Доступні плани</h2>
		<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
			{#each data.plans as plan (plan.id)}
				{@const features = getPlanFeatures(plan.permissions)}
				{@const isCurrentPlan = currentSubscription?.plan_id === plan.id}
				
				<div 
					class="bg-white p-6 rounded-lg shadow-lg border"
					class:border-indigo-500={isCurrentPlan}
					class:border-gray-100={!isCurrentPlan}
				>
					<h3 class="text-xl font-bold text-gray-900">{plan.name}</h3>
					<p class="text-2xl font-bold text-gray-800 my-3">
						{Math.round(plan.price_per_month)} грн<span class="text-sm font-normal text-gray-500">/міс</span>
					</p>
					<p class="text-sm text-gray-600 min-h-10">{plan.description}</p>
					
					<ul class="my-6 space-y-2 text-sm text-gray-700">
						{#each features as feature}
							<li class="flex items-center gap-2">
								<span class="text-green-500">✔</span> {feature}
							</li>
						{/each}
					</ul>

					<Button
						onclick={() => handleSubscribe(plan.id)}
						loading={loadingPlanId === plan.id}
						disabled={isCurrentPlan}
						class="w-full"
					>
						{isCurrentPlan ? 'Це ваш план' : 'Обрати план'}
					</Button>
				</div>
			{/each}
		</div>
	</div>
</div>