/** Affiche le texte indexé en prose lisible (pas en bloc de code). */
export default function DocumentContent({ content }) {
  const paragraphs = String(content || "")
    .replace(/\r\n/g, "\n")
    .split(/\n{2,}/)
    .map((block) => block.replace(/\n+/g, " ").replace(/\s+/g, " ").trim())
    .filter(Boolean);

  if (paragraphs.length === 0) return null;

  return (
    <div className="document-content">
      {paragraphs.map((paragraph, index) => (
        <p key={`p-${index}`}>{paragraph}</p>
      ))}
    </div>
  );
}
