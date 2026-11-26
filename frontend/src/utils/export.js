function slugify(value) {
  const slug = String(value || "document")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-zA-Z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "")
    .slice(0, 60);
  return slug || "document";
}

export function downloadDocumentFiche(doc) {
  const lines = [
    "DocSearch — Fiche document",
    `Titre : ${doc.title}`,
    `Type : ${doc.file_type}`,
    `Taille : ${doc.size_bytes} octets`,
    `Indexé : ${doc.indexed_at || "—"}`,
    `Tags : ${(doc.tags || []).join(", ") || "—"}`,
    "",
    "Résumé",
    doc.summary || "—",
    "",
    "Texte indexé",
    doc.content || "—",
  ];
  const blob = new Blob([`${lines.join("\n")}\n`], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${slugify(doc.title)}.txt`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}
