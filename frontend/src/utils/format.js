export function formatSize(bytes) {
  if (!bytes) return "—";
  if (bytes < 1024) return `${bytes} o`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} Ko`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} Mo`;
}

export function formatDate(value) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "—";
  return date.toLocaleString("fr-FR", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

/** Autorise uniquement les balises <mark> provenant de Whoosh. */
export function sanitizeHighlightHtml(html) {
  if (!html) return "";
  const slots = [];
  // Protège d'abord les balises mark (avec attributs éventuels), puis échappe le reste
  const tokenized = String(html).replace(/<\/?mark\b[^>]*>/gi, (tag) => {
    const safe = /^<\s*\/\s*mark/i.test(tag) ? "</mark>" : "<mark>";
    const index = slots.push(safe) - 1;
    return `\u0000MARK${index}\u0000`;
  });
  const escaped = tokenized
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
  return escaped.replace(/\u0000MARK(\d+)\u0000/g, (_, index) => slots[Number(index)] || "");
}

export const FILE_LABELS = {
  pdf: { label: "PDF", className: "badge-pdf" },
  docx: { label: "Word", className: "badge-docx" },
  csv: { label: "CSV", className: "badge-csv" },
  txt: { label: "Texte", className: "badge-txt" },
};

export const CATEGORY_LABELS = {
  scientific: { label: "Scientifique", className: "badge-scientific" },
  archives: { label: "Archives IBAM", className: "badge-archives" },
};

export const CATEGORY_FILTERS = [
  { value: "", label: "Toutes les classes" },
  { value: "scientific", label: "Scientifique" },
  { value: "archives", label: "Archives IBAM" },
];

export const SEARCH_MODES = [
  { value: "hybrid", label: "Hybride", hint: "Mots-clés + TF-IDF" },
  { value: "keyword", label: "Mots-clés", hint: "Correspondance exacte (BM25)" },
  {
    value: "semantic",
    label: "Sémantique",
    hint: "Similarité TF-IDF (pas d’embedding neuronal)",
  },
];

export const FILE_TYPE_FILTERS = [
  { value: "", label: "Tous types" },
  { value: "pdf", label: "PDF" },
  { value: "docx", label: "Word" },
  { value: "csv", label: "CSV" },
  { value: "txt", label: "Texte" },
];

export const DEMO_QUERIES = [
  { q: "BM25", hint: "articles scientifiques sur le ranking lexical" },
  { q: "TF-IDF", hint: "similarité et vectorisation de documents" },
  { q: "index inversé", hint: "fondements de la recherche d'information" },
  { q: "embedding", hint: "NLP et représentations vectorielles" },
  { q: "formation", hint: "pièces IBAM (plan RH, ateliers)" },
  { q: "budget documentaire", hint: "pièces IBAM (ligne archives)" },
];

