import { FILE_LABELS } from "../utils/format";

export default function FileBadge({ fileType }) {
  const info = FILE_LABELS[fileType] || {
    label: fileType?.toUpperCase() || "?",
    className: "badge-default",
  };
  return <span className={`file-badge ${info.className}`}>{info.label}</span>;
}
