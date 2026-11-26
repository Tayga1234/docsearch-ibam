import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import CategoryBadge from "../components/CategoryBadge";
import ConfirmDialog from "../components/ConfirmDialog";
import EmptyState from "../components/EmptyState";
import FileBadge from "../components/FileBadge";
import Icon from "../components/Icon";
import { useApp } from "../context/AppContext";
import { deleteDocument, fetchDocuments, uploadDocument } from "../services/api";
import { CATEGORY_LABELS, FILE_TYPE_FILTERS, formatDate, formatSize } from "../utils/format";

const PAGE_SIZE = 12;
const ACCEPT = ".txt,.pdf,.docx,.csv";
const CLASSES = [
  { key: "scientific", title: "Documents scientifiques" },
  { key: "archives", title: "Archives IBAM" },
];

function ClassSection({
  classKey,
  title,
  total,
  items,
  page,
  pageCount,
  loading,
  busy,
  onPageChange,
  onDelete,
}) {
  const from = total === 0 ? 0 : (page - 1) * PAGE_SIZE + 1;
  const to = Math.min(total, page * PAGE_SIZE);

  return (
    <section className="docs-class-block">
      <header className="docs-class-head">
        <CategoryBadge category={classKey} />
        <div>
          <strong>{title}</strong>
          <span>
            {total} document{total > 1 ? "s" : ""}
            {total > 0 ? ` · ${from}–${to}` : ""}
          </span>
        </div>
      </header>

      {loading && items.length === 0 && (
        <p className="muted-line">Chargement de la classe…</p>
      )}

      {!loading && items.length === 0 && (
        <p className="muted-line">Aucun document dans cette classe pour les filtres actuels.</p>
      )}

      {items.length > 0 && (
        <div className="docs-table-wrap">
          <table className="docs-table">
            <thead>
              <tr>
                <th>Type</th>
                <th>Titre</th>
                <th>Taille</th>
                <th>Indexé</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {items.map((doc) => (
                <tr key={doc.id}>
                  <td>
                    <FileBadge fileType={doc.file_type} />
                  </td>
                  <td>
                    <Link to={`/documents/${doc.id}`} className="docs-title">
                      {doc.title}
                    </Link>
                  </td>
                  <td>{formatSize(doc.size_bytes)}</td>
                  <td>{formatDate(doc.indexed_at)}</td>
                  <td>
                    <div className="docs-actions">
                      <Link
                        to={`/documents/${doc.id}`}
                        className="icon-action"
                        title="Voir la fiche"
                        aria-label={`Voir ${doc.title}`}
                      >
                        <Icon name="eye" />
                      </Link>
                      <button
                        type="button"
                        className="icon-action is-danger"
                        disabled={busy}
                        title="Supprimer"
                        aria-label={`Supprimer ${doc.title}`}
                        onClick={() => onDelete(doc)}
                      >
                        <Icon name="trash" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {pageCount > 1 && (
        <div className="pager">
          <button
            type="button"
            className="btn ghost"
            disabled={page <= 1}
            onClick={() => onPageChange(page - 1)}
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
            onClick={() => onPageChange(page + 1)}
          >
            Suivant
          </button>
        </div>
      )}
    </section>
  );
}

export default function DocumentsPage() {
  const { apiStatus, refreshHealth, setError } = useApp();
  const [params, setParams] = useSearchParams();
  const fileType = params.get("type") || "";
  const query = params.get("q") || "";
  const pageScientific = Math.max(1, Number(params.get("ps") || 1) || 1);
  const pageArchives = Math.max(1, Number(params.get("pa") || 1) || 1);

  const [sections, setSections] = useState({
    scientific: { items: [], total: 0 },
    archives: { items: [], total: 0 },
  });
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState("");
  const [deletingId, setDeletingId] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [notice, setNotice] = useState(null);
  const [pendingDelete, setPendingDelete] = useState(null);
  const [pendingFiles, setPendingFiles] = useState(null);

  const busy = uploading || Boolean(deletingId);
  const offline = !apiStatus;
  const hasFilters = Boolean(fileType || query);
  const grandTotal = sections.scientific.total + sections.archives.total;

  const load = useCallback(async () => {
    const [scientific, archives] = await Promise.all([
      fetchDocuments({
        limit: PAGE_SIZE,
        offset: (pageScientific - 1) * PAGE_SIZE,
        fileType,
        q: query.trim(),
        category: "scientific",
        sort: "title",
      }),
      fetchDocuments({
        limit: PAGE_SIZE,
        offset: (pageArchives - 1) * PAGE_SIZE,
        fileType,
        q: query.trim(),
        category: "archives",
        sort: "title",
      }),
    ]);
    setSections({
      scientific: { items: scientific.items || [], total: scientific.total || 0 },
      archives: { items: archives.items || [], total: archives.total || 0 },
    });
  }, [fileType, query, pageScientific, pageArchives]);

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
    const merged = {
      type: fileType,
      q: query,
      ps: pageScientific,
      pa: pageArchives,
      ...next,
    };
    const clean = {};
    if (merged.type) clean.type = merged.type;
    if (merged.q) clean.q = merged.q;
    if (merged.ps && Number(merged.ps) > 1) clean.ps = String(merged.ps);
    if (merged.pa && Number(merged.pa) > 1) clean.pa = String(merged.pa);
    setParams(clean);
  }

  function requestIngest(fileList) {
    const files = Array.from(fileList || []);
    if (!files.length) return;
    setPendingFiles(files);
  }

  async function ingestFiles(files) {
    if (!files?.length) return;
    setUploading(true);
    setError(null);
    setNotice(null);
    let indexed = 0;
    let skipped = 0;
    let errors = 0;
    try {
      for (let index = 0; index < files.length; index += 1) {
        const file = files[index];
        setUploadProgress(`${index + 1}/${files.length}`);
        try {
          const data = await uploadDocument(file);
          if (data.status === "skipped") skipped += 1;
          else indexed += 1;
        } catch {
          errors += 1;
        }
      }
      const parts = [`${indexed} ajouté${indexed > 1 ? "s" : ""}`];
      if (skipped) parts.push(`${skipped} ignoré${skipped > 1 ? "s" : ""}`);
      if (errors) parts.push(`${errors} erreur${errors > 1 ? "s" : ""}`);
      setNotice(parts.join(" · "));
      await refreshHealth();
      await load();
    } finally {
      setUploading(false);
      setUploadProgress("");
    }
  }

  async function confirmDelete() {
    const doc = pendingDelete;
    if (!doc) return;
    setDeletingId(doc.id);
    setError(null);
    try {
      await deleteDocument(doc.id);
      setPendingDelete(null);
      await refreshHealth();
      await load();
    } catch (err) {
      setError(err.message);
    } finally {
      setDeletingId(null);
    }
  }

  const typeCounts = apiStatus?.formats || { pdf: 0, docx: 0, csv: 0, txt: 0 };
  const pages = useMemo(
    () => ({
      scientific: Math.max(1, Math.ceil(sections.scientific.total / PAGE_SIZE)),
      archives: Math.max(1, Math.ceil(sections.archives.total / PAGE_SIZE)),
    }),
    [sections]
  );

  return (
    <section className="page page-documents">
      <header className="page-intro">
        <p className="eyebrow">Administration</p>
        <h1>Documents</h1>
        <p>
          Les pièces sont rangées en deux classes : scientifique et archives IBAM.
          {grandTotal > 0 ? ` ${grandTotal} document${grandTotal > 1 ? "s" : ""} au total.` : ""}
        </p>
      </header>

      <label
        className={`docs-drop ${dragging ? "is-dragging" : ""} ${busy || offline ? "is-disabled" : ""}`}
        onDragOver={(event) => {
          event.preventDefault();
          if (!busy && !offline) setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(event) => {
          event.preventDefault();
          setDragging(false);
          if (!busy && !offline) requestIngest(event.dataTransfer.files);
        }}
      >
        <input
          type="file"
          accept={ACCEPT}
          multiple
          hidden
          disabled={busy || offline}
          onChange={(event) => {
            requestIngest(event.target.files);
            event.target.value = "";
          }}
        />
        <strong>{uploading ? `Import ${uploadProgress}…` : "Ajouter des documents"}</strong>
        <span>Déposez des fichiers ici, ou cliquez pour les choisir (PDF, Word, CSV, TXT).</span>
      </label>

      {notice && (
        <div className="docs-notice">
          <span>{notice}</span>
          <button type="button" className="alert-dismiss" onClick={() => setNotice(null)}>
            Fermer
          </button>
        </div>
      )}

      <div className="filters-panel">
        <div className="filter-row">
          <span className="filter-legend">Type (dans chaque classe)</span>
          <div className="chip-row">
            {FILE_TYPE_FILTERS.map((option) => {
              const count = option.value ? typeCounts?.[option.value] : apiStatus?.documents;
              const active = fileType === option.value;
              return (
                <button
                  key={option.value || "all"}
                  type="button"
                  className={`chip ${active ? "is-active" : ""}`}
                  onClick={() => patchParams({ type: option.value, ps: 1, pa: 1 })}
                  disabled={!apiStatus}
                >
                  {option.label}
                  {count != null ? ` · ${count}` : ""}
                </button>
              );
            })}
          </div>
        </div>
        <div className="filter-row filter-search-row">
          <label className="library-filter">
            <span className="filter-legend">Parcourir dans les classes</span>
            <input
              type="search"
              value={query}
              onChange={(event) => patchParams({ q: event.target.value, ps: 1, pa: 1 })}
              placeholder="Filtrer le titre ou le contenu"
              disabled={!apiStatus}
            />
          </label>
          {hasFilters && (
            <button type="button" className="btn ghost" onClick={() => setParams({})} disabled={!apiStatus}>
              Effacer
            </button>
          )}
        </div>
      </div>

      {loading && grandTotal === 0 && (
        <EmptyState icon="spinner">
          <p>Classement des documents…</p>
        </EmptyState>
      )}

      {!loading && grandTotal === 0 && (
        <EmptyState title={hasFilters ? "Aucun document pour ces filtres" : "Aucun document"}>
          <p>
            {hasFilters
              ? "Élargissez le type ou le texte parcouru."
              : "Ajoutez des fichiers ci-dessus, ou indexez le dossier local."}
          </p>
          {hasFilters ? (
            <button type="button" className="btn ghost" onClick={() => setParams({})}>
              Effacer les filtres
            </button>
          ) : (
            <Link to="/indexation" className="btn ghost">
              Aller à l’indexation
            </Link>
          )}
        </EmptyState>
      )}

      {(grandTotal > 0 || loading) && (
        <div className="docs-classified">
          {CLASSES.map((entry) => {
            const data = sections[entry.key];
            const page = entry.key === "scientific" ? pageScientific : pageArchives;
            const safePage = data.total > 0 ? Math.min(page, pages[entry.key]) : page;
            return (
              <ClassSection
                key={entry.key}
                classKey={entry.key}
                title={CATEGORY_LABELS[entry.key]?.label || entry.title}
                total={data.total}
                items={data.items}
                page={safePage}
                pageCount={pages[entry.key]}
                loading={loading}
                busy={busy}
                onPageChange={(next) =>
                  patchParams(entry.key === "scientific" ? { ps: next } : { pa: next })
                }
                onDelete={setPendingDelete}
              />
            );
          })}
        </div>
      )}

      <ConfirmDialog
        open={Boolean(pendingFiles)}
        tone="warning"
        title="Ajouter ces fichiers au fonds ?"
        message="Chaque fichier sera copié, enrichi puis indexé. Un doublon déjà présent peut être ignoré."
        details={(pendingFiles || []).slice(0, 8).map((file) => file.name)}
        confirmLabel={pendingFiles?.length > 1 ? `Importer ${pendingFiles.length} fichiers` : "Importer"}
        busy={uploading}
        onCancel={() => !uploading && setPendingFiles(null)}
        onConfirm={async () => {
          await ingestFiles(pendingFiles);
          setPendingFiles(null);
        }}
      />

      <ConfirmDialog
        open={Boolean(pendingDelete)}
        tone="danger"
        title="Supprimer ce document ?"
        message="Le fichier sera retiré du fonds, de l’index et du dossier local. Cette action est définitive."
        details={pendingDelete ? [pendingDelete.title] : []}
        confirmLabel="Supprimer définitivement"
        confirmWord="SUPPRIMER"
        busy={Boolean(deletingId)}
        onCancel={() => !deletingId && setPendingDelete(null)}
        onConfirm={confirmDelete}
      />
    </section>
  );
}
