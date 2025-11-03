import { api } from '$lib/services/api';
import type { IAuthor } from '$lib/types/author';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch }) => {
	const { id } = params;
	try {
		const author = await api.get<IAuthor>(`/admin/authors/${id}`, fetch);
		return {
			author
		};
	} catch (error) {
		console.error(`Failed to load author ${id}:`, error);
		return {
			author: null
		};
	}
};