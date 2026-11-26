import { useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import EmptyState from "../components/EmptyState";
import ModeCompare from "../components/ModeCompare";
import ResultRow from "../components/ResultRow";
import SearchBar from "../components/SearchBar";
import { useApp } from "../context/AppContext";
import { searchDocuments } from "../services/api";
import { SEARCH_MODES } from "../utils/format";
import { clearHistory, pushHistory, readHistory } from "../utils/history";

export default function SearchPage() {
  const { apiStatus, setError } = useApp();
  const [params, setParams] = useSearchParams();
  const navigate = useNavigate();
  const q = params.get("q") || "";
  const mode = SEARCH_MODES.some((item) => item.value === params.get("mode"))
    ? params.get("mode")
    : "hybrid";

  const [query, setQuery] = useState(q);
  const [results, setResults] = useState(null);
  const [searching, setSearching] = useState(false);
  const [history, setHistory] = useState(readHistory);

  useEffect(() => {
    setQuery(q);
  }, [q]);

  useEffect(() => {
    if (!q.trim()) {
      setResults(null);
      setSearching(false);
      return undefined;
    }

    let cancelled = false;
    setSearching(true);
    searchDocuments(q, mode)
      .then((data) => {
        if (!cancelled) {
          setResults(data);
          setHistory(pushHistory(q, mode));
        }
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setSearching(false);
      });

    return () => {
      cancelled = true;
    };
  }, [q, mode, setError]);

  function handleSubmit(event) {
    event.preventDefault();
    const cleaned = query.trim();
    if (!cleaned) {
      setParams({});
      return;
    }
    setParams({ q: cleaned, mode });
  }

  function handleClear() {
    setQuery("");
    setParams(mode === "hybrid" ? {} : { mode });
  }

  const maxScore = useMemo(
    () => (results?.results || []).reduce((best, doc) => Math.max(best, Number(doc.score) || 0), 0),
    [results]
  );
  const categoryBreakdown = useMemo(() => {
    const items = results?.results || [];
    let scientific = 0;
    let archives = 0;
    items.forEach((doc) => {
      if (doc.category === "scientific") scientific += 1;
      else archives += 1;
    });
    return { scientific, archives };
  }, [results]);
  const idle = !q && !results;
  const modeLabel = SEARCH_MODES.find((item) => item.value === mode)?.label || mode;
  const modeHint = SEARCH_MODES.find((item) => item.value === mode)?.hint || "";

  return (
    <section className={`page page-search ${idle ? "is-idle" : ""}`}>
      <div className="page-narrow">
        {idle && (
          <header className="page-intro hero-intro">
            <p className="eyebrow">Espace public</p>
            <h1>Recherchez dans le fonds</h1>
            <p>Tapez un mot, choisissez un mode, ouvrez la fiche.</p>
          </header>
        )}

        <SearchBar
          searchQuery={query}
          searchMode={mode}
          searching={searching}
          apiStatus={apiStatus}
          onQueryChange={setQuery}
          onModeChange={(value) => {
            const next = { mode: value };
            if (query.trim()) next.q = query.trim();
            setParams(next);
          }}
          onSubmit={handleSubmit}
          onClear={handleClear}
          compact={!idle}
        />

        {idle && history.length > 0 && (
          <div className="history-row">
            <span className="filter-legend">Recherches de la session</span>
            <div className="chip-row">
              {history.map((item) => (
                <button
                  key={`${item.q}-${item.at}`}
                  type="button"
                  className="chip"
                  onClick={() => setParams({ q: item.q, mode: item.mode || "hybrid" })}
                >
                  {item.q}
                </button>
              ))}
              <button type="button" className="chip" onClick={() => setHistory(clearHistory())}>
                Effacer
              </button>
            </div>
          </div>
        )}

        {results && (
          <div className="result-toolbar">
            <div className="result-summary">
              <p className="result-count">
                <strong>
                  {results.total} résultat{results.total > 1 ? "s" : ""}
                </strong>
                {" · "}
                mode {modeLabel}
                {" · "}
                « {results.query} »
              </p>
              {results.total > 0 && (
                <p className="result-breakdown">
                  {categoryBreakdown.scientific > 0 && (
                    <span className="result-pill is-scientific">
                      {categoryBreakdown.scientific} scientifique
                      {categoryBreakdown.scientific > 1 ? "s" : ""}
                    </span>
                  )}
                  {categoryBreakdown.archives > 0 && (
                    <span className="result-pill is-archives">
                      {categoryBreakdown.archives} archive
                      {categoryBreakdown.archives > 1 ? "s" : ""}
                    </span>
                  )}
                  {modeHint && <span className="result-mode-hint">{modeHint}</span>}
                </p>
              )}
            </div>
            <button type="button" className="btn ghost" onClick={handleClear}>
              Nouvelle recherche
            </button>
          </div>
        )}

        {searching && (
          <EmptyState icon="spinner">
            <p>Classement des documents…</p>
          </EmptyState>
        )}

        {!searching && results?.total === 0 && (
          <EmptyState title="Aucun résultat">
            <p>Essayez un autre mot, ou passez en Hybride.</p>
            <button type="button" className="btn ghost" onClick={handleClear}>
              Effacer la requête
            </button>
          </EmptyState>
        )}

        {results?.results?.length > 0 && (
          <ol className="result-list">
            {results.results.map((doc, index) => (
              <ResultRow
                key={doc.id}
                doc={doc}
                rank={index + 1}
                maxScore={maxScore}
                showScore
                onTagClick={(tag) => navigate(`/fonds?tag=${encodeURIComponent(tag)}`)}
              />
            ))}
          </ol>
        )}

        {q && !searching && <ModeCompare query={q} onError={setError} />}
      </div>
    </section>
  );
}
