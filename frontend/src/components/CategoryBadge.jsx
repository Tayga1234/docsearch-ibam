import { CATEGORY_LABELS } from "../utils/format";

export default function CategoryBadge({ category }) {
  const meta = CATEGORY_LABELS[category] || CATEGORY_LABELS.archives;
  return <span className={`file-badge category-badge ${meta.className}`}>{meta.label}</span>;
}
