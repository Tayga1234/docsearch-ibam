import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import CategoryBadge from "../components/CategoryBadge";
import EmptyState from "../components/EmptyState";
import FiltersBar from "../components/FiltersBar";
import ResultRow from "../components/ResultRow";
import { useApp } from "../context/AppContext";
import { useAuth } from "../context/AuthContext";
import { fetchDocuments } from "../services/api";
import { CATEGORY_LABELS } from "../utils/format";

const PAGE_SIZE = 20;
const SORTS = ["category", "date", "title", "type"];

export default function LibraryPage() {
  const { apiStatus, setError } = useApp();
  const { isAdmin } = useAuth();
  const [params, setParams] = useSearchParams();
  const fileType = params.get("type") || "";
  const tag = params.get("tag") || "";
  const category = params.get("category") || "";
  const libraryQuery = params.get("q") || "";
  const sort = SORTS.includes(params.get("sort")) ? params.get("sort") : "category";
  const requestedPage = Math.max(1, Number(params.get("page") || 1) || 1);

  const [documents, setDocuments] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const hasFilters = Boolean(fileType || tag || libraryQuery || category);
  const pageCount = Math.max(1, Math.ceil(total / PAGE_SIZE));
  const page = total > 0 ? Math.min(requestedPage, pageCount) : requestedPage;

  const load = useCallback(async () => {
    const data = await fetchDocuments({
      limit: PAGE_SIZE,
      offset: (page - 1) * PAGE_SIZE,
      fileType,
      tag,
      q: libraryQuery.trim(),
      category,
      sort,
    });
    setDocuments(data.items || []);
    setTotal(data.total || 0);
  }, [fileType, tag, libraryQuery, category, sort, page]);

  useEffect(() => {
    if (!apiStatus) return undefined;
    let cancelled = false;
    const timer = setTimeout(() => {
      load()
        .catch((err) => {
          if (!cancelled) setError(err.message);
        })
        .finally(() => {
          if (!cancelled) setLoading(false);
        });
    }, 200);
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [apiStatus, load, setError]);

  function patchParams(next) {
    const merged = { type: fileType, tag, q: libraryQuery, category, sort, ...next };
    const clean = {};
    if (merged.type) clean.type = merged.type;
    if (merged.tag) clean.tag = merged.tag;
    if (merged.q) clean.q = merged.q;
    if (merged.category) clean.category = merged.category;
    if (merged.sort && merged.sort !== "category") clean.sort = merged.sort;
    const nextPage = merged.page;
    if (nextPage && Number(nextPage) > 1) clean.page = String(nextPage);
    setParams(clean);
  }

  const availableTags = useMemo(() => {
    const tags = new Set();
    documents.forEach((doc) => (doc.tags || []).forEach((item) => tags.add(item)));
    if (tag) tags.add(tag);
    return Array.from(tags).sort();
  }, [documents, tag]);

  const grouped = useMemo(() => {
    if (sort !== "category" || category) {
      return [{ key: "flat", label: null, items: documents }];
    }
    const buckets = [];
    let current = null;
    documents.forEach((doc) => {
      const key = doc.category || "archives";
      if (!current || current.key !== key) {
        current = {
          key,
          label: CATEGORY_LABELS[key]?.label || key,
          items: [],
        };
        buckets.push(current);
      }
      current.items.push(doc);
    });
    return buckets;
  }, [documents, sort, category]);

  const typeCounts = apiStatus?.formats || { pdf: 0, docx: 0, csv: 0, txt: 0 };
  const categoryCounts = apiStatus?.categories || { scientific: 0, archives: 0 };
  const from = total === 0 ? 0 : (page - 1) * PAGE_SIZE + 1;
  const to = Math.min(total, page * PAGE_SIZE);

  return (
    <section className="page page-catalog">
      <header className="page-intro">
        <p className="eyebrow">Collection</p>
        <h1>Fonds</h1>
        <p>
          {total} document{total > 1 ? "s" : ""}
          {hasFilters ? " correspondant aux filtres" : " dans l’index"}
          {total > 0 ? ` · ${from}–${to}` : ""}. Classés en scientifique et archives IBAM.
        </p>
      </header>

      <FiltersBar
        fileType={fileType}
        tag={tag}
        libraryQuery={libraryQuery}
        availableTags={availableTags}
        typeCounts={typeCounts}
        category={category}
        categoryCounts={categoryCounts}
        onFileTypeChange={(value) => patchParams({ type: value, page: 1 })}
        onTagChange={(value) => patchParams({ tag: value, page: 1 })}
        onLibraryQueryChange={(value) => patchParams({ q: value, page: 1 })}
        onCategoryChange={(value) => patchParams({ category: value, page: 1 })}
        sort={sort}
        onSortChange={(value) => patchParams({ sort: value, page: 1 })}
        onReset={() => setParams({})}
        disabled={!apiStatus}
        total={hasFilters ? total : apiStatus?.documents || total}
      />

      {loading && documents.length === 0 && (
        <EmptyState icon="spinner">
          <p>Chargement du fonds…</p>
        </EmptyState>
      )}

      {!loading && documents.length === 0 && hasFilters && (
        <EmptyState title="Aucun document pour ces filtres">
          <p>Élargissez la classe, le type, le tag ou le texte parcouru.</p>
          <button type="button" className="btn ghost" onClick={() => setParams({})}>
            Effacer les filtres
          </button>
        </EmptyState>
      )}

      {!loading && documents.length === 0 && !hasFilters && (
        <EmptyState title="Fonds vide">
          {isAdmin ? (
            <>
              <p>Scannez le dossier local ou importez un fichier.</p>
              <Link to="/documents" className="btn primary">
                Gérer les documents
              </Link>
            </>
          ) : (
            <p>Le fonds n’a pas encore été indexé. Un administrateur doit l’alimenter.</p>
          )}
        </EmptyState>
      )}

      {documents.length > 0 && (
        <>
          {grouped.map((group) => (
            <div key={group.key} className="catalog-group">
              {group.label && (
                <div className="catalog-group-head">
                  <CategoryBadge category={group.key} />
                  <strong>{group.label}</strong>
                  <span>{group.items.length} sur cette page</span>
                </div>
              )}
              <ol className="result-list">
                {group.items.map((doc, index) => {
                  const rank =
                    documents.findIndex((item) => item.id === doc.id) +
                    (page - 1) * PAGE_SIZE +
                    1;
                  return (
                    <ResultRow
                      key={doc.id}
                      doc={doc}
                      rank={rank || index + 1}
                      onTagClick={(value) => patchParams({ tag: value, page: 1 })}
                    />
                  );
                })}
              </ol>
            </div>
          ))}
          {pageCount > 1 && (
            <div className="pager">
              <button
                type="button"
                className="btn ghost"
                disabled={page <= 1}
                onClick={() => patchParams({ page: page - 1 })}
              >
                Précédent
              </button>
              <span>
                Page {page} / {pageCount}
              </span>
              <button
                type="button"
                className="btn ghost"
                disabled={page >= pageCount}
                onClick={() => patchParams({ page: page + 1 })}
              >
                Suivant
              </button>
            </div>
          )}
        </>
      )}
    </section>
  );
}
