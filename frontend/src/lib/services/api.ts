import { adminStore, userStore } from '$lib/stores/authStore';

type FetchFn = typeof fetch;

export class ApiError extends Error {
	status: number;
	body: { msg: string };

	constructor(message: string, status: number, body: any) {
		super(message);
		this.name = 'ApiError';
		this.status = status;
		this.body = body || { msg: message };
	}
}

const handleResponse = async <T>(response: Response): Promise<T> => {
	if (response.ok) {
		if (response.status === 204) {
			return null as T;
		}
		try {
			return await response.json();
		} catch (e) {
			return null as T;
		}
	}

	let errorBody;
	try {
		errorBody = await response.json();
	} catch (e) {
		errorBody = { msg: 'Сталася невідома помилка API.' };
	}

	throw new ApiError(errorBody.msg || 'Запит API не вдався', response.status, errorBody);
};

let isRefreshing = false;
let refreshPromise: Promise<void> | null = null;

async function handleRefresh(url: string, baseFetch: FetchFn): Promise<void> {
	if (isRefreshing && refreshPromise) {
		return refreshPromise;
	}

	isRefreshing = true;

	const isAdmin = url.startsWith('/admin/');
	const refreshUrl = isAdmin ? '/admin/auth/refresh' : '/auth/refresh';
	const logoutUrl = isAdmin ? '/admin/auth/logout' : '/auth/logout';
	const fullRefreshUrl = `/api${refreshUrl}`;
	const fullLogoutUrl = `/api${logoutUrl}`;

	refreshPromise = (async () => {
		try {
			const refreshResponse = await baseFetch(fullRefreshUrl, {
				method: 'POST',
				credentials: 'include'
			});

			if (!refreshResponse.ok) {
				throw new Error('Refresh token failed');
			}
		} catch (e) {
			userStore.set(null);
			adminStore.set(null);

			await baseFetch(fullLogoutUrl, {method: 'POST'})
			throw new ApiError('Сесія вичерпана. Будь ласка, увійдіть знову.', 401, null);
		} finally {
			isRefreshing = false;
			refreshPromise = null;
		}
	})();

	return refreshPromise;
}

const request = async <T>(
	method: string,
	url: string,
	data?: unknown,
	customFetch?: FetchFn
): Promise<T> => {
	const fetchFn = customFetch || fetch;
	const fullUrl = `/api${url}`;

	const options: RequestInit = {
		method,
		credentials: 'include',
		headers: {}
	};

	if (data) {
		options.headers = { 'Content-type': 'application/json' };
		options.body = JSON.stringify(data);
	}

	try {
		const response = await fetchFn(fullUrl, options);

		if (response.status !== 401) {
			return handleResponse<T>(response);
		}

		console.log('Token expired, attempting refresh...');
		await handleRefresh(url, fetchFn);

		console.log('Refresh successful, retrying original request...');
		const retryResponse = await fetchFn(fullUrl, options);

		return handleResponse<T>(retryResponse);
	} catch (error) {
		if (error instanceof ApiError) {
			throw error;
		}
		
		if (error instanceof Error) {
			throw new ApiError(error.message || 'Network error', 0, null);
		}

		throw new ApiError(String(error) || 'Network error', 0, null);
	}
};

export const api = {
	get: <T>(url: string, customFetch?: FetchFn) => request<T>('GET', url, undefined, customFetch),
	post: <T>(url: string, data: unknown, customFetch?: FetchFn) =>
		request<T>('POST', url, data, customFetch),
	put: <T>(url: string, data: unknown, customFetch?: FetchFn) =>
		request<T>('PUT', url, data, customFetch),
	del: <T>(url: string, customFetch?: FetchFn) => request<T>('DELETE', url, undefined, customFetch)
};