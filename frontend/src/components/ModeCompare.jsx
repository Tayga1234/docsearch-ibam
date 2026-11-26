import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import CategoryBadge from "./CategoryBadge";
import FileBadge from "./FileBadge";
import { compareSearch } from "../services/api";
import { SEARCH_MODES } from "../utils/format";

export default function ModeCompare({ query, onError }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!query.trim()) return undefined;
    let cancelled = false;
    setData(null);
    setLoading(true);
    compareSearch(query)
      .then((payload) => {
        if (!cancelled) setData(payload);
      })
      .catch((err) => {
        if (!cancelled) onError?.(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [query, onError]);

  if (loading && !data) {
    return <p className="muted-line">Comparaison des trois modes…</p>;
  }

  if (!data) return null;

  return (
    <section className="compare-panel">
      <div className="compare-head">
        <span className="section-label">Même requête, trois modes</span>
        <p>Les 3 premiers résultats de chaque moteur, pour montrer l’effet de l’indexation.</p>
      </div>
      <div className="compare-grid">
        {SEARCH_MODES.map((mode) => {
          const hits = data.modes?.[mode.value] || [];
          return (
            <article key={mode.value} className="compare-card">
              <h3>{mode.label}</h3>
              <p>{mode.hint}</p>
              {hits.length === 0 ? (
                <p className="muted-line">Aucun hit.</p>
              ) : (
                <ol className="compare-list">
                  {hits.map((hit, index) => (
                    <li key={`${mode.value}-${hit.id}`}>
                      <span className="compare-rank">{index + 1}</span>
                      <div className="compare-hit">
                        <div className="compare-hit-badges">
                          <FileBadge fileType={hit.file_type} />
                          <CategoryBadge category={hit.category || "archives"} />
                        </div>
                        <Link to={`/documents/${hit.id}`}>{hit.title}</Link>
                      </div>
                      <span className="compare-score">{Number(hit.score).toFixed(2)}</span>
                    </li>
                  ))}
                </ol>
              )}
            </article>
          );
        })}
      </div>
    </section>
  );
}
