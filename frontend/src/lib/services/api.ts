import { error } from '@sveltejs/kit';

// Використовуємо глобальний fetch, оскільки ми в SPA-режимі
const handleResponse = async (response: Response) => {
	if (response.ok) {
		if (response.status === 204) {
			return null;
		}
		try {
			return await response.json();
		} catch (e) {
			return null; // Повертаємо null, якщо тіло відповіді порожнє
		}
	}

	let errorBody;
	try {
		errorBody = await response.json();
	} catch (e) {
		errorBody = { msg: 'An unknown error occurred.' };
	}

	const apiError = new Error(errorBody.msg || 'API request failed');
	(apiError as any).status = response.status;
	(apiError as any).body = errorBody;
	throw apiError;
};

const request = async <T>(method: string, url: string, data?: unknown): Promise<T> => {
	const options: RequestInit = {
		method,
		credentials: 'include',
		headers: {}
	};

	if (data) {
		options.headers = {'Content-type': 'application/json'};
		options.body = JSON.stringify(data);
	}

	const response = await fetch(`/api${url}`, options);
	return handleResponse(response);
};

// Експортуємо простий об'єкт з методами
export const api = {
	get: <T>(url: string) => request<T>('GET', url),
	post: <T>(url: string, data: unknown) => request<T>('POST', url, data),
	put: <T>(url: string, data: unknown) => request<T>('PUT', url, data),
	del: <T>(url: string) => request<T>('DELETE', url)
};