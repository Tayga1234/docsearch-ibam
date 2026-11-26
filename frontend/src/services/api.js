const API_BASE_URL =
  import.meta.env.VITE_API_URL || (import.meta.env.DEV ? "/api" : "http://127.0.0.1:8010");

const TOKEN_KEY = "docusearch_token";
const USER_KEY = "docusearch_user";

export function getStoredSession() {
  try {
    const token = localStorage.getItem(TOKEN_KEY);
    const user = JSON.parse(localStorage.getItem(USER_KEY) || "null");
    if (token && user) return { token, user };
  } catch {
    // ignore
  }
  return null;
}

export function storeSession(token, user) {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function clearSession() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

function authHeaders() {
  const token = localStorage.getItem(TOKEN_KEY);
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function parseError(response) {
  const raw = await response.text();
  try {
    const data = JSON.parse(raw);
    if (typeof data.detail === "string") return data.detail;
    if (Array.isArray(data.detail)) {
      return data.detail.map((item) => item.msg || JSON.stringify(item)).join(" ; ");
    }
  } catch {
    // ignore JSON parse
  }
  return raw || `Erreur API: ${response.status}`;
}

async function request(path, options = {}) {
  const headers = { ...authHeaders(), ...(options.headers || {}) };
  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });

  if (response.status === 401) {
    clearSession();
    window.dispatchEvent(new Event("docusearch:unauthorized"));
  }

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export function login(username, password) {
  return request("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
}

export function fetchMe() {
  return request("/auth/me");
}

export function logout() {
  return request("/auth/logout", { method: "POST" }).catch(() => null);
}

export function checkHealth() {
  return request("/health");
}

export function scanDocuments(force = false) {
  const query = force ? "?force=true" : "";
  return request(`/ingest/scan${query}`, { method: "POST" });
}

export function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);

  return request("/ingest/upload", {
    method: "POST",
    body: formData,
  });
}

export function rebuildIndex() {
  return request("/index/rebuild?confirm=true", { method: "POST" });
}

export function fetchDocuments({
  limit = 100,
  offset = 0,
  fileType = "",
  tag = "",
  q = "",
  category = "",
  sort = "category",
} = {}) {
  const params = new URLSearchParams({
    limit: String(limit),
    offset: String(offset),
    sort,
  });
  if (fileType) params.set("file_type", fileType);
  if (tag) params.set("tag", tag);
  if (q) params.set("q", q);
  if (category) params.set("category", category);
  return request(`/documents?${params.toString()}`);
}

export function fetchDocument(documentId) {
  return request(`/documents/${documentId}`);
}

export function deleteDocument(documentId) {
  return request(`/documents/${encodeURIComponent(documentId)}?confirm=true`, { method: "DELETE" });
}

export function searchDocuments(query, mode = "keyword", limit = 100) {
  const params = new URLSearchParams({ q: query, mode, limit: String(limit) });
  return request(`/search?${params.toString()}`);
}

export function compareSearch(query) {
  const params = new URLSearchParams({ q: query });
  return request(`/search/compare?${params.toString()}`);
}

export function swaggerDocsUrl() {
  const configured = import.meta.env.VITE_API_URL;
  if (!configured || configured === "/api") {
    return "http://127.0.0.1:8010/docs";
  }
  return `${String(configured).replace(/\/$/, "")}/docs`;
}
