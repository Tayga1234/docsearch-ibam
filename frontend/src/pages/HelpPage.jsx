import { Link } from "react-router-dom";
import { swaggerDocsUrl } from "../services/api";
import { DEMO_QUERIES, SEARCH_MODES } from "../utils/format";

const API_ROUTES = [
  { method: "GET", path: "/health", access: "Espace public", role: "État du service et nombre de documents" },
  { method: "GET", path: "/search", access: "Espace public", role: "Recherche (q, mode, limit)" },
  { method: "GET", path: "/search/compare", access: "Espace public", role: "Comparaison des trois modes (top 3)" },
  { method: "GET", path: "/documents", access: "Espace public", role: "Liste paginée du fonds" },
  { method: "GET", path: "/documents/{id}", access: "Espace public", role: "Détail enrichi" },
  { method: "POST", path: "/auth/login", access: "Administrateur", role: "Authentification (jeton Bearer)" },
  { method: "POST", path: "/ingest/scan", access: "Administrateur", role: "Indexer le dossier data/raw" },
  { method: "POST", path: "/ingest/upload", access: "Administrateur", role: "Téléverser et indexer un fichier" },
  { method: "DELETE", path: "/documents/{id}", access: "Administrateur", role: "Suppression base et index" },
  { method: "POST", path: "/index/rebuild", access: "Administrateur", role: "Reconstruction de l’index Whoosh" },
];

export default function HelpPage() {
  const docsUrl = swaggerDocsUrl();

  return (
    <section className="page page-help">
      <header className="page-intro">
        <p className="eyebrow">Mode d’emploi</p>
        <h1>Aide</h1>
        <p>Requêtes de démonstration, accès, modes de recherche et API REST.</p>
      </header>

      <article className="info-card">
        <span className="section-label">Requêtes de démo</span>
        <p className="card-lead">Cliquez une requête pour l’ouvrir dans la recherche hybride.</p>
        <div className="demo-list">
          {DEMO_QUERIES.map((item) => (
            <Link key={item.q} className="demo-link" to={`/?q=${encodeURIComponent(item.q)}&mode=hybrid`}>
              <strong>{item.q}</strong>
              <span>{item.hint}</span>
            </Link>
          ))}
        </div>
      </article>

      <div className="help-grid">
        <article className="info-card">
          <span className="section-label">Accès</span>
          <ul className="plain-list">
            <li>
              <strong>Espace public</strong> — rechercher, parcourir le fonds, ouvrir une fiche et
              consulter l’état du système, sans connexion.
            </li>
            <li>
              <strong>Administrateur</strong> — se connecte pour indexer, importer, supprimer et
              reconstruire l’index (<code>admin</code> / <code>archives</code>).
            </li>
          </ul>
        </article>

        <article className="info-card">
          <span className="section-label">Modes</span>
          <ul className="plain-list">
            {SEARCH_MODES.map((mode) => (
              <li key={mode.value}>
                <strong>{mode.label}</strong> — {mode.hint}
              </li>
            ))}
            <li>
              Le mode « sémantique » repose sur une similarité TF-IDF locale, pas sur un embedding
              neuronal.
            </li>
            <li>Après une recherche, le top 3 de chaque mode s’affiche côte à côte.</li>
          </ul>
        </article>
      </div>

      <article className="info-card">
        <span className="section-label">API REST</span>
        <h2>Ingestion, recherche et administration</h2>
        <p className="card-lead">
          Les lecteurs consultent l’espace public. L’administrateur s’authentifie pour indexer et
          maintenir l’index. Les données sont validées par Pydantic. La documentation OpenAPI est
          générée automatiquement.
        </p>
        <div className="docs-table-wrap api-table-wrap">
          <table className="docs-table api-table">
            <thead>
              <tr>
                <th>Méthode</th>
                <th>Route</th>
                <th>Accès</th>
                <th>Rôle</th>
              </tr>
            </thead>
            <tbody>
              {API_ROUTES.map((route) => (
                <tr key={`${route.method}-${route.path}`}>
                  <td>
                    <span className={`api-method ${route.method.toLowerCase()}`}>{route.method}</span>
                  </td>
                  <td>
                    <code className="api-path">{route.path}</code>
                  </td>
                  <td>{route.access}</td>
                  <td>{route.role}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <ul className="plain-list api-errors">
          <li>
            Format non supporté ou fichier trop volumineux : <strong>400</strong> (limite 20 Mo).
          </li>
          <li>
            Requête de recherche vide, mode inconnu ou limite hors intervalle :{" "}
            <strong>400</strong>.
          </li>
          <li>
            Identifiant inconnu : <strong>404</strong>.
          </li>
        </ul>
        <p className="api-docs-cta">
          <a className="btn" href={docsUrl} target="_blank" rel="noreferrer">
            Ouvrir Swagger /docs
          </a>
          <span className="muted-line">Interface OpenAPI générée par FastAPI.</span>
        </p>
      </article>

      <article className="info-card">
        <span className="section-label">Organisation</span>
        <h2>Direction de la Documentation et des Archives</h2>
        <p>
          Institut Burkinabè des Arts et Métiers (Université Joseph Ki-Zerbo, Ouagadougou). Le
          prototype indexe notes, budgets, conventions, CSV et guides du Centre de documentation.
        </p>
      </article>
    </section>
  );
}
