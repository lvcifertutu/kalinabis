const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:5000';
const PROJECT_CODE = 'demo';

function baseHeaders(json = false): Record<string, string> {
  const h: Record<string, string> = { 'X-Project-Code': PROJECT_CODE };
  if (json) h['Content-Type'] = 'application/json';
  return h;
}

async function checkStatus(res: Response): Promise<Response> {
  if (!res.ok) {
    let message = `HTTP ${res.status}`;
    try {
      const body = await res.clone().json();
      if (body.error) message = body.error;
    } catch {
      // respuesta sin JSON — usar el status
    }
    throw new Error(message);
  }
  return res;
}

export const apiClient = {
  get<T>(path: string, signal?: AbortSignal): Promise<T> {
    return fetch(`${BACKEND_URL}${path}`, {
      headers: baseHeaders(),
      signal,
    })
      .then(checkStatus)
      .then((r) => r.json() as Promise<T>);
  },

  post<T>(path: string, body: unknown, signal?: AbortSignal): Promise<T> {
    return fetch(`${BACKEND_URL}${path}`, {
      method: 'POST',
      headers: baseHeaders(true),
      body: JSON.stringify(body),
      signal,
    })
      .then(checkStatus)
      .then((r) => r.json() as Promise<T>);
  },
};
