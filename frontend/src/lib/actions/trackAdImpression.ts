import { api } from '$lib/services/api';

interface Options {
	adId: number;
}

let observer: IntersectionObserver;

function getAdObserver(): IntersectionObserver {
	if (observer) {
		return observer;
	}

	observer = new IntersectionObserver(
		(entries) => {
			entries.forEach((entry) => {
				if (entry.isIntersecting) {
					const node = entry.target as HTMLElement;
					const adId = node.dataset.adId;

					if (adId) {
						api.post(`/ads/${adId}/impression`, {}).catch(
							(err) => {
								console.error(
									`Failed to track impression for Ad ${adId}`,
									err
								);
							}
						);
						observer.unobserve(node);
					}
				}
			});
		},
		{
			root: null,
			threshold: 0.5
		}
	);

	return observer;
}

export function trackAdImpression(node: HTMLElement, options: Options) {
	if (!options || !options.adId) {
		console.warn('trackAdImpression action requires adId');
		return;
	}

	node.dataset.adId = options.adId.toString();
	
	const obs = getAdObserver();
	obs.observe(node);

	return {
		destroy() {
			obs.unobserve(node);
		}
	};
}