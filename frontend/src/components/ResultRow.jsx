import { Link } from "react-router-dom";
import CategoryBadge from "./CategoryBadge";
import DocumentExcerpt from "./DocumentExcerpt";
import FileBadge from "./FileBadge";
import TagList from "./TagList";
import { CATEGORY_LABELS, FILE_LABELS, formatDate, formatSize } from "../utils/format";

export default function ResultRow({ doc, rank, maxScore, showScore, onTagClick }) {
  const score = Number(doc.score) || 0;
  const relevance = showScore && maxScore ? Math.max(6, Math.round((score / maxScore) * 100)) : 0;
  const typeMeta = FILE_LABELS[doc.file_type] || { label: (doc.file_type || "?").toUpperCase() };
  const category = doc.category || "archives";
  const categoryMeta = CATEGORY_LABELS[category] || CATEGORY_LABELS.archives;

  return (
    <li className="result-row" style={{ "--stagger": `${Math.max(0, rank - 1) * 40}ms` }}>
      <Link to={`/documents/${doc.id}`} className={`result-main ${showScore ? "has-rank" : ""}`}>
        {showScore && (
          <div className="result-rank-col">
            <span className="result-rank" aria-hidden>
              {String(rank).padStart(2, "0")}
            </span>
            {relevance > 0 && (
              <span className="result-relevance" title={`Pertinence relative ${relevance} %`}>
                {relevance}%
              </span>
            )}
          </div>
        )}

        <div className="result-body">
          <div className="result-topline">
            <FileBadge fileType={doc.file_type} />
            <CategoryBadge category={category} />
            <h3 className="result-title">{doc.title}</h3>
          </div>

          <div className="result-meta-row">
            <span className="result-pill">{typeMeta.label}</span>
            <span className="result-pill">{categoryMeta.label}</span>
            {doc.size_bytes ? <span className="result-pill">{formatSize(doc.size_bytes)}</span> : null}
            {doc.indexed_at ? <span className="result-pill">{formatDate(doc.indexed_at)}</span> : null}
          </div>

          <DocumentExcerpt excerpt={doc.excerpt} />

          {showScore && (
            <div className="score-meter" title={`Score ${score.toFixed(2)}`}>
              <div className="score-track">
                <span className="score-meter-fill" style={{ width: `${relevance}%` }} />
              </div>
              <span className="score-meter-label">{score.toFixed(2)}</span>
            </div>
          )}
        </div>

        <span className="result-open">Ouvrir</span>
      </Link>

      {(doc.tags || []).length > 0 && (
        <div className="result-tags">
          <TagList tags={doc.tags} onTagClick={onTagClick} />
        </div>
      )}
    </li>
  );
}
