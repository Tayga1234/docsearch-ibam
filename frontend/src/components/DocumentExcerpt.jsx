import { sanitizeHighlightHtml } from "../utils/format";

export default function DocumentExcerpt({ excerpt }) {
  const safe = sanitizeHighlightHtml(excerpt);
  return <p className="document-excerpt" dangerouslySetInnerHTML={{ __html: safe }} />;
}
