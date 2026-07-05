export const API_BASE = process.env.NEXT_PUBLIC_BACKEND_API_URL ?? "http://localhost:8000";

export async function apiGet<T>(path: string, token?: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    cache: "no-store",
    headers: token ? { Authorization: `Bearer ${token}` } : undefined
  });
  if (!response.ok) {
    throw new Error("API通信に失敗しました");
  }
  return response.json() as Promise<T>;
}

export async function apiPost<T>(path: string, body: unknown, token?: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    },
    body: JSON.stringify(body)
  });
  return response.json() as Promise<T>;
}

export function getToken(): string {
  if (typeof window === "undefined") return "";
  return localStorage.getItem("auth_lab_token") ?? "";
}
