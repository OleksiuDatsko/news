import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals }) => {
	if (!locals.admin) {
		throw redirect(303, '/admin/login');
	}
	return {
		admin: locals.admin
	};
};