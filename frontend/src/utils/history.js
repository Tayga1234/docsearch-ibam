const KEY = "docsearch_history";
const LIMIT = 8;

export function readHistory() {
  try {
    const items = JSON.parse(sessionStorage.getItem(KEY) || "[]");
    return Array.isArray(items) ? items : [];
  } catch {
    return [];
  }
}

export function pushHistory(query, mode) {
  const cleaned = String(query || "").trim();
  if (!cleaned) return readHistory();
  const next = [
    { q: cleaned, mode, at: Date.now() },
    ...readHistory().filter((item) => item.q !== cleaned),
  ].slice(0, LIMIT);
  sessionStorage.setItem(KEY, JSON.stringify(next));
  return next;
}

export function clearHistory() {
  sessionStorage.removeItem(KEY);
  return [];
}
