import { writable } from 'svelte/store';
import type { ICategory } from '$lib/types/category';

export const categoryStore = writable<ICategory[]>([]);
