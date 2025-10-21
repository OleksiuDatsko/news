import { writable } from 'svelte/store';
import type { IUser } from '$lib/types/user';
import type { IAdmin } from '$lib/types/admin';

export const userStore = writable<IUser | null>(null);
export const adminStore = writable<IAdmin | null>(null);