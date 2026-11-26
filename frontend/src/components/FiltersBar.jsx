import { CATEGORY_FILTERS, FILE_TYPE_FILTERS } from "../utils/format";

export default function FiltersBar({
  fileType,
  tag,
  libraryQuery,
  availableTags,
  typeCounts,
  category = "",
  categoryCounts,
  onFileTypeChange,
  onTagChange,
  onLibraryQueryChange,
  onCategoryChange,
  onReset,
  disabled,
  total = 0,
  sort = "category",
  onSortChange,
}) {
  const hasFilters = Boolean(fileType || tag || libraryQuery || category);

  return (
    <div className="filters-panel">
      <div className="filter-row">
        <span className="filter-legend">Classe</span>
        <div className="chip-row">
          {CATEGORY_FILTERS.map((option) => {
            const count = option.value
              ? categoryCounts?.[option.value]
              : total;
            const active = category === option.value;
            return (
              <button
                key={option.value || "all-cat"}
                type="button"
                className={`chip ${active ? "is-active" : ""}`}
                onClick={() => onCategoryChange?.(option.value)}
                disabled={disabled}
              >
                {option.label}
                {count != null ? ` · ${count}` : ""}
              </button>
            );
          })}
        </div>
      </div>

      <div className="filter-row">
        <span className="filter-legend">Type</span>
        <div className="chip-row">
          {FILE_TYPE_FILTERS.map((option) => {
            const count = option.value ? typeCounts?.[option.value] : total;
            const active = fileType === option.value;
            return (
              <button
                key={option.value || "all"}
                type="button"
                className={`chip ${active ? "is-active" : ""}`}
                onClick={() => onFileTypeChange(option.value)}
                disabled={disabled}
              >
                {option.label}
                {count != null ? ` · ${count}` : ""}
              </button>
            );
          })}
        </div>
      </div>

      {availableTags.length > 0 && (
        <div className="filter-row">
          <span className="filter-legend">Tags</span>
          <div className="chip-row wrap">
            <button
              type="button"
              className={`chip ${tag === "" ? "is-active" : ""}`}
              onClick={() => onTagChange("")}
              disabled={disabled}
            >
              Tous
            </button>
            {availableTags.map((item) => (
              <button
                key={item}
                type="button"
                className={`chip ${tag === item ? "is-active" : ""}`}
                onClick={() => onTagChange(item)}
                disabled={disabled}
              >
                {item}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="filter-row filter-search-row">
        <label className="library-filter">
          <span className="filter-legend">Parcourir</span>
          <input
            type="search"
            value={libraryQuery}
            onChange={(event) => onLibraryQueryChange(event.target.value)}
            placeholder="Filtrer le titre, le contenu ou un tag"
            disabled={disabled}
          />
        </label>
        <label className="library-filter sort-filter">
          <span className="filter-legend">Trier</span>
          <select value={sort} onChange={(event) => onSortChange?.(event.target.value)} disabled={disabled}>
            <option value="category">Classe (scientifique / archives)</option>
            <option value="date">Plus récents</option>
            <option value="title">Titre</option>
            <option value="type">Type de fichier</option>
          </select>
        </label>
        {hasFilters && (
          <button type="button" className="btn ghost" onClick={onReset} disabled={disabled}>
            Effacer
          </button>
        )}
      </div>
    </div>
  );
}
