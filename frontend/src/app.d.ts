import type { IAdmin } from '$lib/types/admin';
import type { IUser } from '$lib/types/user';

declare global {
	namespace App {
		interface Locals {
			user: IUser | null;
			admin: IAdmin | null;
		}
	}
}

export { };