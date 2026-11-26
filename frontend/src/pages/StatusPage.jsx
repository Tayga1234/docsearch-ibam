import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import FileBadge from "../components/FileBadge";
import { useApp } from "../context/AppContext";
import { useAuth } from "../context/AuthContext";
import { fetchDocuments, swaggerDocsUrl } from "../services/api";
import { FILE_LABELS, SEARCH_MODES, formatDate } from "../utils/format";

const PIPELINE = [
  { step: "01", title: "Extraction", text: "PDF, Word, CSV et TXT unifiés en texte." },
  { step: "02", title: "Enrichissement", text: "Tags, résumé extractif et entités." },
  { step: "03", title: "Indexation", text: "SQLite pour le fonds, Whoosh pour l’index inversé." },
  { step: "04", title: "Recherche", text: "Mots-clés, sémantique TF-IDF et hybride 0,6 / 0,4." },
];

export default function StatusPage() {
  const { apiStatus, loading, refreshHealth, setError } = useApp();
  const { user, isAdmin } = useAuth();
  const [recent, setRecent] = useState([]);
  const [refreshing, setRefreshing] = useState(false);

  const online = Boolean(apiStatus);
  const indexReady = Boolean(apiStatus?.index_ready);
  const formats = apiStatus?.formats || {};
  const total = Number(apiStatus?.documents) || 0;

  useEffect(() => {
    let cancelled = false;
    fetchDocuments({ limit: 6 })
      .then((data) => {
        if (!cancelled) setRecent(data.items || []);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      });
    return () => {
      cancelled = true;
    };
  }, [apiStatus?.documents, setError]);

  async function handleRefresh() {
    setRefreshing(true);
    try {
      await refreshHealth();
      const data = await fetchDocuments({ limit: 6 });
      setRecent(data.items || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setRefreshing(false);
    }
  }

  return (
    <section className="page page-status">
      <header className="page-intro status-head">
        <div>
          <p className="eyebrow">Supervision</p>
          <h1>État du système</h1>
          <p>Vue d’ensemble du portail, de l’index et de l’accès en cours.</p>
        </div>
        <button type="button" className="btn ghost" onClick={handleRefresh} disabled={refreshing}>
          {refreshing ? "Actualisation…" : "Actualiser"}
        </button>
      </header>

      {loading && !apiStatus && <p className="muted-line">Lecture du service…</p>}

      <div className="stat-grid">
        <article className={`stat-card ${online ? "is-ok" : "is-off"}`}>
          <span className="section-label">API</span>
          <strong>{online ? "En ligne" : "Hors ligne"}</strong>
          <p>{apiStatus?.service || "DocSearch API"}</p>
        </article>
        <article className="stat-card">
          <span className="section-label">Documents</span>
          <strong>{apiStatus?.documents ?? "—"}</strong>
          <p>fichiers dans l’index</p>
        </article>
        <article className={`stat-card ${indexReady ? "is-ok" : "is-off"}`}>
          <span className="section-label">Whoosh</span>
          <strong>{indexReady ? "Prêt" : "Absent"}</strong>
          <p>index inversé</p>
        </article>
        <article className="stat-card">
          <span className="section-label">Version</span>
          <strong>{apiStatus?.version || "—"}</strong>
          <p>service FastAPI</p>
        </article>
      </div>

      <div className="help-grid">
        <article className="info-card">
          <span className="section-label">Accès</span>
          <h2>{isAdmin ? user?.name : "Visiteur"}</h2>
          <dl className="spec-list">
            <div>
              <dt>Fonction</dt>
              <dd>{isAdmin ? user?.title || "—" : "Consultation libre"}</dd>
            </div>
            <div>
              <dt>Identifiant</dt>
              <dd>{isAdmin ? user?.username || "—" : "Aucun (espace public)"}</dd>
            </div>
            <div>
              <dt>Rôle</dt>
              <dd>{isAdmin ? "Administrateur" : "Espace public"}</dd>
            </div>
          </dl>
        </article>

        <article className="info-card">
          <span className="section-label">Droits</span>
          <h2>{isAdmin ? "Maintenance du fonds" : "Consultation du fonds"}</h2>
          <ul className="plain-list">
            <li>Rechercher (mots-clés, sémantique TF-IDF, hybride)</li>
            <li>Parcourir le fonds et ouvrir une fiche</li>
            <li>Consulter l’état du système</li>
            {isAdmin ? (
              <>
                <li>Indexer le dossier local et importer un fichier</li>
                <li>Reconstruire l’index et retirer un document</li>
              </>
            ) : (
              <li>
                L’indexation et la suppression restent à l’administrateur (
                <Link to="/connexion">se connecter</Link>).
              </li>
            )}
          </ul>
        </article>
      </div>

      <article className="info-card">
        <span className="section-label">Composition du fonds</span>
        <h2>{total} document{total > 1 ? "s" : ""} indexé{total > 1 ? "s" : ""}</h2>
        <p className="card-lead">
          Dernière indexation : {formatDate(apiStatus?.last_indexed_at)} · {apiStatus?.raw_files ?? "—"} fichiers
          dans <code>data/raw</code>
        </p>
        <div className="format-grid">
          {Object.entries(FILE_LABELS).map(([type, meta]) => {
            const count = formats[type] ?? 0;
            const percent = total ? Math.round((count / total) * 100) : 0;
            return (
              <Link key={type} className="format-card" to={`/fonds?type=${type}`}>
                <FileBadge fileType={type} />
                <strong>{count}</strong>
                <span>{meta.label} · {percent} %</span>
              </Link>
            );
          })}
        </div>
      </article>

      <div className="help-grid">
        <article className="info-card">
          <span className="section-label">Chaîne de traitement</span>
          <ol className="pipeline">
            {PIPELINE.map((item) => (
              <li key={item.step}>
                <span>{item.step}</span>
                <div>
                  <strong>{item.title}</strong>
                  <p>{item.text}</p>
                </div>
              </li>
            ))}
          </ol>
        </article>

        <article className="info-card">
          <span className="section-label">Modes de recherche</span>
          <ul className="plain-list">
            {SEARCH_MODES.map((mode) => (
              <li key={mode.value}>
                <strong>{mode.label}</strong> — {mode.hint}
                {mode.value === "hybrid" && apiStatus?.hybrid
                  ? ` (${apiStatus.hybrid.keyword} / ${apiStatus.hybrid.semantic})`
                  : ""}
              </li>
            ))}
          </ul>
          <p className="card-lead">Formats acceptés : {(apiStatus?.supported || [".txt", ".pdf", ".docx", ".csv"]).join(", ")}</p>
        </article>
      </div>

      <article className="info-card">
        <span className="section-label">Stockage</span>
        <h2>Local, sans cloud</h2>
        <dl className="spec-list spec-list-wide">
          <div>
            <dt>Base</dt>
            <dd>{apiStatus?.store || "SQLite"}</dd>
          </div>
          <div>
            <dt>Moteur</dt>
            <dd>{apiStatus?.engine || "Whoosh"}</dd>
          </div>
          <div>
            <dt>Dossier brut</dt>
            <dd>data/raw</dd>
          </div>
          <div>
            <dt>Upload max</dt>
            <dd>{apiStatus?.max_upload_mb ?? 20} Mo</dd>
          </div>
        </dl>
      </article>

      <article className="info-card">
        <span className="section-label">Derniers documents</span>
        {recent.length === 0 ? (
          <p className="card-lead">Aucun document à afficher.</p>
        ) : (
          <ul className="recent-list">
            {recent.map((doc) => (
              <li key={doc.id}>
                <Link to={`/documents/${doc.id}`}>
                  <FileBadge fileType={doc.file_type} />
                  <strong>{doc.title}</strong>
                  <span>{formatDate(doc.indexed_at)}</span>
                </Link>
              </li>
            ))}
          </ul>
        )}
        <Link to="/fonds" className="alert-link">
          Voir tout le fonds
        </Link>
      </article>

      <div className="status-actions">
        <Link to="/" className="btn primary">
          Lancer une recherche
        </Link>
        {isAdmin && (
          <>
            <Link to="/documents" className="btn ghost">
              Gérer les documents
            </Link>
            <Link to="/indexation" className="btn ghost">
              Gérer l’indexation
            </Link>
          </>
        )}
        <Link to="/aide" className="btn ghost">
          Consulter l’aide
        </Link>
        <a className="btn ghost" href={swaggerDocsUrl()} target="_blank" rel="noreferrer">
          Documentation OpenAPI
        </a>
      </div>
    </section>
  );
}
