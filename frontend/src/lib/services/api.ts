type FetchFn = typeof fetch;

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

const request = async <T>(
	method: string,
	url: string,
	data?: unknown,
	customFetch?: FetchFn
): Promise<T> => {
	const options: RequestInit = {
		method,
		credentials: 'include',
		headers: {}
	};

	if (data) {
		options.headers = { 'Content-type': 'application/json' };
		options.body = JSON.stringify(data);
	}

	const fetchFn = customFetch || fetch;

	const baseUrl = "/api";

	const fullUrl = `${baseUrl}${url}`;

	const response = await fetchFn(fullUrl, options);
	return handleResponse(response);
};

export const api = {
	get: <T>(url: string, customFetch?: FetchFn) => request<T>('GET', url, undefined, customFetch),
	post: <T>(url: string, data: unknown, customFetch?: FetchFn) =>
		request<T>('POST', url, data, customFetch),
	put: <T>(url: string, data: unknown, customFetch?: FetchFn) =>
		request<T>('PUT', url, data, customFetch),
	del: <T>(url: string, customFetch?: FetchFn) => request<T>('DELETE', url, undefined, customFetch)
};