import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import ConfirmDialog from "../components/ConfirmDialog";
import DocumentContent from "../components/DocumentContent";
import EmptyState from "../components/EmptyState";
import Icon from "../components/Icon";
import EntityList from "../components/EntityList";
import FileBadge from "../components/FileBadge";
import TagList from "../components/TagList";
import { useApp } from "../context/AppContext";
import { useAuth } from "../context/AuthContext";
import { deleteDocument, fetchDocument } from "../services/api";
import { downloadDocumentFiche } from "../utils/export";
import { formatDate, formatSize } from "../utils/format";

export default function DocumentPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { refreshHealth, setError } = useApp();
  const { isAdmin } = useAuth();
  const [document, setDocument] = useState(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);
  const [askDelete, setAskDelete] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetchDocument(id)
      .then((data) => {
        if (!cancelled) setDocument(data);
      })
      .catch((err) => {
        if (!cancelled) {
          setDocument(null);
          setError(err.message);
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [id, setError]);

  async function confirmDelete() {
    if (!document) return;
    setDeleting(true);
    try {
      await deleteDocument(document.id);
      await refreshHealth();
      navigate(isAdmin ? "/documents" : "/fonds");
    } catch (err) {
      setError(err.message);
      setDeleting(false);
    }
  }

  if (loading) {
    return (
      <section className="page">
        <EmptyState icon="spinner">
          <p>Ouverture du document…</p>
        </EmptyState>
      </section>
    );
  }

  if (!document) {
    return (
      <section className="page">
        <EmptyState title="Document introuvable">
          <Link to={isAdmin ? "/documents" : "/fonds"} className="btn ghost">
            {isAdmin ? "Retour aux documents" : "Retour au fonds"}
          </Link>
        </EmptyState>
      </section>
    );
  }

  const hasContent = Boolean(document.content?.trim());
  const entities = document.metadata?.entities;
  const showAside =
    isAdmin ||
    (entities &&
      typeof entities === "object" &&
      !Array.isArray(entities) &&
      Object.values(entities).some((values) => Array.isArray(values) && values.length > 0));

  return (
    <section className="page page-document">
      <p className="crumb">
        <Link to={isAdmin ? "/documents" : "/fonds"}>{isAdmin ? "Documents" : "Fonds"}</Link>
        <span> / </span>
        <span className="crumb-current">{document.title}</span>
      </p>

      <header className="doc-head">
        <div>
          <p className="eyebrow">Fiche</p>
          <h1>{document.title}</h1>
          <p className="result-meta">
            <FileBadge fileType={document.file_type} />
            <span>{formatSize(document.size_bytes)}</span>
            {document.indexed_at ? <span>Indexé {formatDate(document.indexed_at)}</span> : null}
          </p>
        </div>
        <div className="doc-actions">
          <button type="button" className="btn ghost" onClick={() => downloadDocumentFiche(document)}>
            <Icon name="download" />
            Exporter
          </button>
          <Link
            to={isAdmin ? "/documents" : "/fonds"}
            className="back-fab"
            aria-label={isAdmin ? "Retour aux documents" : "Retour au fonds"}
            title="Retour"
          >
            <svg className="back-fab-icon" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">
              <path
                d="M14.5 5.5 7 12l7.5 6.5"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.8"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </Link>
        </div>
      </header>

      <TagList
        tags={document.tags}
        onTagClick={(tag) =>
          navigate(`${isAdmin ? "/documents" : "/fonds"}?tag=${encodeURIComponent(tag)}`)
        }
      />

      <div className="doc-layout">
        <div className="doc-stack">
          {document.summary && (
            <div className="info-card">
              <span className="section-label">Résumé</span>
              <p>{document.summary}</p>
            </div>
          )}

          <div className="info-card">
            <span className="section-label">Contenu</span>
            {hasContent ? (
              <DocumentContent content={document.content} />
            ) : (
              <p className="empty-extract">
                Aucun texte extractible. Un PDF image sans OCR ne peut pas alimenter l’index.
              </p>
            )}
          </div>
        </div>

        {showAside && (
          <aside className="doc-stack">
            <EntityList entities={entities} />
            {isAdmin && (
              <div className="info-card admin-card">
                <span className="section-label">Administration</span>
                <p>Retirer ce document de l’index et de la base.</p>
                <button type="button" className="btn danger" onClick={() => setAskDelete(true)} disabled={deleting}>
                  <Icon name="trash" />
                  Retirer du fonds
                </button>
              </div>
            )}
          </aside>
        )}
      </div>

      <ConfirmDialog
        open={askDelete}
        tone="danger"
        title="Supprimer ce document ?"
        message="Le fichier sera retiré du fonds, de l’index et du dossier local. Cette action est définitive."
        details={[document.title]}
        confirmLabel="Supprimer définitivement"
        confirmWord="SUPPRIMER"
        busy={deleting}
        onCancel={() => !deleting && setAskDelete(false)}
        onConfirm={confirmDelete}
      />
    </section>
  );
}
