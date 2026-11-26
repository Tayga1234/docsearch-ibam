import { useEffect, useRef } from "react";
import { SEARCH_MODES } from "../utils/format";

export default function SearchBar({
  searchQuery,
  searchMode,
  searching,
  apiStatus,
  onQueryChange,
  onModeChange,
  onSubmit,
  onClear,
  compact = false,
}) {
  const inputRef = useRef(null);
  const activeHint = SEARCH_MODES.find((mode) => mode.value === searchMode)?.hint;

  useEffect(() => {
    if (apiStatus && !compact) inputRef.current?.focus();
  }, [apiStatus, compact]);

  useEffect(() => {
    function onKey(event) {
      const tag = event.target.tagName;
      if (event.key === "/" && tag !== "INPUT" && tag !== "TEXTAREA" && tag !== "SELECT") {
        event.preventDefault();
        inputRef.current?.focus();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <form className={`search-form ${compact ? "is-compact" : ""}`} onSubmit={onSubmit}>
      <div className="search-field">
        <span className="search-icon" aria-hidden>
          ⌕
        </span>
        <input
          ref={inputRef}
          type="search"
          value={searchQuery}
          onChange={(event) => onQueryChange(event.target.value)}
          placeholder="Titre, thème, nom, service…"
          disabled={!apiStatus}
          aria-label="Requête de recherche"
        />
        {searchQuery && onClear && (
          <button type="button" className="search-clear" onClick={onClear} aria-label="Effacer la requête">
            ×
          </button>
        )}
        <button type="submit" className="btn primary search-go" disabled={searching || !apiStatus}>
          {searching ? "Recherche…" : "Rechercher"}
        </button>
      </div>
      <div className="search-toolbar">
        <div className="mode-switch" role="group" aria-label="Mode de recherche">
          {SEARCH_MODES.map((mode) => (
            <button
              key={mode.value}
              type="button"
              className={`mode-btn ${searchMode === mode.value ? "is-active" : ""}`}
              onClick={() => onModeChange(mode.value)}
              disabled={!apiStatus}
              title={mode.hint}
            >
              {mode.label}
            </button>
          ))}
        </div>
        {activeHint && <p className="mode-hint">{activeHint}</p>}
      </div>
    </form>
  );
}
